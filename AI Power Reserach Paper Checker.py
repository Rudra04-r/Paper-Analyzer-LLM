# 1. Install dependencies (this might take a minute)
!pip install -q streamlit pymupdf google-generativeai
!npm install -g localtunnel

# 2. Write the Streamlit app code to a file
app_code = """
import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# Configure Streamlit page
st.set_page_config(page_title="AI Research Assistant", page_icon="🧠", layout="wide")

st.title("🧠 AI-Powered Research Paper Assistant")
st.write("Upload a research paper (PDF) to automatically extract its core components, get recommendations, and discover future work ideas.")

# Sidebar for API Key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
st.sidebar.markdown("[Get a free Gemini API key here](https://aistudio.google.com/app/apikey)")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def analyze_paper(text, api_key):
    genai.configure(api_key=api_key)
    
    # UPDATED: Using the currently supported Gemini 2.5 Flash model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f'''
    You are an expert AI academic research assistant. I will provide you with the text of a research paper.
    Please analyze the paper and provide a beautifully formatted markdown response with the following sections:

    1. **📝 Summary**: A concise 2-3 paragraph summary of the paper.
    2. **🎯 Problem Statement**: What specific problem or gap in the literature is this paper trying to solve?
    3. **🔬 Methodology**: How did the authors approach solving the problem? (Summarize the architecture, datasets, or formulas used).
    4. **📊 Results**: What were the key findings, metrics, or results?
    5. **💡 Suggested Improvements**: Provide constructive critiques or ways the methodology could be improved.
    6. **🚀 Future Work Ideas**: Suggest 3 promising directions for future research based on this paper.
    7. **📚 Recommended Similar Papers**: Suggest 3-5 real, well-known academic papers or foundational concepts related to this specific topic that the reader should explore next.

    Here is the paper text:
    ---
    {text}
    ---
    '''
    response = model.generate_content(prompt)
    return response.text

# Main UI Flow
uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type=["pdf"])

if uploaded_file is not None:
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar to proceed.")
    else:
        with st.spinner("📄 Extracting text from PDF..."):
            paper_text = extract_text_from_pdf(uploaded_file)
            st.success(f"Text extracted successfully! ({len(paper_text)} characters)")
            
        with st.spinner("🤖 Analyzing paper with AI... This might take 10-20 seconds."):
            try:
                analysis = analyze_paper(paper_text, api_key)
                st.markdown("---")
                st.markdown(analysis)
            except Exception as e:
                st.error(f"An error occurred during API communication: {e}")
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

# 3. Get the Endpoint IP for Localtunnel security verification
import urllib.request
ip = urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip("\n")
print(f"\n{'='*60}")
print(f"🔒 YOUR ENDPOINT IP IS: {ip}")
print(f"Copy this IP address. You will need to paste it into the localtunnel page.")
print(f"{'='*60}\n")

# 4. Start Streamlit in the background and expose it via localtunnel
import subprocess
subprocess.Popen(["streamlit", "run", "app.py", "--server.address=localhost", "--server.port=8501"])
!npx localtunnel --port 8501