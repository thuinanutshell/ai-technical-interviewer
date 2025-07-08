# Ava – AI Technical Interviewer

Ava is an AI-powered mock technical interviewer that helps job seekers practice coding and behavioral interviews by simulating real-world interview conditions and offering real-time feedback.

---

## Table of Contents

1. [Day 1: User Flow & Research](#day-1-user-flow--research)
2. [Day 2: Database Design & Pseudocode](#day-2-database-design--pseudocode)
3. [Day 3: Feature: Audio Transcription & PDF Parsing](#day-3-feature-audio-transcription--pdf-parsing)
4. [Day 4: Feature: AI Conversation & Follow-up Questions](#day-4-feature-ai-conversation--follow-up-questions)
5. [Day 5: Feature: Analytics (If Time Permits)](#day-5-feature-analytics-if-time-permits)
6. [Day 6: CI/CD & Deployment](#day-6-cicd--deployment)
7. [Day 7: Documentation](#day-7-documentation)

---

# Day 1: User Flow & Research

## Problem Statement

Interview prep is one of the most important parts of the job application process. Preparing alone can feel isolating, and finding the right accountability partner is often challenging. **Ava** is a mock AI interviewer designed to simulate real interviews and provide users with a structured environment to think out loud and receive instant feedback.

### Coding Mode

In Coding Mode, users follow the [UMPIRE framework](https://guides.codepath.com/compsci/UMPIRE-Interview-Strategy):

1. **Understand** – Clarify the problem using examples and questions.
2. **Match** – Identify the problem category and known strategies.
3. **Plan** – Use visualizations and write pseudocode.
4. **Implement** – Write the code in the sandbox.
5. **Review** – Walk through the code with test cases.
6. **Evaluate** – Analyze time/space complexity and tradeoffs.

![image](https://github.com/user-attachments/assets/b63e255a-46ea-4c14-b5dd-b00d105e6f9f)

#### Coding Mode Flow

1. User selects a topic (e.g., Trees, DP)
2. A random question is displayed
3. The user starts the timer
4. User records answer for each UMPIRE step
5. The system transcribes the answer and gives AI feedback
6. Final feedback is provided based on performance

---

### Behavioral Mode

![image](https://github.com/user-attachments/assets/3f835add-60a9-4a2f-af4e-4356b2fb1dda)

#### Behavioral Mode Flow

1. User uploads resume (PDF)
2. The system parses it to create context
3. AI generates personalized questions
4. User records responses
5. AI transcribes and asks up to 2 follow-up questions
6. Final AI feedback is provided

---

## Feature Prioritization

| Feature                     | Priority | Reason |
|----------------------------|-------------|--------|
| Audio Recording & Transcription | 🔥🔥🔥 | Core to simulating interviews because the key focus here is to let the users **practice thinking out loud in a structured way** |
| PDF Parsing                | 🔥🔥🔥 | Enables resume-based behavioral questions because the system needs a **context** to generate a list of appropriate questions |
| AI Conversation            | 🔥🔥🔥 | Enables dynamic mock interview with a **two-way** interaction |
| Code Editor           | 🔥🔥🔥 | Enables **code editor-like** to type out the implementation |
| Follow-up Questions        | 🔥🔥   | Adds realism and depth |
| Analytics                  | 🔥🔥   | Tracks user progress |
| Text-to-Speech             | 🔥     | AI Interviewer speaks like humans instead of just returning text|
| Timer                      | 🔥     | Simulates real interview pressure |
| Authentication             | 🔥     | Required for account setup |

## Technical Research
| Feature                     | Technology | Notes |
|----------------------------|-------------|--------|
| STT - Audio Recording & Transcription | MediaStream Recording API, OpenAI Whisper API | The first API can be used to record audio in the browser, and the second API is used to transcribe the audio into text.|
| PDF Parsing                | PDF.js, Gemini API (with built-in feature for PDF parsing), PyMuPDF| Both can read and parse PDF into text ready to be used in the AI's context, but if I use Gemini API, it will cost towards the number of tokens used |
| AI Conversation            | Gemini API, Claude API | Enables dynamic mock interview |
| Code Editor           | CodeMirror | Enables **code editor-like** to type out the implementation |
| Follow-up Questions        | Gemini API, Claude API   | Adds realism and depth |
| Analytics                  | Rechart.js   | Tracks user progress by providing some data visualizations |
| TTS - Text-to-Speech       | ElevenLabs API   | AI Interviewer speaks like humans instead of just returning text only |
| Authentication             | Supabase     | Required for account setup |

---

# Day 2: Database Design & Pseudocode

### Database Design
For the first version of this app, I had to make a decision between complexity and storage. The part that got me thinking is that: *Do I really need to store the audio files from the users?* My reasoning is that 

1. Saved audio files are not of significant importance because what matters is that the user can receive the assessment of their performance after a mock interview session and suggestions on how to improve the next time. One might argue that if the user needs to review the audio of themselves later, or re-run the analysis. But as someone whose main focus is to practice **thinking out loud in a structured** way, reviewing audio is way less important than having a functional space to do as much practice as possible.
2. Saved audio files cost more storage, while the value per storage is not high, unless the key feedback is to use the data to train some models, which is not the case here.

As a result, my final database schema design is shown below, which I believe strikes a balance between simplicity and functionality with the following tables:
| Table     | Description                                                                                         |
|-----------|-----------------------------------------------------------------------------------------------------|
| **User**  | Stores basic user personal information                                                              |
| **Question** | A question bank that stores all questions (both coding and behavioral). The `type` field indicates whether the question is behavioral, tree, dynamic programming, etc. |
| **Resume** | A simple table to store a user's resume data                                                       |
| **Session** | Stores a complete mock interview session for a user that includes the initial context (coding question description or parsed resume data) |
| **Message** | Stores the conversation between the user and the AI system                                        |
| **Feedback** | Stores the feedback for the session as a whole                                                   |


<img width="1115" alt="Screenshot 2025-07-08 at 9 54 49 AM" src="https://github.com/user-attachments/assets/1b3e83bf-b643-4d4c-8ed3-702d774423f6" />


## Structure & Pseudocode for Backend & Frontend
### Tech Stack
| Layer          | Tech                                 | Reason                                                                                                 |
| -------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| **Backend**    | FastAPI                              | Lightweight, async-friendly, production-ready. I had extensive experience with Flask before, so I want to try something similar.|
| **Frontend**   | Next.js                              | Hybrid SSR/SPA; pairs well with Vercel and Supabase Auth out of the box.|
| **Auth**       | Supabase Auth                        | Simple to set up, good support for email/password and OAuth; tightly integrates with Next.js.|
| **Database**   | Supabase DB (PostgreSQL)             | Simplify the process of setting up the database|
| **Deployment** | Railway (backend), Vercel (frontend) | Simple, scalable, CI/CD-friendly.|

![image](https://github.com/user-attachments/assets/04229f23-8891-4632-ab48-dc6a676f8cc2)

### Backend
| **Action**                           | **Method**             | **Route**                         | **Description**                                                              |
| ------------------------------------ | ---------------------- | --------------------------------- | ---------------------------------------------------------------------------- |
| Create a new interview session       | `POST`                 | `/sessions`                       | Starts a new session (e.g. after selecting a question or uploading a resume) |
| Get session details                  | `GET`                  | `/sessions/{session_id}`          | Fetch a specific session’s metadata, messages, etc.                          |
| Submit a user answer (audio)         | `POST`                 | `/sessions/{session_id}/messages` | Adds a new message from the user (with audio blob) to the session            |
| Respond with system feedback         | `POST`                 | `/sessions/{session_id}/messages` | Same route: system's follow-up is added as another message                   |
| Get full conversation history        | `GET`                  | `/sessions/{session_id}/messages` | Returns the list of user + system messages                                   |
| Generate final feedback for session  | `POST`                 | `/sessions/{session_id}/feedback` | Generates and stores tone summary, speech rate, overall evaluation           |
| Get feedback for session             | `GET`                  | `/sessions/{session_id}/feedback` | Retrieve saved feedback (for review or display)                              |
| Upload & parse resume                | `POST`                 | `/resumes`                        | Upload resume (PDF), parse it on server, store parsed data                   |
| Get parsed resume for user           | `GET`                  | `/resumes/user/{user_id}`         | Retrieve a user’s uploaded resumes                                           |
| Generate questions based on resume   | `POST`                 | `/questions/generated`            | Dynamically generate questions from a parsed resume                          |
| Create a new custom question         | `POST`                 | `/questions`                      | Add a manual question (coding or behavioral) to the question bank            |
| Get all questions                    | `GET`                  | `/questions`                      | Retrieve question bank (optionally filtered by type or user)                 |
| Get a specific question              | `GET`                  | `/questions/{question_id}`        | Fetch one question by ID                                                     |
| Delete a question                    | `DELETE`               | `/questions/{question_id}`        | Remove a question (admin or owner only)                                      |

### Frontend 
#### Lofi Mockup

The app has two primary interview modes: **Coding** and **Behavioral**.

![image](https://github.com/user-attachments/assets/4604cd04-4462-4457-b8a0-2b2ec7e15328)

#### Next.js App Structure
```
/frontend
│
├── app/                      # Next.js app directory (App Router)
│   ├── page.jsx              # Landing page or redirect to dashboard
│   │
│   ├── auth/                 # Auth routes
│   │   ├── login/page.jsx    # Login form page
│   │   └── register/page.jsx # Register form page
│   │
│   ├── dashboard/            # Authenticated main dashboard
│   │   ├── layout.jsx        # Shared layout for dashboard pages
│   │   └── page.jsx          # Main interview session launcher
│   │
│   ├── session/              # Dynamic session pages
│      └── [id]/page.jsx     # Multi-turn interview session (chat, code, feedback)
|
├── components/               # Reusable UI components
│   ├── ChatBox.jsx           # Chat UI for user-AI conversation
│   ├── CodeEditor.jsx        # Embedded code editor
│   ├── Feedback.jsx          # Final feedback display
│   ├── QuestionDisplay.jsx   # Displays current question
│   ├── CreateQuestionModal.jsx # Modal to create a new question
│   ├── AudioRecorder.jsx     # Audio recording component using MediaStream API
│   ├── LoadingSpinner.jsx    # Generic loading spinner
│   └── ErrorMessage.jsx      # Generic error display
│
├── hooks/                    # Custom React hooks
│   ├── useSession.js         # Manage session state, question progress
│   ├── useChat.js            # Manages chat messages (user/system turns)
│   └── useAudioRecorder.js   # Handles MediaStream Recording logic
│
├── lib/                      # API utility functions and helpers
│   ├── api.js                # Functions to call FastAPI backend routes
│   └── supabaseClient.js     # Supabase config & instance
│
├── styles/                   # Global styles and Tailwind config
│   └── globals.css
│
├── public/                   # Static files (logo, icons, etc.)
│
├── .env.local                # API keys, Supabase credentials
├── tailwind.config.js
├── postcss.config.js
├── package.json
└── README.md

```

---
## Day 3: Feature: Audio Transcription & PDF Parsing

- Integrate Whisper (or another model) for transcription
- Use `pdfplumber`, `PyMuPDF`, or third-party API for resume parsing
- Normalize parsed content for embedding/context

### Demo
### Tests

---

## Day 4: Feature: AI Conversation & Follow-up Questions

- Use OpenAI/Gemma with structured prompts
- Memory chain to store context (e.g., LangChain)
- Rule-based or confidence-threshold triggers for follow-up

### Demo
### Tests

---

## Day 5: Feature: Analytics (If Time Permits)

- Track completion, AI ratings, time per question, weak areas
- Visualize via simple dashboard (e.g., Recharts or Chart.js)

### Demo
### Tests

---

## Day 6: CI/CD & Deployment

- GitHub Actions for test + lint checks
- Deploy backend (Railway)
- Deploy frontend (Vercel)
- Use `.env` for secrets + environment configs

---

## Day 7: Documentation

- README with:
  - Overview
  - Feature List
  - Installation & Setup
  - API Reference
- Record a Loom demo
