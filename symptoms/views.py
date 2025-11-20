"""
Views for Symptom Checker
"""
from django.shortcuts import render
from .symptom_checker import SymptomChecker


def symptom_checker(request):
    """
    Symptom checker form and results page
    """
    result = None
    
    if request.method == 'POST':
        symptom_description = request.POST.get('symptoms', '')
        age = int(request.POST.get('age', 25))
        gender = request.POST.get('gender', 'O')
        category = request.POST.get('category', 'general')
        
        # Analyze symptoms
        result = SymptomChecker.analyze_symptoms(
            symptom_description=symptom_description,
            age=age,
            gender=gender,
            category=category
        )
        
        # Add form data to result for display
        result['form_data'] = {
            'symptoms': symptom_description,
            'age': age,
            'gender': gender,
            'category': category,
        }
    
    # Get categories for dropdown
    categories = [
        ('general', 'General / Other'),
        ('fever', 'Fever'),
        ('cough_cold', 'Cough/Cold'),
        ('stomach_issues', 'Stomach Issues'),
        ('headache', 'Headache'),
        ('chest_discomfort', 'Chest Discomfort'),
        ('skin_issues', 'Skin Issues'),
        ('joint_pain', 'Joint/Bone Pain'),
        ('mental_health', 'Mental Health / Stress'),
    ]
    
    context = {
        'result': result,
        'categories': categories,
    }
    
    return render(request, 'symptoms/symptom_checker.html', context)
