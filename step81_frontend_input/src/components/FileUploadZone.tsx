import React, { useRef, useState } from 'react';
import { UploadCloud, Trash2, FileCheck, AlertCircle, Image as ImageIcon } from 'lucide-react';
import { FileItem } from '../store/slices/sessionSlice';
import { DEFAULT_FILE_SIZE_LIMIT_MB, DEFAULT_NUMBER_OF_FILES } from '../constants/config';

interface FileUploadZoneProps {
  title: string;
  subtitle: string;
  badgeText: string;
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

  return (
    <div style={{
      background: '#ffffff',
      borderRadius: '16px',
      border: '1px solid #e2e8f0',
      padding: '24px',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05)',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      flex: 1,
      minWidth: '320px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h2 style={{ fontSize: '16px', fontWeight: 700, color: '#0f172a', margin: 0 }}>
              {title}
            </h2>
            <span style={{
              background: '#eff6ff',
              color: '#2563eb',
              border: '1px solid #bfdbfe',
              fontSize: '11px',
              fontWeight: 700,
              padding: '2px 8px',
              borderRadius: '999px'
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
              border: '1px solid #fecaca',
              padding: '6px 12px',
              borderRadius: '8px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'background 0.15s ease'
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
          border: isDragging ? '2px dashed #3b82f6' : '2px dashed #cbd5e1',
          background: isDragging ? '#eff6ff' : '#f8fafc',
          borderRadius: '12px',
          padding: '28px 20px',
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '10px'
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
          width: '50px',
          height: '50px',
          borderRadius: '50%',
          background: isDragging ? '#dbeafe' : '#f1f5f9',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <UploadCloud size={26} color={isDragging ? '#2563eb' : '#64748b'} />
        </div>
        <div>
          <p style={{ fontSize: '14px', fontWeight: 600, color: '#1e293b', margin: 0 }}>
            Drag &amp; drop files here, or <span style={{ color: '#2563eb' }}>browse</span>
          </p>
          <p style={{ fontSize: '12px', color: '#94a3b8', margin: '4px 0 0 0' }}>
            Max {DEFAULT_FILE_SIZE_LIMIT_MB}MB per file &bull; Up to {DEFAULT_NUMBER_OF_FILES} files
          </p>
        </div>
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            fileInputRef.current?.click();
          }}
          style={{
            background: '#ffffff',
            border: '1px solid #cbd5e1',
            color: '#334155',
            padding: '7px 16px',
            borderRadius: '8px',
            fontSize: '13px',
            fontWeight: 600,
            cursor: 'pointer',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)'
          }}
        >
          {buttonLabel}
        </button>
      </div>

      {/* Files Attached Summary / Preview */}
      {files.length > 0 ? (
        <div style={{
          background: '#f8fafc',
          border: '1px solid #e2e8f0',
          borderRadius: '10px',
          padding: '12px 16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '8px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileCheck size={18} color="#16a34a" />
            <span style={{ fontSize: '13px', fontWeight: 600, color: '#0f172a' }}>
              {files.length} {files.length === 1 ? 'file' : 'files'} attached
            </span>
            <span style={{ fontSize: '12px', color: '#64748b' }}>
              ({totalSizeMB} MB total)
            </span>
          </div>
          <div style={{ display: 'flex', gap: '4px', overflowX: 'auto', maxWidth: '200px' }}>
            {files.slice(0, 5).map((f) => (
              <span
                key={f.id}
                title={f.name}
                style={{
                  fontSize: '10px',
                  background: '#e2e8f0',
                  color: '#475569',
                  padding: '2px 6px',
                  borderRadius: '4px',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  maxWidth: '70px'
                }}
              >
                {f.name}
              </span>
            ))}
            {files.length > 5 && (
              <span style={{ fontSize: '10px', color: '#64748b', alignSelf: 'center' }}>
                +{files.length - 5}
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
          color: '#94a3b8'
        }}>
          <AlertCircle size={14} />
          <span>No custom files attached yet. (Default dataset will be used if left empty).</span>
        </div>
      )}
    </div>
  );
};
