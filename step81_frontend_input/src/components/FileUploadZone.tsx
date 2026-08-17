import React, { useRef, useState } from 'react';
import { Upload, Trash2, FileCheck2, AlertCircle } from 'lucide-react';
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
      border: '1px solid rgba(0, 0, 0, 0.08)',
      padding: '24px',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.02), 0 6px 24px -4px rgba(0, 0, 0, 0.04)',
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      flex: 1,
      minWidth: '320px',
      transition: 'border-color 0.2s ease, box-shadow 0.2s ease'
    }}>
      {/* Header Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h2 style={{ fontSize: '15px', fontWeight: 700, color: '#09090b', letterSpacing: '-0.02em', margin: 0 }}>
              {title}
            </h2>
            <span style={{
              background: '#f4f4f5',
              color: '#18181b',
              border: '1px solid #e4e4e7',
              fontSize: '11px',
              fontWeight: 700,
              padding: '2px 8px',
              borderRadius: '6px'
            }}>
              {badgeText}
            </span>
          </div>
          <p style={{ fontSize: '12px', color: '#71717a', margin: '4px 0 0 0' }}>
            {subtitle}
          </p>
        </div>

        {files.length > 0 && (
          <button
            onClick={onClearFiles}
            style={{
              background: '#ffffff',
              color: '#ef4444',
              border: '1px solid #fecaca',
              padding: '5px 10px',
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
            <Trash2 size={13} />
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
          border: isDragging ? '1.5px dashed #09090b' : '1.5px dashed #e4e4e7',
          background: isDragging ? '#f4f4f5' : '#fafafa',
          borderRadius: '12px',
          padding: '28px 20px',
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.15s ease',
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
          width: '42px',
          height: '42px',
          borderRadius: '10px',
          background: '#ffffff',
          border: '1px solid #e4e4e7',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 1px 3px rgba(0,0,0,0.04)'
        }}>
          <Upload size={18} color="#18181b" />
        </div>
        <div>
          <p style={{ fontSize: '13px', fontWeight: 600, color: '#09090b', margin: 0 }}>
            Drag &amp; drop files here, or <span style={{ textDecoration: 'underline' }}>browse</span>
          </p>
          <p style={{ fontSize: '11px', color: '#a1a1aa', margin: '3px 0 0 0' }}>
            Max {DEFAULT_FILE_SIZE_LIMIT_MB}MB per file &bull; Up to {DEFAULT_NUMBER_OF_FILES} files (.png, .jpg, .webp, .csv)
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
            border: '1px solid #d4d4d8',
            color: '#18181b',
            padding: '6px 14px',
            borderRadius: '8px',
            fontSize: '12px',
            fontWeight: 600,
            cursor: 'pointer',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.04)',
            transition: 'background 0.15s ease'
          }}
        >
          {buttonLabel}
        </button>
      </div>

      {/* Files Attached Summary / Preview */}
      {files.length > 0 ? (
        <div style={{
          background: '#fafafa',
          border: '1px solid #e4e4e7',
          borderRadius: '10px',
          padding: '10px 14px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '8px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileCheck2 size={16} color="#16a34a" />
            <span style={{ fontSize: '12px', fontWeight: 600, color: '#09090b' }}>
              {files.length} {files.length === 1 ? 'file' : 'files'} attached
            </span>
            <span style={{ fontSize: '11px', color: '#71717a' }}>
              ({totalSizeMB} MB)
            </span>
          </div>
          <div style={{ display: 'flex', gap: '4px', overflowX: 'auto', maxWidth: '200px' }}>
            {files.slice(0, 4).map((f) => (
              <span
                key={f.id}
                title={f.name}
                style={{
                  fontSize: '10px',
                  background: '#ffffff',
                  border: '1px solid #e4e4e7',
                  color: '#52525b',
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
            {files.length > 4 && (
              <span style={{ fontSize: '10px', color: '#71717a', alignSelf: 'center', fontWeight: 600 }}>
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
          color: '#a1a1aa'
        }}>
          <AlertCircle size={13} />
          <span>No custom files attached yet. (Default dataset will be loaded automatically).</span>
        </div>
      )}
    </div>
  );
};
