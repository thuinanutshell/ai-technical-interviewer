'use client';

import {
    getAuthToken,
    getInterviewById,
    getQuestionsByInterviewId,
} from '@/lib/api';
import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import ChatBox from '../../../components/ChatBox';
import CodeEditor from '../../../components/CodeEditor';
import QuestionDisplay from '../../../components/QuestionDisplay';

export default function InterviewSessionPage() {
  const rawParams = useParams();
  const router = useRouter();
  const id = typeof rawParams?.id === 'string' ? rawParams.id : String(rawParams?.id);

  const [interview, setInterview] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [interviewCompleted, setInterviewCompleted] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [fetchingFeedback, setFetchingFeedback] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const interviewData = await getInterviewById(id);

        // Default questions array
        let questionData = [];

        // Fetch structured questions only for behavioral
        if (interviewData.interview_type === 'behavioral') {
          questionData = await getQuestionsByInterviewId(id);
        }

        // For coding, treat context as a single question
        if (interviewData.interview_type === 'coding') {
          questionData = [
            {
              id: `${id}-code`, // fake ID
              type: 'coding',
              content: interviewData.context,
              language: 'python', // default, can adjust
            },
          ];
        }

        setInterview(interviewData);
        setQuestions(questionData);
      } catch (err) {
        console.error('Error loading interview or questions:', err);
      } finally {
        setLoading(false);
      }
    }

    if (id) fetchData();
  }, [id]);

  const handleAnswerRecorded = async (isCompleted) => {
    const isLastQuestion = currentQuestionIndex >= questions.length - 1;
    const shouldComplete = isCompleted || isLastQuestion;

    if (shouldComplete) {
      setFetchingFeedback(true);
      try {
        const token = getAuthToken();
        const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/interviews/${id}/feedback`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) throw new Error('Failed to fetch feedback');
        const feedbackData = await res.json();
        setFeedback(feedbackData);
      } catch (err) {
        console.error('Error generating feedback:', err);
      } finally {
        setFetchingFeedback(false);
        setInterviewCompleted(true);
      }
    } else {
      setCurrentQuestionIndex((prev) => prev + 1);
    }
  };

  const currentQuestion = questions[currentQuestionIndex];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading interview...</p>
        </div>
      </div>
    );
  }

  if (interviewCompleted) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <div className="bg-white p-8 rounded-lg shadow-lg max-w-xl w-full space-y-6">
          <h2 className="text-2xl font-bold text-gray-900 text-center">Interview Completed</h2>
          {feedback ? (
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-gray-700">🎯 Overall Feedback</h3>
                <p className="text-gray-600">{feedback.overall_feedback}</p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-700">🎤 Tone Summary</h3>
                <p className="text-gray-600">{feedback.tone_summary}</p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-700">⏱️ Speech Rate</h3>
                <p className="text-gray-600">{feedback.speech_rate}</p>
              </div>
            </div>
          ) : (
            <p className="text-gray-600 text-center">
              Your interview was completed, but feedback couldn't be generated.
            </p>
          )}
          <div className="pt-6 text-center">
            <button
              onClick={() => router.push('/dashboard')}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Return to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <header className="mb-6 flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">{interview?.title || 'Interview Session'}</h2>
        <a href="/dashboard" className="text-blue-600 hover:underline text-sm">
          ← Back to Dashboard
        </a>
      </header>

      {/* Progress Bar */}
      <div className="mb-6 bg-white rounded-lg p-4 shadow-sm">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Progress</span>
          <span className="text-sm text-gray-500">
            {currentQuestionIndex + 1} of {questions.length || 1}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentQuestionIndex + 1) / (questions.length || 1)) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Question Display */}
      {currentQuestion && (
        <QuestionDisplay
          question={currentQuestion}
          index={currentQuestionIndex}
          total={questions.length || 1}
        />
      )}

      {/* Code Editor (only for coding questions) */}
      {currentQuestion?.type === 'coding' && (
        <div className="my-4">
          <CodeEditor language={currentQuestion.language || 'python'} />
        </div>
      )}

      {/* Chat */}
      {currentQuestion?.id && id && (
        <div className="mt-6">
          <ChatBox
            questionId={currentQuestion.id}
            interviewId={id}
            mode={currentQuestion.type}
            onAnswerRecorded={handleAnswerRecorded}
            currentQuestionIndex={currentQuestionIndex}
            totalQuestions={questions.length || 1}
            question={currentQuestion.content} // Pass actual question content for coding mode
          />
        </div>
      )}
    </div>
  );
}
