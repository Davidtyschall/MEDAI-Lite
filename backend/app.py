"""
MEDAI-Lite Flask Application
Main application file for the health risk assessment backend.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from backend.routes.api_routes import api_bp
from backend.routes.aggregate_routes import aggregate_bp
from backend.routes.watch_routes import watch_bp
from backend.routes.admin_routes import admin_bp


def create_app(config=None):
    """
    Application factory function
    
    Args:
        config (dict): Configuration dictionary
        
    Returns:
        Flask: Flask application instance
    """
    app = Flask(__name__, 
                static_folder='../frontend/build',
                static_url_path='')
    
    # Enable CORS for development
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configuration
    if config:
        app.config.update(config)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(aggregate_bp)
    app.register_blueprint(watch_bp)
    app.register_blueprint(admin_bp)
    
    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        """Serve React frontend"""
        # Prevent path traversal attacks
        if path and not path.startswith('..') and not os.path.isabs(path):
            file_path = os.path.join(app.static_folder, path)
            # Ensure the resolved path is within static_folder
            if os.path.exists(file_path) and os.path.commonpath([app.static_folder, file_path]) == app.static_folder:
                return send_from_directory(app.static_folder, path)
        # Fallback to index.html for React Router (safe: hardcoded filename)
        return send_from_directory(app.static_folder, 'index.html')
    
    return app


if __name__ == '__main__':
    import os
    app = create_app()
    # Use environment variables for production deployment
    debug_mode = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(debug=debug_mode, host=host, port=port)

# Create app instance for production deployment (gunicorn, render, etc.)
app = create_app()
