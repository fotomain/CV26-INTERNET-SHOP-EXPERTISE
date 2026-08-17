import React, { useRef, useState } from 'react';
import { Upload, Trash2, FileCheck, Sparkles, FolderPlus } from 'lucide-react';
import { FileItem } from '../store/slices/sessionSlice';
import { DEFAULT_FILE_SIZE_LIMIT_MB, DEFAULT_NUMBER_OF_FILES } from '../constants/config';

interface FileUploadZoneProps {
  title: string;
  subtitle: string;
  badgeText: string;
  badgeColor?: 'blue' | 'purple' | 'amber' | 'emerald';
  files: FileItem[];
  onAddFiles: (files: File[]) => void;
  onClearFiles: () => void;
  acceptTypes?: string;
  buttonLabel?: string;
}

export const FileUploadZone: React.FC<FileUploadZoneProps> = ({
  title,
  subtitle,
  badgeText,
  badgeColor = 'blue',
  files,
  onAddFiles,
  onClearFiles,
  acceptTypes = 'image/jpeg,image/png,image/webp,.csv',
  buttonLabel = 'Select Files',
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onAddFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onAddFiles(Array.from(e.target.files));
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const totalSizeMB = (
    files.reduce((acc, f) => acc + f.size, 0) / (1024 * 1024)
  ).toFixed(2);

  const isPurple = badgeColor === 'purple';
  const accentGradient = isPurple
    ? 'linear-gradient(135deg, #a855f7 0%, #7c3aed 100%)'
    : 'linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%)';
  const cardBg = isPurple ? '#faf5ff' : '#f0f9ff';
  const cardBorder = isPurple ? '#e9d5ff' : '#bae6fd';
  const badgeBg = isPurple ? '#f3e8ff' : '#e0f2fe';
  const badgeTextColor = isPurple ? '#6b21a8' : '#0369a1';
  const badgeBorder = isPurple ? '#d8b4fe' : '#7dd3fc';

  return (
    <div style={{
      background: '#ffffff',
      borderRadius: '20px',
      border: `2px solid ${cardBorder}`,
      padding: '24px',
      boxShadow: '0 8px 24px -4px rgba(0, 0, 0, 0.04)',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      flex: 1,
      minWidth: '320px',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Decorative top colorful bar */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '5px',
        background: accentGradient
      }} />

      {/* Header Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px', marginTop: '4px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h2 style={{ fontSize: '16px', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em', margin: 0 }}>
              {title}
            </h2>
            <span style={{
              background: badgeBg,
              color: badgeTextColor,
              border: `1px solid ${badgeBorder}`,
              fontSize: '11px',
              fontWeight: 800,
              padding: '2px 9px',
              borderRadius: '999px',
              textTransform: 'uppercase',
              letterSpacing: '0.04em'
            }}>
              {badgeText}
            </span>
          </div>
          <p style={{ fontSize: '13px', color: '#64748b', margin: '4px 0 0 0' }}>
            {subtitle}
          </p>
        </div>

        {files.length > 0 && (
          <button
            onClick={onClearFiles}
            style={{
              background: '#fef2f2',
              color: '#dc2626',
              border: '1.5px solid #fca5a5',
              padding: '6px 12px',
              borderRadius: '10px',
              fontSize: '12px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.15s ease'
            }}
          >
            <Trash2 size={14} />
            Clear files ({files.length})
          </button>
        )}
      </div>

      {/* Drag & Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        style={{
          border: isDragging ? '2px dashed #f59e0b' : `2px dashed ${badgeBorder}`,
          background: isDragging ? '#fffbeb' : cardBg,
          borderRadius: '14px',
          padding: '30px 20px',
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '12px'
        }}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={acceptTypes}
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <div style={{
          width: '48px',
          height: '48px',
          borderRadius: '14px',
          background: '#ffffff',
          border: `1.5px solid ${badgeBorder}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)',
          transform: isDragging ? 'scale(1.15)' : 'scale(1)'
        }}>
          <FolderPlus size={22} color={isPurple ? '#7c3aed' : '#0284c7'} />
        </div>
        <div>
          <p style={{ fontSize: '14px', fontWeight: 700, color: '#0f172a', margin: 0 }}>
            Drag &amp; drop files here, or <span style={{ color: isPurple ? '#7c3aed' : '#0284c7', textDecoration: 'underline' }}>browse</span>
          </p>
          <p style={{ fontSize: '12px', color: '#64748b', margin: '4px 0 0 0' }}>
            Max <strong>{DEFAULT_FILE_SIZE_LIMIT_MB}MB</strong> &bull; Up to <strong>{DEFAULT_NUMBER_OF_FILES} files</strong> (.png, .jpg, .webp, .csv)
          </p>
        </div>
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            fileInputRef.current?.click();
          }}
          style={{
            background: accentGradient,
            border: 'none',
            color: '#ffffff',
            padding: '8px 18px',
            borderRadius: '10px',
            fontSize: '13px',
            fontWeight: 700,
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.12)',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <Upload size={14} />
          {buttonLabel}
        </button>
      </div>

      {/* Files Attached Summary / Preview */}
      {files.length > 0 ? (
        <div style={{
          background: '#f8fafc',
          border: '1.5px solid #e2e8f0',
          borderRadius: '12px',
          padding: '12px 16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '8px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileCheck size={18} color="#16a34a" />
            <span style={{ fontSize: '13px', fontWeight: 700, color: '#0f172a' }}>
              {files.length} {files.length === 1 ? 'file' : 'files'} attached
            </span>
            <span style={{ fontSize: '12px', color: '#64748b', fontWeight: 600 }}>
              ({totalSizeMB} MB)
            </span>
          </div>
          <div style={{ display: 'flex', gap: '4px', overflowX: 'auto', maxWidth: '220px' }}>
            {files.slice(0, 4).map((f) => (
              <span
                key={f.id}
                title={f.name}
                style={{
                  fontSize: '10.5px',
                  background: '#ffffff',
                  border: '1px solid #cbd5e1',
                  color: '#334155',
                  fontWeight: 600,
                  padding: '3px 7px',
                  borderRadius: '6px',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  maxWidth: '75px'
                }}
              >
                {f.name}
              </span>
            ))}
            {files.length > 4 && (
              <span style={{ fontSize: '11px', color: '#64748b', alignSelf: 'center', fontWeight: 700 }}>
                +{files.length - 4}
              </span>
            )}
          </div>
        </div>
      ) : (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          fontSize: '12px',
          color: '#64748b',
          fontWeight: 500
        }}>
          <Sparkles size={14} color="#f59e0b" />
          <span>No custom files attached yet. (Default dataset will be loaded automatically).</span>
        </div>
      )}
    </div>
  );
};
