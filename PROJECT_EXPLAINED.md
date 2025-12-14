# TalentScout: The Big Picture 🌟

## What is this project?

Imagine you're a hiring manager who is overwhelmed with hundreds of resumes. **TalentScout** is your intelligent assistant that steps in to help. It's an AI-powered chatbot that talks to job candidates for you.

Instead of just filling out a boring form, candidates have a conversation with TalentScout. It reads their resume first, understands their background, and then interviews them almost like a real person would.

## How does it work? (The Simple Version)

1. **The Handshake (Landing Page)**:
    When a candidate opens the app, they are welcomed by a clean screen asking for their resume. This mimics walking into an interview room and handing over your CV.

2. **The "Read-Through" (AI Analysis)**:
    Once the resume is uploaded, our AI "brain" (Google Gemini) reads it instantly. It doesn't just look for keywords; it actually understands what the candidate has done, their skills, and their experience level.

3. **The Interview (Chat Interface)**:
    After reading the resume, the chat begins.
    - **Context Matters**: The AI knows the candidate's name and background immediately. It won't ask "What is your name?" if it's right there on the paper.
    - **Smart Questions**: If the candidate is a Python developer, it asks Python questions. If they are a designer, it asks about design tools. It adapts the questions based on the resume.

4. **The Memory (Auto-Save)**:
    We know technical glitches happen. That's why the app saves everything automatically. If the internet cuts out or the tab closes, the conversation is safe in our database (MongoDB) up to the very last message.

## Why is it built this way?

We wanted to solve a few specific problems:

- **"I forgot what I said":**
    Older chatbots often forget context. We fixed this by giving the AI a "long-term memory" of the entire conversation, so it never asks for the same info twice.

- **"This feels robotic":**
    Standard forms are cold. By using a chat interface, we make the screening process feel more human and engaging for the candidate.

- **"I lost my data":**
    We implemented a robust **Auto-Save** feature. Every time someone speaks, the data is locked away safely.

## The Technology (Simplified)

Think of the app like a car:
- **The Body (Streamlit)**: This is what you see—the buttons, the chat window, the layout. It's built to be simple and beautiful.
- **The Engine (Google Gemini AI)**: This is the smart part. It generates the questions and understands the answers.
- **The Trunk (MongoDB)**: This is where we store all the "luggage"—the candidate's details and the conversation history—so nothing gets lost.

---
*Built with ❤️ to make hiring human again.*
