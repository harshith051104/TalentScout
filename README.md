# TalentScout - AI Hiring Assistant

An intelligent hiring assistant chatbot built with **Agno Agent Framework**, **Google Gemini 2.0 Flash**, **Streamlit**, and **MongoDB**. It screens candidates by gathering information, analyzing resumes, and generating technical questions.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Agno](https://img.shields.io/badge/Agno-2.0+-green.svg)

## 📋 Features

- **Smart Greeting**: Welcomes candidates and explains the screening process
- **Information Gathering**: Collects name, email, phone, experience, position, location, and tech stack
- **Resume Analysis**: Upload PDF resumes for AI-powered analysis and personalized questions
- **Technical Questions**: Generates 3-5 relevant questions based on declared tech stack
- **Context Awareness**: Maintains conversation flow using Agno's memory features
- **Graceful Exit**: Handles exit keywords and summarizes the session
- **Data Persistence**: Stores candidate data in MongoDB

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **LLM Framework** | Agno Agent Framework |
| **Model** | Google Gemini 2.0 Flash |
| **Frontend** | Streamlit |
| **Database** | MongoDB |
| **PDF Parsing** | PyPDF2 |

## 📦 Installation

### Prerequisites

- Python 3.9+
- MongoDB (local or cloud)
- Google AI API Key

### Setup

1. **Clone/Navigate to the project**:

   ```bash
   cd d:\Internship\Appleton\TalentScout
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Edit `.env` file:

   ```
   GOOGLE_API_KEY=your_google_api_key_here
   MONGODB_URI=mongodb://localhost:27017
   ```

5. **Start MongoDB** (if using local):

   ```bash
   mongod
   ```

6. **Run the application**:

   ```bash
   streamlit run app.py
   ```

## 🚀 Usage

1. Open the app in your browser (usually `http://localhost:8501`)
2. **(Optional)** Upload your resume PDF in the sidebar
3. Chat with the assistant - answer questions about yourself
4. Provide your tech stack when asked
5. Answer the generated technical questions
6. Say "bye" or "thank you" to end the session

### Exit Keywords

The conversation ends when you say: `bye`, `exit`, `quit`, `goodbye`, `thank you`, `thanks`, `end`

## 📁 Project Structure

```
TalentScout/
├── app.py           # Streamlit UI and main logic
├── agent.py         # Agno Agent with Gemini model
├── config.py        # Configuration and constants
├── database.py      # MongoDB operations
├── requirements.txt # Python dependencies
├── .env             # Environment variables (gitignored)
├── .gitignore
└── README.md
```

## 🎨 Prompt Design

### System Prompt

The agent uses a carefully crafted system prompt that:

- Defines the TalentScout persona
- Lists required information to collect in order
- Provides rules for staying on-topic
- Handles exit scenarios gracefully

### Resume Analysis Prompt

Extracts skills, experience, and generates 2-3 questions from resume content.

### Technical Question Prompt

Generates 3-5 practical questions based on the candidate's declared tech stack and desired position.

## 🔒 Data Privacy

- All data is stored locally in MongoDB
- Resume text is processed in-memory
- No data is shared with external services (except Gemini API for processing)
- Session ends when user says goodbye

## ⚠️ Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Context Maintenance** | Used Agno's `add_history_to_messages=True` for conversation memory |
| **Off-topic Handling** | System prompt instructs agent to redirect politely |
| **PDF Text Extraction** | PyPDF2 handles various PDF formats |
| **Exit Detection** | Keyword matching before processing |
