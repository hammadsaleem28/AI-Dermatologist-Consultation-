from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import requests
import base64
import io
import os
from PIL import Image
import json
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# Import configuration
from config import Config

# Configuration
app.config.from_object(Config)
GEMINI_API_KEY = Config.GEMINI_API_KEY
UPLOAD_FOLDER = Config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Pakistan medicines database for common skin conditions
PAKISTAN_MEDICINES = {
    "acne": [
        {"name": "Tretinoin Cream 0.025%", "brand": "Acretin", "company": "Getz Pharma", "price": "Rs. 250-300"},
        {"name": "Clindamycin Gel", "brand": "Dalacin T", "company": "Pfizer", "price": "Rs. 180-220"},
        {"name": "Benzoyl Peroxide", "brand": "Benzac AC", "company": "Galderma", "price": "Rs. 400-500"}
    ],
    "eczema": [
        {"name": "Hydrocortisone Cream", "brand": "Dermacort", "company": "Searle", "price": "Rs. 120-150"},
        {"name": "Betamethasone Cream", "brand": "Betnovate", "company": "GSK", "price": "Rs. 200-250"},
        {"name": "Moisturizing Cream", "brand": "Cetaphil", "company": "Galderma", "price": "Rs. 800-1000"}
    ],
    "psoriasis": [
        {"name": "Clobetasol Cream", "brand": "Dermovate", "company": "GSK", "price": "Rs. 300-400"},
        {"name": "Calcipotriol Cream", "brand": "Daivonex", "company": "Leo Pharma", "price": "Rs. 1200-1500"},
        {"name": "Coal Tar Shampoo", "brand": "T-Gel", "company": "Johnson & Johnson", "price": "Rs. 600-800"}
    ],
    "fungal_infection": [
        {"name": "Terbinafine Cream", "brand": "Lamisil", "company": "Novartis", "price": "Rs. 300-400"},
        {"name": "Clotrimazole Cream", "brand": "Canesten", "company": "Bayer", "price": "Rs. 150-200"},
        {"name": "Ketoconazole Shampoo", "brand": "Nizoral", "company": "Johnson & Johnson", "price": "Rs. 400-500"}
    ],
    "dermatitis": [
        {"name": "Hydrocortisone Cream", "brand": "Dermacort", "company": "Searle", "price": "Rs. 120-150"},
        {"name": "Calamine Lotion", "brand": "Calamine", "company": "GSK", "price": "Rs. 80-100"},
        {"name": "Antihistamine", "brand": "Cetirizine", "company": "Getz Pharma", "price": "Rs. 50-80"}
    ]
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_dermatology_related(text):
    """Check if the query is related to dermatology/skin conditions"""
    dermatology_keywords = [
        'skin', 'acne', 'eczema', 'psoriasis', 'rash', 'dermatitis', 'fungal', 'infection',
        'dry skin', 'oily skin', 'spots', 'pimples', 'blackheads', 'wrinkles', 'aging',
        'moles', 'freckles', 'pigmentation', 'vitiligo', 'melasma', 'sunburn', 'allergy',
        'itching', 'scratching', 'burning', 'scaling', 'peeling', 'redness', 'inflammation',
        'dermatologist', 'skincare', 'treatment', 'cream', 'ointment', 'lotion',
        # Urdu keywords
        'جلد', 'کیل', 'مہاسے', 'خارش', 'داغ', 'دھبے', 'علاج', 'دوا', 'کریم', 'تیل', 'خشک', 'چکتے',
        'سوجن', 'جلن', 'لالی', 'انفیکشن', 'فنگل', 'ایکزیما', 'سوریاسس', 'الرجی', 'روک', 'ٹھیک',
        # Common words that indicate skin problems
        'ulaj', 'ilaj', 'dawai', 'thik', 'rok', 'kese', 'kaise', 'medicine', 'cure', 'heal'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in dermatology_keywords)

def get_medicine_recommendations(detected_condition):
    """Get medicine recommendations for detected skin condition"""
    condition_lower = detected_condition.lower()
    
    for condition, medicines in PAKISTAN_MEDICINES.items():
        if condition in condition_lower:
            return medicines
    
    # Default recommendations for general skin issues
    return PAKISTAN_MEDICINES.get("dermatitis", [])

def analyze_skin_image(image_data, user_query="Analyze this skin condition"):
    """Send image to Gemini API for skin analysis"""
    
    dermatology_prompt = f"""
    You are an experienced dermatologist examining this clinical photograph. The patient has uploaded an image and asked a specific question.

    IMPORTANT: Address the patient's SPECIFIC question/concern about the image.

    Patient's specific question/concern: {user_query}

    Instructions:
    1. Look at the skin image and focus on what the patient is asking about
    2. Give targeted answer to their specific concern
    3. Provide diagnosis related to their question
    4. Suggest specific treatments available in Pakistan
    5. Keep response focused and under 100 words
    6. Sound like a real dermatologist examining the photo
    7. Reply in the same language as patient's question

    Give a targeted professional response to their specific concern about the image.
    """

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": dermatology_prompt
                        },
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_data
                            }
                        }
                    ]
                }
            ]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Sorry, I couldn't analyze the image. Please try uploading a clearer image of the skin condition."
        else:
            return f"Error analyzing image: {response.status_code}"
            
    except Exception as e:
        return f"Error processing image: {str(e)}"

def chat_with_dermatologist(user_message):
    """Chat function for dermatology-related queries"""
    
    # Always respond as dermatologist - don't reject questions
    # if not is_dermatology_related(user_message):
    #     return "I'm a dermatologist specializing in skin conditions. Please describe any skin problems, rashes, or dermatological concerns you may have."
    
    dermatology_prompt = f"""
    You are an experienced dermatologist. Handle language switching intelligently.

    LANGUAGE DETECTION:
    - "in english" / "english mein" / "translate to english" = Switch to ENGLISH immediately
    - "urdu mein" / "اردو میں" = Switch to URDU immediately  
    - When switching languages, answer their PREVIOUS medical question in the NEW language
    - DO NOT say "I am a dermatologist" again when switching languages

    RESPONSE RULES:
    1. If they ask for language change, take their LAST medical question and answer it in the NEW language
    2. Give direct medical advice in 30-50 words
    3. Recommend Pakistani medicines when relevant
    4. Don't repeat introductions or explanations about language switching
    5. Act like a real doctor having a conversation

    Patient's message: {user_message}

    Respond intelligently - if it's language switching, answer their medical concern in the requested language.
    """

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": dermatology_prompt
                        }
                    ]
                }
            ]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "I apologize, but I'm having trouble processing your question. Please rephrase your dermatology-related query."
        else:
            return "I'm experiencing technical difficulties. Please try again later."
            
    except Exception as e:
        return "I'm currently unable to process your request. Please try again later."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    user_query = request.form.get('query', 'Analyze this skin condition')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Save file
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Convert image to base64
        with open(filepath, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Analyze image
        analysis = analyze_skin_image(image_data, user_query)
        
        # Get medicine recommendations based on analysis
        medicines = get_medicine_recommendations(analysis)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'analysis': analysis,
            'medicines': medicines,
            'timestamp': datetime.now().isoformat()
        })
    
    return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, or JPEG files.'}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = chat_with_dermatologist(user_message)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/medicines/<condition>')
def get_medicines(condition):
    medicines = PAKISTAN_MEDICINES.get(condition.lower(), [])
    return jsonify({'medicines': medicines})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 