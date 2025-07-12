'use client';

import { CheckCircle } from 'lucide-react';

const steps = ['Understand', 'Match', 'Plan', 'Implement', 'Review', 'Evaluate'];

export default function UmpireStepper({ currentStep = 0 }) {
  return (
    <div className="flex justify-between px-6 py-3 border-b border-gray-200 bg-white">
      {steps.map((step, idx) => (
        <div key={idx} className="flex-1 flex flex-col items-center">
          <div
            className={`w-6 h-6 flex items-center justify-center rounded-full text-xs font-bold 
              ${idx < currentStep ? 'bg-green-500 text-white' : ''}
              ${idx === currentStep ? 'bg-blue-600 text-white' : ''}
              ${idx > currentStep ? 'bg-gray-200 text-gray-500' : ''}
            `}
          >
            {idx < currentStep ? <CheckCircle size={16} /> : idx + 1}
          </div>
          <span
            className={`text-xs mt-1 text-center ${
              idx === currentStep
                ? 'text-blue-600 font-semibold'
                : idx < currentStep
                ? 'text-gray-500'
                : 'text-gray-400'
            }`}
          >
            {step}
          </span>
        </div>
      ))}
    </div>
  );
}
