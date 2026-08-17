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
  const [isExtractingFolder, setIsExtractingFolder] = useState(false);
  const [folderConfirmation, setFolderConfirmation] = useState<{
    folderName: string;
    files: File[];
  } | null>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  /**
   * Recursively traverses dropped directories and files using HTML5 FileSystem API.
   */
  const extractAllFilesFromDataTransfer = async (
    dataTransfer: DataTransfer
  ): Promise<{ files: File[]; isFolder: boolean; folderName: string }> => {
    const items = dataTransfer.items;
    const extracted: File[] = [];
    let isFolder = false;
    let folderName = '';

    if (items && items.length > 0) {
      const entries: any[] = [];
      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.kind === 'file') {
          const entry = item.webkitGetAsEntry
            ? item.webkitGetAsEntry()
            : (item as any).getAsEntry
            ? (item as any).getAsEntry()
            : null;
          if (entry) {
            entries.push(entry);
          }
        }
      }

      if (entries.length > 0) {
        const readEntry = async (entry: any): Promise<void> => {
          if (entry.isFile) {
            return new Promise<void>((resolve) => {
              entry.file(
                (file: File) => {
                  if (!file.name.startsWith('.') && !file.name.toLowerCase().includes('thumbs.db')) {
                    extracted.push(file);
                  }
                  resolve();
                },
                () => resolve()
              );
            });
          } else if (entry.isDirectory) {
            isFolder = true;
            if (!folderName) {
              folderName = entry.name;
            }
            const reader = entry.createReader();
            const readBatch = async (): Promise<any[]> => {
              return new Promise<any[]>((resolve) => {
                reader.readEntries(
                  (results: any[]) => resolve(results || []),
                  () => resolve([])
                );
              });
            };

            let batch: any[] = [];
            do {
              batch = await readBatch();
              for (const childEntry of batch) {
                await readEntry(childEntry);
              }
            } while (batch.length > 0);
          }
        };

        for (const entry of entries) {
          await readEntry(entry);
        }
      }
    }

    // Fallback if FileSystem entry API yielded no files
    if (extracted.length === 0 && dataTransfer.files && dataTransfer.files.length > 0) {
      const fallbackFiles = Array.from(dataTransfer.files).filter(
        (f) => !f.name.startsWith('.') && !f.name.toLowerCase().includes('thumbs.db')
      );
      extracted.push(...fallbackFiles);
    }

    return {
      files: extracted,
      isFolder,
      folderName: folderName || 'Selected Folder',
    };
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    try {
      setIsExtractingFolder(true);
      const { files: extractedFiles, isFolder, folderName } = await extractAllFilesFromDataTransfer(
        e.dataTransfer
      );
      setIsExtractingFolder(false);

      if (extractedFiles.length === 0) return;

      if (isFolder) {
        // Ask the same question as browser's Select Folder confirmation prompt
        setFolderConfirmation({
          folderName,
          files: extractedFiles,
        });
      } else {
        onAddFiles(extractedFiles);
      }
    } catch (err) {
      setIsExtractingFolder(false);
      console.error('[DropError] Failed to parse folder items:', err);
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        const fallback = Array.from(e.dataTransfer.files).filter(
          (f) => !f.name.startsWith('.') && !f.name.toLowerCase().includes('thumbs.db')
        );
        onAddFiles(fallback);
      }
    }
  };

  const handleSelectFolder = async (e: React.MouseEvent) => {
    e.stopPropagation();
    // Try modern File System Access API (showDirectoryPicker) to bypass browser's default system warning prompt
    if ('showDirectoryPicker' in window) {
      try {
        const dirHandle = await (window as any).showDirectoryPicker();
        if (!dirHandle) return;

        setIsExtractingFolder(true);
        const extracted: File[] = [];

        const readDirHandle = async (handle: any) => {
          for await (const entry of handle.values()) {
            if (entry.kind === 'file') {
              const file = await entry.getFile();
              if (!file.name.startsWith('.') && !file.name.toLowerCase().includes('thumbs.db')) {
                extracted.push(file);
              }
            } else if (entry.kind === 'directory') {
              await readDirHandle(entry);
            }
          }
        };

        await readDirHandle(dirHandle);
        setIsExtractingFolder(false);

        if (extracted.length > 0) {
          setFolderConfirmation({
            folderName: dirHandle.name || 'Selected Folder',
            files: extracted,
          });
        }
      } catch (err: any) {
        setIsExtractingFolder(false);
        if (err.name !== 'AbortError') {
          console.warn('[DirectoryPicker] Fallback to input picker:', err);
          folderInputRef.current?.click();
        }
      }
    } else {
      folderInputRef.current?.click();
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
      if (allFolderFiles.length > 0) {
        let folderName = 'Selected Folder';
        const relPath = (allFolderFiles[0] as any).webkitRelativePath;
        if (relPath) {
          folderName = relPath.split('/')[0] || folderName;
        }
        console.log(`[FolderUpload] Extracted ${allFolderFiles.length} files from folder: ${folderName}`);
        setFolderConfirmation({
          folderName,
          files: allFolderFiles,
        });
      }
    }
    if (folderInputRef.current) {
      folderInputRef.current.value = '';
    }
  };

  const totalSizeMB = (
    files.reduce((acc, f) => acc + f.size, 0) / (1024 * 1024)
  ).toFixed(2);

  const totalFolderSizeMB = folderConfirmation
    ? (folderConfirmation.files.reduce((acc, f) => acc + f.size, 0) / (1024 * 1024)).toFixed(2)
    : '0.00';

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
            onClick={handleSelectFolder}
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
          gap: '10px',
          width: '100%',
          boxSizing: 'border-box'
        }}>
          {/* Left / Center content: Info & Preview Chips */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', flex: 1, minWidth: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
              <FileCheck size={16} color="#16a34a" />
              <span style={{ fontSize: '12.5px', fontWeight: 700, color: '#0f172a' }}>
                {files.length} {files.length === 1 ? 'file' : 'files'} attached
              </span>
              <span style={{ fontSize: '11.5px', color: '#64748b', fontWeight: 600 }}>
                ({totalSizeMB} MB)
              </span>
            </div>

            <div style={{ display: 'flex', gap: '4px', overflowX: 'auto', maxWidth: '140px', flexShrink: 0 }}>
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

          {/* Right border: Clear Button */}
          <button
            type="button"
            onClick={onClearFiles}
            style={{
              background: '#fef2f2',
              color: '#dc2626',
              border: '1.5px solid #fca5a5',
              padding: '5px 12px',
              borderRadius: '8px',
              fontSize: '11.5px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              marginLeft: 'auto',
              flexShrink: 0,
              transition: 'all 0.15s ease',
              boxShadow: '0 1px 3px rgba(220, 38, 38, 0.08)'
            }}
            title="Clear all attached files"
          >
            <Trash2 size={12} />
            Clear
          </button>
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

      {/* Custom Nice Folder Upload Confirmation Modal */}
      {folderConfirmation && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(15, 23, 42, 0.75)',
          backdropFilter: 'blur(6px)',
          WebkitBackdropFilter: 'blur(6px)',
          zIndex: 50,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '16px',
          borderRadius: '20px',
          animation: 'fadeIn 0.2s ease-out'
        }}>
          <div style={{
            background: '#ffffff',
            borderRadius: '20px',
            padding: '26px 22px',
            maxWidth: '360px',
            width: '100%',
            boxShadow: '0 20px 45px rgba(0, 0, 0, 0.28), 0 4px 16px rgba(0, 0, 0, 0.08)',
            border: '2px solid #fed7aa',
            display: 'flex',
            flexDirection: 'column',
            gap: '14px',
            textAlign: 'center',
            position: 'relative'
          }}>
            <div style={{
              width: '52px',
              height: '52px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%)',
              border: '2px solid #fde68a',
              color: '#d97706',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto',
              boxShadow: '0 4px 14px rgba(245, 158, 11, 0.25)'
            }}>
              <FolderOpen size={26} color="#ea580c" />
            </div>

            <div>
              <h4 style={{ fontSize: '15.5px', fontWeight: 900, color: '#0f172a', margin: 0, letterSpacing: '-0.02em', lineHeight: 1.4 }}>
                Are you sure you want to upload all files from “{folderConfirmation.folderName}”?
              </h4>
              <p style={{ fontSize: '12.5px', color: '#64748b', margin: '8px 0 0 0', lineHeight: 1.45, fontWeight: 500 }}>
                Only do this if you trust the site.
              </p>
            </div>

            {/* Folder files summary pill */}
            <div style={{
              background: '#f8fafc',
              border: '1.5px solid #e2e8f0',
              borderRadius: '12px',
              padding: '8px 12px',
              fontSize: '12px',
              color: '#334155',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <span style={{ color: '#0369a1' }}>
                📁 {folderConfirmation.files.length} {folderConfirmation.files.length === 1 ? 'file' : 'files'}
              </span>
              <span style={{ color: '#64748b', fontSize: '11px', fontWeight: 600 }}>
                {totalFolderSizeMB} MB
              </span>
            </div>

            {/* File names preview */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', justifyContent: 'center', maxHeight: '65px', overflowY: 'auto' }}>
              {folderConfirmation.files.slice(0, 4).map((f, i) => (
                <span
                  key={i}
                  title={f.name}
                  style={{
                    fontSize: '10.5px',
                    background: '#f1f5f9',
                    border: '1px solid #cbd5e1',
                    color: '#475569',
                    padding: '2px 7px',
                    borderRadius: '6px',
                    maxWidth: '120px',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis'
                  }}
                >
                  {f.name}
                </span>
              ))}
              {folderConfirmation.files.length > 4 && (
                <span style={{ fontSize: '10.5px', color: '#94a3b8', fontWeight: 700, alignSelf: 'center' }}>
                  +{folderConfirmation.files.length - 4} more
                </span>
              )}
            </div>

            <div style={{ display: 'flex', gap: '10px', marginTop: '4px' }}>
              <button
                type="button"
                onClick={() => setFolderConfirmation(null)}
                style={{
                  flex: 1,
                  background: '#f8fafc',
                  border: '1.5px solid #cbd5e1',
                  color: '#475569',
                  padding: '10px 14px',
                  borderRadius: '12px',
                  fontSize: '13px',
                  fontWeight: 700,
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => {
                  onAddFiles(folderConfirmation.files);
                  setFolderConfirmation(null);
                }}
                style={{
                  flex: 1,
                  background: 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)',
                  border: 'none',
                  color: '#ffffff',
                  padding: '10px 14px',
                  borderRadius: '12px',
                  fontSize: '13px',
                  fontWeight: 800,
                  cursor: 'pointer',
                  boxShadow: '0 4px 14px rgba(245, 158, 11, 0.4)',
                  transition: 'all 0.15s ease'
                }}
              >
                Upload Files
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Extracting Folder Loader Overlay */}
      {isExtractingFolder && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(255, 255, 255, 0.85)',
          backdropFilter: 'blur(3px)',
          zIndex: 40,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '10px',
          borderRadius: '20px'
        }}>
          <div style={{
            width: '28px',
            height: '28px',
            border: '3px solid #0ea5e9',
            borderTopColor: 'transparent',
            borderRadius: '50%',
            animation: 'spin 0.8s linear infinite'
          }} />
          <span style={{ fontSize: '12.5px', fontWeight: 700, color: '#0369a1' }}>
            Reading files from folder...
          </span>
        </div>
      )}
    </div>
  );
};
