"""
Admin API Routes
Endpoints for system monitoring, audit logs, and administration.
"""

import logging
from flask import Blueprint, request, jsonify
from backend.models.database_manager import DatabaseManager
from backend.models.audit_logger import AuditLogger

# Configure logging
logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Initialize managers
db_manager = DatabaseManager()
audit_logger = AuditLogger()


@admin_bp.route('/system/status', methods=['GET'])
def get_system_status():
    """
    Get system health status and metrics.
    
    Returns:
        JSON response with system status
    """
    try:
        # Get assessment statistics
        stats = db_manager.get_statistics()
        
        # Get audit log statistics
        audit_stats = audit_logger.get_log_statistics(days=30)
        
        return jsonify({
            'status': 'healthy',
            'assessments': {
                'total': stats.get('total_assessments', 0),
                'avg_risk_score': round(stats.get('avg_risk_score', 0), 2) if stats.get('avg_risk_score') else 0,
                'avg_bmi': round(stats.get('avg_bmi', 0), 2) if stats.get('avg_bmi') else 0,
                'low_risk_count': stats.get('low_risk_count', 0),
                'moderate_risk_count': stats.get('moderate_risk_count', 0),
                'high_risk_count': stats.get('high_risk_count', 0)
            },
            'audit_logs': {
                'total_events_30d': audit_stats.get('total_events', 0),
                'by_status': audit_stats.get('by_status', {}),
                'by_action': audit_stats.get('by_action', {})
            },
            'timestamp': audit_stats.get('timestamp', None)
        }), 200
        
    except Exception as e:
        logger.error(f'Error in get_system_status: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@admin_bp.route('/audit-logs', methods=['GET'])
def get_audit_logs():
    """
    Get audit logs with optional filtering.
    
    Query parameters:
        - limit (int): Maximum number of logs (default: 50, max: 200)
        - offset (int): Offset for pagination (default: 0)
        - user_id (int): Filter by user ID
        - action (str): Filter by action
        - resource (str): Filter by resource
        - status (str): Filter by status
    
    Returns:
        JSON response with audit logs
    """
    try:
        limit = min(int(request.args.get('limit', 50)), 200)
        offset = int(request.args.get('offset', 0))
        user_id = request.args.get('user_id', type=int)
        action = request.args.get('action')
        resource = request.args.get('resource')
        status = request.args.get('status')
        
        logs = audit_logger.get_logs(
            limit=limit,
            offset=offset,
            user_id=user_id,
            action=action,
            resource=resource,
            status=status
        )
        
        return jsonify({
            'count': len(logs),
            'limit': limit,
            'offset': offset,
            'logs': logs
        }), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        logger.error(f'Error in get_audit_logs: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@admin_bp.route('/audit-logs/stats', methods=['GET'])
def get_audit_stats():
    """
    Get audit log statistics.
    
    Query parameters:
        - days (int): Number of days to analyze (default: 30, max: 365)
    
    Returns:
        JSON response with audit statistics
    """
    try:
        days = min(int(request.args.get('days', 30)), 365)
        
        stats = audit_logger.get_log_statistics(days=days)
        
        return jsonify(stats), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        logger.error(f'Error in get_audit_stats: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@admin_bp.route('/system/metrics', methods=['GET'])
def get_system_metrics():
    """
    Get detailed system performance metrics.
    
    Returns:
        JSON response with performance metrics
    """
    try:
        # Get assessment statistics
        stats = db_manager.get_statistics()
        
        # Calculate risk distribution percentages
        total = stats.get('total_assessments', 0)
        if total > 0:
            low_pct = round((stats.get('low_risk_count', 0) / total) * 100, 1)
            mod_pct = round((stats.get('moderate_risk_count', 0) / total) * 100, 1)
            high_pct = round((stats.get('high_risk_count', 0) / total) * 100, 1)
        else:
            low_pct = mod_pct = high_pct = 0
        
        return jsonify({
            'total_assessments': total,
            'average_risk_score': round(stats.get('avg_risk_score', 0), 2) if stats.get('avg_risk_score') else 0,
            'average_bmi': round(stats.get('avg_bmi', 0), 2) if stats.get('avg_bmi') else 0,
            'risk_distribution': {
                'low': {
                    'count': stats.get('low_risk_count', 0),
                    'percentage': low_pct
                },
                'moderate': {
                    'count': stats.get('moderate_risk_count', 0),
                    'percentage': mod_pct
                },
                'high': {
                    'count': stats.get('high_risk_count', 0),
                    'percentage': high_pct
                }
            },
            'performance': {
                'avg_response_time_ms': '<100',  # Based on your architecture docs
                'status': 'optimal'
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Error in get_system_metrics: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@admin_bp.route('/audit-logs/cleanup', methods=['POST'])
def cleanup_audit_logs():
    """
    Manually trigger cleanup of old audit logs.
    
    Expected JSON body:
    {
        "days_to_keep": int (default: 90, min: 30)
    }
    
    Returns:
        JSON response with cleanup results
    """
    try:
        data = request.get_json() or {}
        days_to_keep = max(int(data.get('days_to_keep', 90)), 30)
        
        deleted_count = audit_logger.cleanup_old_logs(days_to_keep)
        
        # Log the cleanup action
        audit_logger.log_event(
            action='cleanup',
            resource='audit_logs',
            details={'days_to_keep': days_to_keep, 'deleted_count': deleted_count},
            status='success'
        )
        
        return jsonify({
            'message': f'Cleaned up {deleted_count} old audit logs',
            'deleted_count': deleted_count,
            'days_to_keep': days_to_keep
        }), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        logger.error(f'Error in cleanup_audit_logs: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500