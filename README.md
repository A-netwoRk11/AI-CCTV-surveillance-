# AI-powered CCTV Surveillance System (Streamlit Edition)

## 🚀 Quick Start

### 1. Check Python Version
```bash
python --version
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Upgrade pip
```bash
python.exe -m pip install --upgrade pip
```

### 5. Install Requirements
```bash
pip install -r requirements.txt
```

### 6. Start the Streamlit Web App
```bash
streamlit run app.py
```

This launches the modern web interface at `http://localhost:8501` with all surveillance features accessible through your browser.

## 🌐 Web Interface Features

- **Video Upload & Analysis**: Upload surveillance videos for AI processing
- **Live Recording**: Record and analyze video directly from your webcam or CCTV
- **Modern UI**: Clean, responsive interface for viewing results
- **Output Management**: View, download, and delete analysis results
- **No Flask/HTML templates required**: 100% Streamlit-based

## 📦 Deployment

You can deploy this app on any platform that supports Streamlit, including:

- **Local machine** (recommended for most users)
- **Google Colab** (see `streamlit_deployment_demo.ipynb` for a demo)
- **Streamlit Community Cloud**

### Local Development
```bash
streamlit run app.py
```

### Google Colab/Drive
See the included `streamlit_deployment_demo.ipynb` for a ready-to-use notebook.

### Streamlit Community Cloud
1. Push your code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repo and deploy

## 🛠️ Troubleshooting

- If you encounter dependency issues, ensure your Python version matches the requirements in `requirements.txt`.
- If you see webcam errors, make sure your device is connected and accessible.
- For GPU acceleration, ensure your environment supports CUDA and the correct PyTorch version.
