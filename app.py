import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()

try:
    client = genai.Client()
except Exception:
    client = None

st.set_page_config(page_title="AI README Architect", page_icon="📝", layout="wide")

st.title("📝 AI GitHub README Architect")
st.caption("Paste your project details or sample code, and let AI build a professional documentation landing page.")

if not os.environ.get("GEMINI_API_KEY"):
    st.warning("⚠️ API Key missing! Please set your GEMINI_API_KEY in a .env file or your environment variables.")

st.sidebar.header("🛠️ Project Metadata")
project_name = st.sidebar.text_input("Project Name", placeholder="e.g., Smart-Task-Scheduler")
tech_stack = st.sidebar.text_input("Tech Stack (comma-separated)", placeholder="e.g., Python, Streamlit, SQLite")
license_type = st.sidebar.selectbox("License", ["MIT", "Apache 2.0", "GPL v3", "None"])

st.subheader("💻 Core Project Code & Mechanics")
raw_context = st.text_area(
    "Paste key code snippets, file structure, or a rough summary of what your project does:",
    height=250,
    placeholder="e.g.,\n- main.py: Has a function that takes tasks and uses a priority queue...\n- requirements.txt: streamlit, pandas..."
)

generate_btn = st.button("🚀 Architect README", type="primary")


if generate_btn:
    if not project_name or not raw_context:
        st.error("Please provide at least a Project Name and some Code Context!")
    elif not os.environ.get("GEMINI_API_KEY"):
        st.error("Cannot generate without a valid Gemini API Key.")
    else:
        
        prompt = f"""
        You are an expert technical writer and developer open-source advocate. 
        Your task is to generate a comprehensive, highly professional, and visually stunning GitHub README.md file based on the following metadata:
        
        - Project Name: {project_name}
        - Tech Stack: {tech_stack}
        - License: {license_type}
        
        Raw Project Context / Code Snippets:
        \"\"\"
        {raw_context}
        \"\"\"
        
        Please include the following sections in standard, clean GitHub Markdown format:
        1. A catchy Header with Project Name and tech badges placeholder.
        2. A concise 2-sentence Overview of what this tool fixes.
        3. 🚀 Key Features (bulleted, with emojis).
        4. 📦 Installation instructions (mock codeblocks based on the stack).
        5. 🛠️ Usage guide (how to run or test it).
        6. 🤝 Contributing guidelines and License block.
        
        Output raw markdown text only. Do not wrap your entire response inside a single massive markdown code block.
        """
        
        st.subheader("✨ Generated Documentation Preview")
        
        
        preview_tab, raw_tab = st.tabs(["👀 Rendered Preview", "📄 Raw Markdown Content"])
        
        with st.spinner("Analyzing code architecture and generating markdown..."):
            try:
            
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                readme_content = response.text
                
            
                with preview_tab:
                    st.markdown(readme_content)
                    
                with raw_tab:
                    st.code(readme_content, language="markdown")
                    st.caption("Tip: You can easily copy the block above directly into your README.md file!")
                    
            except Exception as e:
                st.error(f"An error occurred while communicating with the AI model: {e}")