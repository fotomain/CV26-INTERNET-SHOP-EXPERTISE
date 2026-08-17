import React, { useRef, useState } from 'react';
import { Upload, Trash2, FileCheck, Sparkles, FolderPlus, FolderOpen, Files } from 'lucide-react';
import { FileItem } from '../store/slices/sessionSlice';
import { DEFAULT_FILE_SIZE_LIMIT_MB, DEFAULT_NUMBER_OF_FILES } from '../constants/config';

interface FileUploadZoneProps {
  title: string;
  subtitle: string;
  badgeText: string;
  badgeColor?: 'blue' | 'purple' | 'rose' | 'amber' | 'emerald';
  files: FileItem[];
  onAddFiles: (files: File[]) => void;
  onClearFiles: () => void;
  acceptTypes?: string;
  buttonLabel?: string;
  folderButtonLabel?: string;
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
  folderButtonLabel = 'Select Folder',
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const folderInputRef = useRef<HTMLInputElement>(null);
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
      const validFiles = Array.from(e.dataTransfer.files).filter(
        (f) => !f.name.startsWith('.') && !f.name.toLowerCase().includes('thumbs.db')
      );
      onAddFiles(validFiles);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const validFiles = Array.from(e.target.files).filter(
        (f) => !f.name.startsWith('.') && !f.name.toLowerCase().includes('thumbs.db')
      );
      onAddFiles(validFiles);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleFolderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      // Automatically include all valid files from selected folder
      const allFolderFiles = Array.from(e.target.files).filter((f) => {
        const isHidden = f.name.startsWith('.') || f.name.toLowerCase().includes('thumbs.db');
        return !isHidden;
      });
      console.log(`[FolderUpload] Automatically extracted ${allFolderFiles.length} files from selected folder`);
      onAddFiles(allFolderFiles);
    }
    if (folderInputRef.current) {
      folderInputRef.current.value = '';
    }
  };

  const totalSizeMB = (
    files.reduce((acc, f) => acc + f.size, 0) / (1024 * 1024)
  ).toFixed(2);

  let accentGradient = 'linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%)';
  let cardBg = '#f0f9ff';
  let cardBorder = '#bae6fd';
  let badgeBg = '#e0f2fe';
  let badgeTextColor = '#0369a1';
  let badgeBorder = '#7dd3fc';
  let iconColor = '#0284c7';

  if (badgeColor === 'purple') {
    accentGradient = 'linear-gradient(135deg, #a855f7 0%, #7c3aed 100%)';
    cardBg = '#faf5ff';
    cardBorder = '#e9d5ff';
    badgeBg = '#f3e8ff';
    badgeTextColor = '#6b21a8';
    badgeBorder = '#d8b4fe';
    iconColor = '#7c3aed';
  } else if (badgeColor === 'rose') {
    accentGradient = 'linear-gradient(135deg, #fb7185 0%, #e11d48 100%)';
    cardBg = '#fff1f2';
    cardBorder = '#fecdd3';
    badgeBg = '#ffe4e6';
    badgeTextColor = '#9f1239';
    badgeBorder = '#fda4af';
    iconColor = '#e11d48';
  }

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
      minWidth: '300px',
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
            <h2 style={{ fontSize: '15.5px', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em', margin: 0 }}>
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
          <p style={{ fontSize: '12.5px', color: '#64748b', margin: '4px 0 0 0' }}>
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
              padding: '5px 10px',
              borderRadius: '10px',
              fontSize: '11.5px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
              transition: 'all 0.15s ease'
            }}
          >
            <Trash2 size={13} />
            Clear ({files.length})
          </button>
        )}
      </div>

      {/* Drag & Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        style={{
          border: isDragging ? '2px dashed #f59e0b' : `2px dashed ${badgeBorder}`,
          background: isDragging ? '#fffbeb' : cardBg,
          borderRadius: '14px',
          padding: '24px 16px',
          textAlign: 'center',
          transition: 'all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '12px'
        }}
      >
        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={acceptTypes}
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />

        {/* Hidden Folder / Directory Input */}
        <input
          ref={folderInputRef}
          type="file"
          multiple
          {...({ webkitdirectory: '', directory: '', mozdirectory: '' } as any)}
          onChange={handleFolderChange}
          style={{ display: 'none' }}
        />

        <div style={{
          width: '44px',
          height: '44px',
          borderRadius: '12px',
          background: '#ffffff',
          border: `1.5px solid ${badgeBorder}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)',
          transform: isDragging ? 'scale(1.15)' : 'scale(1)'
        }}>
          <FolderPlus size={20} color={iconColor} />
        </div>

        <div>
          <p style={{ fontSize: '13.5px', fontWeight: 700, color: '#0f172a', margin: 0 }}>
            Drag &amp; drop files or folders here
          </p>
          <p style={{ fontSize: '11.5px', color: '#64748b', margin: '3px 0 0 0' }}>
            Max <strong>{DEFAULT_FILE_SIZE_LIMIT_MB}MB</strong> per file &bull; Up to <strong>{DEFAULT_NUMBER_OF_FILES} files</strong>
          </p>
        </div>

        {/* Two Buttons: Select Files & Select Folder */}
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', justifyContent: 'center' }}>
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
              padding: '7px 15px',
              borderRadius: '9px',
              fontSize: '12.5px',
              fontWeight: 700,
              cursor: 'pointer',
              boxShadow: '0 3px 10px rgba(0, 0, 0, 0.12)',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.15s ease'
            }}
          >
            <Files size={14} />
            {buttonLabel}
          </button>

          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              folderInputRef.current?.click();
            }}
            style={{
              background: '#ffffff',
              border: `1.5px solid ${badgeBorder}`,
              color: badgeTextColor,
              padding: '7px 15px',
              borderRadius: '9px',
              fontSize: '12.5px',
              fontWeight: 700,
              cursor: 'pointer',
              boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.15s ease'
            }}
          >
            <FolderOpen size={14} color={iconColor} />
            {folderButtonLabel}
          </button>
        </div>
      </div>

      {/* Files Attached Summary */}
      {files.length > 0 ? (
        <div style={{
          background: '#f8fafc',
          border: '1.5px solid #e2e8f0',
          borderRadius: '12px',
          padding: '10px 14px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '8px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileCheck size={16} color="#16a34a" />
            <span style={{ fontSize: '12.5px', fontWeight: 700, color: '#0f172a' }}>
              {files.length} {files.length === 1 ? 'file' : 'files'} attached
            </span>
            <span style={{ fontSize: '11.5px', color: '#64748b', fontWeight: 600 }}>
              ({totalSizeMB} MB)
            </span>
          </div>
          <div style={{ display: 'flex', gap: '4px', overflowX: 'auto', maxWidth: '180px' }}>
            {files.slice(0, 3).map((f) => (
              <span
                key={f.id}
                title={f.name}
                style={{
                  fontSize: '10px',
                  background: '#ffffff',
                  border: '1px solid #cbd5e1',
                  color: '#334155',
                  fontWeight: 600,
                  padding: '2px 6px',
                  borderRadius: '6px',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  maxWidth: '65px'
                }}
              >
                {f.name}
              </span>
            ))}
            {files.length > 3 && (
              <span style={{ fontSize: '11px', color: '#64748b', alignSelf: 'center', fontWeight: 700 }}>
                +{files.length - 3}
              </span>
            )}
          </div>
        </div>
      ) : (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          fontSize: '11.5px',
          color: '#64748b',
          fontWeight: 500
        }}>
          <Sparkles size={13} color="#f59e0b" />
          <span>No files attached (uses default dataset/lookbook).</span>
        </div>
      )}
    </div>
  );
};
