"""
Unit tests for RiskCalculator
"""

import unittest
from backend.models.risk_calculator import RiskCalculator


class TestRiskCalculator(unittest.TestCase):
    """Test cases for RiskCalculator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = RiskCalculator()
    
    def test_calculate_bmi(self):
        """Test BMI calculation"""
        # Normal BMI
        bmi = self.calculator.calculate_bmi(70, 175)
        self.assertAlmostEqual(bmi, 22.86, places=2)
        
        # Underweight BMI
        bmi = self.calculator.calculate_bmi(50, 175)
        self.assertAlmostEqual(bmi, 16.33, places=2)
    
    def test_get_bmi_risk_score(self):
        """Test BMI risk scoring"""
        # Normal weight
        self.assertEqual(self.calculator.get_bmi_risk_score(22), 10)
        
        # Underweight
        self.assertEqual(self.calculator.get_bmi_risk_score(17), 30)
        
        # Overweight
        self.assertEqual(self.calculator.get_bmi_risk_score(27), 40)
        
        # Obese
        self.assertEqual(self.calculator.get_bmi_risk_score(32), 70)
    
    def test_get_age_risk_score(self):
        """Test age risk scoring"""
        self.assertEqual(self.calculator.get_age_risk_score(25), 10)
        self.assertEqual(self.calculator.get_age_risk_score(35), 20)
        self.assertEqual(self.calculator.get_age_risk_score(50), 40)
        self.assertEqual(self.calculator.get_age_risk_score(65), 60)
    
    def test_get_blood_pressure_risk_score(self):
        """Test blood pressure risk scoring"""
        # Normal
        self.assertEqual(self.calculator.get_blood_pressure_risk_score(115, 75), 10)
        
        # Elevated
        self.assertEqual(self.calculator.get_blood_pressure_risk_score(125, 78), 20)
        
        # Stage 1 Hypertension
        self.assertEqual(self.calculator.get_blood_pressure_risk_score(135, 85), 50)
        
        # Stage 2 Hypertension
        self.assertEqual(self.calculator.get_blood_pressure_risk_score(145, 95), 80)
    
    def test_get_cholesterol_risk_score(self):
        """Test cholesterol risk scoring"""
        # Desirable
        self.assertEqual(self.calculator.get_cholesterol_risk_score(180), 10)
        
        # Borderline high
        self.assertEqual(self.calculator.get_cholesterol_risk_score(220), 40)
        
        # High
        self.assertEqual(self.calculator.get_cholesterol_risk_score(260), 70)
    
    def test_get_smoking_risk_score(self):
        """Test smoking risk scoring"""
        self.assertEqual(self.calculator.get_smoking_risk_score(False), 10)
        self.assertEqual(self.calculator.get_smoking_risk_score(True), 60)
    
    def test_get_exercise_risk_score(self):
        """Test exercise risk scoring"""
        self.assertEqual(self.calculator.get_exercise_risk_score(5), 10)
        self.assertEqual(self.calculator.get_exercise_risk_score(3), 20)
        self.assertEqual(self.calculator.get_exercise_risk_score(1), 40)
        self.assertEqual(self.calculator.get_exercise_risk_score(0), 60)
    
    def test_calculate_risk_low(self):
        """Test overall risk calculation for low risk profile"""
        data = {
            'age': 25,
            'weight_kg': 70,
            'height_cm': 175,
            'systolic': 115,
            'diastolic': 75,
            'cholesterol': 180,
            'is_smoker': False,
            'exercise_days': 5
        }
        
        result = self.calculator.calculate_risk(data)
        
        self.assertIn('overall_score', result)
        self.assertIn('risk_level', result)
        self.assertIn('bmi', result)
        self.assertIn('breakdown', result)
        self.assertEqual(result['risk_level'], 'Low')
        self.assertAlmostEqual(result['bmi'], 22.86, places=2)
    
    def test_calculate_risk_high(self):
        """Test overall risk calculation for high risk profile"""
        data = {
            'age': 65,
            'weight_kg': 95,
            'height_cm': 170,
            'systolic': 150,
            'diastolic': 95,
            'cholesterol': 260,
            'is_smoker': True,
            'exercise_days': 0
        }
        
        result = self.calculator.calculate_risk(data)
        
        self.assertEqual(result['risk_level'], 'High')
        self.assertGreater(result['overall_score'], 50)


if __name__ == '__main__':
    unittest.main()
