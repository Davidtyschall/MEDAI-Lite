"""
Audit Logger
Tracks system events and user actions for compliance and security.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List


class AuditLogger:
    """
    Audit logging system for tracking system events and user actions.
    """
    
    def __init__(self, db_path='medai_lite.db'):
        """
        Initialize AuditLogger.
        
        Args:
            db_path (str): Path to SQLite database
        """
        self.db_path = db_path
        self.init_audit_table()
    
    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_audit_table(self):
        """Initialize audit log table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id INTEGER,
                action TEXT NOT NULL,
                resource TEXT NOT NULL,
                details TEXT,
                ip_address TEXT,
                user_agent TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_audit_timestamp 
            ON audit_logs(timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_audit_user 
            ON audit_logs(user_id)
        ''')
        
        conn.commit()
        conn.close()
    
    def log_event(self, action: str, resource: str, user_id: int = None, 
                  details: Dict[str, Any] = None, ip_address: str = None,
                  user_agent: str = None, status: str = 'success') -> int:
        """
        Log an audit event.
        
        Args:
            action (str): Action performed (e.g., 'create', 'read', 'update', 'delete')
            resource (str): Resource affected (e.g., 'assessment', 'user', 'config')
            user_id (int): User ID (optional)
            details (dict): Additional details (optional)
            ip_address (str): IP address (optional)
            user_agent (str): User agent string (optional)
            status (str): Event status ('success', 'failure', 'error')
            
        Returns:
            int: Audit log entry ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        details_json = json.dumps(details) if details else None
        
        cursor.execute('''
            INSERT INTO audit_logs 
            (timestamp, user_id, action, resource, details, ip_address, user_agent, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, user_id, action, resource, details_json, ip_address, user_agent, status))
        
        log_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return log_id
    
    def get_logs(self, limit: int = 100, offset: int = 0, 
                 user_id: int = None, action: str = None,
                 resource: str = None, status: str = None) -> List[Dict]:
        """
        Retrieve audit logs with optional filtering.
        
        Args:
            limit (int): Maximum number of logs to return
            offset (int): Offset for pagination
            user_id (int): Filter by user ID
            action (str): Filter by action
            resource (str): Filter by resource
            status (str): Filter by status
            
        Returns:
            list: Audit log entries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM audit_logs WHERE 1=1'
        params = []
        
        if user_id is not None:
            query += ' AND user_id = ?'
            params.append(user_id)
        
        if action:
            query += ' AND action = ?'
            params.append(action)
        
        if resource:
            query += ' AND resource = ?'
            params.append(resource)
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            log = dict(row)
            if log['details']:
                log['details'] = json.loads(log['details'])
            logs.append(log)
        
        return logs
    
    def get_log_statistics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get audit log statistics for past N days.
        
        Args:
            days (int): Number of days to analyze
            
        Returns:
            dict: Statistics
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = (cutoff_date - timedelta(days=days)).isoformat()
        
        # Total events
        cursor.execute('''
            SELECT COUNT(*) as total FROM audit_logs 
            WHERE timestamp >= ?
        ''', (cutoff_date,))
        total = cursor.fetchone()['total']
        
        # Events by action
        cursor.execute('''
            SELECT action, COUNT(*) as count 
            FROM audit_logs 
            WHERE timestamp >= ?
            GROUP BY action
        ''', (cutoff_date,))
        by_action = {row['action']: row['count'] for row in cursor.fetchall()}
        
        # Events by status
        cursor.execute('''
            SELECT status, COUNT(*) as count 
            FROM audit_logs 
            WHERE timestamp >= ?
            GROUP BY status
        ''', (cutoff_date,))
        by_status = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Most active users
        cursor.execute('''
            SELECT user_id, COUNT(*) as count 
            FROM audit_logs 
            WHERE timestamp >= ? AND user_id IS NOT NULL
            GROUP BY user_id
            ORDER BY count DESC
            LIMIT 10
        ''', (cutoff_date,))
        active_users = [
            {'user_id': row['user_id'], 'event_count': row['count']}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            'period_days': days,
            'total_events': total,
            'by_action': by_action,
            'by_status': by_status,
            'most_active_users': active_users
        }
    
    def cleanup_old_logs(self, days_to_keep: int = 90) -> int:
        """
        Clean up old audit logs.
        
        Args:
            days_to_keep (int): Number of days to retain
            
        Returns:
            int: Number of logs deleted
        """
        from datetime import timedelta
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cutoff_iso = cutoff_date.isoformat()
        
        cursor.execute('''
            DELETE FROM audit_logs WHERE timestamp < ?
        ''', (cutoff_iso,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
