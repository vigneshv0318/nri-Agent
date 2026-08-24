import React from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Globe, Award, Star, Flame, LogOut, ArrowLeft, Volume2, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { AmmachiMascot } from '../components/common/AmmachiMascot';

export const ProfilePage = () => {
  const { user, logout } = useAuth();
  const { currentLanguage, setLanguage, languages, activeLangMeta } = useLanguage();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  return (
    <div className="space-y-6 max-w-2xl mx-auto animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-amber-200/80 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-black text-amber-700 uppercase tracking-wider mb-1">
            <Link to="/" className="hover:underline flex items-center gap-1">
              <ArrowLeft className="w-3.5 h-3.5" /> Dashboard
            </Link>
            <span>•</span>
            <span>Student Profile</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-amber-950 tracking-tight">
            Child Profile & Settings
          </h1>
        </div>
      </div>

      {/* Profile Card */}
      <div className="bg-white border-2 border-amber-200 rounded-3xl p-6 shadow-sm flex flex-col sm:flex-row items-center gap-6">
        <AmmachiMascot size="lg" className="ring-4 ring-amber-200" />
        <div className="text-center sm:text-left space-y-1">
          <h2 className="text-2xl font-black text-amber-950">
            {user?.username || 'Student'}
          </h2>
          <p className="text-xs font-bold text-amber-800 uppercase tracking-wider">
            Active Native Language: <strong>{currentLanguage} ({activeLangMeta.nativeName})</strong>
          </p>
          <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2 pt-2">
            <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-extrabold flex items-center gap-1">
              <Star className="w-3.5 h-3.5 text-amber-500 fill-amber-400" />
              {user?.points || 0} Points
            </span>
            <span className="px-3 py-1 rounded-full bg-orange-100 text-orange-900 text-xs font-extrabold flex items-center gap-1">
              <Flame className="w-3.5 h-3.5 text-orange-500 fill-orange-400" />
              {user?.streak || 1} Day Streak
            </span>
          </div>
        </div>
      </div>

      {/* Language Preference Setting */}
      <div className="bg-white border-2 border-amber-200 rounded-3xl p-6 shadow-sm space-y-4">
        <h3 className="text-lg font-black text-amber-950 flex items-center gap-2">
          <Globe className="w-5 h-5 text-amber-600" />
          <span>Switch Native Language</span>
        </h3>
        <p className="text-xs font-medium text-stone-600">
          Choose which native Indian language Ammachi will teach you across all writing, speaking, and cultural modules.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {languages.map((lang) => (
            <button
              key={lang.id}
              onClick={() => setLanguage(lang.id)}
              className={`p-4 rounded-2xl border-2 text-left transition-all select-none ${
                currentLanguage === lang.id
                  ? 'bg-amber-400 border-amber-600 shadow-md text-amber-950 font-black scale-105'
                  : 'bg-amber-50/50 border-amber-200 hover:border-amber-400 text-stone-700 font-bold'
              }`}
            >
              <span className="text-base block">{lang.name}</span>
              <span className="text-xl block mt-0.5">{lang.nativeName}</span>
              <span className="text-[10px] opacity-80 block mt-1">{lang.persona}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Security & Logout */}
      <div className="bg-white border-2 border-stone-200 rounded-3xl p-6 shadow-sm flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-stone-100 flex items-center justify-center text-stone-600">
            <ShieldCheck className="w-5 h-5 text-emerald-600" />
          </div>
          <div>
            <span className="text-sm font-bold text-stone-900 block">Session Security</span>
            <span className="text-xs text-stone-500">JWT Token securely stored locally</span>
          </div>
        </div>

        <button
          onClick={handleLogout}
          type="button"
          className="btn-outline border-red-200 text-red-700 hover:bg-red-50 hover:border-red-400 py-2.5 px-4 text-xs font-bold"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign Out</span>
        </button>
      </div>
    </div>
  );
};
