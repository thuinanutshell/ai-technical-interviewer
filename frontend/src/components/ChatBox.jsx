'use client';

import { getAuthToken } from '@/lib/api';
import { useEffect, useRef, useState } from 'react';
import AudioRecorder from './AudioRecorder';

const UMPIRE_STEPS = [
  'Understand',
  'Match',
  'Plan',
  'Implement',
  'Review',
  'Evaluate',
];

export default function ChatBox({
  interviewId,
  questionId,
  mode,
  onAnswerRecorded,
  currentQuestionIndex,
  totalQuestions,
}) {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [hasAnswered, setHasAnswered] = useState(false);
  const [umpireStep, setUmpireStep] = useState(0);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    setHasAnswered(false);
    setMessages([]);
    setError('');
    setUmpireStep(0);
  }, [questionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initial welcome message
  useEffect(() => {
    if (messages.length === 0) {
      let welcomeMessage =
        mode === 'coding'
          ? 'Let’s begin the coding interview. Start by sharing how you understand the problem.'
          : 'Welcome to your behavioral interview! Please record your answer to the question displayed above.';
      setMessages([{ role: 'ai', content: welcomeMessage }]);
    }
  }, [mode, messages.length]);

  const handleRecordingComplete = async (audioBlob) => {
    setIsLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');

      const token = getAuthToken();
      const route =
        mode === 'coding'
          ? `/interviews/${interviewId}/chat/coding`
          : `/interviews/${interviewId}/chat`;

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}${route}`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      const userMsg = { role: 'user', content: data[0]?.content || 'Audio recorded' };
      const aiMsg = { role: 'ai', content: data[1]?.content || 'Thank you for your response.' };

      setMessages((prev) => [...prev, userMsg, aiMsg]);
      setHasAnswered(true);

      // Handle progression
      if (mode === 'coding') {
        if (umpireStep < UMPIRE_STEPS.length - 1) {
          setTimeout(() => {
            setUmpireStep((prev) => prev + 1);
            setHasAnswered(false);
          }, 2000);
        } else {
          setTimeout(() => {
            onAnswerRecorded?.(true); // completed
          }, 2000);
        }
      } else {
        if (
          aiMsg.content.includes("You've completed the interview") ||
          aiMsg.content.includes('generate your feedback')
        ) {
          setTimeout(() => {
            onAnswerRecorded?.(true);
          }, 2000);
        } else {
          setTimeout(() => {
            onAnswerRecorded?.(false);
          }, 2000);
        }
      }
    } catch (err) {
      console.error('Error processing recording:', err);
      setError('Failed to process recording. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRecordingError = (errorMessage) => {
    setError(errorMessage);
  };

  const handleNextQuestion = () => {
    onAnswerRecorded?.(false);
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
      {/* Header */}
      <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-sm font-medium text-gray-900">Interview Assistant</h3>
            <p className="text-xs text-gray-500">
              {mode === 'coding'
                ? `UMPIRE Stage: ${UMPIRE_STEPS[umpireStep]}`
                : 'Record your answer to continue'}
            </p>
          </div>
          <div className="text-xs text-gray-500">
            Question {currentQuestionIndex + 1} of {totalQuestions}
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="h-80 overflow-y-auto p-4 space-y-3 bg-gray-50">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg text-sm ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-900 border border-gray-200'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg px-4 py-2 text-sm text-gray-500">
              <div className="flex items-center space-x-2">
                <div className="animate-pulse">●</div>
                <span>Processing your response...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error */}
      {error && (
        <div className="px-4 py-2 bg-red-50 border-t border-red-200">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Controls */}
      <div className="p-4 bg-white border-t border-gray-200">
        <div className="flex justify-center space-x-3">
          <AudioRecorder
            onRecordingComplete={handleRecordingComplete}
            onError={handleRecordingError}
            disabled={isLoading || hasAnswered}
          />

          {hasAnswered &&
            !isLoading &&
            mode === 'behavioral' &&
            currentQuestionIndex < totalQuestions - 1 && (
              <button
                onClick={handleNextQuestion}
                className="flex items-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
              >
                <span>Next Question</span>
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            )}
        </div>
      </div>
    </div>
  );
}
