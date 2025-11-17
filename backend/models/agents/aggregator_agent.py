"""
Aggregator Agent
Integrates and synthesizes results from multiple disease-specific agents
to provide a comprehensive overall health risk assessment.
"""

from typing import Dict, Any, List
import time
from .cardio_agent import CardioAgent
from .metabolic_agent import MetabolicAgent
from .neuro_agent import NeuroAgent


class AggregatorAgent:
    """
    Aggregates health risk assessments from multiple specialized agents
    to compute an overall health index and provide integrated recommendations.
    """
    
    def __init__(self):
        """Initialize aggregator with all disease-specific agents."""
        self.agents = {
            'cardio': CardioAgent(),
            'metabolic': MetabolicAgent(),
            'neuro': NeuroAgent()
        }
        
        # Performance monitoring
        self.assessment_log = []
    
    def assess_comprehensive_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive health risk assessment using all agents.
        
        Args:
            data (dict): Complete health data including all required fields
                
        Returns:
            dict: Comprehensive assessment with overall health index
        """
        start_time = time.time()
        
        # Run all agents
        agent_results = {}
        for agent_name, agent in self.agents.items():
            try:
                result = agent.assess_with_timing(data)
                agent_results[agent_name] = result
            except Exception as e:
                # Log error but continue with other agents
                agent_results[agent_name] = {
                    'error': str(e),
                    'risk_score': None,
                    'agent_name': agent_name
                }
        
        # Calculate overall health index
        overall_index = self._calculate_overall_index(agent_results)
        
        # Generate integrated recommendations
        integrated_recommendations = self._integrate_recommendations(agent_results)
        
        # Identify critical areas
        critical_areas = self._identify_critical_areas(agent_results)
        
        # Calculate total processing time
        total_time = time.time() - start_time
        
        # Performance check (should be ≤3s per requirements)
        performance_status = 'optimal' if total_time <= 3.0 else 'degraded'
        
        result = {
            'overall_health_index': overall_index['score'],
            'overall_risk_level': overall_index['level'],
            'agent_assessments': agent_results,
            'critical_areas': critical_areas,
            'integrated_recommendations': integrated_recommendations,
            'performance': {
                'total_time_ms': round(total_time * 1000, 2),
                'status': performance_status,
                'agent_times': {
                    name: result.get('processing_time_ms', 0)
                    for name, result in agent_results.items()
                }
            },
            'metadata': {
                'timestamp': time.time(),
                'agents_used': list(self.agents.keys()),
                'assessment_id': self._generate_assessment_id()
            }
        }
        
        # Log assessment
        self.assessment_log.append({
            'timestamp': time.time(),
            'total_time_ms': result['performance']['total_time_ms'],
            'overall_score': overall_index['score']
        })
        
        return result
    
    def _calculate_overall_index(self, agent_results: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Calculate overall health index from agent results.
        Uses weighted average based on agent weights.
        """
        total_weight = 0
        weighted_sum = 0
        
        for agent_name, result in agent_results.items():
            if 'error' not in result and result.get('risk_score') is not None:
                agent = self.agents[agent_name]
                weight = agent.weight
                score = result['risk_score']
                
                weighted_sum += score * weight
                total_weight += weight
        
        if total_weight == 0:
            return {'score': 0, 'level': 'Unknown'}
        
        overall_score = weighted_sum / total_weight
        
        # Determine overall risk level
        if overall_score < 25:
            level = 'Low'
        elif overall_score < 50:
            level = 'Moderate'
        elif overall_score < 75:
            level = 'High'
        else:
            level = 'Critical'
        
        return {
            'score': round(overall_score, 2),
            'level': level,
            'weights_used': {
                name: self.agents[name].weight 
                for name in agent_results.keys() 
                if 'error' not in agent_results[name]
            }
        }
    
    def _integrate_recommendations(self, agent_results: Dict[str, Dict]) -> List[str]:
        """
        Integrate recommendations from all agents.
        Prioritizes critical recommendations and removes duplicates.
        """
        all_recommendations = []
        critical_recommendations = []
        
        for agent_name, result in agent_results.items():
            if 'recommendations' in result:
                for rec in result['recommendations']:
                    if rec.startswith('⚠️'):
                        critical_recommendations.append(rec)
                    else:
                        all_recommendations.append(rec)
        
        # Remove duplicates while preserving order
        integrated = []
        seen = set()
        
        # Critical recommendations first
        for rec in critical_recommendations:
            if rec not in seen:
                integrated.append(rec)
                seen.add(rec)
        
        # Then regular recommendations
        for rec in all_recommendations:
            if rec not in seen:
                integrated.append(rec)
                seen.add(rec)
        
        # Add general integrated recommendations
        if len(critical_recommendations) == 0:
            integrated.insert(0, "Continue maintaining healthy lifestyle habits across all health domains")
        else:
            integrated.insert(0, "Multiple health concerns identified - comprehensive medical evaluation recommended")
        
        return integrated[:15]  # Limit to top 15 recommendations
    
    def _identify_critical_areas(self, agent_results: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Identify critical health areas requiring immediate attention.
        """
        critical = []
        
        for agent_name, result in agent_results.items():
            if 'error' in result:
                continue
            
            risk_level = result.get('risk_level', '')
            risk_score = result.get('risk_score', 0)
            
            if risk_level in ['High', 'Critical'] or risk_score >= 75:
                critical.append({
                    'category': result.get('category', agent_name),
                    'risk_level': risk_level,
                    'risk_score': risk_score,
                    'agent': agent_name,
                    'priority': 'urgent' if risk_score >= 75 else 'high'
                })
        
        # Sort by risk score (highest first)
        critical.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return critical
    
    def _generate_assessment_id(self) -> str:
        """Generate unique assessment ID."""
        import hashlib
        timestamp = str(time.time())
        return hashlib.md5(timestamp.encode()).hexdigest()[:16]
    
    def get_agent_performance_stats(self) -> Dict[str, Dict]:
        """
        Get performance statistics for all agents.
        
        Returns:
            dict: Performance stats for each agent
        """
        return {
            name: agent.get_performance_stats()
            for name, agent in self.agents.items()
        }
    
    def get_overall_performance_stats(self) -> Dict[str, Any]:
        """
        Get overall aggregator performance statistics.
        
        Returns:
            dict: Overall performance metrics
        """
        if not self.assessment_log:
            return {
                'total_assessments': 0,
                'avg_time_ms': 0,
                'performance_target_met': None
            }
        
        times = [log['total_time_ms'] for log in self.assessment_log]
        avg_time = sum(times) / len(times)
        
        # Check if meeting ≤3s performance requirement
        performance_target_met = avg_time <= 3000
        
        return {
            'total_assessments': len(self.assessment_log),
            'avg_time_ms': round(avg_time, 2),
            'max_time_ms': max(times),
            'min_time_ms': min(times),
            'performance_target_met': performance_target_met,
            'target_ms': 3000
        }
