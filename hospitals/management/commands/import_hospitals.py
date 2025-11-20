"""
Management command to import real Indian hospital data from CSV
"""
import csv
import os
from django.core.management.base import BaseCommand
from hospitals.models import Hospital
from decimal import Decimal


class Command(BaseCommand):
    help = 'Import real Indian hospital data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data/india_hospitals.csv',
            help='Path to CSV file (default: data/india_hospitals.csv)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing hospital data before importing'
        )

    def handle(self, *args, **options):
        csv_file = options['file']
        clear_data = options['clear']

        # Check if file exists
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file}'))
            return

        # Clear existing data if requested
        if clear_data:
            count = Hospital.objects.count()
            Hospital.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing hospitals'))

        # Import data
        imported_count = 0
        skipped_count = 0
        
        self.stdout.write(self.style.NOTICE(f'Importing hospitals from {csv_file}...'))

        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        # Check if hospital already exists (by name and state)
                        if Hospital.objects.filter(
                            name=row['facility_name'].strip(),
                            state=row['state_name'].strip()
                        ).exists():
                            skipped_count += 1
                            continue

                        # Parse has_emergency
                        has_emergency = row.get('has_emergency', 'False').strip().lower() in ['true', '1', 'yes']
                        
                        # Create hospital
                        Hospital.objects.create(
                            name=row['facility_name'].strip(),
                            state=row['state_name'].strip(),
                            district=row['district_name'].strip(),
                            address=row.get('address', '').strip(),
                            facility_type=row.get('facility_type', '').strip(),
                            latitude=Decimal(row['latitude'].strip()) if row.get('latitude') else None,
                            longitude=Decimal(row['longitude'].strip()) if row.get('longitude') else None,
                            contact_number=row.get('contact', '').strip(),
                            has_emergency=has_emergency,
                            # Set some defaults for real hospitals
                            has_ambulance=has_emergency,  # Assume emergency hospitals have ambulances
                            beds_available=100 if 'Tertiary' in row.get('facility_type', '') else 50,
                            rating=Decimal('4.0')
                        )
                        
                        imported_count += 1
                        
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error importing {row.get("facility_name", "Unknown")}: {str(e)}')
                        )
                        skipped_count += 1
                        continue

            self.stdout.write(
                self.style.SUCCESS(
                    f'\nImport complete!'
                    f'\n✓ Imported: {imported_count} hospitals'
                    f'\n✗ Skipped: {skipped_count} hospitals'
                    f'\n📊 Total in database: {Hospital.objects.count()} hospitals'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading CSV file: {str(e)}'))
            return
