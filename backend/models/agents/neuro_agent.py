"""
Neurological Risk Assessment Agent
Specialized agent for cognitive and neurological health risk evaluation.
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class NeuroAgent(BaseAgent):
    """
    Assesses neurological health risks including cognitive decline,
    stroke risk, and brain health based on various health indicators.
    """
    
    def __init__(self):
        super().__init__(name="NeuroAgent", weight=0.30)
    
    def assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess neurological risk.
        
        Args:
            data (dict): Must contain:
                - age (int): Age in years
                - systolic (int): Systolic BP (for stroke risk)
                - diastolic (int): Diastolic BP
                - cholesterol (int): Total cholesterol
                - is_smoker (bool): Smoking status
                - exercise_days (int): Exercise frequency (neuroprotective)
                
        Returns:
            dict: Neurological risk assessment
        """
        self.validate_data(data, [
            'age', 'systolic', 'diastolic', 'cholesterol', 
            'is_smoker', 'exercise_days'
        ])
        
        # Calculate individual risk components
        cognitive_age_risk = self._assess_cognitive_age_risk(data['age'])
        stroke_risk = self._assess_stroke_risk(
            data['age'], data['systolic'], data['diastolic'], 
            data['is_smoker'], data['cholesterol']
        )
        neuroprotective_factors = self._assess_neuroprotection(
            data['exercise_days']
        )
        vascular_health = self._assess_vascular_health(
            data['systolic'], data['cholesterol']
        )
        
        # Calculate weighted neurological risk score
        risk_score = (
            cognitive_age_risk * 0.25 +
            stroke_risk * 0.35 +
            vascular_health * 0.25 +
            neuroprotective_factors * 0.15
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
            'category': 'Neurological',
            'breakdown': {
                'cognitive_aging': cognitive_age_risk,
                'stroke_risk': stroke_risk,
                'vascular_health': vascular_health,
                'neuroprotection': neuroprotective_factors
            },
            'details': {
                'stroke_risk_category': self._classify_stroke_risk(stroke_risk),
                'brain_health_factors': self._analyze_brain_health(data)
            }
        }
    
    def _assess_cognitive_age_risk(self, age: int) -> float:
        """Calculate age-related cognitive decline risk."""
        if age < 40:
            return 5  # Minimal risk
        elif age < 50:
            return 15  # Low risk
        elif age < 60:
            return 30  # Moderate risk
        elif age < 70:
            return 50  # Elevated risk
        elif age < 80:
            return 70  # High risk
        else:
            return 85  # Very high risk
    
    def _assess_stroke_risk(self, age: int, systolic: int, diastolic: int, 
                           is_smoker: bool, cholesterol: int) -> float:
        """Calculate stroke risk based on multiple factors."""
        risk = 0
        
        # Age factor
        if age < 45:
            risk += 10
        elif age < 55:
            risk += 25
        elif age < 65:
            risk += 45
        elif age < 75:
            risk += 65
        else:
            risk += 80
        
        # Blood pressure factor (major stroke risk)
        if systolic >= 180 or diastolic >= 110:
            risk += 40
        elif systolic >= 160 or diastolic >= 100:
            risk += 30
        elif systolic >= 140 or diastolic >= 90:
            risk += 15
        
        # Smoking multiplier effect
        if is_smoker:
            risk = risk * 1.4  # 40% increase
        
        # Cholesterol factor
        if cholesterol >= 280:
            risk += 15
        elif cholesterol >= 240:
            risk += 10
        
        return min(risk, 100)  # Cap at 100
    
    def _assess_neuroprotection(self, exercise_days: int) -> float:
        """
        Calculate neuroprotective factors (lower is better).
        Regular exercise is strongly neuroprotective.
        """
        if exercise_days >= 5:
            return 10  # Excellent neuroprotection
        elif exercise_days >= 3:
            return 25  # Good neuroprotection
        elif exercise_days >= 1:
            return 50  # Limited protection
        else:
            return 80  # Minimal neuroprotection
    
    def _assess_vascular_health(self, systolic: int, cholesterol: int) -> float:
        """
        Assess vascular health (critical for brain health).
        Poor vascular health increases dementia and stroke risk.
        """
        vascular_score = 0
        
        # Blood pressure component
        if systolic < 120:
            vascular_score += 10
        elif systolic < 140:
            vascular_score += 30
        elif systolic < 160:
            vascular_score += 60
        else:
            vascular_score += 85
        
        # Cholesterol component
        if cholesterol < 200:
            vascular_score += 10
        elif cholesterol < 240:
            vascular_score += 35
        else:
            vascular_score += 60
        
        return vascular_score / 2  # Average of both components
    
    def _classify_stroke_risk(self, stroke_risk: float) -> str:
        """Classify stroke risk category."""
        if stroke_risk < 25:
            return 'Low Risk'
        elif stroke_risk < 50:
            return 'Moderate Risk'
        elif stroke_risk < 75:
            return 'High Risk'
        else:
            return 'Critical Risk'
    
    def _analyze_brain_health(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Analyze overall brain health factors."""
        analysis = {}
        
        # Exercise impact on brain
        if data['exercise_days'] >= 4:
            analysis['exercise_impact'] = 'Excellent - strong neuroprotection'
        elif data['exercise_days'] >= 2:
            analysis['exercise_impact'] = 'Moderate - some neuroprotection'
        else:
            analysis['exercise_impact'] = 'Poor - limited neuroprotection'
        
        # Vascular health impact
        if data['systolic'] < 130 and data['cholesterol'] < 200:
            analysis['vascular_status'] = 'Healthy - supports brain health'
        elif data['systolic'] < 140 and data['cholesterol'] < 240:
            analysis['vascular_status'] = 'Moderate - monitor for brain health'
        else:
            analysis['vascular_status'] = 'Compromised - may affect brain health'
        
        # Smoking impact
        if data['is_smoker']:
            analysis['smoking_impact'] = 'Negative - increases stroke and dementia risk'
        else:
            analysis['smoking_impact'] = 'Positive - no tobacco-related brain risks'
        
        return analysis
    
    def get_recommendations(self, risk_score: float) -> list:
        """
        Generate neurological health recommendations.
        
        Args:
            risk_score (float): Neurological risk score
            
        Returns:
            list: Personalized recommendations
        """
        recommendations = []
        
        if risk_score < 25:
            recommendations.extend([
                "Maintain brain-healthy lifestyle habits",
                "Continue regular physical exercise for cognitive health",
                "Engage in mentally stimulating activities",
                "Monitor cardiovascular health (impacts brain health)"
            ])
        elif risk_score < 50:
            recommendations.extend([
                "Increase cardiovascular exercise (proven neuroprotective)",
                "Consider cognitive training exercises",
                "Monitor and manage blood pressure closely",
                "Ensure adequate sleep (7-9 hours nightly)",
                "Mediterranean diet recommended for brain health"
            ])
        elif risk_score < 75:
            recommendations.extend([
                "Schedule consultation with neurologist",
                "Comprehensive vascular health assessment needed",
                "Intensive blood pressure management required",
                "Cognitive baseline testing recommended",
                "Quit smoking immediately if applicable",
                "Daily physical activity essential"
            ])
        else:
            recommendations.extend([
                "⚠️ URGENT: Immediate neurological evaluation required",
                "High stroke risk - emergency medical consultation needed",
                "Comprehensive brain health assessment",
                "Aggressive cardiovascular risk factor management",
                "May require preventive medication (antiplatelet, statins)",
                "Consider carotid artery screening"
            ])
        
        return recommendations
