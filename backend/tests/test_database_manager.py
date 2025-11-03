"""
Unit tests for DatabaseManager
"""

import unittest
import os
import tempfile
from backend.models.database_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager class"""
    
    def setUp(self):
        """Set up test fixtures with temporary database"""
        # Create temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.db_manager = DatabaseManager(self.db_path)
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Close and remove temporary database
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_database_initialization(self):
        """Test database tables are created"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Check users table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        """)
        self.assertIsNotNone(cursor.fetchone())
        
        # Check risk_assessments table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='risk_assessments'
        """)
        self.assertIsNotNone(cursor.fetchone())
        
        conn.close()
    
    def test_save_assessment(self):
        """Test saving an assessment"""
        health_data = {
            'age': 30,
            'weight_kg': 70.0,
            'height_cm': 175.0,
            'systolic': 120,
            'diastolic': 80,
            'cholesterol': 190,
            'is_smoker': False,
            'exercise_days': 3
        }
        
        risk_result = {
            'overall_score': 25.5,
            'risk_level': 'Moderate',
            'bmi': 22.86,
            'breakdown': {
                'age': 20,
                'bmi': 10,
                'blood_pressure': 10,
                'cholesterol': 10,
                'smoking': 10,
                'exercise': 20
            }
        }
        
        assessment_id = self.db_manager.save_assessment(None, health_data, risk_result)
        
        self.assertIsNotNone(assessment_id)
        self.assertGreater(assessment_id, 0)
    
    def test_get_assessment_by_id(self):
        """Test retrieving an assessment by ID"""
        # Save an assessment first
        health_data = {
            'age': 30,
            'weight_kg': 70.0,
            'height_cm': 175.0,
            'systolic': 120,
            'diastolic': 80,
            'cholesterol': 190,
            'is_smoker': False,
            'exercise_days': 3
        }
        
        risk_result = {
            'overall_score': 25.5,
            'risk_level': 'Moderate',
            'bmi': 22.86,
            'breakdown': {
                'age': 20,
                'bmi': 10,
                'blood_pressure': 10,
                'cholesterol': 10,
                'smoking': 10,
                'exercise': 20
            }
        }
        
        assessment_id = self.db_manager.save_assessment(None, health_data, risk_result)
        
        # Retrieve the assessment
        retrieved = self.db_manager.get_assessment_by_id(assessment_id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['age'], 30)
        self.assertEqual(retrieved['risk_level'], 'Moderate')
        self.assertAlmostEqual(retrieved['overall_score'], 25.5)
    
    def test_get_assessment_history(self):
        """Test retrieving assessment history"""
        # Save multiple assessments
        for i in range(3):
            health_data = {
                'age': 30 + i,
                'weight_kg': 70.0,
                'height_cm': 175.0,
                'systolic': 120,
                'diastolic': 80,
                'cholesterol': 190,
                'is_smoker': False,
                'exercise_days': 3
            }
            
            risk_result = {
                'overall_score': 25.5 + i,
                'risk_level': 'Moderate',
                'bmi': 22.86,
                'breakdown': {
                    'age': 20,
                    'bmi': 10,
                    'blood_pressure': 10,
                    'cholesterol': 10,
                    'smoking': 10,
                    'exercise': 20
                }
            }
            
            self.db_manager.save_assessment(None, health_data, risk_result)
        
        # Retrieve history
        history = self.db_manager.get_assessment_history(limit=10)
        
        self.assertEqual(len(history), 3)
        # Check order (most recent first)
        self.assertEqual(history[0]['age'], 32)
        self.assertEqual(history[1]['age'], 31)
        self.assertEqual(history[2]['age'], 30)
    
    def test_get_statistics(self):
        """Test retrieving statistics"""
        # Save assessments with different risk levels
        test_data = [
            ('Low', 20.0),
            ('Moderate', 35.0),
            ('High', 60.0)
        ]
        
        for risk_level, score in test_data:
            health_data = {
                'age': 30,
                'weight_kg': 70.0,
                'height_cm': 175.0,
                'systolic': 120,
                'diastolic': 80,
                'cholesterol': 190,
                'is_smoker': False,
                'exercise_days': 3
            }
            
            risk_result = {
                'overall_score': score,
                'risk_level': risk_level,
                'bmi': 22.86,
                'breakdown': {
                    'age': 20,
                    'bmi': 10,
                    'blood_pressure': 10,
                    'cholesterol': 10,
                    'smoking': 10,
                    'exercise': 20
                }
            }
            
            self.db_manager.save_assessment(None, health_data, risk_result)
        
        # Get statistics
        stats = self.db_manager.get_statistics()
        
        self.assertEqual(stats['total_assessments'], 3)
        self.assertEqual(stats['low_risk_count'], 1)
        self.assertEqual(stats['moderate_risk_count'], 1)
        self.assertEqual(stats['high_risk_count'], 1)
        self.assertAlmostEqual(stats['avg_risk_score'], 38.33, places=2)
    
    def test_delete_assessment(self):
        """Test deleting an assessment"""
        # Save an assessment first
        health_data = {
            'age': 30,
            'weight_kg': 70.0,
            'height_cm': 175.0,
            'systolic': 120,
            'diastolic': 80,
            'cholesterol': 190,
            'is_smoker': False,
            'exercise_days': 3
        }
        
        risk_result = {
            'overall_score': 25.5,
            'risk_level': 'Moderate',
            'bmi': 22.86,
            'breakdown': {
                'age': 20,
                'bmi': 10,
                'blood_pressure': 10,
                'cholesterol': 10,
                'smoking': 10,
                'exercise': 20
            }
        }
        
        assessment_id = self.db_manager.save_assessment(None, health_data, risk_result)
        
        # Delete the assessment
        deleted = self.db_manager.delete_assessment(assessment_id)
        self.assertTrue(deleted)
        
        # Verify it's deleted
        retrieved = self.db_manager.get_assessment_by_id(assessment_id)
        self.assertIsNone(retrieved)


if __name__ == '__main__':
    unittest.main()
