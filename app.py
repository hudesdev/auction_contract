from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from src.experts import SportsExpert, FoodExpert, AIExpert, SudoStarExpert
from src.core.expert_selector import ExpertSelector
from src.utils.config import ConfigLoader

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize expert system
try:
    logger.info("Initializing expert system...")
    config = ConfigLoader.load_config()
    sports_expert = SportsExpert(config)
    food_expert = FoodExpert(config)
    ai_expert = AIExpert(config)
    sudostar_expert = SudoStarExpert(config)
    expert_selector = ExpertSelector()
    logger.info("Expert system initialized successfully")
except Exception as e:
    logger.error(f"Error initializing expert system: {str(e)}")
    sports_expert = None
    food_expert = None
    ai_expert = None
    sudostar_expert = None
    expert_selector = None

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'version': '1.0.0',
        'endpoints': {
            'ask': '/ask (POST) - Get expert response',
            'health': '/health (GET) - Check system health'
        }
    })

@app.route('/health')
def health():
    expert_status = 'running' if expert_selector is not None else 'error'
    
    response = {
        'status': 'healthy' if expert_selector is not None else 'unhealthy',
        'services': {
            'api': 'running',
            'telegram_bot': 'disabled',
            'expert_system': expert_status
        }
    }
    
    logger.info(f"Health check: {response}")
    return jsonify(response)

@app.route('/ask', methods=['POST'])
async def ask():
    try:
        if expert_selector is None:
            error_msg = 'Expert system is not initialized'
            logger.error(error_msg)
            return jsonify({
                'status': 'error',
                'error': error_msg,
                'code': 'EXPERT_SYSTEM_ERROR'
            }), 500

        data = request.get_json()
        if not data:
            error_msg = 'No JSON data received'
            logger.error(error_msg)
            return jsonify({
                'status': 'error',
                'error': error_msg,
                'code': 'NO_DATA'
            }), 400

        question = data.get('question')
        if not question:
            error_msg = 'Question is required'
            logger.error(error_msg)
            return jsonify({
                'status': 'error',
                'error': error_msg,
                'code': 'MISSING_QUESTION'
            }), 400

        logger.info(f"Received question: {question}")
        
        # Select expert and get response
        expert_type, direct_response = await expert_selector.select_expert(question)
        logger.info(f"Selected expert: {expert_type}")
        
        if expert_type:
            if expert_type == "sports" and sports_expert:
                response = await sports_expert.get_response(question)
            elif expert_type == "food" and food_expert:
                response = await food_expert.get_response(question)
            elif expert_type == "ai" and ai_expert:
                response = await ai_expert.get_response(question)
            elif expert_type == "sudostar" and sudostar_expert:
                response = await sudostar_expert.get_response(question)
            else:
                response = None
        else:
            response = direct_response

        if not response:
            error_msg = 'Could not generate response'
            logger.error(error_msg)
            return jsonify({
                'status': 'error',
                'error': error_msg,
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
        error_msg = f"Error in /ask endpoint: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'status': 'error',
            'error': error_msg,
            'code': 'INTERNAL_ERROR'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port) 