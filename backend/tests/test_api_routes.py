"""
Unit tests for API routes
"""

import unittest
import json
import os
import tempfile
from backend.app import create_app
from backend.models.database_manager import DatabaseManager


class TestAPIRoutes(unittest.TestCase):
    """Test cases for API routes"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Override database path in the app
        os.environ['DATABASE_PATH'] = self.db_path
        
        # Create test app
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Clean up test fixtures"""
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
    
    def test_calculate_risk_success(self):
        """Test risk calculation with valid data"""
        test_data = {
            'age': 30,
            'weight_kg': 70,
            'height_cm': 175,
            'systolic': 120,
            'diastolic': 80,
            'cholesterol': 190,
            'is_smoker': False,
            'exercise_days': 3
        }
        
        response = self.client.post('/api/risk',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('overall_score', data)
        self.assertIn('risk_level', data)
        self.assertIn('bmi', data)
        self.assertIn('assessment_id', data)
    
    def test_calculate_risk_missing_fields(self):
        """Test risk calculation with missing fields"""
        test_data = {
            'age': 30,
            'weight_kg': 70
        }
        
        response = self.client.post('/api/risk',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_calculate_risk_invalid_age(self):
        """Test risk calculation with invalid age"""
        test_data = {
            'age': 200,  # Invalid age
            'weight_kg': 70,
            'height_cm': 175,
            'systolic': 120,
            'diastolic': 80,
            'cholesterol': 190,
            'is_smoker': False,
            'exercise_days': 3
        }
        
        response = self.client.post('/api/risk',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_get_history(self):
        """Test getting assessment history"""
        # First, create an assessment
        test_data = {
            'age': 30,
            'weight_kg': 70,
            'height_cm': 175,
            'systolic': 120,
            'diastolic': 80,
            'cholesterol': 190,
            'is_smoker': False,
            'exercise_days': 3
        }
        
        self.client.post('/api/risk',
                        data=json.dumps(test_data),
                        content_type='application/json')
        
        # Get history
        response = self.client.get('/api/history')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', data)
        self.assertIn('assessments', data)
        self.assertGreater(data['count'], 0)
    
    def test_get_assessment_by_id(self):
        """Test getting a specific assessment"""
        # Create an assessment first
        test_data = {
            'age': 30,
            'weight_kg': 70,
            'height_cm': 175,
            'systolic': 120,
            'diastolic': 80,
            'cholesterol': 190,
            'is_smoker': False,
            'exercise_days': 3
        }
        
        create_response = self.client.post('/api/risk',
                                          data=json.dumps(test_data),
                                          content_type='application/json')
        create_data = json.loads(create_response.data)
        assessment_id = create_data['assessment_id']
        
        # Get the assessment
        response = self.client.get(f'/api/history/{assessment_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['age'], 30)
    
    def test_get_assessment_not_found(self):
        """Test getting a non-existent assessment"""
        response = self.client.get('/api/history/999999')
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_assessment(self):
        """Test deleting an assessment"""
        # Create an assessment first
        test_data = {
            'age': 30,
            'weight_kg': 70,
            'height_cm': 175,
            'systolic': 120,
            'diastolic': 80,
            'cholesterol': 190,
            'is_smoker': False,
            'exercise_days': 3
        }
        
        create_response = self.client.post('/api/risk',
                                          data=json.dumps(test_data),
                                          content_type='application/json')
        create_data = json.loads(create_response.data)
        assessment_id = create_data['assessment_id']
        
        # Delete the assessment
        response = self.client.delete(f'/api/history/{assessment_id}')
        
        self.assertEqual(response.status_code, 200)
        
        # Verify it's deleted
        get_response = self.client.get(f'/api/history/{assessment_id}')
        self.assertEqual(get_response.status_code, 404)
    
    def test_get_statistics(self):
        """Test getting statistics"""
        # Create a few assessments
        for i in range(3):
            test_data = {
                'age': 30 + i,
                'weight_kg': 70,
                'height_cm': 175,
                'systolic': 120,
                'diastolic': 80,
                'cholesterol': 190,
                'is_smoker': False,
                'exercise_days': 3
            }
            
            self.client.post('/api/risk',
                           data=json.dumps(test_data),
                           content_type='application/json')
        
        # Get statistics
        response = self.client.get('/api/statistics')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_assessments', data)
        self.assertEqual(data['total_assessments'], 3)


if __name__ == '__main__':
    unittest.main()
