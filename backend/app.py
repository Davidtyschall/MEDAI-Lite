"""
MEDAI-Lite Flask Application
Main application file for the health risk assessment backend.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from backend.routes.api_routes import api_bp


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
    
    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        """Serve React frontend"""
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
