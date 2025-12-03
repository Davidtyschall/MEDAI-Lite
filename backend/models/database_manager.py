"""
Database Manager Module
Manages SQLite database operations for health risk assessments.
"""

import sqlite3
import json
import os


class DatabaseManager:
    """
    Manages database operations for storing and retrieving health risk assessments.
    """
    
    def __init__(self, db_path='/var/data/medai_lite.db'):
        """
        Initialize DatabaseManager
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """
        Get database connection
        
        Returns:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """
        Initialize database tables if they don't exist
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create risk_assessments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                age INTEGER NOT NULL,
                weight_kg REAL NOT NULL,
                height_cm REAL NOT NULL,
                systolic INTEGER NOT NULL,
                diastolic INTEGER NOT NULL,
                cholesterol INTEGER NOT NULL,
                is_smoker BOOLEAN NOT NULL,
                exercise_days INTEGER NOT NULL,
                bmi REAL NOT NULL,
                overall_score REAL NOT NULL,
                risk_level TEXT NOT NULL,
                breakdown TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_assessment(self, user_id, health_data, risk_result):
        """
        Save a risk assessment to the database
        
        Args:
            user_id (int): User ID (can be None for guest users)
            health_data (dict): Health data parameters
            risk_result (dict): Risk calculation results
            
        Returns:
            int: Assessment ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO risk_assessments (
                user_id, age, weight_kg, height_cm, systolic, diastolic,
                cholesterol, is_smoker, exercise_days, bmi, overall_score,
                risk_level, breakdown
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            health_data['age'],
            health_data['weight_kg'],
            health_data['height_cm'],
            health_data['systolic'],
            health_data['diastolic'],
            health_data['cholesterol'],
            health_data['is_smoker'],
            health_data['exercise_days'],
            risk_result['bmi'],
            risk_result['overall_score'],
            risk_result['risk_level'],
            json.dumps(risk_result['breakdown'])
        ))
        
        assessment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return assessment_id
    
    def get_assessment_history(self, user_id=None, limit=10):
        """
        Get assessment history
        
        Args:
            user_id (int): User ID (None for all assessments)
            limit (int): Maximum number of records to return
            
        Returns:
            list: List of assessment records
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id is not None:
            cursor.execute('''
                SELECT * FROM risk_assessments
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT * FROM risk_assessments
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        assessments = []
        for row in rows:
            assessment = dict(row)
            assessment['breakdown'] = json.loads(assessment['breakdown'])
            assessments.append(assessment)
        
        return assessments
    
    def get_assessment_by_id(self, assessment_id):
        """
        Get a specific assessment by ID
        
        Args:
            assessment_id (int): Assessment ID
            
        Returns:
            dict: Assessment record or None if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM risk_assessments
            WHERE id = ?
        ''', (assessment_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            assessment = dict(row)
            assessment['breakdown'] = json.loads(assessment['breakdown'])
            return assessment
        
        return None
    
    def get_statistics(self, user_id=None):
        """
        Get statistics about assessments
        
        Args:
            user_id (int): User ID (None for all assessments)
            
        Returns:
            dict: Statistics including total assessments, average scores, etc.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id is not None:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_assessments,
                    AVG(overall_score) as avg_risk_score,
                    AVG(bmi) as avg_bmi,
                    SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk_count,
                    SUM(CASE WHEN risk_level = 'Moderate' THEN 1 ELSE 0 END) as moderate_risk_count,
                    SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) as high_risk_count
                FROM risk_assessments
                WHERE user_id = ?
            ''', (user_id,))
        else:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_assessments,
                    AVG(overall_score) as avg_risk_score,
                    AVG(bmi) as avg_bmi,
                    SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk_count,
                    SUM(CASE WHEN risk_level = 'Moderate' THEN 1 ELSE 0 END) as moderate_risk_count,
                    SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) as high_risk_count
                FROM risk_assessments
            ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'total_assessments': row['total_assessments'],
                'avg_risk_score': round(row['avg_risk_score'], 2) if row['avg_risk_score'] else 0,
                'avg_bmi': round(row['avg_bmi'], 2) if row['avg_bmi'] else 0,
                'low_risk_count': row['low_risk_count'],
                'moderate_risk_count': row['moderate_risk_count'],
                'high_risk_count': row['high_risk_count']
            }
        
        return None
    
    def delete_assessment(self, assessment_id):
        """
        Delete an assessment by ID
        
        Args:
            assessment_id (int): Assessment ID
            
        Returns:
            bool: True if deleted, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM risk_assessments WHERE id = ?', (assessment_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
