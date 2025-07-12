# Ava – AI Technical Interviewer

Ava is an AI-powered mock technical interviewer that helps job seekers practice coding and behavioral interviews by simulating real-world interview conditions and offering real-time feedback.

## ⚙️ Tech Stack

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

![OpenAI Whisper](https://img.shields.io/badge/OpenAI%20Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)
![Gemini API](https://img.shields.io/badge/Gemini%20API-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

![image](https://github.com/user-attachments/assets/04229f23-8891-4632-ab48-dc6a676f8cc2)

---

## Table of Contents

1. [Day 1: User Flow & Research](#day-1-user-flow--research)
2. [Day 2: Database Design & Pseudocode](#day-2-database-design--pseudocode)
3. [Day 3: Feature: Authentication](#day-3-feature-authentication)
4. [Day 4: Feature: Audio Transcription & PDF Parsing](#day-4-feature-audio-transcription--pdf-parsing)
5. [Day 5: Feature: AI Conversation](#day-5-feature-ai-conversation)
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

```
backend/
│
├── app/                             # Main application package
│   ├── __init__.py
│   ├── main.py                      # Entry point for FastAPI app
│   │
│   ├── api/                         # API route definitions
│   │   ├── __init__.py
│   │   ├── auth.py                  # Routes for login, signup
│   │   ├── session.py               # Start session, submit answer, get response
│   │   ├── resume.py                # Upload + parse resume
│   │   ├── feedback.py              # Final feedback generation
│   │   └── question.py              # Create, list questions
│   │
│   ├── models/                      # Pydantic models for request/response validation
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── resume.py
│   │   ├── feedback.py
│   │   └── question.py
│   │
│   ├── services/                    # Business logic, Gemini/Whisper wrappers
│   │   ├── __init__.py
│   │   ├── whisper.py               # Audio transcription (OpenAI Whisper)
│   │   ├── gemini.py                # Gemini response generation
│   │   ├── resume_parser.py         # PDF parsing using PyMuPDF or LlamaIndex
│   │   └── feedback_generator.py    # Feedback creation logic
│   │
│   ├── db/                          # DB access and Supabase client
│   │   ├── __init__.py
│   │   ├── supabase.py              # Supabase connection instance
│   │   └── crud.py                  # Abstractions for DB operations
│   │
│   ├── core/                        # Settings, dependencies, utils
│   │   ├── config.py                # Environment & app configs
│   │   ├── security.py              # JWT, password hashing (bcrypt)
│   │   └── dependencies.py          # Shared dependencies
│
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
```

### Frontend 
#### Lofi Mockup

The app has two primary interview modes: **Coding** and **Behavioral**.

![image](https://github.com/user-attachments/assets/b7436152-97bc-4bc6-9460-e48b75eb2cd6)

#### Next.js App Structure
```
/frontend
│
├── app/                      # App router structure (Next.js 13+)
│   ├── page.jsx              # Landing or redirect to dashboard
│   │
│   ├── auth/                 # Supabase auth pages
│   │   ├── login/page.jsx
│   │   └── register/page.jsx
│   │
│   ├── dashboard/            # Entry point after login (choose mode)
│   │   ├── layout.jsx
│   │   └── page.jsx
│   │
│   ├── session/              # Dynamic session pages
│   │   └── [id]/page.jsx     # Live session: chat, code, question flow, feedback
│
├── components/               # Reusable UI and logic components
│   ├── session/              # Interview-specific components
│   │   ├── ChatBox.jsx
│   │   ├── CodeEditor.jsx
│   │   ├── QuestionDisplay.jsx
│   │   ├── Feedback.jsx
│   │   └── CreateQuestionModal.jsx
│   │
│   ├── shared/               # Generic UI components
│   │   ├── AudioRecorder.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── ErrorMessage.jsx
│
├── hooks/                    # Custom React hooks
│   ├── useSession.js         # Handle session ID, mode, etc.
│   ├── useChat.js            # Multi-turn conversation logic
│   └── useAudioRecorder.js   # Audio recording logic
│
├── lib/                      # Utility and service functions
│   ├── api.js                # Calls FastAPI backend
│   └── supabaseClient.js     # Supabase instance config
│
├── constants/                # Static data (question types, enums)
│   └── questionTypes.js
│
├── public/                   # Static assets (logo, icons)
├── styles/                   # Global CSS & Tailwind config
│   └── globals.css
│
├── .env.local                # Supabase, backend URLs
├── tailwind.config.js
├── postcss.config.js
├── package.json
└── README.md
```

---
## Day 3: Feature: Authentication
### Progress
The structure below shows my progress so far. There are some modifications compared to what I planned yesterday. Because I'm new to FastAPI (I have more experience with Flask), I rely on the [fullstack template provided by FastAPI](https://github.com/fastapi/full-stack-fastapi-template/tree/master/backend) to structure my folder. I made some modifications that meet my needs and level. 

Currently, when tested with SwaggerUI, the registration, login, and logout endpoints work. This is also the first time I used `Pydantic` for data validation. I also successfully connected the backend with the Postgres connector using `Supabase`. For the next steps, I want to modify the config file to set up 3 different environments: `testing`, `development`, and `production`. I'm thinking of using a local database for the testing environment, and one Supabase database for development and one Supabase database for production. 

I think I underestimated how long it took to write code that I actually understand. This took me around 3 hours to write code, read the code template to understand what's going on, and think about how to structure the code best to make it functional yet focused and simple. Here's what I've learned today:
- When defining Pydantic models, I need to define the input that the server is expected to receive from the client and the output that is sent from the server to the client
- Before running the app, we need a file to initialize/populate the database (create all tables), and this file should be separate instead of being put inside the main file to avoid the database being recreated every time at app startup.
- One more thing to take into consideration, if you use Supabase and have already defined the tables before coding, make sure not to recreate them one more time when starting the app.
- I've done with the part to set up different environments for testing, dev, and prod:
  1. For testing, I just use an in-memory database to run the test using `pytest`
  2. For development and production, I currently use one Supabase database, but I plan to create a different one for production
  3. To make things easier to run, I created a folder `scripts` to store different shell scripts for test, dev, and prod, and learned to make the scripts executable by using `chmod +x scripts/*.sh`

### Bugs
- I encountered a compatibility issue between `passlib` and `bcrypt`, so to resolve the problem, I asked Claude and found out that the newer version of `bcrypt` is not compatible with `passlib`. Then, one solution was to use `argon2`, which is more secure and compatible.
```python
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
```
- I installed `jwt` instead of `PyJWT` for JWT-based auth; the latter is the correct one
```
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
           ^^^^^^^^^^
AttributeError: module 'jwt' has no attribute 'encode'
```
- I put the `tests` folder in the wrong location - the correct one should be inside the root level of the `backend` folder, not in the `app` folder.

🎉 Authentication works!

https://github.com/user-attachments/assets/8e0a527a-93a9-40a5-b492-3d4fc856fc73

---

## Day 4: Feature: Audio Transcription & PDF Parsing
### Planning
1. Start by creating the backend logic for creating manual questions
   - Create the frontend component for the create-question modal
3. Then, continue to create the backend logic for parsing the resume and generating questions from the parsed data
   - Create the frontend component for uploading a resume
   - Create the frontend component for displaying generated questions/manual questions
5. Then, create the backend logic for audio transcription
   - Create the audio recorder component on the frontend
     
### Progress
I've done with the logic to parse the resume data. We can actually use `PyMuPDF4LLM` to parse the PDF text into markdown. This is a specific library built for parsing PDF into input used for different LLMs. Basically, the function takes the uploaded resume input as raw bytes. 
- `tempfile.NamedTemporaryFile(...)` creates a temporary file on disk that will be deleted after the `with` block and has a `.pdf` suffix so pymupdf4llm recognizes it as a PDF.
- `tmp.write(file_bytes)` writes the raw bytes into the temporary PDF file.
- `tmp.flush()` ensures that all data is written from the buffer to disk, so it’s ready for reading by other processes.
- Using `strip()` to return the cleaned-up (stripped of leading/trailing whitespace) Markdown string.
  
```python
def parse_resume_to_markdown(file_bytes: bytes) -> str:
    """Write PDF to a temp file and extract markdown using pymupdf4llm."""
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp.flush()

            # Parse the file into markdown!
            markdown = pymupdf4llm.to_markdown(tmp.name)
            if not markdown or not markdown.strip():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Could not extract text from PDF. The file may be corrupted or contain only images.",
                )

        return markdown.strip()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse PDF: {str(e)}",
        )
```

---

## Day 5: AI Conversation
Wow, this one is much harder and more confusing than I thought. I used open-source Whisper model for audio transcription and Gemini API to respond to user's answers.

---

## Day 6: CI/CD & Deployment

---

## Day 7: Documentation

- README with:
  - Overview
  - Feature List
  - Installation & Setup
  - API Reference
- Record a Loom demo
