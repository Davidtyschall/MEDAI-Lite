"""
Apple Watch Integration API Routes
Endpoints for Apple Watch/HealthKit data integration (mock).
"""

import logging
from flask import Blueprint, request, jsonify
from backend.integrations import AppleWatchMock

# Configure logging
logger = logging.getLogger(__name__)

watch_bp = Blueprint('watch', __name__, url_prefix='/api/watch')

# Store active watch connections (in production, use proper session management)
active_watches = {}


@watch_bp.route('/connect', methods=['POST'])
def connect_watch():
    """
    Connect Apple Watch for a user.
    
    Expected JSON body:
    {
        "user_id": int (optional)
    }
    
    Returns:
        JSON response with connection status
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        
        # Create mock Apple Watch instance
        watch = AppleWatchMock(user_id=user_id)
        connection_result = watch.connect()
        
        # Store in active connections
        session_key = f"user_{user_id}" if user_id else "guest"
        active_watches[session_key] = watch
        
        return jsonify({
            **connection_result,
            'session_key': session_key,
            'message': 'Apple Watch connected successfully'
        }), 200
        
    except Exception as e:
        logger.error(f'Error in connect_watch: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@watch_bp.route('/disconnect', methods=['POST'])
def disconnect_watch():
    """
    Disconnect Apple Watch.
    
    Expected JSON body:
    {
        "session_key": str
    }
    
    Returns:
        JSON response with disconnection status
    """
    try:
        data = request.get_json() or {}
        session_key = data.get('session_key', 'guest')
        
        if session_key in active_watches:
            watch = active_watches[session_key]
            result = watch.disconnect()
            del active_watches[session_key]
            
            return jsonify({
                **result,
                'message': 'Apple Watch disconnected'
            }), 200
        else:
            return jsonify({'error': 'No active watch connection found'}), 404
        
    except Exception as e:
        logger.error(f'Error in disconnect_watch: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@watch_bp.route('/vitals', methods=['GET'])
def get_current_vitals():
    """
    Get current vital signs from Apple Watch.
    
    Query parameters:
        - session_key (optional): Watch session key
    
    Returns:
        JSON response with current vitals
    """
    try:
        session_key = request.args.get('session_key', 'guest')
        
        if session_key not in active_watches:
            return jsonify({'error': 'No active watch connection'}), 404
        
        watch = active_watches[session_key]
        vitals = watch.get_current_vitals()
        
        return jsonify(vitals), 200
        
    except Exception as e:
        logger.error(f'Error in get_current_vitals: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@watch_bp.route('/heart-rate', methods=['GET'])
def get_heart_rate_data():
    """
    Get heart rate history from Apple Watch.
    
    Query parameters:
        - session_key (optional): Watch session key
        - days (optional): Number of days of history (default: 7)
    
    Returns:
        JSON response with heart rate data
    """
    try:
        session_key = request.args.get('session_key', 'guest')
        days = request.args.get('days', default=7, type=int)
        
        if session_key not in active_watches:
            return jsonify({'error': 'No active watch connection'}), 404
        
        if not (1 <= days <= 30):
            return jsonify({'error': 'Days must be between 1 and 30'}), 400
        
        watch = active_watches[session_key]
        data = watch.get_heart_rate_data(days)
        
        return jsonify({
            'count': len(data),
            'days': days,
            'data': data
        }), 200
        
    except Exception as e:
        logger.error(f'Error in get_heart_rate_data: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@watch_bp.route('/activity', methods=['GET'])
def get_activity_data():
    """
    Get activity summary from Apple Watch.
    
    Query parameters:
        - session_key (optional): Watch session key
        - days (optional): Number of days of history (default: 7)
    
    Returns:
        JSON response with activity data
    """
    try:
        session_key = request.args.get('session_key', 'guest')
        days = request.args.get('days', default=7, type=int)
        
        if session_key not in active_watches:
            return jsonify({'error': 'No active watch connection'}), 404
        
        if not (1 <= days <= 30):
            return jsonify({'error': 'Days must be between 1 and 30'}), 400
        
        watch = active_watches[session_key]
        data = watch.get_activity_summary(days)
        
        return jsonify({
            'count': len(data),
            'days': days,
            'summaries': data
        }), 200
        
    except Exception as e:
        logger.error(f'Error in get_activity_data: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@watch_bp.route('/sleep', methods=['GET'])
def get_sleep_data():
    """
    Get sleep tracking data from Apple Watch.
    
    Query parameters:
        - session_key (optional): Watch session key
        - days (optional): Number of days of history (default: 7)
    
    Returns:
        JSON response with sleep data
    """
    try:
        session_key = request.args.get('session_key', 'guest')
        days = request.args.get('days', default=7, type=int)
        
        if session_key not in active_watches:
            return jsonify({'error': 'No active watch connection'}), 404
        
        if not (1 <= days <= 30):
            return jsonify({'error': 'Days must be between 1 and 30'}), 400
        
        watch = active_watches[session_key]
        data = watch.get_sleep_data(days)
        
        return jsonify({
            'count': len(data),
            'days': days,
            'sleep_data': data
        }), 200
        
    except Exception as e:
        logger.error(f'Error in get_sleep_data: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@watch_bp.route('/workouts', methods=['GET'])
def get_workout_history():
    """
    Get workout history from Apple Watch.
    
    Query parameters:
        - session_key (optional): Watch session key
        - days (optional): Number of days of history (default: 7)
    
    Returns:
        JSON response with workout data
    """
    try:
        session_key = request.args.get('session_key', 'guest')
        days = request.args.get('days', default=7, type=int)
        
        if session_key not in active_watches:
            return jsonify({'error': 'No active watch connection'}), 404
        
        if not (1 <= days <= 30):
            return jsonify({'error': 'Days must be between 1 and 30'}), 400
        
        watch = active_watches[session_key]
        data = watch.get_workout_history(days)
        
        return jsonify({
            'count': len(data),
            'days': days,
            'workouts': data
        }), 200
        
    except Exception as e:
        logger.error(f'Error in get_workout_history: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@watch_bp.route('/export', methods=['GET'])
def export_health_data():
    """
    Export comprehensive health data from Apple Watch.
    Simulates full HealthKit data export.
    
    Query parameters:
        - session_key (optional): Watch session key
    
    Returns:
        JSON response with complete health data export
    """
    try:
        session_key = request.args.get('session_key', 'guest')
        
        if session_key not in active_watches:
            return jsonify({'error': 'No active watch connection'}), 404
        
        watch = active_watches[session_key]
        export_data = watch.export_health_data()
        
        return jsonify(export_data), 200
        
    except Exception as e:
        logger.error(f'Error in export_health_data: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@watch_bp.route('/sample-data', methods=['GET'])
def get_sample_data():
    """
    Generate sample health data for testing.
    Useful for populating the risk assessment form.
    
    Returns:
        JSON response with sample health data
    """
    try:
        sample_data = AppleWatchMock.generate_sample_user_data()
        
        return jsonify({
            'message': 'Sample data generated from Apple Watch mock',
            'data': sample_data
        }), 200
        
    except Exception as e:
        logger.error(f'Error in get_sample_data: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
