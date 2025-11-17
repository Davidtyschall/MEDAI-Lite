"""
Metabolic Risk Assessment Agent
Specialized agent for metabolic syndrome and diabetes risk evaluation.
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class MetabolicAgent(BaseAgent):
    """
    Assesses metabolic health risks including diabetes, obesity,
    and metabolic syndrome based on BMI, blood glucose, and other indicators.
    """
    
    def __init__(self):
        super().__init__(name="MetabolicAgent", weight=0.35)
        
        # BMI categories
        self.bmi_categories = {
            'underweight': 18.5,
            'normal': 25.0,
            'overweight': 30.0,
            'obese': 35.0,
            'severely_obese': 40.0
        }
    
    def assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess metabolic risk.
        
        Args:
            data (dict): Must contain:
                - weight_kg (float): Weight in kilograms
                - height_cm (float): Height in centimeters
                - age (int): Age in years
                - exercise_days (int): Exercise frequency
                - cholesterol (int): Total cholesterol (for metabolic syndrome)
                
        Returns:
            dict: Metabolic risk assessment
        """
        self.validate_data(data, [
            'weight_kg', 'height_cm', 'age', 'exercise_days', 'cholesterol'
        ])
        
        # Calculate BMI
        bmi = self._calculate_bmi(data['weight_kg'], data['height_cm'])
        
        # Calculate individual risk components
        bmi_risk = self._assess_bmi_risk(bmi)
        age_risk = self._assess_age_metabolic_risk(data['age'])
        exercise_risk = self._assess_exercise_impact(data['exercise_days'])
        lipid_risk = self._assess_lipid_profile(data['cholesterol'])
        
        # Calculate weighted metabolic risk score
        risk_score = (
            bmi_risk * 0.40 +
            lipid_risk * 0.30 +
            exercise_risk * 0.20 +
            age_risk * 0.10
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
            'category': 'Metabolic',
            'bmi': round(bmi, 2),
            'breakdown': {
                'bmi': bmi_risk,
                'lipid_profile': lipid_risk,
                'exercise': exercise_risk,
                'age': age_risk
            },
            'details': {
                'bmi_classification': self._classify_bmi(bmi),
                'metabolic_syndrome_indicators': self._check_metabolic_syndrome(
                    bmi, data['cholesterol']
                )
            }
        }
    
    def _calculate_bmi(self, weight_kg: float, height_cm: float) -> float:
        """Calculate Body Mass Index."""
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    def _assess_bmi_risk(self, bmi: float) -> float:
        """Calculate risk score from BMI."""
        if bmi < 18.5:
            return 40  # Underweight - health risk
        elif bmi < 25:
            return 10  # Normal
        elif bmi < 30:
            return 45  # Overweight
        elif bmi < 35:
            return 70  # Obese Class I
        elif bmi < 40:
            return 85  # Obese Class II
        else:
            return 95  # Obese Class III (Severe)
    
    def _classify_bmi(self, bmi: float) -> str:
        """Classify BMI category."""
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal Weight'
        elif bmi < 30:
            return 'Overweight'
        elif bmi < 35:
            return 'Obese Class I'
        elif bmi < 40:
            return 'Obese Class II'
        else:
            return 'Obese Class III (Severe)'
    
    def _assess_age_metabolic_risk(self, age: int) -> float:
        """Calculate age-related metabolic risk."""
        if age < 30:
            return 10
        elif age < 45:
            return 25
        elif age < 60:
            return 45
        else:
            return 65
    
    def _assess_exercise_impact(self, exercise_days: int) -> float:
        """Calculate metabolic risk from exercise frequency."""
        if exercise_days >= 5:
            return 10  # Excellent
        elif exercise_days >= 3:
            return 25  # Good
        elif exercise_days >= 1:
            return 50  # Fair
        else:
            return 80  # Poor - high metabolic risk
    
    def _assess_lipid_profile(self, cholesterol: int) -> float:
        """Calculate metabolic risk from lipid levels."""
        if cholesterol < 200:
            return 10  # Optimal
        elif cholesterol < 240:
            return 40  # Borderline
        elif cholesterol < 280:
            return 70  # High
        else:
            return 90  # Very High
    
    def _check_metabolic_syndrome(self, bmi: float, cholesterol: int) -> Dict[str, bool]:
        """
        Check for metabolic syndrome indicators.
        Note: This is a simplified check. Full diagnosis requires additional tests.
        """
        return {
            'elevated_bmi': bmi >= 30,
            'elevated_cholesterol': cholesterol >= 240,
            'risk_present': bmi >= 30 or cholesterol >= 240
        }
    
    def get_recommendations(self, risk_score: float) -> list:
        """
        Generate metabolic health recommendations.
        
        Args:
            risk_score (float): Metabolic risk score
            
        Returns:
            list: Personalized recommendations
        """
        recommendations = []
        
        if risk_score < 25:
            recommendations.extend([
                "Maintain your healthy weight and lifestyle",
                "Continue balanced diet and regular exercise",
                "Annual metabolic health screening recommended"
            ])
        elif risk_score < 50:
            recommendations.extend([
                "Consult with a nutritionist for diet optimization",
                "Increase physical activity to 30-45 minutes daily",
                "Monitor weight and BMI regularly",
                "Consider metabolic panel blood work"
            ])
        elif risk_score < 75:
            recommendations.extend([
                "Schedule consultation with endocrinologist",
                "Implement structured weight management program",
                "Regular monitoring of blood glucose and lipids",
                "Consider working with certified diabetes educator",
                "Increase exercise to 60 minutes daily, 5-6 days/week"
            ])
        else:
            recommendations.extend([
                "⚠️ URGENT: Immediate medical evaluation required",
                "Comprehensive metabolic assessment needed",
                "May require medication management",
                "Intensive lifestyle modification program",
                "Regular medical monitoring essential"
            ])
        
        return recommendations
