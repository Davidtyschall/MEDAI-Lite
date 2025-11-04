"""
Unit tests for Health Assessment Agents
"""

import unittest
from backend.models.agents import CardioAgent, MetabolicAgent, NeuroAgent, AggregatorAgent


class TestCardioAgent(unittest.TestCase):
    """Test cases for CardioAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = CardioAgent()
        self.test_data = {
            'age': 45,
            'systolic': 130,
            'diastolic': 85,
            'cholesterol': 210,
            'is_smoker': False,
            'exercise_days': 3
        }
    
    def test_agent_initialization(self):
        """Test agent is properly initialized"""
        self.assertEqual(self.agent.name, "CardioAgent")
        self.assertEqual(self.agent.weight, 0.35)
    
    def test_assess_risk_low(self):
        """Test low cardiovascular risk assessment"""
        data = {
            'age': 30,
            'systolic': 115,
            'diastolic': 75,
            'cholesterol': 180,
            'is_smoker': False,
            'exercise_days': 5
        }
        result = self.agent.assess_risk(data)
        
        self.assertIn('risk_score', result)
        self.assertIn('risk_level', result)
        self.assertEqual(result['category'], 'Cardiovascular')
        self.assertLess(result['risk_score'], 30)
    
    def test_assess_risk_high(self):
        """Test high cardiovascular risk assessment"""
        data = {
            'age': 65,
            'systolic': 170,
            'diastolic': 100,
            'cholesterol': 280,
            'is_smoker': True,
            'exercise_days': 0
        }
        result = self.agent.assess_risk(data)
        
        self.assertEqual(result['category'], 'Cardiovascular')
        self.assertGreater(result['risk_score'], 60)
        self.assertIn(result['risk_level'], ['High', 'Critical'])
    
    def test_blood_pressure_classification(self):
        """Test blood pressure classification"""
        result = self.agent.assess_risk(self.test_data)
        self.assertIn('details', result)
        self.assertIn('bp_classification', result['details'])
    
    def test_recommendations(self):
        """Test recommendation generation"""
        recs = self.agent.get_recommendations(30.0)
        self.assertIsInstance(recs, list)
        self.assertGreater(len(recs), 0)
    
    def test_missing_required_field(self):
        """Test that missing required fields raise ValueError"""
        incomplete_data = {'age': 45, 'systolic': 130}
        with self.assertRaises(ValueError):
            self.agent.assess_risk(incomplete_data)


class TestMetabolicAgent(unittest.TestCase):
    """Test cases for MetabolicAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = MetabolicAgent()
        self.test_data = {
            'age': 40,
            'weight_kg': 75,
            'height_cm': 175,
            'exercise_days': 3,
            'cholesterol': 200
        }
    
    def test_agent_initialization(self):
        """Test agent is properly initialized"""
        self.assertEqual(self.agent.name, "MetabolicAgent")
        self.assertEqual(self.agent.weight, 0.35)
    
    def test_bmi_calculation(self):
        """Test BMI calculation"""
        result = self.agent.assess_risk(self.test_data)
        self.assertIn('bmi', result)
        # Expected BMI: 75 / (1.75^2) ≈ 24.49
        self.assertAlmostEqual(result['bmi'], 24.49, places=1)
    
    def test_assess_risk_normal_weight(self):
        """Test metabolic risk with normal weight"""
        data = {
            'age': 30,
            'weight_kg': 70,
            'height_cm': 175,
            'exercise_days': 5,
            'cholesterol': 180
        }
        result = self.agent.assess_risk(data)
        
        self.assertIn('risk_score', result)
        self.assertEqual(result['category'], 'Metabolic')
        self.assertLess(result['risk_score'], 30)
    
    def test_assess_risk_obesity(self):
        """Test metabolic risk with obesity"""
        data = {
            'age': 50,
            'weight_kg': 120,
            'height_cm': 170,
            'exercise_days': 0,
            'cholesterol': 260
        }
        result = self.agent.assess_risk(data)
        
        self.assertGreater(result['risk_score'], 50)
        self.assertIn('bmi_classification', result['details'])
    
    def test_metabolic_syndrome_indicators(self):
        """Test metabolic syndrome indicator detection"""
        data = {
            'age': 55,
            'weight_kg': 100,
            'height_cm': 170,
            'exercise_days': 1,
            'cholesterol': 250
        }
        result = self.agent.assess_risk(data)
        
        self.assertIn('metabolic_syndrome_indicators', result['details'])
        indicators = result['details']['metabolic_syndrome_indicators']
        self.assertIn('elevated_bmi', indicators)
        self.assertIn('elevated_cholesterol', indicators)


