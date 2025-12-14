import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
from datetime import datetime, timezone
import tempfile
import os

from pathlib import Path
import signal
import sys

if sys.platform.startswith('win'):
    for sig in ['SIGHUP', 'SIGTSTP', 'SIGCONT']:
        if not hasattr(signal, sig):
            setattr(signal, sig, signal.SIGTERM)


_original_signal = signal.signal
def _patched_signal(signalnum, handler):
    try:
        return _original_signal(signalnum, handler)
    except ValueError:
        pass
signal.signal = _patched_signal

from crew_agent import TalentScoutCrew, get_resume_analysis_prompt, get_tech_questions_prompt
from database import save_candidate, update_candidate
import config

st.set_page_config(
    page_title="TalentScout - Hiring Assistant",
    page_icon=" ",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 1rem;
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        text-align: center;
        color: #a0a0a0;
        margin-bottom: 2rem;
    }
    
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .stChatInput input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
    }
    
    .sidebar .stButton button {
        width: 100%;
        background: linear-gradient(90deg, #00d4ff, #7b2cbf);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .candidate-info {
        background: rgba(0, 212, 255, 0.1);
        border-left: 3px solid #00d4ff;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .success-box {
        background: rgba(0, 255, 136, 0.1);
        border-left: 3px solid #00ff88;
        padding: 1rem;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = TalentScoutCrew()
    
    if "candidate_data" not in st.session_state:
        st.session_state.candidate_data = {
            "full_name": None,
            "email": None,
            "phone": None,
            "years_of_experience": None,
            "desired_position": None,
            "location": None,
            "tech_stack": None,
            "resume_text": None,
            "resume_analysis": None,
            "technical_questions": [],
            "qa_responses": [],
        }
    
    if "conversation_stage" not in st.session_state:
        st.session_state.conversation_stage = "greeting"
    
    if "conversation_ended" not in st.session_state:
        st.session_state.conversation_ended = False
    
    if "resume_uploaded" not in st.session_state:
        st.session_state.resume_uploaded = False
    
    if "resume_file_path" not in st.session_state:
        st.session_state.resume_file_path = None
        
    if "session_id" not in st.session_state:
        st.session_state.session_id = None


def extract_pdf_text(pdf_file) -> str:
    """Extract text from uploaded PDF file."""
    try:
        pdf_reader = PdfReader(BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


def check_exit_keywords(message: str) -> bool:
    """Check if message contains exit keywords as whole words."""
    import re
    message_lower = message.lower().strip()
    for keyword in config.EXIT_KEYWORDS:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, message_lower):
            return True
    return False


def get_agent_response(user_message: str) -> str:
    """Get response from Agno agent."""
    try:
        context = "\n".join([
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in st.session_state.messages
        ])
        
        candidate_context = ""
        cd = st.session_state.candidate_data
        if cd["full_name"]:
            candidate_context += f"\nCandidate Name: {cd['full_name']}"
        if cd["tech_stack"]:
            candidate_context += f"\nTech Stack: {cd['tech_stack']}"
        if cd["desired_position"]:
            candidate_context += f"\nDesired Position: {cd['desired_position']}"
        if cd["resume_analysis"]:
            candidate_context += f"\nResume Analysis: {cd['resume_analysis']}"
        
        full_prompt = f"""Previous conversation:
{context}

Collected candidate information:{candidate_context}

Current user message: {user_message}

Respond appropriately as the hiring assistant. If you haven't collected all required information yet, 
ask for the next piece of information. If all info is collected and you haven't asked technical questions yet,
generate and ask technical questions based on their tech stack."""
        
       
        if st.session_state.candidate_data.get("resume_text"):
            full_prompt += f"\n\nRESUME CONTENT:\n{st.session_state.candidate_data['resume_text']}"
        
        response = st.session_state.agent.run(full_prompt)
        
        return response
    except Exception as e:
        return f"I apologize, but I encountered an issue. Please try again. (Error: {str(e)})"


def auto_save_session():
    """Auto-save conversation to MongoDB."""
    try:
        candidate_data = st.session_state.candidate_data.copy()
        candidate_data["conversation_history"] = st.session_state.messages
        candidate_data["last_active"] = datetime.now(timezone.utc)
        
        if st.session_state.session_id:
            update_candidate(st.session_state.session_id, candidate_data)
        else:
            candidate_data["session_start"] = datetime.now(timezone.utc)
            doc_id = save_candidate(candidate_data)
            st.session_state.session_id = doc_id
            
    except Exception as e:
        print(f"Auto-save error: {e}")




def display_landing_page():
    """Display the initial landing page for resume upload."""
    st.markdown('<h1 class="main-header">TalentScout</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Hiring Assistant for Technology Recruitment</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h3 style='text-align: center'>👋 Welcome!</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center'>To begin your interview process, please upload your resume. I'll analyze it to customize our conversation.</p>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload your Resume (PDF)",
            type=["pdf"],
            key="resume_uploader"
        )
        
        if uploaded_file:
            with st.spinner("🚀 Analyzing your resume... please wait..."):
                temp_dir = tempfile.gettempdir()
                temp_path = Path(temp_dir) / f"resume_{uploaded_file.name}"
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.session_state.resume_file_path = str(temp_path)
                
                analysis_prompt = """Analyze this resume thoroughly and extract ALL available information.

Provide your response in exactly this format:

**EXTRACTED INFORMATION:**
- Full Name: [extract from resume or "Not found"]
- Email: [extract from resume or "Not found"]
- Phone: [extract from resume or "Not found"]
- Years of Experience: [estimate from work history or "Not found"]
- Current/Recent Position: [extract from resume or "Not found"]
- Location: [extract from resume or "Not found"]
- Tech Stack/Skills: [list all technologies, languages, frameworks, tools mentioned]

**CANDIDATE SUMMARY:**
[2-3 sentences summarizing their background and expertise]

**SUGGESTED INTERVIEW QUESTIONS:**
[2-3 relevant questions based on their projects/experience mentioned in the resume]"""
                
                resume_text = ""
                with open(temp_path, "rb") as f:
                    resume_text = extract_pdf_text(f)
                
                st.session_state.candidate_data["resume_text"] = resume_text

                analysis_prompt_with_context = f"{analysis_prompt}\n\nRESUME CONTENT:\n{resume_text}"
                
                analysis_response = st.session_state.agent.run(analysis_prompt_with_context)
                
                st.session_state.candidate_data["resume_analysis"] = analysis_response
                st.session_state.resume_uploaded = True
                
                analysis_text = analysis_response
                
                def extract_field(text, field_name):
                    """Extract a field value from the analysis text."""
                    import re
                    pattern = rf"{field_name}:\s*(.+?)(?:\n|$)"
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        value = match.group(1).strip()
                        if value.lower() not in ["not found", "n/a", "", "-"]:
                            return value
                    return None
                
                extracted_name = extract_field(analysis_text, "Full Name")
                extracted_email = extract_field(analysis_text, "Email")
                extracted_phone = extract_field(analysis_text, "Phone")
                extracted_exp = extract_field(analysis_text, "Years of Experience")
                extracted_position = extract_field(analysis_text, "Current/Recent Position")
                extracted_location = extract_field(analysis_text, "Location")
                extracted_tech = extract_field(analysis_text, "Tech Stack/Skills")
                
                if extracted_name:
                    st.session_state.candidate_data["full_name"] = extracted_name
                if extracted_email:
                    st.session_state.candidate_data["email"] = extracted_email
                if extracted_phone:
                    st.session_state.candidate_data["phone"] = extracted_phone
                if extracted_exp:
                    st.session_state.candidate_data["years_of_experience"] = extracted_exp
                if extracted_position:
                    st.session_state.candidate_data["desired_position"] = extracted_position
                if extracted_location:
                    st.session_state.candidate_data["location"] = extracted_location
                if extracted_tech:
                    st.session_state.candidate_data["tech_stack"] = extracted_tech
                
                st.success("Resume analyzed successfully!")
                
                ack_response = st.session_state.agent.run(
                    f"""The candidate has shared their resume. Here's the analysis:

{analysis_response}

Acknowledge the resume upload, briefly summarize the key information you extracted (name, experience, skills), thank them for sharing it, and then proceed with the interview. Ask about any critical missing information OR if everything is extracted, move to the first technical question based on their tech stack."""
                )
                
                if not st.session_state.messages:
                     st.session_state.messages.append({"role": "assistant", "content": ack_response})
                
                auto_save_session()
                st.rerun()


def display_chat():
    """Display chat messages."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    """Main application entry point."""
    initialize_session_state()
    
    if not st.session_state.resume_uploaded:
        display_landing_page()
    else:
        
        st.markdown('<h2 class="main-header" style="font-size: 1.5rem; margin-bottom: 0;">TalentScout Process</h2>', unsafe_allow_html=True)
        st.markdown('---')
    
        display_chat()
        
        if not st.session_state.conversation_ended:
            if prompt := st.chat_input("Type your message here..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                if check_exit_keywords(prompt):
                    st.session_state.conversation_ended = True
                    
                    auto_save_session()
                    doc_id = st.session_state.session_id
                    
                    farewell = f"""Thank you so much for taking the time to speak with me today! 🙏

**Here's a summary of what we collected:**
- Name: {st.session_state.candidate_data.get('full_name', 'Not provided')}
- Position: {st.session_state.candidate_data.get('desired_position', 'Not specified')}
- Tech Stack: {st.session_state.candidate_data.get('tech_stack', 'Not specified')}

**Next Steps:**
Our HR team will review your application and get back to you within **3-5 business days**.

Best of luck with your application! 🌟

*Session ID: {doc_id if doc_id else 'Local session'}*"""
                    
                    st.session_state.messages.append({"role": "assistant", "content": farewell})
                    
                    with st.chat_message("assistant"):
                        st.markdown(farewell)
                else:
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response = get_agent_response(prompt)
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            auto_save_session()
                
                st.rerun()
        else:
            st.info("🔒 This session has ended. Click 'Start New Session' in the sidebar to begin again.")


if __name__ == "__main__":
    main()
