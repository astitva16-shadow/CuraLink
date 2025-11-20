from hospitals.models import Hospital

print(f"Total hospitals: {Hospital.objects.count()}")
print(f"Delhi hospitals: {Hospital.objects.filter(state='Delhi').count()}")
print(f"Emergency hospitals: {Hospital.objects.filter(has_emergency=True).count()}")
print(f"\nStates covered:")
states = Hospital.objects.values_list('state', flat=True).distinct().order_by('state')
for state in states:
    count = Hospital.objects.filter(state=state).count()
    print(f"  - {state}: {count} hospitals")

print(f"\nSample hospitals:")
for h in Hospital.objects.all()[:10]:
    print(f"  - {h.name} ({h.district}, {h.state}) - {h.facility_type}")
