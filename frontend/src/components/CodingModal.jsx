'use client';

import { createInterview } from '@/lib/api';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function CodingModal({ onClose }) {
  const [question, setQuestion] = useState('');
  const [language, setLanguage] = useState('python');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async () => {
    if (!question.trim()) {
      alert('Please enter a coding question.');
      return;
    }

    setLoading(true);
    try {
      const interview = await createInterview({
        title: `Coding Interview - ${new Date().toLocaleDateString()}`,
        context: question,
        interview_type: 'coding',
      });

      router.push(`/session/${interview.id}`);
    } catch (err) {
      console.error(err);
      alert('Failed to start coding interview.');
    } finally {
      setLoading(false);
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50 px-4">
      <div className="bg-white p-6 rounded-lg w-full max-w-lg">
        <h2 className="text-xl font-semibold mb-4">Create Coding Interview</h2>

        <label className="block mb-1 font-medium">Problem Description</label>
        <textarea
          rows={4}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full border rounded-md p-2 mb-4 text-sm"
          placeholder="e.g. Implement a function to reverse a linked list..."
        />

        <label className="block mb-1 font-medium">Language</label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="w-full border rounded-md px-2 py-2 text-sm mb-6"
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
        </select>

        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="bg-gray-200 px-4 py-2 rounded-md text-sm"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="bg-green-600 text-white px-4 py-2 rounded-md text-sm disabled:opacity-50"
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Start Interview'}
          </button>
        </div>
      </div>
    </div>
  );
}
