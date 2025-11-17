"""
Apple Watch / HealthKit Mock Integration
Simulates Apple Watch data for development and testing.
In production, this would connect to actual HealthKit API.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any


class AppleWatchMock:
    """
    Mock Apple Watch/HealthKit data provider.
    Generates realistic health data for testing and demonstration.
    """
    
    def __init__(self, user_id: int = None):
        """
        Initialize mock Apple Watch.
        
        Args:
            user_id (int): User ID for consistent data generation
        """
        self.user_id = user_id
        self.is_connected = False
        self.device_info = {
            'model': 'Apple Watch Series 9',
            'os_version': 'watchOS 10.0',
            'paired_iphone': 'iPhone 15 Pro'
        }
        
        # Seed random for consistency per user
        if user_id:
            random.seed(user_id)
    
    def connect(self) -> Dict[str, Any]:
        """
        Simulate Apple Watch connection.
        
        Returns:
            dict: Connection status and device info
        """
        self.is_connected = True
        return {
            'connected': True,
            'device': self.device_info,
            'timestamp': datetime.now().isoformat(),
            'data_sources': [
                'heart_rate',
                'blood_oxygen',
                'steps',
                'exercise_minutes',
                'sleep',
                'stand_hours'
            ]
        }
    
    def disconnect(self) -> Dict[str, bool]:
        """Disconnect Apple Watch."""
        self.is_connected = False
        return {'connected': False, 'timestamp': datetime.now().isoformat()}
    
    def get_heart_rate_data(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get heart rate data for past N days.
        
        Args:
            days (int): Number of days of history
            
        Returns:
            list: Heart rate measurements
        """
        data = []
        base_hr = random.randint(60, 80)
        
        for day in range(days):
            date = datetime.now() - timedelta(days=day)
            
            # Generate readings for different times of day
            for hour in [6, 9, 12, 15, 18, 21]:
                reading = {
                    'timestamp': date.replace(hour=hour, minute=0).isoformat(),
                    'value': base_hr + random.randint(-10, 15),
                    'unit': 'bpm',
                    'type': 'resting' if hour in [6, 21] else 'active'
                }
                data.append(reading)
        
        return data
    
    def get_blood_oxygen_data(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get blood oxygen saturation data.
        
        Args:
            days (int): Number of days of history
            
        Returns:
            list: SpO2 measurements
        """
        data = []
        
        for day in range(days):
            date = datetime.now() - timedelta(days=day)
            
            for hour in [8, 14, 20]:
                reading = {
                    'timestamp': date.replace(hour=hour, minute=0).isoformat(),
                    'value': random.randint(95, 99),
                    'unit': '%',
                    'source': 'Apple Watch'
                }
                data.append(reading)
        
        return data
    
    def get_activity_summary(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get daily activity summaries.
        
        Args:
            days (int): Number of days of history
            
        Returns:
            list: Activity summaries
        """
        data = []
        
        for day in range(days):
            date = datetime.now() - timedelta(days=day)
            
            summary = {
                'date': date.strftime('%Y-%m-%d'),
                'steps': random.randint(3000, 12000),
                'distance_km': round(random.uniform(2.0, 8.0), 2),
                'active_calories': random.randint(200, 600),
                'exercise_minutes': random.randint(0, 90),
                'stand_hours': random.randint(6, 12),
                'move_goal_percentage': random.randint(50, 150)
            }
            data.append(summary)
        
        return data
    
    def get_sleep_data(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get sleep tracking data.
        
        Args:
            days (int): Number of days of history
            
        Returns:
            list: Sleep data
        """
        data = []
        
        for day in range(1, days + 1):
            date = datetime.now() - timedelta(days=day)
            
            sleep_hours = round(random.uniform(5.5, 9.0), 1)
            deep_sleep_pct = random.randint(15, 30)
            rem_sleep_pct = random.randint(20, 30)
            light_sleep_pct = 100 - deep_sleep_pct - rem_sleep_pct
            
            summary = {
                'date': date.strftime('%Y-%m-%d'),
                'total_hours': sleep_hours,
                'deep_sleep_percentage': deep_sleep_pct,
                'rem_sleep_percentage': rem_sleep_pct,
                'light_sleep_percentage': light_sleep_pct,
                'sleep_score': random.randint(60, 95),
                'bedtime': '22:30',
                'wake_time': '06:30'
            }
            data.append(summary)
        
        return data
    
    def get_current_vitals(self) -> Dict[str, Any]:
        """
        Get current vital signs (simulated real-time data).
        
        Returns:
            dict: Current vital signs
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'heart_rate': {
                'value': random.randint(65, 85),
                'unit': 'bpm'
            },
            'blood_oxygen': {
                'value': random.randint(96, 99),
                'unit': '%'
            },
            'respiratory_rate': {
                'value': random.randint(12, 18),
                'unit': 'breaths/min'
            }
        }
    
    def get_workout_history(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get workout history.
        
        Args:
            days (int): Number of days of history
            
        Returns:
            list: Workout sessions
        """
        workouts = []
        workout_types = ['Running', 'Walking', 'Cycling', 'Strength', 'Yoga', 'Swimming']
        
        # Random number of workouts in period
        num_workouts = random.randint(3, days * 2)
        
        for i in range(num_workouts):
            day_offset = random.randint(0, days - 1)
            date = datetime.now() - timedelta(days=day_offset)
            
            workout = {
                'date': date.strftime('%Y-%m-%d'),
                'type': random.choice(workout_types),
                'duration_minutes': random.randint(20, 90),
                'calories': random.randint(150, 600),
                'average_heart_rate': random.randint(110, 160),
                'distance_km': round(random.uniform(0, 10.0), 2)
            }
            workouts.append(workout)
        
        # Sort by date (most recent first)
        workouts.sort(key=lambda x: x['date'], reverse=True)
        
        return workouts
    
    def export_health_data(self) -> Dict[str, Any]:
        """
        Export comprehensive health data package.
        Simulates what would be received from HealthKit export.
        
        Returns:
            dict: Complete health data export
        """
        return {
            'export_date': datetime.now().isoformat(),
            'device': self.device_info,
            'user_id': self.user_id,
            'data': {
                'vitals': {
                    'current': self.get_current_vitals(),
                    'heart_rate_history': self.get_heart_rate_data(7),
                    'blood_oxygen_history': self.get_blood_oxygen_data(7)
                },
                'activity': {
                    'daily_summaries': self.get_activity_summary(7),
                    'workouts': self.get_workout_history(7)
                },
                'sleep': {
                    'history': self.get_sleep_data(7)
                }
            },
            'insights': {
                'avg_resting_heart_rate': self._calculate_avg_resting_hr(),
                'avg_daily_steps': self._calculate_avg_daily_steps(),
                'avg_sleep_hours': self._calculate_avg_sleep(),
                'weekly_exercise_days': random.randint(2, 6)
            }
        }
    
    def _calculate_avg_resting_hr(self) -> int:
        """Calculate average resting heart rate."""
        return random.randint(55, 75)
    
    def _calculate_avg_daily_steps(self) -> int:
        """Calculate average daily steps."""
        return random.randint(5000, 10000)
    
    def _calculate_avg_sleep(self) -> float:
        """Calculate average sleep hours."""
        return round(random.uniform(6.5, 8.0), 1)
    
    @staticmethod
    def generate_sample_user_data() -> Dict[str, Any]:
        """
        Generate sample user health data for demo purposes.
        
        Returns:
            dict: Sample health data that can be used for risk assessment
        """
        return {
            'age': random.randint(25, 65),
            'weight_kg': round(random.uniform(60, 100), 1),
            'height_cm': random.randint(160, 190),
            'systolic': random.randint(110, 140),
            'diastolic': random.randint(70, 90),
            'cholesterol': random.randint(160, 240),
            'is_smoker': random.choice([True, False]),
            'exercise_days': random.randint(0, 6),
            'data_source': 'Apple Watch Mock'
        }
