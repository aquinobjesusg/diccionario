'use client'
import { useState } from "react";
import { AuthScreen } from "./components/AuthScreen";
import { Dashboard } from "./components/Dashboard";

import { Footer } from "./components/Footer";

export default function Home() {
  const [authed, setAuthed] = useState(false);
  return (
        <div className="min-h-screen bg-gradient-to-b from-sky-300 via-cyan-300 to-emerald-300 text-slate-800">
          {authed ? (
            <Dashboard onLogout={() => setAuthed(false)} />
          ) : (
            <>
              <AuthScreen onLogin={() => setAuthed(true)} />
           
              <Footer />
            </>
          )}
        </div>
  );
}
