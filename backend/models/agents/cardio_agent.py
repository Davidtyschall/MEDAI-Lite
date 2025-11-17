"""
Cardiovascular Risk Assessment Agent
Specialized agent for cardiovascular disease risk evaluation.
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class CardioAgent(BaseAgent):
    """
    Assesses cardiovascular health risks based on blood pressure,
    cholesterol, smoking status, and other cardiac indicators.
    """
    
    def __init__(self):
        super().__init__(name="CardioAgent", weight=0.35)
        
        # Risk thresholds
        self.bp_thresholds = {
            'optimal': (120, 80),
            'normal': (130, 85),
            'high_normal': (140, 90),
            'stage1': (160, 100),
            'stage2': (180, 110)
        }
        
        self.cholesterol_thresholds = {
            'desirable': 200,
            'borderline': 240,
            'high': 280
        }
    
    def assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess cardiovascular risk.
        
        Args:
            data (dict): Must contain:
                - systolic (int): Systolic BP
                - diastolic (int): Diastolic BP
                - cholesterol (int): Total cholesterol
                - is_smoker (bool): Smoking status
                - age (int): Age in years
                - exercise_days (int): Exercise frequency
                
        Returns:
            dict: Cardiovascular risk assessment
        """
        self.validate_data(data, [
            'systolic', 'diastolic', 'cholesterol', 
            'is_smoker', 'age', 'exercise_days'
        ])
        
        # Calculate individual risk components
        bp_risk = self._assess_blood_pressure(data['systolic'], data['diastolic'])
        cholesterol_risk = self._assess_cholesterol(data['cholesterol'])
        smoking_risk = 80 if data['is_smoker'] else 10
        age_risk = self._assess_age_risk(data['age'])
        exercise_risk = self._assess_exercise_risk(data['exercise_days'])
        
        # Calculate weighted cardiovascular risk score
        risk_score = (
            bp_risk * 0.35 +
            cholesterol_risk * 0.30 +
            smoking_risk * 0.20 +
            age_risk * 0.10 +
            exercise_risk * 0.05
        )
        
        # Determine risk level
        if risk_score < 25:
            risk_level = 'Low'
        elif risk_score < 50:
            risk_level = 'Moderate'
        elif risk_score < 75:
            risk_level = 'High'
        else:
            risk_level = 'Critical'
        
        return {
            'risk_score': round(risk_score, 2),
            'risk_level': risk_level,
            'category': 'Cardiovascular',
            'breakdown': {
                'blood_pressure': bp_risk,
                'cholesterol': cholesterol_risk,
                'smoking': smoking_risk,
                'age': age_risk,
                'exercise': exercise_risk
            },
            'details': {
                'bp_classification': self._classify_blood_pressure(
                    data['systolic'], data['diastolic']
                ),
                'cholesterol_classification': self._classify_cholesterol(
                    data['cholesterol']
                )
            }
        }
    
    def _assess_blood_pressure(self, systolic: int, diastolic: int) -> float:
        """Calculate risk score from blood pressure."""
        if systolic < 120 and diastolic < 80:
            return 10  # Optimal
        elif systolic < 130 and diastolic < 85:
            return 20  # Normal
        elif systolic < 140 or diastolic < 90:
            return 40  # High Normal
        elif systolic < 160 or diastolic < 100:
            return 60  # Stage 1 Hypertension
        elif systolic < 180 or diastolic < 110:
            return 80  # Stage 2 Hypertension
        else:
            return 100  # Severe Hypertension
    
    def _classify_blood_pressure(self, systolic: int, diastolic: int) -> str:
        """Classify blood pressure category."""
        if systolic < 120 and diastolic < 80:
            return 'Optimal'
        elif systolic < 130 and diastolic < 85:
            return 'Normal'
        elif systolic < 140 or diastolic < 90:
            return 'High Normal'
        elif systolic < 160 or diastolic < 100:
            return 'Stage 1 Hypertension'
        elif systolic < 180 or diastolic < 110:
            return 'Stage 2 Hypertension'
        else:
            return 'Severe Hypertension'
    
    def _assess_cholesterol(self, cholesterol: int) -> float:
        """Calculate risk score from cholesterol level."""
        if cholesterol < 200:
            return 10  # Desirable
        elif cholesterol < 240:
            return 50  # Borderline High
        elif cholesterol < 280:
            return 75  # High
        else:
            return 95  # Very High
    
    def _classify_cholesterol(self, cholesterol: int) -> str:
        """Classify cholesterol category."""
        if cholesterol < 200:
            return 'Desirable'
        elif cholesterol < 240:
            return 'Borderline High'
        elif cholesterol < 280:
            return 'High'
        else:
            return 'Very High'
    
    def _assess_age_risk(self, age: int) -> float:
        """Calculate age-related cardiovascular risk."""
        if age < 30:
            return 10
        elif age < 40:
            return 20
        elif age < 50:
            return 35
        elif age < 60:
            return 50
        elif age < 70:
            return 70
        else:
            return 85
    
    def _assess_exercise_risk(self, exercise_days: int) -> float:
        """Calculate risk from exercise frequency."""
        if exercise_days >= 5:
            return 10  # Very active
        elif exercise_days >= 3:
            return 30  # Moderately active
        elif exercise_days >= 1:
            return 50  # Lightly active
        else:
            return 80  # Sedentary
    
    def get_recommendations(self, risk_score: float) -> list:
        """
        Generate cardiovascular health recommendations.
        
        Args:
            risk_score (float): Cardiovascular risk score
            
        Returns:
            list: Personalized recommendations
        """
        recommendations = []
        
        if risk_score < 25:
            recommendations.extend([
                "Maintain your current healthy lifestyle",
                "Continue regular cardiovascular exercise",
                "Keep monitoring your blood pressure and cholesterol"
            ])
        elif risk_score < 50:
            recommendations.extend([
                "Consult with a healthcare provider about your cardiovascular health",
                "Increase physical activity to at least 150 minutes per week",
                "Consider dietary changes to lower cholesterol",
                "Monitor blood pressure regularly"
            ])
        elif risk_score < 75:
            recommendations.extend([
                "Schedule an appointment with a cardiologist",
                "Implement immediate lifestyle modifications",
                "Quit smoking if applicable",
                "Consider medication for blood pressure/cholesterol management",
                "Daily cardiovascular exercise as approved by your doctor"
            ])
        else:
            recommendations.extend([
                "⚠️ URGENT: Seek immediate medical attention",
                "Schedule emergency consultation with a cardiologist",
                "Begin prescribed medication regimen",
                "Strict lifestyle modification under medical supervision",
                "Daily monitoring of vital signs"
            ])
        
        return recommendations
