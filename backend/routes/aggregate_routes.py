"""
Aggregated Risk Assessment API Routes
Endpoints for comprehensive multi-agent health risk assessment.
"""

import os
import logging
from flask import Blueprint, request, jsonify
from backend.models.agents import AggregatorAgent
from backend.models.database_manager import DatabaseManager

# Configure logging
logger = logging.getLogger(__name__)

aggregate_bp = Blueprint('aggregate', __name__, url_prefix='/api/aggregate')

# Initialize aggregator agent
aggregator = AggregatorAgent()


@aggregate_bp.route('', methods=['POST'])
def assess_comprehensive_risk():
    """
    Comprehensive health risk assessment using all specialized agents.
    
    Expected JSON body:
    {
        "age": int,
        "weight_kg": float,
        "height_cm": float,
        "systolic": int,
        "diastolic": int,
        "cholesterol": int,
        "is_smoker": bool,
        "exercise_days": int,
        "user_id": int (optional)
    }
    
    Returns:
        JSON response with comprehensive multi-agent assessment
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'age', 'weight_kg', 'height_cm', 'systolic', 
            'diastolic', 'cholesterol', 'is_smoker', 'exercise_days'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate data types and ranges
        try:
            age = int(data['age'])
            weight_kg = float(data['weight_kg'])
            height_cm = float(data['height_cm'])
            systolic = int(data['systolic'])
            diastolic = int(data['diastolic'])
            cholesterol = int(data['cholesterol'])
            is_smoker = bool(data['is_smoker'])
            exercise_days = int(data['exercise_days'])
            
            # Basic validation
            if not (0 < age < 150):
                return jsonify({'error': 'Invalid age value'}), 400
            if not (20 < weight_kg < 500):
                return jsonify({'error': 'Invalid weight value'}), 400
            if not (50 < height_cm < 300):
                return jsonify({'error': 'Invalid height value'}), 400
            if not (50 < systolic < 250):
                return jsonify({'error': 'Invalid systolic blood pressure'}), 400
            if not (30 < diastolic < 150):
                return jsonify({'error': 'Invalid diastolic blood pressure'}), 400
            if not (100 < cholesterol < 400):
                return jsonify({'error': 'Invalid cholesterol value'}), 400
            if not (0 <= exercise_days <= 7):
                return jsonify({'error': 'Invalid exercise days value'}), 400
            
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid data type provided'}), 400
        
        # Prepare health data
        health_data = {
            'age': age,
            'weight_kg': weight_kg,
            'height_cm': height_cm,
            'systolic': systolic,
            'diastolic': diastolic,
            'cholesterol': cholesterol,
            'is_smoker': is_smoker,
            'exercise_days': exercise_days
        }
        
        # Perform comprehensive assessment
        assessment_result = aggregator.assess_comprehensive_risk(health_data)
        
        # Save to database
        db_manager = DatabaseManager()
        user_id = data.get('user_id', 'guest')
        
        db_manager.save_assessment(
            user_id=user_id,
            age=age,
            weight_kg=weight_kg,
            height_cm=height_cm,
            systolic=systolic,
            diastolic=diastolic,
            cholesterol=cholesterol,
            is_smoker=is_smoker,
            exercise_days=exercise_days,
            risk_score=assessment_result['overall_health_index'],
            bmi=assessment_result['agent_assessments']['metabolic'].get('bmi', 0),
            risk_level=assessment_result['overall_risk_level']
        )
        
        # Add user_id if provided
        if 'user_id' in data:
            assessment_result['user_id'] = data['user_id']
        
        return jsonify(assessment_result), 200
        
    except Exception as e:
        logger.error(f'Error in assess_comprehensive_risk: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@aggregate_bp.route('/performance', methods=['GET'])
def get_performance_stats():
    """
    Get performance statistics for the aggregator and all agents.
    
    Returns:
        JSON response with performance metrics
    """
    try:
        overall_stats = aggregator.get_overall_performance_stats()
        agent_stats = aggregator.get_agent_performance_stats()
        
        return jsonify({
            'overall': overall_stats,
            'agents': agent_stats
        }), 200
        
    except Exception as e:
        logger.error(f'Error in get_performance_stats: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@aggregate_bp.route('/agents', methods=['GET'])
def get_available_agents():
    """
    Get list of available specialized agents.
    
    Returns:
        JSON response with agent information
    """
    try:
        agents_info = []
        
        for name, agent in aggregator.agents.items():
            agents_info.append({
                'name': name,
                'display_name': agent.name,
                'weight': agent.weight,
                'category': name.capitalize()
            })
        
        return jsonify({
            'agents': agents_info,
            'total_agents': len(agents_info)
        }), 200
        
    except Exception as e:
        logger.error(f'Error in get_available_agents: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
