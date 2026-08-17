import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { Sparkles, Copy, Check, Lock, Zap } from 'lucide-react';

export const Header: React.FC = () => {
  const userSessionGUID = useSelector((state: RootState) => state.session.userSessionGUID);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(userSessionGUID);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <header style={{
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      padding: '16px 28px',
      borderBottom: '2px solid #fef3c7',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: '16px',
      boxShadow: '0 4px 20px -2px rgba(245, 158, 11, 0.08)'
    }}>
      {/* Brand & Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          width: '44px',
          height: '44px',
          borderRadius: '14px',
          background: 'linear-gradient(135deg, #f59e0b 0%, #ea580c 50%, #e11d48 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 14px rgba(245, 158, 11, 0.4)',
          transform: 'rotate(-2deg)'
        }}>
          <Sparkles size={24} color="#ffffff" />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 style={{ fontSize: '18px', fontWeight: 900, letterSpacing: '-0.03em', margin: 0, color: '#0f172a' }}>
              CV26 DSS Marketing Intelligence
            </h1>
            <span style={{
              background: 'linear-gradient(135deg, #fef08a 0%, #fde047 100%)',
              color: '#854d0e',
              border: '1px solid #facc15',
              fontSize: '11px',
              fontWeight: 800,
              padding: '3px 8px',
              borderRadius: '999px',
              boxShadow: '0 2px 6px rgba(250, 204, 21, 0.25)',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              <Zap size={11} fill="#854d0e" />
              CAPSTONE COLOR EDITION
            </span>
          </div>
          <p style={{ fontSize: '12.5px', color: '#64748b', margin: '2px 0 0 0', fontWeight: 500 }}>
            🎨 Multi-Palette Style DNA &bull; Purchase Manager Decision Support System
          </p>
        </div>
      </div>

      {/* Persistent Immutable userSessionGUID Badge (Read-Only) */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
        <div style={{
          background: '#fffbeb',
          border: '1.5px solid #fde68a',
          borderRadius: '12px',
          padding: '6px 12px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          boxShadow: '0 2px 8px rgba(245, 158, 11, 0.1)'
        }}>
          <span title="Immutable userSessionGUID (constant)">
            <Lock size={13} color="#d97706" />
          </span>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '9px', color: '#b45309', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              userSessionGUID (Constant)
            </span>
            <code style={{ fontSize: '12px', color: '#92400e', fontFamily: 'JetBrains Mono, monospace', fontWeight: 700 }}>
              {userSessionGUID}
            </code>
          </div>
          <button
            onClick={handleCopy}
            title="Copy constant userSessionGUID"
            style={{
              background: '#ffffff',
              border: '1px solid #fcd34d',
              color: '#b45309',
              padding: '6px 8px',
              borderRadius: '8px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
              transition: 'all 0.15s ease',
              fontSize: '11px',
              fontWeight: 700
            }}
          >
            {copied ? (
              <>
                <Check size={12} color="#16a34a" />
                <span style={{ color: '#16a34a' }}>Copied</span>
              </>
            ) : (
              <>
                <Copy size={12} />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>
      </div>
    </header>
  );
};
