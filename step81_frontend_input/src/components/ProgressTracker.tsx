import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { Activity, CheckCircle2, AlertTriangle, Layers } from 'lucide-react';

export const ProgressTracker: React.FC = () => {
  const { isActive, progress, history } = useSelector((state: RootState) => state.progress);
  const isSubmitting = useSelector((state: RootState) => state.session.isSubmitting);

  if (!isActive && !isSubmitting && progress.percent === 0) {
    return null;
  }

  const isCompleted = progress.percent >= 100;
  const isError = progress.stepId === -1;

  const getStepColor = () => {
    if (isError) return '#ef4444';
    if (isCompleted) return '#10b981';
    return '#3b82f6';
  };

  return (
    <div style={{
      background: '#ffffff',
      borderRadius: '16px',
      border: `1px solid ${isCompleted ? '#a7f3d0' : isError ? '#fecaca' : '#bfdbfe'}`,
      padding: '24px',
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.05)',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {isCompleted ? (
            <CheckCircle2 size={22} color="#10b981" />
          ) : isError ? (
            <AlertTriangle size={22} color="#ef4444" />
          ) : (
            <Activity size={22} color="#3b82f6" className="animate-spin" />
          )}
          <div>
            <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#0f172a', margin: 0 }}>
              {progress.stepName || 'Processing ML Pipeline'}
            </h3>
            <p style={{ fontSize: '12px', color: '#64748b', margin: '2px 0 0 0' }}>
              {progress.details || 'Evaluating catalog against target market preferences...'}
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{
            fontSize: '11px',
            fontWeight: 700,
            background: isCompleted ? '#d1fae5' : isError ? '#fee2e2' : '#dbeafe',
            color: isCompleted ? '#065f46' : isError ? '#991b1b' : '#1e40af',
            padding: '3px 10px',
            borderRadius: '999px'
          }}>
            {isCompleted ? 'Finished' : isError ? 'Error' : `Step ${progress.stepId} of 5`}
          </span>
          <span style={{ fontSize: '18px', fontWeight: 800, color: getStepColor(), fontFamily: 'JetBrains Mono, monospace' }}>
            {progress.percent}%
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div style={{
        width: '100%',
        height: '10px',
        background: '#f1f5f9',
        borderRadius: '999px',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${Math.min(100, Math.max(0, progress.percent))}%`,
          height: '100%',
          background: `linear-gradient(90deg, #3b82f6 0%, ${getStepColor()} 100%)`,
          borderRadius: '999px',
          transition: 'width 0.4s ease'
        }} />
      </div>

      {/* Step History Chips */}
      {history.length > 0 && (
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '4px' }}>
          {history.map((h, idx) => (
            <div
              key={idx}
              style={{
                fontSize: '11px',
                background: '#f8fafc',
                border: '1px solid #e2e8f0',
                borderRadius: '6px',
                padding: '4px 8px',
                color: '#475569',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <Layers size={12} color="#94a3b8" />
              <span>{h.stepName}</span>
              <strong style={{ color: '#0f172a' }}>{h.percent}%</strong>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
