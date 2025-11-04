"""
Base Agent Class
Abstract base class for disease-specific health assessment agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import time


class BaseAgent(ABC):
    """
    Abstract base class for health assessment agents.
    Defines the interface and common functionality for all disease-specific agents.
    """
    
    def __init__(self, name: str, weight: float = 1.0):
        """
        Initialize base agent.
        
        Args:
            name (str): Agent name
            weight (float): Weight factor for aggregation (0.0-1.0)
        """
        self.name = name
        self.weight = weight
        self.performance_log = []
    
    @abstractmethod
    def assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess health risk based on input data.
        Must be implemented by subclasses.
        
        Args:
            data (dict): Health metrics and parameters
            
        Returns:
            dict: Risk assessment results including score, level, and breakdown
        """
        pass
    
    @abstractmethod
    def get_recommendations(self, risk_score: float) -> list:
        """
        Generate health recommendations based on risk score.
        
        Args:
            risk_score (float): Calculated risk score
            
        Returns:
            list: List of recommendation strings
        """
        pass
    
    def assess_with_timing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess risk with performance monitoring.
        
        Args:
            data (dict): Health metrics
            
        Returns:
            dict: Assessment results with timing metadata
        """
        start_time = time.time()
        result = self.assess_risk(data)
        elapsed_time = time.time() - start_time
        
        # Add metadata
        result['agent_name'] = self.name
        result['processing_time_ms'] = round(elapsed_time * 1000, 2)
        result['recommendations'] = self.get_recommendations(result.get('risk_score', 0))
        
        # Log performance
        self.performance_log.append({
            'timestamp': time.time(),
            'processing_time_ms': result['processing_time_ms']
        })
        
        return result
    
    def get_performance_stats(self) -> Dict[str, float]:
        """
        Get performance statistics for this agent.
        
        Returns:
            dict: Performance metrics
        """
        if not self.performance_log:
            return {'avg_time_ms': 0, 'max_time_ms': 0, 'min_time_ms': 0}
        
        times = [log['processing_time_ms'] for log in self.performance_log]
        return {
            'avg_time_ms': round(sum(times) / len(times), 2),
            'max_time_ms': max(times),
            'min_time_ms': min(times),
            'total_assessments': len(times)
        }
    
    def validate_data(self, data: Dict[str, Any], required_fields: list) -> None:
        """
        Validate that required fields are present in data.
        
        Args:
            data (dict): Data to validate
            required_fields (list): List of required field names
            
        Raises:
            ValueError: If required fields are missing
        """
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValueError(f"{self.name}: Missing required fields: {', '.join(missing)}")
