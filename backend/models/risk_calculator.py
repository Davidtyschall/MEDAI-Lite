"""
Risk Calculator Module
Calculates health risk scores based on user input parameters.
"""


class RiskCalculator:
    """
    Calculates health risk scores based on various health parameters.
    """
    
    def __init__(self):
        # Risk factor weights
        self.weights = {
            'age': 0.15,
            'bmi': 0.20,
            'blood_pressure': 0.25,
            'cholesterol': 0.20,
            'smoking': 0.10,
            'exercise': 0.10
        }
    
    def calculate_bmi(self, weight_kg, height_cm):
        """
        Calculate Body Mass Index (BMI)
        
        Args:
            weight_kg (float): Weight in kilograms
            height_cm (float): Height in centimeters
            
        Returns:
            float: BMI value
        """
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    def get_bmi_risk_score(self, bmi):
        """
        Get risk score based on BMI
        
        Args:
            bmi (float): BMI value
            
        Returns:
            int: Risk score (0-100)
        """
        if bmi < 18.5:
            return 30  # Underweight
        elif 18.5 <= bmi < 25:
            return 10  # Normal
        elif 25 <= bmi < 30:
            return 40  # Overweight
        else:
            return 70  # Obese
    
    def get_age_risk_score(self, age):
        """
        Get risk score based on age
        
        Args:
            age (int): Age in years
            
        Returns:
            int: Risk score (0-100)
        """
        if age < 30:
            return 10
        elif 30 <= age < 45:
            return 20
        elif 45 <= age < 60:
            return 40
        else:
            return 60
    
    def get_blood_pressure_risk_score(self, systolic, diastolic):
        """
        Get risk score based on blood pressure
        
        Args:
            systolic (int): Systolic blood pressure
            diastolic (int): Diastolic blood pressure
            
        Returns:
            int: Risk score (0-100)
        """
        if systolic < 120 and diastolic < 80:
            return 10  # Normal
        elif systolic < 130 and diastolic < 80:
            return 20  # Elevated
        elif systolic < 140 or diastolic < 90:
            return 50  # Stage 1 Hypertension
        else:
            return 80  # Stage 2 Hypertension
    
    def get_cholesterol_risk_score(self, total_cholesterol):
        """
        Get risk score based on cholesterol levels
        
        Args:
            total_cholesterol (int): Total cholesterol in mg/dL
            
        Returns:
            int: Risk score (0-100)
        """
        if total_cholesterol < 200:
            return 10  # Desirable
        elif 200 <= total_cholesterol < 240:
            return 40  # Borderline high
        else:
            return 70  # High
    
    def get_smoking_risk_score(self, is_smoker):
        """
        Get risk score based on smoking status
        
        Args:
            is_smoker (bool): Whether the person smokes
            
        Returns:
            int: Risk score (0-100)
        """
        return 60 if is_smoker else 10
    
    def get_exercise_risk_score(self, exercise_days_per_week):
        """
        Get risk score based on exercise frequency
        
        Args:
            exercise_days_per_week (int): Number of days exercising per week
            
        Returns:
            int: Risk score (0-100)
        """
        if exercise_days_per_week >= 5:
            return 10  # Very active
        elif exercise_days_per_week >= 3:
            return 20  # Moderately active
        elif exercise_days_per_week >= 1:
            return 40  # Lightly active
        else:
            return 60  # Sedentary
    
    def calculate_risk(self, data):
        """
        Calculate overall health risk score
        
        Args:
            data (dict): Health data containing:
                - age (int)
                - weight_kg (float)
                - height_cm (float)
                - systolic (int)
                - diastolic (int)
                - cholesterol (int)
                - is_smoker (bool)
                - exercise_days (int)
                
        Returns:
            dict: Risk assessment results including overall score and breakdown
        """
        # Calculate BMI
        bmi = self.calculate_bmi(data['weight_kg'], data['height_cm'])
        
        # Calculate individual risk scores
        age_score = self.get_age_risk_score(data['age'])
        bmi_score = self.get_bmi_risk_score(bmi)
        bp_score = self.get_blood_pressure_risk_score(data['systolic'], data['diastolic'])
        cholesterol_score = self.get_cholesterol_risk_score(data['cholesterol'])
        smoking_score = self.get_smoking_risk_score(data['is_smoker'])
        exercise_score = self.get_exercise_risk_score(data['exercise_days'])
        
        # Calculate weighted overall risk score
        overall_score = (
            age_score * self.weights['age'] +
            bmi_score * self.weights['bmi'] +
            bp_score * self.weights['blood_pressure'] +
            cholesterol_score * self.weights['cholesterol'] +
            smoking_score * self.weights['smoking'] +
            exercise_score * self.weights['exercise']
        )
        
        # Determine risk level
        if overall_score < 25:
            risk_level = 'Low'
        elif overall_score < 50:
            risk_level = 'Moderate'
        else:
            risk_level = 'High'
        
        return {
            'overall_score': round(overall_score, 2),
            'risk_level': risk_level,
            'bmi': round(bmi, 2),
            'breakdown': {
                'age': age_score,
                'bmi': bmi_score,
                'blood_pressure': bp_score,
                'cholesterol': cholesterol_score,
                'smoking': smoking_score,
                'exercise': exercise_score
            }
        }