class TestNeuroAgent(unittest.TestCase):
    """Test cases for NeuroAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = NeuroAgent()
        self.test_data = {
            'age': 50,
            'systolic': 130,
            'diastolic': 85,
            'cholesterol': 210,
            'is_smoker': False,
            'exercise_days': 3
        }
    
    def test_agent_initialization(self):
        """Test agent is properly initialized"""
        self.assertEqual(self.agent.name, "NeuroAgent")
        self.assertEqual(self.agent.weight, 0.30)
    
    def test_assess_risk_low_stroke_risk(self):
        """Test low neurological/stroke risk"""
        data = {
            'age': 35,
            'systolic': 115,
            'diastolic': 75,
            'cholesterol': 180,
            'is_smoker': False,
            'exercise_days': 5
        }
        result = self.agent.assess_risk(data)
        
        self.assertEqual(result['category'], 'Neurological')
        self.assertLess(result['risk_score'], 30)
    
    def test_assess_risk_high_stroke_risk(self):
        """Test high stroke risk factors"""
        data = {
            'age': 70,
            'systolic': 180,
            'diastolic': 110,
            'cholesterol': 280,
            'is_smoker': True,
            'exercise_days': 0
        }
        result = self.agent.assess_risk(data)
        
        self.assertGreater(result['risk_score'], 60)
        self.assertIn('stroke_risk', result['breakdown'])
    
    def test_brain_health_analysis(self):
        """Test brain health factor analysis"""
        result = self.agent.assess_risk(self.test_data)
        
        self.assertIn('brain_health_factors', result['details'])
        factors = result['details']['brain_health_factors']
        self.assertIn('exercise_impact', factors)
        self.assertIn('vascular_status', factors)
        self.assertIn('smoking_impact', factors)


class TestAggregatorAgent(unittest.TestCase):
    """Test cases for AggregatorAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.aggregator = AggregatorAgent()
        self.complete_data = {
            'age': 45,
            'weight_kg': 80,
            'height_cm': 175,
            'systolic': 135,
            'diastolic': 88,
            'cholesterol': 220,
            'is_smoker': False,
            'exercise_days': 3
        }
    
    def test_aggregator_initialization(self):
        """Test aggregator has all required agents"""
        self.assertIn('cardio', self.aggregator.agents)
        self.assertIn('metabolic', self.aggregator.agents)
        self.assertIn('neuro', self.aggregator.agents)
        self.assertEqual(len(self.aggregator.agents), 3)
    
    def test_comprehensive_assessment(self):
        """Test comprehensive multi-agent assessment"""
        result = self.aggregator.assess_comprehensive_risk(self.complete_data)
        
        self.assertIn('overall_health_index', result)
        self.assertIn('overall_risk_level', result)
        self.assertIn('agent_assessments', result)
        self.assertIn('integrated_recommendations', result)
        self.assertIn('performance', result)
        self.assertIn('metadata', result)
    
    def test_all_agents_run(self):
        """Test that all agents produce results"""
        result = self.aggregator.assess_comprehensive_risk(self.complete_data)
        
        assessments = result['agent_assessments']
        self.assertIn('cardio', assessments)
        self.assertIn('metabolic', assessments)
        self.assertIn('neuro', assessments)
        
        # Check each agent produced valid results
        for agent_name, assessment in assessments.items():
            if 'error' not in assessment:
                self.assertIn('risk_score', assessment)
                self.assertIn('risk_level', assessment)
    
    def test_performance_monitoring(self):
        """Test performance monitoring (≤3s requirement)"""
        result = self.aggregator.assess_comprehensive_risk(self.complete_data)
        
        self.assertIn('performance', result)
        perf = result['performance']
        self.assertIn('total_time_ms', perf)
        self.assertIn('status', perf)
        
        # Check performance target (≤3000ms)
        self.assertLess(perf['total_time_ms'], 3000)
        self.assertEqual(perf['status'], 'optimal')
    
    def test_critical_areas_identification(self):
        """Test identification of critical health areas"""
        high_risk_data = {
            'age': 70,
            'weight_kg': 120,
            'height_cm': 165,
            'systolic': 180,
            'diastolic': 110,
            'cholesterol': 290,
            'is_smoker': True,
            'exercise_days': 0
        }
        
        result = self.aggregator.assess_comprehensive_risk(high_risk_data)
        
        self.assertIn('critical_areas', result)
        critical = result['critical_areas']
        
        # Should have multiple critical areas
        self.assertGreater(len(critical), 0)
        
        # Check structure
        if len(critical) > 0:
            area = critical[0]
            self.assertIn('category', area)
            self.assertIn('risk_level', area)
            self.assertIn('priority', area)
    
    def test_integrated_recommendations(self):
        """Test integrated recommendation generation"""
        result = self.aggregator.assess_comprehensive_risk(self.complete_data)
        
        recommendations = result['integrated_recommendations']
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        self.assertLessEqual(len(recommendations), 15)
    
    def test_performance_stats(self):
        """Test performance statistics tracking"""
        # Run multiple assessments
        for _ in range(3):
            self.aggregator.assess_comprehensive_risk(self.complete_data)
        
        stats = self.aggregator.get_overall_performance_stats()
        
        self.assertEqual(stats['total_assessments'], 3)
        self.assertIn('avg_time_ms', stats)
        self.assertIn('performance_target_met', stats)
        self.assertTrue(stats['performance_target_met'])


if __name__ == '__main__':
    unittest.main()
