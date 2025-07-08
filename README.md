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

## Day 1: User Flow & Research

### Problem Statement

Interview prep is one of the most important parts of the job application process. Preparing alone can feel isolating, and finding the right accountability partner is often challenging. **Ava** is a mock AI interviewer designed to simulate real interviews and provide users with a structured environment to think out loud and receive instant feedback.

### Lofi Mockup

The app has two primary interview modes: **Coding** and **Behavioral**.

![image](https://github.com/user-attachments/assets/4604cd04-4462-4457-b8a0-2b2ec7e15328)

---

#### Coding Mode

In Coding Mode, users follow the [UMPIRE framework](https://guides.codepath.com/compsci/UMPIRE-Interview-Strategy):

1. **Understand** – Clarify the problem using examples and questions.
2. **Match** – Identify the problem category and known strategies.
3. **Plan** – Use visualizations and write pseudocode.
4. **Implement** – Write the code in the sandbox.
5. **Review** – Walk through the code with test cases.
6. **Evaluate** – Analyze time/space complexity and tradeoffs.

![image](https://github.com/user-attachments/assets/b63e255a-46ea-4c14-b5dd-b00d105e6f9f)

##### Coding Mode Flow

1. User selects a topic (e.g., Trees, DP)
2. A random question is displayed
3. User starts the timer
4. User records answer for each UMPIRE step
5. System transcribes the answer and gives AI feedback
6. Final feedback is provided based on performance

---

#### Behavioral Mode

![image](https://github.com/user-attachments/assets/3f835add-60a9-4a2f-af4e-4356b2fb1dda)

##### Behavioral Mode Flow

1. User uploads resume (PDF)
2. The system parses it to create context
3. AI generates personalized questions
4. User records responses
5. AI transcribes and asks up to 2 follow-up questions
6. Final AI feedback is provided

---

### Feature Prioritization

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

### Technical Research
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

### Next Steps
- [ ] Check the MediaStream Recording API doc and learn to set it up properly
- [ ] Check OpenAI Whisper API and its configuration
- [ ] Try different PDF parsing libraries and decide on which performs best for the app's use cases
- [ ] Simulate a short conversation using the Gemini API
- [ ] Set up ElevenLabs API to gauge how difficult it is to incorporate it into the app
- [ ] Re-check how to set up authentication with Supabase
---

## Day 2: Database Design & Pseudocode

### Database Design
For the first version of this app, I had to make a decision between complexity and storage. The part that got me thinking is that: *Do I really need to store the audio files from the users?* My reasoning is that 

1. Saved audio files are not of significant importance because the what matters is that the user can receives the assessment of their performance after a mock interview session and suggestions on how to improve the next time. One might argue that if the user needs to review the audio of themselves later or re-run the analysis. But as someone whose main focus is to practice **thinking out loud in a structure** way, reviewing audio is way less important than having a functional space to do as many practice as possible.
2. Saved audio files cost more storage while the value per storage is not high, unless the key feedback is to use the data to train some models, which is not the case here.

As a result, my final database schema design is shown below, which I believes strike a balance between simplicity and functionality.


### Structure & Pseudocode for Backend & Frontend

*(High-level plan for organizing API routes, React components, etc.)*

### Authentication Setup

- Setup using Supabase/Auth0 or a custom JWT-based solution
- Session flow with refresh tokens (if applicable)

---

## Day 3: Feature: Audio Transcription & PDF Parsing

- Integrate Whisper (or another model) for transcription
- Use `pdfplumber`, `PyMuPDF`, or third-party API for resume parsing
- Normalize parsed content for embedding/context

---

## Day 4: Feature: AI Conversation & Follow-up Questions

- Use OpenAI/Gemma with structured prompts
- Memory chain to store context (e.g., LangChain)
- Rule-based or confidence-threshold triggers for follow-up

---

## Day 5: Feature: Analytics (If Time Permits)

- Track completion, AI ratings, time per question, weak areas
- Visualize via simple dashboard (e.g., Recharts or Chart.js)

---

## Day 6: CI/CD & Deployment

- GitHub Actions for test + lint checks
- Deploy backend (e.g., Vercel, Fly.io, or Render)
- Deploy frontend (e.g., Netlify or Vercel)
- Use `.env` for secrets + environment configs

---

## Day 7: Documentation

- README with:
  - Overview
  - Feature List
  - Installation & Setup
  - API Reference
- Record a Loom demo
