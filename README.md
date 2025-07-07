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

Interview prep is one of the most important parts of the job application process. Preparing alone can feel isolating, and finding the right accountability partner is often challenging.

**Ava** is a mock AI interviewer designed to simulate real interviews and provide users with a structured environment to think out loud and receive instant feedback.

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

![image](https://github.com/user-attachments/assets/55ecdd07-6a17-4d0f-8e00-2ad9c7e84639)

##### Coding Mode Flow

1. User selects a topic (e.g., Trees, DP)
2. Random question is displayed
3. User starts timer
4. User records answer for each UMPIRE step
5. System transcribes answer and gives AI feedback
6. Final feedback is provided based on performance

---

#### Behavioral Mode

![image](https://github.com/user-attachments/assets/88f939e8-c5e1-463a-95f5-b1411b6f97ad)

##### Behavioral Mode Flow

1. User uploads resume (PDF)
2. System parses it to create context
3. AI generates personalized questions
4. User records responses
5. AI transcribes and asks up to 2 follow-up questions
6. Final AI feedback is provided

---

### Feature Prioritization

| Feature                     | Priority | Reason |
|----------------------------|-------------|--------|
| Audio Recording & Transcription | 🔥🔥🔥 | Core to simulating interviews |
| PDF Parsing                | 🔥🔥🔥 | Enables resume-based behavioral questions |
| AI Conversation            | 🔥🔥🔥 | Enables dynamic mock interview |
| Follow-up Questions        | 🔥🔥   | Adds realism and depth |
| Analytics                  | 🔥🔥   | Tracks user progress |
| Timer                      | 🔥     | Simulates real interview pressure |
| Authentication             | 🔥     | Required for account setup |

---

## Day 2: Database Design & Pseudocode

### Database Design

*(To be added: ER diagrams, schemas, etc.)*

### Structure & Pseudocode for Backend & Frontend

*(High-level plan for organizing API routes, React components, etc.)*

### Authentication Setup

- Setup using Firebase/Auth0 or custom JWT-based solution
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
