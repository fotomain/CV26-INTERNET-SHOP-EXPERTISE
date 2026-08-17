import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { Activity, CheckCircle, AlertTriangle, Layers } from 'lucide-react';

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
      borderRadius: '16px',
      border: `1px solid ${isCompleted ? '#bbf7d0' : isError ? '#fecaca' : 'rgba(0, 0, 0, 0.08)'}`,
      padding: '20px 24px',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.02), 0 6px 24px -4px rgba(0, 0, 0, 0.04)',
      display: 'flex',
      flexDirection: 'column',
      gap: '14px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {isCompleted ? (
            <CheckCircle size={20} color="#16a34a" />
          ) : isError ? (
            <AlertTriangle size={20} color="#dc2626" />
          ) : (
            <div style={{
              width: '18px',
              height: '18px',
              border: '2px solid #09090b',
              borderTopColor: 'transparent',
              borderRadius: '50%',
              animation: 'spin 0.8s linear infinite'
            }} />
          )}
          <div>
            <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#09090b', letterSpacing: '-0.01em', margin: 0 }}>
              {progress.stepName || 'Processing Pipeline'}
            </h3>
            <p style={{ fontSize: '12px', color: '#71717a', margin: '2px 0 0 0' }}>
              {progress.details || 'Calculating color distributions and scoring catalog SKUs...'}
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{
            fontSize: '11px',
            fontWeight: 700,
            background: isCompleted ? '#f0fdf4' : isError ? '#fef2f2' : '#f4f4f5',
            color: isCompleted ? '#166534' : isError ? '#991b1b' : '#18181b',
            border: `1px solid ${isCompleted ? '#bbf7d0' : isError ? '#fecaca' : '#e4e4e7'}`,
            padding: '2px 8px',
            borderRadius: '6px'
          }}>
            {isCompleted ? 'Finished' : isError ? 'Error' : `Step ${progress.stepId} of 5`}
          </span>
          <span style={{ fontSize: '16px', fontWeight: 800, color: '#09090b', fontFamily: 'JetBrains Mono, monospace' }}>
            {progress.percent}%
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div style={{
        width: '100%',
        height: '6px',
        background: '#f4f4f5',
        borderRadius: '999px',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${Math.min(100, Math.max(0, progress.percent))}%`,
          height: '100%',
          background: isCompleted ? '#16a34a' : isError ? '#dc2626' : '#09090b',
          borderRadius: '999px',
          transition: 'width 0.3s ease'
        }} />
      </div>

      {/* Step History Chips */}
      {history.length > 0 && (
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '2px' }}>
          {history.map((h, idx) => (
            <div
              key={idx}
              style={{
                fontSize: '11px',
                background: '#fafafa',
                border: '1px solid #e4e4e7',
                borderRadius: '6px',
                padding: '3px 7px',
                color: '#52525b',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
            >
              <Layers size={11} color="#a1a1aa" />
              <span>{h.stepName}</span>
              <strong style={{ color: '#09090b' }}>{h.percent}%</strong>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
