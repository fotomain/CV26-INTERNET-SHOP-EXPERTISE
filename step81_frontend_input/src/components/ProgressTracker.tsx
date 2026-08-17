import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { Activity, CheckCircle, AlertTriangle, Layers, Flame, Sparkles, Target, Zap, ShieldCheck } from 'lucide-react';

const MISSIONS = [
  { id: 1, name: 'M1: Product Ingestion & CNN', tag: 'Classification', color: '#0284c7', bg: '#f0f9ff', border: '#bae6fd' },
  { id: 2, name: 'M2: Quality Audit & Filter', tag: 'Quality Check', color: '#16a34a', bg: '#f0fdf4', border: '#bbf7d0' },
  { id: 3, name: 'M3: 4-Color K-Means Palette', tag: 'Fabric Colors', color: '#ca8a04', bg: '#fefce8', border: '#fef08a' },
  { id: 4, name: 'M4: Style DNA & 3 Palettes', tag: 'Demographics', color: '#9333ea', bg: '#faf5ff', border: '#e9d5ff' },
  { id: 5, name: 'M5: DSS Decision Engine', tag: 'Compatibility', color: '#e11d48', bg: '#fff1f2', border: '#fecdd3' },
];

export const ProgressTracker: React.FC = () => {
  const { isActive, progress, history } = useSelector((state: RootState) => state.progress);
  const isSubmitting = useSelector((state: RootState) => state.session.isSubmitting);
  const { hasResults } = useSelector((state: RootState) => state.result);

  const [maxMissionsStep, setMaxMissionsStep] = React.useState<number>(0);

  // Reset max step when a completely new execution starts
  React.useEffect(() => {
    if (!isActive && !isSubmitting && progress.percent === 0 && !hasResults) {
      setMaxMissionsStep(0);
    }
  }, [isActive, isSubmitting, progress.percent, hasResults]);

  // Strictly non-decreasing step tracker (never decreases / no back values)
  React.useEffect(() => {
    if (progress.stepId > 0) {
      setMaxMissionsStep((prev) => Math.max(prev, progress.stepId));
    }
    if (progress.percent >= 100 || hasResults) {
      setMaxMissionsStep(5);
    }
  }, [progress.stepId, progress.percent, hasResults]);

  if (!isActive && !isSubmitting && progress.percent === 0 && !hasResults) {
    return null;
  }

  const isCompleted = progress.percent >= 100 || hasResults || maxMissionsStep >= 5;
  const isError = progress.stepId === -1;

  // Simple, direct function of step number: step * 20% (0%, 20%, 40%, 60%, 80%, 100%)
  const effectiveStep = isCompleted ? 5 : isError ? Math.max(0, maxMissionsStep) : Math.max(0, Math.min(5, maxMissionsStep));
  const completedMissionsCount = effectiveStep;
  const totalMissionsPercent = Math.min(100, Math.max(0, effectiveStep * 20));

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      width: '100%'
    }}>
      {/* ------------------------------------------------------------- */}
      {/* PROGRESSOR 1: Total % of All Missions Completed               */}
      {/* ------------------------------------------------------------- */}
      <div style={{
        background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f0fdf4 100%)',
        borderRadius: '20px',
        border: `2px solid ${isCompleted ? '#86efac' : isError ? '#fca5a5' : '#fed7aa'}`,
        padding: '24px',
        boxShadow: '0 8px 28px -4px rgba(0, 0, 0, 0.06)',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Top Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '12px',
              background: isCompleted ? 'linear-gradient(135deg, #dcfce7 0%, #86efac 100%)' : 'linear-gradient(135deg, #fed7aa 0%, #fb923c 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 3px 10px rgba(0, 0, 0, 0.08)'
            }}>
              <Target size={22} color={isCompleted ? '#166534' : '#7c2d12'} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h3 style={{ fontSize: '17px', fontWeight: 900, color: '#0f172a', letterSpacing: '-0.02em', margin: 0 }}>
                  Total Missions Completed
                </h3>
                <span style={{
                  background: isCompleted ? '#dcfce7' : '#fff7ed',
                  color: isCompleted ? '#15803d' : '#ea580c',
                  border: `1px solid ${isCompleted ? '#86efac' : '#fdba74'}`,
                  fontSize: '11px',
                  fontWeight: 800,
                  padding: '2px 8px',
                  borderRadius: '999px',
                  textTransform: 'uppercase'
                }}>
                  {completedMissionsCount} of 5 Missions
                </span>
              </div>
              <p style={{ fontSize: '12.5px', color: '#64748b', margin: '3px 0 0 0' }}>
                Overall completion rate across Missions 1–5 (Ingestion, QA, K-Means, Style DNA, DSS Match).
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
            <span style={{
              fontSize: '32px',
              fontWeight: 900,
              color: isCompleted ? '#16a34a' : isError ? '#dc2626' : '#ea580c',
              fontFamily: 'JetBrains Mono, monospace',
              letterSpacing: '-0.03em'
            }}>
              {totalMissionsPercent}%
            </span>
            <span style={{ fontSize: '13px', color: '#64748b', fontWeight: 700 }}>
              total completed
            </span>
          </div>
        </div>

        {/* Total Missions Multi-Segment Progress Bar */}
        <div style={{
          width: '100%',
          height: '14px',
          background: '#e2e8f0',
          borderRadius: '999px',
          overflow: 'hidden',
          boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.1)',
          display: 'flex',
          padding: '2px'
        }}>
          <div style={{
            width: `${totalMissionsPercent}%`,
            height: '100%',
            background: isCompleted
              ? 'linear-gradient(90deg, #10b981 0%, #059669 100%)'
              : isError
              ? '#ef4444'
              : 'linear-gradient(90deg, #3b82f6 0%, #10b981 25%, #f59e0b 50%, #8b5cf6 75%, #ec4899 100%)',
            borderRadius: '999px',
            transition: 'width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
          }} />
        </div>

        {/* 5 Missions Status Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '10px',
          marginTop: '4px'
        }}>
          {MISSIONS.map((m) => {
            const isMissionDone = isCompleted || (effectiveStep >= m.id);
            const isMissionActive = !isCompleted && (effectiveStep === m.id - 1 && progress.stepId === m.id);
            const isMissionPending = !isCompleted && !isMissionDone && !isMissionActive;

            return (
              <div
                key={m.id}
                style={{
                  background: isMissionDone ? m.bg : isMissionActive ? '#ffffff' : '#f8fafc',
                  border: `1.5px solid ${isMissionDone ? m.border : isMissionActive ? m.color : '#e2e8f0'}`,
                  borderRadius: '12px',
                  padding: '10px 12px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px',
                  boxShadow: isMissionActive ? `0 4px 12px -2px ${m.color}33` : '0 1px 3px rgba(0,0,0,0.02)',
                  opacity: isMissionPending ? 0.65 : 1,
                  transform: isMissionActive ? 'scale(1.02)' : 'none',
                  transition: 'all 0.2s ease'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '10.5px', fontWeight: 800, color: m.color, textTransform: 'uppercase' }}>
                    {m.tag}
                  </span>
                  {isMissionDone ? (
                    <CheckCircle size={14} color="#16a34a" />
                  ) : isMissionActive ? (
                    <div style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      background: m.color,
                      boxShadow: `0 0 8px ${m.color}`
                    }} />
                  ) : (
                    <span style={{ fontSize: '10px', color: '#94a3b8', fontWeight: 700 }}>
                      Pending
                    </span>
                  )}
                </div>
                <div style={{ fontSize: '12px', fontWeight: 800, color: '#0f172a' }}>
                  {m.name}
                </div>
                <div style={{ fontSize: '10.5px', color: isMissionDone ? '#16a34a' : isMissionActive ? m.color : '#64748b', fontWeight: 700 }}>
                  {isMissionDone ? '✓ 100% Completed' : isMissionActive ? '● In Progress' : 'Waiting in Queue'}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ------------------------------------------------------------- */}
      {/* PROGRESSOR 2: Active Pipeline Step & Live Details             */}
      {/* ------------------------------------------------------------- */}
      <div style={{
        background: '#ffffff',
        borderRadius: '20px',
        border: `2px solid ${isCompleted ? '#86efac' : isError ? '#fca5a5' : '#fed7aa'}`,
        padding: '20px 24px',
        boxShadow: '0 6px 20px -4px rgba(0, 0, 0, 0.04)',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '9px',
              background: 'linear-gradient(135deg, #fef08a 0%, #fde047 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 2px 6px rgba(234, 179, 8, 0.3)'
            }}>
              <Flame size={18} color="#b45309" />
            </div>
            <div>
              <h4 style={{ fontSize: '14.5px', fontWeight: 800, color: '#0f172a', margin: 0 }}>
                {progress.stepName || 'Processing Active Step'}
              </h4>
              <p style={{ fontSize: '12px', color: '#64748b', margin: '2px 0 0 0' }}>
                {progress.details || 'Evaluating catalog SKUs against target demographic styles...'}
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{
              fontSize: '11px',
              fontWeight: 800,
              background: isCompleted ? '#dcfce7' : isError ? '#fee2e2' : '#fff7ed',
              color: isCompleted ? '#166534' : isError ? '#991b1b' : '#c2410c',
              border: `1.5px solid ${isCompleted ? '#86efac' : isError ? '#fca5a5' : '#fed7aa'}`,
              padding: '2px 9px',
              borderRadius: '999px'
            }}>
              {isCompleted ? 'Finished' : isError ? 'Error' : `Active Step ${progress.stepId || 1} of 5`}
            </span>
            <span style={{
              fontSize: '18px',
              fontWeight: 900,
              color: isCompleted ? '#16a34a' : isError ? '#dc2626' : '#ea580c',
              fontFamily: 'JetBrains Mono, monospace'
            }}>
              {progress.percent}%
            </span>
          </div>
        </div>

        {/* Step Micro Progress Bar */}
        <div style={{
          width: '100%',
          height: '8px',
          background: '#f1f5f9',
          borderRadius: '999px',
          overflow: 'hidden'
        }}>
          <div style={{
            width: `${Math.min(100, Math.max(0, progress.percent))}%`,
            height: '100%',
            background: isCompleted
              ? 'linear-gradient(90deg, #10b981 0%, #059669 100%)'
              : isError
              ? '#ef4444'
              : 'linear-gradient(90deg, #f59e0b 0%, #ea580c 50%, #e11d48 100%)',
            borderRadius: '999px',
            transition: 'width 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)'
          }} />
        </div>

        {/* History Chips */}
        {history.length > 0 && (
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '2px' }}>
            {history.map((h, idx) => (
              <div
                key={idx}
                style={{
                  fontSize: '10.5px',
                  background: '#fafafa',
                  border: '1px solid #e2e8f0',
                  borderRadius: '6px',
                  padding: '3px 8px',
                  color: '#475569',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px'
                }}
              >
                <Sparkles size={10} color="#f59e0b" />
                <span>{h.stepName}</span>
                <strong style={{ color: '#0f172a' }}>{h.percent}%</strong>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
