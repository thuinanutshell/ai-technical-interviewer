'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import BehavioralModal from '../../components/BehavioralModal';
import CodingModal from '../../components/CodingModal';

export default function DashboardPage() {
  const { user, logout, loading, isAuthenticated } = useAuth();
  const router = useRouter();
  const [showBehavioralModal, setShowBehavioralModal] = useState(false);
  const [showCodingModal, setShowCodingModal] = useState(false);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [loading, isAuthenticated, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">
              AI Technical Interviewer
            </h1>
            <button
              onClick={logout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg p-8">
            <div className="text-center">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Coding Interview Button */}
                <div className="bg-white p-6 rounded-lg shadow">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Coding Interview</h3>
                  <p className="text-gray-600">
                    Manually create and solve technical coding problems using UMPIRE.
                  </p>
                  <button
                    onClick={() => setShowCodingModal(true)}
                    className="mt-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                  >
                    Start Coding Interview
                  </button>
                </div>

                {/* Behavioral Interview Button */}
                <div className="bg-white p-6 rounded-lg shadow">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Behavioral Interview
                  </h3>
                  <p className="text-gray-600">
                    Upload your resume and let AI generate behavioral questions.
                  </p>
                  <button
                    onClick={() => setShowBehavioralModal(true)}
                    className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                  >
                    Start Behavioral Interview
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Modal Section */}
      {showBehavioralModal && (
        <BehavioralModal onClose={() => setShowBehavioralModal(false)} />
      )}
      {showCodingModal && (
        <CodingModal onClose={() => setShowCodingModal(false)} />
      )}
    </div>
  );
}
