# app.py
import streamlit as st
from langchain_ollama import OllamaLLM
from gtts import gTTS
import tempfile
import os

# Page config
st.set_page_config(
    page_title="Scientific Expert",
    page_icon="🔬",
    layout="centered"
)

# UI Styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a192f 0%, #112240 100%);
        color: white;
    }
    .stTextInput input {
        background-color: #1E1E2E;
        color: white;
        border: 2px solid #64ffda;
        border-radius: 5px;
    }
    .stTextInput input:focus {
        border-color: #64ffda;
        box-shadow: 0 0 5px #64ffda;
    }
    .stMarkdown {
        color: #8892b0;
    }
    h1, h2, h3 {
        color: #64ffda !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize LLM with strict parameters
def init_llm():
    prompt = """You are a highly accurate scientific expert. Follow these rules strictly:
    1. Only provide verified scientific facts
    2. If you're unsure, say "I need to verify this information"
    3. Keep responses focused and precise
    4. Correct any misconceptions immediately
    5. Use proper scientific terminology"""
    
    return OllamaLLM(
        model="mistral",
        temperature=0.1,
        system_prompt=prompt
    )

# Function to get scientific response
def get_scientific_response(llm, question):
    prompt = f"""Please provide a scientifically accurate answer to: {question}
    
    Requirements:
    - Use only verified scientific facts
    - Be clear and precise
    - Correct any misconceptions in the question
    - Include relevant scientific principles
    - If uncertain, state that explicitly
    
    Question: {question}
    Scientific Answer:"""
    
    return llm.invoke(prompt)

# Text to speech function
def text_to_speech(text):
    try:
        tts = gTTS(text=str(text), lang='en')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

# Main UI
st.title("🔬 Scientific Expert")
st.subheader("Ask me anything about science")

# Initialize LLM
llm = init_llm()

# User input
question = st.text_input(
    "Enter your scientific question:",
    placeholder="Example: What is quantum entanglement?"
)

if question:
    with st.spinner("Researching..."):
        try:
            # Get text response
            response = get_scientific_response(llm, question)
            
            # Display text response
            st.markdown("### Answer:")
            st.write(response)
            
            # Generate and play audio
            with st.spinner("Generating audio..."):
                audio_file = text_to_speech(response)
                if audio_file:
                    st.audio(audio_file)
                    # Cleanup
                    os.unlink(audio_file)
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Sidebar with examples
with st.sidebar:
    st.markdown("### Example Questions")
    st.markdown("""
    - What is DNA?
    - How do black holes work?
    - Explain photosynthesis
    - What causes earthquakes?
    - How do neurons communicate?
    """)
    
    st.markdown("### About")
    st.markdown("""
    This AI provides:
    - Verified scientific facts
    - Clear explanations
    - Audio responses
    - Immediate corrections
    """)

# Footer
st.markdown("---")
st.markdown("*For educational purposes only. Verify critical information.*")