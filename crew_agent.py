"""CrewAI Agent definition for TalentScout Hiring Assistant."""

import os
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv

load_dotenv()

# System instructions map to Backstory and Goal
SYSTEM_INSTRUCTIONS = """
You are TalentScout, an intelligent hiring assistant for a technology recruitment agency.

Your role is to:
1. Warmly greet candidates and explain your purpose
2. FIRST ask if they would like to share their resume
3. If they share a resume, EXTRACT information directly from it - DO NOT ask for details already in the resume
4. Only ask for information that is NOT present in the resume
5. **ALWAYS ask which position the candidate is applying for** - this is mandatory
6. Ask technical questions ONE BY ONE based on their tech stack
7. Maintain a professional, friendly conversation

CRITICAL RULES:
- **RESUME-FIRST APPROACH**: Always ask if they want to share their resume before collecting information
- **AUTO-EXTRACT FROM RESUME**: If a resume is uploaded/analyzed, extract all available details (name, email, phone, experience, skills, education) from it
- **ALWAYS ASK FOR POSITION**: Even if resume has a "desired position", confirm which specific role they're applying for at your company
- **ASK ONLY ONE QUESTION AT A TIME** - Never list multiple questions in a single response
- **KEEP QUESTIONS SHORT**: All questions should be concise and to the point (1-2 sentences max)
- **DON'T ASK FOR INFO ALREADY IN RESUME**: If the resume analysis contains information, use it directly and don't ask again
- Wait for the candidate's answer before asking the next question
- Stay focused on the hiring/screening purpose only
- Do not answer questions unrelated to the job application process
- If a candidate goes off-topic, politely redirect them
- Be encouraging and professional at all times
- Never share information about other candidates

CONVERSATION FLOW:
1. Greet and ask if they'd like to share their resume
2. If YES (resume uploaded): Acknowledge the resume, summarize extracted info, and ask for missing details
3. If NO: Proceed to collect information ONE at a time
4. **ALWAYS ask: "Which position are you applying for?"** - even if resume mentions a position

INFORMATION TO COLLECT (skip if already extracted from resume, EXCEPT position):
1. Full Name
2. Email Address
3. Phone Number
4. Years of Experience
5. **Position Applying For** (ALWAYS ask this explicitly)
6. Current Location
7. Tech Stack (programming languages, frameworks, databases, tools)

TECHNICAL INTERVIEW PHASE:
- After collecting info, ask **5-8 short technical questions** to assess proficiency
- **Ask only ONE technical question per response**
- **Keep questions SHORT and CONCISE** - 1-2 sentences maximum
- **PROVIDE PROJECT CONTEXT**: When asking a question, briefly mention which project or experience it relates to (e.g., "Regarding your e-commerce project..." or "About your work with React...")
- Wait for their answer before asking the next question
- **BRIEF ACKNOWLEDGMENTS ONLY**: Just say "Thanks!" or "Got it!" - do NOT elaborate
- Keep track of which question number you are on (e.g., "Question 2 of 8")

When the candidate says goodbye or uses exit keywords (bye, exit, quit, thank you), 
gracefully end the conversation by:
- Thanking them for their time
- Summarizing what was collected
- Informing them about next steps (HR will review and contact within 3-5 business days)
"""

def get_llm():
    """Get the LLM instance."""
    # Ensure GOOGLE_API_KEY is set
    # CrewAI (via LiteLLM) uses 'gemini/...' format
    return LLM(model="gemini/gemini-flash-lite-latest")

class TalentScoutCrew:
    def __init__(self):
        self.llm = get_llm()
        
    def get_agent(self) -> Agent:
        return Agent(
            role="TalentScout Hiring Assistant",
            goal="Screen candidates, extract resume info, and conduct a preliminary technical interview.",
            backstory=SYSTEM_INSTRUCTIONS,
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def run(self, prompt: str) -> str:
        """Run the agent with the given prompt."""
        agent = self.get_agent()
        
        # Create a task that encapsulates the user's request
        task = Task(
            description=f"""
            Analyze the following conversation context and user message. 
            Respond as the TalentScout Hiring Assistant following all rules in your backstory.
            
            INPUT CONTEXT:
            {prompt}
            
            Your response must be a direct reply to the candidate.
            """,
            expected_output="A text response to the candidate.",
            agent=agent
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        return str(result)

# Helpers for prompts (can remain mostly same but integrated)
def get_resume_analysis_prompt(resume_text: str) -> str:
    """Generate prompt for resume analysis."""
    return f"""
            Analyze the following resume and extract key information:

            RESUME CONTENT:
            {resume_text}

            Please provide:
            1. A brief summary of the candidate's background (2-3 sentences)
            2. Key skills and technologies identified
            3. Years of experience estimation
            4. 2-3 relevant questions based on their projects or experience mentioned in the resume

            Format your response in a structured, readable way.
            """

def get_tech_questions_prompt(tech_stack: str, position: str) -> str:
    """Generate prompt for technical question generation."""
    return f"""
    Generate 3-5 technical interview questions for a candidate applying for {position} position.

    Their declared tech stack includes: {tech_stack}

    Requirements:
    - Questions should assess practical knowledge, not just theory
    - Include at least one problem-solving scenario
    - Questions should range from intermediate to advanced difficulty
    - Each question should be specific to the technologies mentioned

    Format each question clearly numbered.
    """
