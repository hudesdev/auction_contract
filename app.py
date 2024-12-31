"""Main application module"""
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.experts import SportsExpert, FoodExpert, AIExpert, SudoStarExpert
from src.experts.selector import ExpertSelector
from src.utils.openai_client import init_openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize expert system
expert_system = {}

def init_app():
    """Initialize application
    
    Returns:
        bool: True if initialization successful, False otherwise
    """
    try:
        # Initialize OpenAI client
        global openai_api_key
        openai_api_key = init_openai()
        if not openai_api_key:
            logger.error("OpenAI API key not found")
            return False
            
        # Initialize experts
        global expert_system
        expert_system = {
            'sports': SportsExpert(),
            'food': FoodExpert(),
            'ai': AIExpert(),
            'sudostar': SudoStarExpert()
        }
        
        # Initialize expert selector
        expert_system['selector'] = ExpertSelector()
        
        logger.info("Expert system initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing application: {str(e)}")
        return False

@app.route('/health')
def health():
    is_initialized = init_app()
    
    response = {
        'status': 'healthy' if is_initialized else 'unhealthy',
        'services': {
            'api': 'running',
            'openai_api': 'configured' if openai_api_key else 'missing',
            'expert_system': 'running' if expert_system else 'error'
        }
    }
    
    if not is_initialized:
        response['error'] = 'System not properly initialized'
    
    return jsonify(response), 200 if is_initialized else 503

@app.route('/', methods=['POST'])
@app.route('/ask', methods=['POST'])
async def ask():
    if not init_app():
        return jsonify({
            'status': 'error',
            'error': 'System not properly initialized',
            'code': 'INIT_ERROR'
        }), 503

    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'status': 'error',
                'error': 'Question is required',
                'code': 'MISSING_QUESTION'
            }), 400

        question = data['question']
        logger.info(f"Received question: {question}")
        
        # Select expert and get response
        expert_type, direct_response = await expert_system['selector'].select_expert(question)
        logger.info(f"Selected expert: {expert_type}")
        
        response = None
        if expert_type and expert_type in expert_system:
            response = await expert_system[expert_type].get_response(question)
        else:
            response = direct_response

        if not response:
            return jsonify({
                'status': 'error',
                'error': 'Could not generate response',
                'code': 'NO_RESPONSE'
            }), 500

        logger.info(f"Generated response for {expert_type} expert")
        return jsonify({
            'status': 'success',
            'data': {
                'answer': response,
                'expert_type': expert_type or 'general'
            }
        })

    except Exception as e:
        logger.error(f"Error in /ask endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 'INTERNAL_ERROR'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Railway uses port 8080
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port) 