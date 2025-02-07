import whisper
from langchain_ollama import OllamaLLM
from gtts import gTTS

def load_whisper():
    try:
        model = whisper.load_model("base")
        return model
    except Exception as e:
        print(f"Error loading Whisper: {e}")
        return None

# Initialize the scientific LLM
def init_llm():
    """Initialize Mistral model through Ollama"""
    llm = OllamaLLM(
        model="mistral",
        temperature=0.1,  
        prompt_template="""ONLY answer what is directly asked. 
        If unclear or off-topic, say "I don't understand the question."
        
        Question: {question}
        Precise Answer: """
    )
    return llm

def generate_answer(user_query, context_documents):
    """Only answer what's in the query"""
    response = llm.invoke(
        f"Question: {user_query}\n"
        "Give a short, direct answer only about what was asked."
    )
    return response

# Create text-to-speech output
def text_to_speech(text, output_file="response.mp3"):
    """Convert text to speech using gTTS"""
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    return output_file