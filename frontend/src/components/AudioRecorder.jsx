'use client';
import { useRef, useState } from 'react';

export default function AudioRecorder({ 
  onRecordingComplete, 
  onError, 
  disabled = false,
  className = "" 
}) {
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const audioChunks = useRef([]);

  const startRecording = async () => {
    try {
      setRecording(true);
      audioChunks.current = []; // Reset chunks
      
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        
        // Clean up stream
        stream.getTracks().forEach(track => track.stop());
        
        // Call the completion handler
        if (onRecordingComplete) {
          onRecordingComplete(audioBlob);
        }
        
        // Reset state
        audioChunks.current = [];
        setMediaRecorder(null);
      };

      recorder.onerror = (event) => {
        console.error('MediaRecorder error:', event.error);
        if (onError) {
          onError('Recording failed. Please try again.');
        }
        setRecording(false);
      };

      recorder.start();
    } catch (err) {
      console.error('Error starting recording:', err);
      setRecording(false);
      
      let errorMessage = 'Microphone access denied. Please allow microphone access and try again.';
      if (err.name === 'NotFoundError') {
        errorMessage = 'No microphone found. Please connect a microphone and try again.';
      } else if (err.name === 'NotAllowedError') {
        errorMessage = 'Microphone access denied. Please allow microphone access in your browser settings.';
      }
      
      if (onError) {
        onError(errorMessage);
      }
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }
    setRecording(false);
  };

  return (
    <div className={`flex justify-center ${className}`}>
      {recording ? (
        <button
          onClick={stopRecording}
          className="flex items-center space-x-2 bg-red-600 text-white px-6 py-3 rounded-lg text-sm font-medium hover:bg-red-700 transition-colors"
          disabled={disabled}
        >
          <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
          <span>Stop Recording</span>
        </button>
      ) : (
        <button
          onClick={startRecording}
          disabled={disabled}
          className="flex items-center space-x-2 bg-green-600 text-white px-6 py-3 rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path 
              fillRule="evenodd" 
              d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 715 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" 
              clipRule="evenodd" 
            />
          </svg>
          <span>Record Answer</span>
        </button>
      )}
    </div>
  );
}