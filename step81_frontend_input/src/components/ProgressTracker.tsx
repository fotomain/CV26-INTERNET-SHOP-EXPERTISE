import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { Activity, CheckCircle, AlertTriangle, Layers, Flame, Sparkles } from 'lucide-react';

export const ProgressTracker: React.FC = () => {
  const { isActive, progress, history } = useSelector((state: RootState) => state.progress);
  const isSubmitting = useSelector((state: RootState) => state.session.isSubmitting);

  if (!isActive && !isSubmitting && progress.percent === 0) {
    return null;
  }

  const isCompleted = progress.percent >= 100;
  const isError = progress.stepId === -1;

  return (
    <div style={{
      background: '#ffffff',
      borderRadius: '20px',
      border: `2px solid ${isCompleted ? '#86efac' : isError ? '#fca5a5' : '#fed7aa'}`,
      padding: '24px',
      boxShadow: '0 8px 24px -4px rgba(0, 0, 0, 0.06)',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      position: 'relative',
      overflow: 'hidden'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {isCompleted ? (
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: '#dcfce7',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 2px 8px rgba(22, 163, 74, 0.2)'
            }}>
              <CheckCircle size={22} color="#16a34a" />
            </div>
          ) : isError ? (
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: '#fee2e2',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <AlertTriangle size={22} color="#dc2626" />
            </div>
          ) : (
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #fef08a 0%, #fde047 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 2px 8px rgba(234, 179, 8, 0.3)'
            }}>
              <Flame size={20} color="#b45309" />
            </div>
          )}
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em', margin: 0 }}>
              {progress.stepName || 'Processing ML Pipeline'}
            </h3>
            <p style={{ fontSize: '12.5px', color: '#64748b', margin: '2px 0 0 0' }}>
              {progress.details || 'Evaluating catalog SKUs against target demographic styles...'}
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{
            fontSize: '11.5px',
            fontWeight: 800,
            background: isCompleted ? 'linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%)' : isError ? '#fee2e2' : 'linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)',
            color: isCompleted ? '#166534' : isError ? '#991b1b' : '#c2410c',
            border: `1.5px solid ${isCompleted ? '#86efac' : isError ? '#fca5a5' : '#fed7aa'}`,
            padding: '3px 10px',
            borderRadius: '999px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
          }}>
            {isCompleted ? 'Finished' : isError ? 'Error' : `Step ${progress.stepId} of 5`}
          </span>
          <span style={{
            fontSize: '20px',
            fontWeight: 900,
            color: isCompleted ? '#16a34a' : isError ? '#dc2626' : '#ea580c',
            fontFamily: 'JetBrains Mono, monospace'
          }}>
            {progress.percent}%
          </span>
        </div>
      </div>

      {/* Rainbow / Gradient Animated Progress Bar */}
      <div style={{
        width: '100%',
        height: '10px',
        background: '#f1f5f9',
        borderRadius: '999px',
        overflow: 'hidden',
        boxShadow: 'inset 0 1px 2px rgba(0,0,0,0.05)'
      }}>
        <div style={{
          width: `${Math.min(100, Math.max(0, progress.percent))}%`,
          height: '100%',
          background: isCompleted
            ? 'linear-gradient(90deg, #10b981 0%, #059669 100%)'
            : isError
            ? '#ef4444'
            : 'linear-gradient(90deg, #f59e0b 0%, #ea580c 35%, #e11d48 70%, #10b981 100%)',
          borderRadius: '999px',
          transition: 'width 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
          boxShadow: '0 2px 6px rgba(245, 158, 11, 0.4)'
        }} />
      </div>

      {/* Step History Chips */}
      {history.length > 0 && (
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '2px' }}>
          {history.map((h, idx) => (
            <div
              key={idx}
              style={{
                fontSize: '11px',
                background: '#fafafa',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                padding: '4px 9px',
                color: '#475569',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                boxShadow: '0 1px 2px rgba(0,0,0,0.03)'
              }}
            >
              <Sparkles size={11} color="#f59e0b" />
              <span>{h.stepName}</span>
              <strong style={{ color: '#0f172a' }}>{h.percent}%</strong>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
