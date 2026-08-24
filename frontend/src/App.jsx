import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { AuthPage } from './pages/AuthPage';
import { DashboardPage } from './pages/DashboardPage';
import { WritingPage } from './pages/WritingPage';
import { SpeakingPage } from './pages/SpeakingPage';
import { CulturePage } from './pages/CulturePage';
import { ProgressPage } from './pages/ProgressPage';
import { ProfilePage } from './pages/ProfilePage';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { useAuth } from './context/AuthContext';

function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-warmbg text-amber-900 space-y-4">
        <div className="text-6xl animate-bounce">👵</div>
        <p className="text-lg font-black tracking-tight">Opening Ammachi's Classroom...</p>
      </div>
    );
  }

  return (
    <Routes>
      {/* Auth Route: Redirect to dashboard if already authenticated */}
      <Route
        path="/auth"
        element={user ? <Navigate to="/" replace /> : <AuthPage />}
      />

      {/* Main App Shell Layout (Protected Routes) */}
      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<DashboardPage />} />
        <Route path="/writing" element={<WritingPage />} />
        <Route path="/speaking" element={<SpeakingPage />} />
        <Route path="/culture" element={<CulturePage />} />
        <Route path="/progress" element={<ProgressPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
