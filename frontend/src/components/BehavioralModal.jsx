'use client';

import {
    createInterview,
    generateBehavioralQuestions,
    uploadResume,
} from '@/lib/api';
import { Loader2, UploadCloud } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function BehavioralModal({ onClose }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [numQuestions, setNumQuestions] = useState(5);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async () => {
    if (!resumeFile) {
      alert('Please upload your resume.');
      return;
    }

    setLoading(true);

    try {
      const resume = await uploadResume(resumeFile);

      const interview = await createInterview({
        title: `Behavioral Interview - ${new Date().toLocaleDateString()}`,
        context: `Parsed Resume:\n${resume.parsed_data}`,
        interview_type: 'behavioral',
      });

      await generateBehavioralQuestions({
        resume_id: resume.id,
        interview_id: interview.id,
        num_questions: numQuestions,
      });

      router.push(`/session/${interview.id}`);
    } catch (error) {
      console.error(error);
      alert('Failed to start the interview. Please try again.');
    } finally {
      setLoading(false);
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50 px-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-lg p-6 animate-fade-in">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Start Behavioral Interview</h2>

        {/* File Upload */}
        <label className="block text-sm font-medium text-gray-700 mb-1">Upload Resume (PDF)</label>
        <div className="relative mb-4">
          <input
            id="resume"
            type="file"
            accept="application/pdf"
            onChange={(e) => setResumeFile(e.target.files[0])}
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100"
          />
          {resumeFile && (
            <p className="text-xs text-green-600 mt-1">✅ {resumeFile.name}</p>
          )}
        </div>

        {/* Number of Questions */}
        <label className="block text-sm font-medium text-gray-700 mb-1">Number of Questions</label>
        <select
          value={numQuestions}
          onChange={(e) => setNumQuestions(Number(e.target.value))}
          className="mb-6 w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {[1, 3, 5, 7].map((num) => (
            <option key={num} value={num}>
              {num}
            </option>
          ))}
        </select>

        {/* Action Buttons */}
        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            disabled={loading}
            className="px-4 py-2 text-sm rounded-md text-gray-700 border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={loading || !resumeFile}
            className="px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Starting...
              </>
            ) : (
              <>
                <UploadCloud className="w-4 h-4" />
                Start Interview
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
