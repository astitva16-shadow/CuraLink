"""
Symptom Checker Logic

Rule-based system to analyze symptoms and provide recommendations.
This is NOT a medical diagnosis tool - just basic guidance.
"""


class SymptomChecker:
    """
    Rule-based symptom checker with basic health guidance
    """
    
    # Define symptom categories and their associated information
    SYMPTOM_DATABASE = {
        'fever': {
            'keywords': ['fever', 'high temperature', 'hot', 'burning', 'chills'],
            'specialization': 'general',
            'specialization_name': 'General Physician',
            'concern_level': 'moderate',
            'diet_tips': [
                'Drink plenty of fluids (water, coconut water, herbal teas)',
                'Eat light, easily digestible foods',
                'Include vitamin C rich fruits like oranges and lemons',
                'Avoid heavy, fried, or spicy foods',
            ],
            'care_instructions': [
                'Get adequate rest and sleep',
                'Monitor your temperature regularly',
                'Use cool compresses if temperature is very high',
                'Take prescribed fever medication as directed',
                'If fever persists for more than 3 days or goes above 103°F, consult a doctor immediately',
            ]
        },
        'cough_cold': {
            'keywords': ['cough', 'cold', 'runny nose', 'sneezing', 'sore throat', 'congestion'],
            'specialization': 'general',
            'specialization_name': 'General Physician',
            'concern_level': 'mild',
            'diet_tips': [
                'Drink warm water, herbal teas, and soups',
                'Consume honey and ginger tea',
                'Eat vitamin C rich foods',
                'Avoid cold drinks and ice cream',
                'Include turmeric milk before bed',
            ],
            'care_instructions': [
                'Get plenty of rest',
                'Gargle with warm salt water for sore throat',
                'Use steam inhalation for congestion',
                'Keep yourself warm',
                'If symptoms worsen or persist beyond a week, consult a doctor',
            ]
        },
        'stomach_issues': {
            'keywords': ['stomach', 'abdominal', 'belly', 'nausea', 'vomiting', 'diarrhea', 'constipation', 'acidity'],
            'specialization': 'gastroenterology',
            'specialization_name': 'Gastroenterologist',
            'concern_level': 'moderate',
            'diet_tips': [
                'Eat bland foods like rice, bananas, toast',
                'Stay hydrated with ORS or coconut water',
                'Avoid spicy, oily, and fried foods',
                'Eat small, frequent meals',
                'Include probiotics like yogurt',
            ],
            'care_instructions': [
                'Rest and avoid strenuous activities',
                'Monitor for signs of dehydration',
                'Avoid self-medication for severe pain',
                'If there is blood in stool/vomit or severe pain, seek immediate medical help',
                'Keep track of what you eat and symptoms',
            ]
        },
        'headache': {
            'keywords': ['headache', 'head pain', 'migraine', 'head ache'],
            'specialization': 'neurology',
            'specialization_name': 'Neurologist',
            'concern_level': 'mild',
            'diet_tips': [
                'Stay well hydrated',
                'Avoid caffeine and alcohol',
                'Eat regular, balanced meals',
                'Include magnesium-rich foods like nuts and seeds',
                'Avoid processed foods and MSG',
            ],
            'care_instructions': [
                'Rest in a quiet, dark room',
                'Apply cold or warm compress to head',
                'Practice relaxation techniques',
                'Maintain regular sleep schedule',
                'If headaches are severe, frequent, or accompanied by vision changes, consult a doctor',
            ]
        },
        'chest_discomfort': {
            'keywords': ['chest', 'chest pain', 'breathing', 'shortness of breath', 'heart'],
            'specialization': 'cardiology',
            'specialization_name': 'Cardiologist',
            'concern_level': 'severe',
            'diet_tips': [
                'Avoid heavy meals',
                'Reduce salt and fat intake',
                'Stay hydrated',
                'Avoid caffeine and stimulants',
            ],
            'care_instructions': [
                '⚠️ IMPORTANT: Chest pain can be serious',
                'If you experience severe chest pain, call emergency services (112/108) immediately',
                'Do not ignore chest discomfort, especially with sweating, nausea, or arm pain',
                'Rest and avoid physical exertion',
                'Seek immediate medical attention',
            ]
        },
        'skin_issues': {
            'keywords': ['skin', 'rash', 'itching', 'allergy', 'redness', 'acne', 'pimples'],
            'specialization': 'dermatology',
            'specialization_name': 'Dermatologist',
            'concern_level': 'mild',
            'diet_tips': [
                'Drink plenty of water for hydration',
                'Include fruits and vegetables',
                'Avoid oily and junk food',
                'Reduce sugar intake',
                'Include foods rich in Omega-3 fatty acids',
            ],
            'care_instructions': [
                'Keep the affected area clean',
                'Avoid scratching',
                'Use mild, fragrance-free soaps',
                'Apply moisturizer if skin is dry',
                'Avoid known allergens',
                'If rash spreads rapidly or is painful, consult a doctor',
            ]
        },
        'joint_pain': {
            'keywords': ['joint', 'bone', 'arthritis', 'knee', 'back pain', 'muscle pain'],
            'specialization': 'orthopedics',
            'specialization_name': 'Orthopedic',
            'concern_level': 'moderate',
            'diet_tips': [
                'Include anti-inflammatory foods',
                'Consume foods rich in calcium and vitamin D',
                'Include turmeric and ginger in diet',
                'Stay hydrated',
                'Maintain healthy weight',
            ],
            'care_instructions': [
                'Apply ice or heat therapy as appropriate',
                'Rest the affected area',
                'Do gentle stretching exercises',
                'Maintain good posture',
                'If pain is severe or limits movement, consult a doctor',
            ]
        },
        'mental_health': {
            'keywords': ['anxiety', 'depression', 'stress', 'mental', 'sleep issues', 'insomnia', 'panic'],
            'specialization': 'psychiatry',
            'specialization_name': 'Psychiatrist',
            'concern_level': 'moderate',
            'diet_tips': [
                'Eat balanced, regular meals',
                'Limit caffeine and sugar',
                'Include foods rich in Omega-3',
                'Avoid alcohol',
                'Stay hydrated',
            ],
            'care_instructions': [
                'Practice relaxation techniques like deep breathing',
                'Maintain regular sleep schedule',
                'Exercise regularly',
                'Stay connected with friends and family',
                'Seek professional help - mental health is important',
                'If you have thoughts of self-harm, seek immediate help',
            ]
        },
        'general': {
            'keywords': [],  # Default category
            'specialization': 'general',
            'specialization_name': 'General Physician',
            'concern_level': 'mild',
            'diet_tips': [
                'Eat a balanced diet with fruits and vegetables',
                'Stay hydrated',
                'Get adequate sleep',
                'Exercise regularly',
            ],
            'care_instructions': [
                'Monitor your symptoms',
                'Get adequate rest',
                'Maintain good hygiene',
                'Consult a doctor if symptoms persist or worsen',
            ]
        }
    }
    
    @classmethod
    def analyze_symptoms(cls, symptom_description, age, gender, category='general'):
        """
        Analyze symptoms and return recommendations
        
        Args:
            symptom_description: Text description of symptoms
            age: Patient's age
            gender: Patient's gender
            category: Pre-selected category (optional)
        
        Returns:
            Dictionary with analysis results
        """
        symptom_lower = symptom_description.lower()
        
        # Find matching category based on keywords or use provided category
        matched_category = None
        if category and category in cls.SYMPTOM_DATABASE:
            matched_category = category
        else:
            # Search through all categories
            for cat_name, cat_data in cls.SYMPTOM_DATABASE.items():
                if cat_name == 'general':
                    continue
                for keyword in cat_data['keywords']:
                    if keyword in symptom_lower:
                        matched_category = cat_name
                        break
                if matched_category:
                    break
        
        # Use general if no match found
        if not matched_category:
            matched_category = 'general'
        
        category_data = cls.SYMPTOM_DATABASE[matched_category]
        
        # Adjust concern level based on age (elderly and children get higher concern)
        concern_level = category_data['concern_level']
        if age < 5 or age > 65:
            if concern_level == 'mild':
                concern_level = 'moderate'
        
        # Build result
        result = {
            'category': matched_category,
            'concern_level': concern_level,
            'recommended_specialist': category_data['specialization_name'],
            'diet_tips': category_data['diet_tips'],
            'care_instructions': category_data['care_instructions'],
            'disclaimer': 'This is NOT a medical diagnosis. Please consult a qualified healthcare professional for accurate diagnosis and treatment.'
        }
        
        return result
