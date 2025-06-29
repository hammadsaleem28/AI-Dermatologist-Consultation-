# 🚀 Quick Setup Guide - AI Dermatologist

## 📋 Prerequisites
- Python 3.8+ installed
- Internet connection for API calls

## ⚡ Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with Google account
3. Click "Get API Key" 
4. Create new project or select existing
5. Generate API key
6. Copy the key

### Step 3: Configure API Key
Open `config.py` and replace:
```python
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY_HERE'
```
With:
```python
GEMINI_API_KEY = 'your_actual_api_key_here'
```

### Step 4: Run Application
```bash
python run.py
```

### Step 5: Open Browser
Go to: `http://localhost:5000`

## 🎯 Features Ready to Use

### 📸 Image Analysis
- Upload skin images (JPG, PNG, JPEG)
- Get AI-powered diagnosis
- Receive treatment recommendations
- Pakistan-specific medicine suggestions

### 💬 AI Chat
- Ask dermatology questions
- Get professional advice
- Skin condition guidance
- Treatment recommendations

### 💊 Medicine Database
- 50+ medicines available in Pakistan
- Brand names and prices
- Company information
- Condition-specific recommendations

## 🛠️ Troubleshooting

### Common Issues:

**"Templates directory not found"**
```bash
mkdir templates
```

**"API key not configured"**
- Check config.py file
- Ensure API key is correct
- Verify internet connection

**"Port already in use"**
- Change port in config.py
- Or stop other applications using port 5000

**"Module not found"**
```bash
pip install -r requirements.txt
```

## 📱 Usage Tips

1. **Best Image Quality**: Use clear, well-lit photos
2. **Specific Questions**: Be detailed in your descriptions
3. **Professional Advice**: Always consult real dermatologists for serious conditions
4. **Privacy**: Images are processed temporarily and not stored

## 🔧 Advanced Configuration

### Environment Variables (Optional)
```bash
export GEMINI_API_KEY=your_key_here
export FLASK_DEBUG=False
export SECRET_KEY=your_secret_key
```

### Production Deployment
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📞 Support

- Check README.md for detailed documentation
- Review error messages in terminal
- Ensure all dependencies are installed
- Verify API key is valid

---

**🏥 Ready to help with skin health in Pakistan! 🇵🇰** 