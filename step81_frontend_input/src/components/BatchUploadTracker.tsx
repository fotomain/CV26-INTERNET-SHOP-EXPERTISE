import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { UploadCloud, CheckCircle, Clock, Zap, ArrowRight } from 'lucide-react';

export const BatchUploadTracker: React.FC = () => {
  const { uploadProgress } = useSelector((state: RootState) => state.progress);
  const isSubmitting = useSelector((state: RootState) => state.session.isSubmitting);

  if (!uploadProgress.isUploading && !uploadProgress.isComplete && uploadProgress.percent === 0) {
    return null;
  }

  const isComplete = uploadProgress.isComplete || uploadProgress.percent >= 100;

  return (
    <div style={{
      background: isComplete
        ? 'linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%)'
        : 'linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%)',
      borderRadius: '20px',
      border: `2px solid ${isComplete ? '#86efac' : '#7dd3fc'}`,
      padding: '20px 24px',
      boxShadow: '0 6px 20px -4px rgba(2, 132, 199, 0.08)',
      display: 'flex',
      flexDirection: 'column',
      gap: '14px',
      transition: 'all 0.3s ease'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '10px',
            background: isComplete
              ? 'linear-gradient(135deg, #dcfce7 0%, #86efac 100%)'
              : 'linear-gradient(135deg, #bae6fd 0%, #38bdf8 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)'
          }}>
            {isComplete ? (
              <CheckCircle size={20} color="#166534" />
            ) : (
              <UploadCloud size={20} color="#0369a1" />
            )}
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h4 style={{ fontSize: '15px', fontWeight: 900, color: '#0f172a', letterSpacing: '-0.02em', margin: 0 }}>
                Phase 1: File Posting via Batches (10 files / batch)
              </h4>
              <span style={{
                background: isComplete ? '#dcfce7' : '#e0f2fe',
                color: isComplete ? '#15803d' : '#0369a1',
                border: `1px solid ${isComplete ? '#86efac' : '#7dd3fc'}`,
                fontSize: '11px',
                fontWeight: 800,
                padding: '2px 8px',
                borderRadius: '999px'
              }}>
                {isComplete
                  ? 'All Batches Ingested'
                  : `Batch ${uploadProgress.currentBatch} of ${uploadProgress.totalBatches}`}
              </span>
            </div>
            <p style={{ fontSize: '12.5px', color: '#64748b', margin: '3px 0 0 0' }}>
              {uploadProgress.statusText}
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'baseline', gap: '6px' }}>
          <span style={{
            fontSize: '24px',
            fontWeight: 900,
            color: isComplete ? '#16a34a' : '#0284c7',
            fontFamily: 'JetBrains Mono, monospace'
          }}>
            {uploadProgress.percent}%
          </span>
          <span style={{ fontSize: '12px', color: '#64748b', fontWeight: 700 }}>
            {uploadProgress.uploadedFilesCount}/{uploadProgress.totalFilesCount} files
          </span>
        </div>
      </div>

      {/* Batch Upload Progress Bar */}
      <div style={{
        width: '100%',
        height: '10px',
        background: '#e2e8f0',
        borderRadius: '999px',
        overflow: 'hidden',
        boxShadow: 'inset 0 1px 2px rgba(0,0,0,0.06)'
      }}>
        <div style={{
          width: `${Math.min(100, Math.max(0, uploadProgress.percent))}%`,
          height: '100%',
          background: isComplete
            ? 'linear-gradient(90deg, #10b981 0%, #059669 100%)'
            : 'linear-gradient(90deg, #38bdf8 0%, #0284c7 50%, #0369a1 100%)',
          borderRadius: '999px',
          transition: 'width 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)'
        }} />
      </div>
    </div>
  );
};
