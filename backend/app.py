#!/usr/bin/env python3
"""
🛡️ Toxicity & Cyberbullying Detector Backend API
Simple Flask-based REST API for toxicity detection
"""

import sys
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

# Add parent directory to path to import vaderSentiment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vaderSentiment.toxicity_detector import ToxicityDetector

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize detector
detector = ToxicityDetector()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Toxicity Detector API",
        "version": "1.0.0"
    })


@app.route('/api/info', methods=['GET'])
def api_info():
    """Get API information"""
    return jsonify({
        "name": "Toxicity & Cyberbullying Detector",
        "version": "1.0.0",
        "endpoints": [
            {
                "method": "GET",
                "path": "/health",
                "description": "Health check"
            },
            {
                "method": "GET",
                "path": "/api/info",
                "description": "API information"
            },
            {
                "method": "POST",
                "path": "/api/detect",
                "description": "Detect toxicity in a single message",
                "body": {"text": "string"}
            },
            {
                "method": "POST",
                "path": "/api/batch",
                "description": "Detect toxicity in multiple messages",
                "body": {"texts": ["string", "string"]}
            },
            {
                "method": "POST",
                "path": "/api/filter",
                "description": "Filter toxic and clean messages",
                "body": {"texts": ["string"], "threshold": 0.4}
            }
        ]
    })


@app.route('/api/detect', methods=['POST'])
def detect():
    """Analyze a single text message for toxicity"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "error": "Missing 'text' field in request"
            }), 400
        
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                "error": "Text cannot be empty"
            }), 400
        
        result = detector.detect_toxicity(text)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500


@app.route('/api/batch', methods=['POST'])
def batch():
    """Analyze multiple text messages"""
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({
                "error": "Missing 'texts' field in request"
            }), 400
        
        texts = data.get('texts', [])
        
        if not isinstance(texts, list):
            return jsonify({
                "error": "'texts' must be a list"
            }), 400
        
        if not texts:
            return jsonify({
                "error": "texts list cannot be empty"
            }), 400
        
        results = detector.batch_detect(texts)
        
        return jsonify({
            "count": len(results),
            "results": results
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500


@app.route('/api/filter', methods=['POST'])
def filter_toxic():
    """Filter messages into toxic and clean"""
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({
                "error": "Missing 'texts' field in request"
            }), 400
        
        texts = data.get('texts', [])
        threshold = data.get('threshold', 0.4)
        
        if not isinstance(texts, list):
            return jsonify({
                "error": "'texts' must be a list"
            }), 400
        
        if not texts:
            return jsonify({
                "error": "texts list cannot be empty"
            }), 400
        
        filtered = detector.filter_toxic(texts, threshold)
        
        return jsonify({
            "threshold": threshold,
            "toxic_count": len(filtered['toxic']),
            "clean_count": len(filtered['clean']),
            "toxic": filtered['toxic'],
            "clean": filtered['clean']
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "path": request.path,
        "method": request.method
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "error": "Method not allowed",
        "path": request.path,
        "method": request.method
    }), 405


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n🛡️  Toxicity & Cyberbullying Detector")
    print("=" * 50)
    print("🚀 Starting backend server...")
    print("📍 Server running on: http://localhost:8000")
    print("📚 API docs: http://localhost:8000/api/info")
    print("🏥 Health check: http://localhost:8000/health")
    print("=" * 50)
    print()
    
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=False,
        use_reloader=False
    )
