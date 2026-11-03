'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);
  const router = useRouter();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // We will set a cookie and reload
    if (password === 'admin2026') {
      document.cookie = "crm_auth=true; path=/; max-age=31536000"; // 1 year expiry
      window.location.href = '/';
    } else {
      setError(true);
      setTimeout(() => setError(false), 2000);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-main)', position: 'absolute', top: 0, left: 0, zIndex: 9999 }}>
      <div className="glass-panel" style={{ width: '400px', textAlign: 'center', padding: '40px' }}>
        <h1 style={{ fontSize: '24px', color: '#fff', marginBottom: '8px' }}>
          Altus<span style={{ color: 'var(--gold)' }}> Real Estate</span>
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginBottom: '32px' }}>
          Acceso Restringido. Introduce tu contraseña maestra.
        </p>

        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <input 
            type="password" 
            placeholder="Contraseña..."
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              background: 'rgba(0,0,0,0.2)', border: error ? '1px solid #ef4444' : '1px solid var(--border-color)', 
              color: '#fff', padding: '12px 16px', borderRadius: '8px', outline: 'none',
              fontFamily: 'var(--font-inter)'
            }}
            autoFocus
          />
          <button type="submit" className="btn-primary" style={{ padding: '12px', fontSize: '15px' }}>
            Desbloquear CRM
          </button>
        </form>
      </div>
    </div>
  );
}
