"""
API Routes Module
Defines REST API endpoints for the health risk assessment application.
"""

import os
from flask import Blueprint, request, jsonify
from backend.models.risk_calculator import RiskCalculator
from backend.models.database_manager import DatabaseManager

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize calculator
calculator = RiskCalculator()

def get_db_manager():
    """Get database manager instance with configurable path"""
    db_path = os.environ.get('DATABASE_PATH', 'medai_lite.db')
    return DatabaseManager(db_path)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON response with API status
    """
    return jsonify({
        'status': 'healthy',
        'message': 'MEDAI-Lite API is running',
        'version': '1.0.0'
    }), 200


@api_bp.route('/risk', methods=['POST'])
def calculate_risk():
    """
    Calculate health risk based on provided data
    
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
        JSON response with risk assessment results
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
            
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid data type: {str(e)}'}), 400
        
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
        
        # Calculate risk
        risk_result = calculator.calculate_risk(health_data)
        
        # Save to database
        user_id = data.get('user_id')
        db_manager = get_db_manager()
        assessment_id = db_manager.save_assessment(user_id, health_data, risk_result)
        
        # Add assessment ID to response
        risk_result['assessment_id'] = assessment_id
        
        return jsonify(risk_result), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@api_bp.route('/history', methods=['GET'])
def get_history():
    """
    Get assessment history
    
    Query parameters:
        - user_id (optional): Filter by user ID
        - limit (optional): Maximum number of records (default: 10)
    
    Returns:
        JSON response with assessment history
    """
    try:
        user_id = request.args.get('user_id', type=int)
        limit = request.args.get('limit', default=10, type=int)
        
        # Validate limit
        if limit < 1 or limit > 100:
            return jsonify({'error': 'Limit must be between 1 and 100'}), 400
        
        db_manager = get_db_manager()
        assessments = db_manager.get_assessment_history(user_id, limit)
        
        return jsonify({
            'count': len(assessments),
            'assessments': assessments
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@api_bp.route('/history/<int:assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    """
    Get a specific assessment by ID
    
    Args:
        assessment_id (int): Assessment ID
    
    Returns:
        JSON response with assessment details
    """
    try:
        db_manager = get_db_manager()
        assessment = db_manager.get_assessment_by_id(assessment_id)
        
        if assessment is None:
            return jsonify({'error': 'Assessment not found'}), 404
        
        return jsonify(assessment), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@api_bp.route('/history/<int:assessment_id>', methods=['DELETE'])
def delete_assessment(assessment_id):
    """
    Delete an assessment by ID
    
    Args:
        assessment_id (int): Assessment ID
    
    Returns:
        JSON response with deletion status
    """
    try:
        db_manager = get_db_manager()
        deleted = db_manager.delete_assessment(assessment_id)
        
        if not deleted:
            return jsonify({'error': 'Assessment not found'}), 404
        
        return jsonify({'message': 'Assessment deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Get statistics about assessments
    
    Query parameters:
        - user_id (optional): Filter by user ID
    
    Returns:
        JSON response with statistics
    """
    try:
        user_id = request.args.get('user_id', type=int)
        
        db_manager = get_db_manager()
        stats = db_manager.get_statistics(user_id)
        
        if stats is None:
            return jsonify({
                'total_assessments': 0,
                'avg_risk_score': 0,
                'avg_bmi': 0,
                'low_risk_count': 0,
                'moderate_risk_count': 0,
                'high_risk_count': 0
            }), 200
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
