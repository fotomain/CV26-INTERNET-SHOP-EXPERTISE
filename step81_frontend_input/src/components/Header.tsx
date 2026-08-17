import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { regenerateGUID } from '../store/slices/sessionSlice';
import { Sparkles, RefreshCw, Copy, Check, Terminal, ExternalLink } from 'lucide-react';

export const Header: React.FC = () => {
  const dispatch = useDispatch();
  const userSessionGUID = useSelector((state: RootState) => state.session.userSessionGUID);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(userSessionGUID);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <header style={{
      background: 'rgba(255, 255, 255, 0.92)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      color: '#09090b',
      padding: '14px 24px',
      borderBottom: '1px solid rgba(0, 0, 0, 0.07)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: '16px'
    }}>
      {/* Brand & Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          width: '38px',
          height: '38px',
          borderRadius: '10px',
          background: '#09090b',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.12)'
        }}>
          <Sparkles size={20} color="#fbbf24" />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 style={{ fontSize: '16px', fontWeight: 800, letterSpacing: '-0.03em', margin: 0, color: '#09090b' }}>
              CV26 DSS Marketing Intelligence
            </h1>
            <span style={{
              background: '#f4f4f5',
              color: '#18181b',
              border: '1px solid #e4e4e7',
              fontSize: '11px',
              fontWeight: 700,
              padding: '2px 7px',
              borderRadius: '6px',
              letterSpacing: '-0.01em'
            }}>
              Tamagui Light
            </span>
          </div>
          <p style={{ fontSize: '12px', color: '#71717a', margin: '2px 0 0 0' }}>
            Multi-Palette Style DNA &bull; Candidate Catalog Matching
          </p>
        </div>
      </div>

      {/* Persistent userSessionGUID Badge */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
        <div style={{
          background: '#ffffff',
          border: '1px solid #e4e4e7',
          borderRadius: '10px',
          padding: '5px 10px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          boxShadow: '0 1px 2px rgba(0, 0, 0, 0.03)'
        }}>
          <Terminal size={14} color="#71717a" />
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '9px', color: '#a1a1aa', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              userSessionGUID
            </span>
            <code style={{ fontSize: '11px', color: '#09090b', fontFamily: 'JetBrains Mono, monospace', fontWeight: 600 }}>
              {userSessionGUID}
            </code>
          </div>
          <button
            onClick={handleCopy}
            title="Copy userSessionGUID"
            style={{
              background: '#f4f4f5',
              border: '1px solid #e4e4e7',
              color: '#3f3f46',
              padding: '5px',
              borderRadius: '6px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'background 0.15s ease'
            }}
          >
            {copied ? <Check size={13} color="#16a34a" /> : <Copy size={13} />}
          </button>
          <button
            onClick={() => dispatch(regenerateGUID())}
            title="Regenerate userSessionGUID"
            style={{
              background: '#f4f4f5',
              border: '1px solid #e4e4e7',
              color: '#3f3f46',
              padding: '5px',
              borderRadius: '6px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'background 0.15s ease'
            }}
          >
            <RefreshCw size={13} />
          </button>
        </div>
      </div>
    </header>
  );
};
