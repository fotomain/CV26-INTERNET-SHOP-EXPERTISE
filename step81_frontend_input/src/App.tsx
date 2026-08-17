import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from './store';
import {
  setCustomCountryName,
  addDatasetFiles,
  clearDatasetFiles,
  addCountryImagesMan,
  clearCountryImagesMan,
  addCountryImagesWoman,
  clearCountryImagesWoman,
  setFileErrors,
  clearFileErrors,
  FileItem,
} from './store/slices/sessionSlice';
import { DEFAULT_FILE_SIZE_LIMIT_BYTES, DEFAULT_NUMBER_OF_FILES } from './constants/config';
import { registerFile } from './utils/fileRegistry';
import { updateProgressData } from './store/slices/progressSlice';
import { setResultData } from './store/slices/resultSlice';
import { executeMLAction } from './store/sagas/mlExecutionSaga';
import { subscribeToProgress, subscribeToResults } from './services/supabaseClient';
import { Header } from './components/Header';
import { FileUploadZone } from './components/FileUploadZone';
import { CountrySelector } from './components/CountrySelector';
import { ProgressTracker } from './components/ProgressTracker';
import { CapstoneReportComponent } from './components/CapstoneReportComponent';
import { autoDownloadCsvFiles } from './utils/fileDownloader';
import { Play, AlertCircle, Sparkles, ShieldCheck, Zap, Rocket } from 'lucide-react';

export const App: React.FC = () => {
  const dispatch = useDispatch();
  const {
    userSessionGUID,
    customCountryName,
    customDatasetFiles,
    customCountryImagesMan,
    customCountryImagesWoman,
    fileErrors,
    isSubmitting,
    error,
  } = useSelector((state: RootState) => state.session);

  const { progress } = useSelector((state: RootState) => state.progress);
  const { hasResults } = useSelector((state: RootState) => state.result);

  // Subscribe to Supabase Realtime Channels only when execution is active
  useEffect(() => {
    if (!userSessionGUID || !isSubmitting) return;

    const unsubscribeProgress = subscribeToProgress(userSessionGUID, (p) => {
      dispatch(updateProgressData(p));
      if (p.percent >= 100) {
        autoDownloadCsvFiles(userSessionGUID);
      }
    });

    const unsubscribeResults = subscribeToResults(userSessionGUID, (r) => {
      dispatch(setResultData(r));
      autoDownloadCsvFiles(userSessionGUID);
    });

    return () => {
      unsubscribeProgress();
      unsubscribeResults();
    };
  }, [userSessionGUID, isSubmitting, dispatch]);

  // Also monitor progress state changes
  useEffect(() => {
    if (progress.percent >= 100 && userSessionGUID) {
      autoDownloadCsvFiles(userSessionGUID);
    }
  }, [progress.percent, userSessionGUID]);

  const handleAddDatasetFiles = (files: File[]) => {
    const newErrors: string[] = [];
    const validItems: FileItem[] = [];

    files.forEach((file) => {
      if (file.size > DEFAULT_FILE_SIZE_LIMIT_BYTES) {
        newErrors.push(`"${file.name}" exceeds 1MB limit (${(file.size / (1024 * 1024)).toFixed(2)}MB).`);
      } else if (customDatasetFiles.length + validItems.length >= DEFAULT_NUMBER_OF_FILES) {
        newErrors.push(`Exceeded maximum limit of ${DEFAULT_NUMBER_OF_FILES} files.`);
      } else {
        const id = `catalog-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
        registerFile(id, file);
        validItems.push({
          id,
          name: file.name,
          size: file.size,
          type: file.type,
          lastModified: file.lastModified,
        });
      }
    });

    if (validItems.length > 0) {
      dispatch(addDatasetFiles(validItems));
    }
    if (newErrors.length > 0) {
      dispatch(setFileErrors(newErrors));
    }
  };

  const handleAddCountryImagesMan = (files: File[]) => {
    const newErrors: string[] = [];
    const validItems: FileItem[] = [];

    files.forEach((file) => {
      if (file.size > DEFAULT_FILE_SIZE_LIMIT_BYTES) {
        newErrors.push(`"${file.name}" exceeds 1MB limit (${(file.size / (1024 * 1024)).toFixed(2)}MB).`);
      } else if (customCountryImagesMan.length + validItems.length >= DEFAULT_NUMBER_OF_FILES) {
        newErrors.push(`Exceeded maximum limit of ${DEFAULT_NUMBER_OF_FILES} files.`);
      } else {
        const id = `man-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
        registerFile(id, file);
        validItems.push({
          id,
          name: file.name,
          size: file.size,
          type: file.type,
          lastModified: file.lastModified,
        });
      }
    });

    if (validItems.length > 0) {
      dispatch(addCountryImagesMan(validItems));
    }
    if (newErrors.length > 0) {
      dispatch(setFileErrors(newErrors));
    }
  };

  const handleAddCountryImagesWoman = (files: File[]) => {
    const newErrors: string[] = [];
    const validItems: FileItem[] = [];

    files.forEach((file) => {
      if (file.size > DEFAULT_FILE_SIZE_LIMIT_BYTES) {
        newErrors.push(`"${file.name}" exceeds 1MB limit (${(file.size / (1024 * 1024)).toFixed(2)}MB).`);
      } else if (customCountryImagesWoman.length + validItems.length >= DEFAULT_NUMBER_OF_FILES) {
        newErrors.push(`Exceeded maximum limit of ${DEFAULT_NUMBER_OF_FILES} files.`);
      } else {
        const id = `woman-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
        registerFile(id, file);
        validItems.push({
          id,
          name: file.name,
          size: file.size,
          type: file.type,
          lastModified: file.lastModified,
        });
      }
    });

    if (validItems.length > 0) {
      dispatch(addCountryImagesWoman(validItems));
    }
    if (newErrors.length > 0) {
      dispatch(setFileErrors(newErrors));
    }
  };

  const handleExecuteML = () => {
    dispatch(executeMLAction());
  };

  const totalFilesAttached = customDatasetFiles.length + customCountryImagesMan.length + customCountryImagesWoman.length;
  const hasFilesSelected = totalFilesAttached > 0;
  const isButtonEnabled = !isSubmitting && hasFilesSelected;

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#fafaf9' }}>
      <Header />

      <main style={{
        flex: 1,
        maxWidth: '1280px',
        width: '100%',
        margin: '0 auto',
        padding: '24px 16px',
        display: 'flex',
        flexDirection: 'column',
        gap: '22px',
        minWidth: '350px'
      }}>
        {/* Colorful Hero Card */}
        <div style={{
          background: 'linear-gradient(135deg, #ffffff 0%, #fffbeb 50%, #f0fdf4 100%)',
          border: '2px solid #fed7aa',
          borderRadius: '24px',
          padding: '28px 32px',
          boxShadow: '0 8px 30px -4px rgba(245, 158, 11, 0.12), 0 4px 12px rgba(0, 0, 0, 0.04)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '20px',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', flexWrap: 'wrap' }}>
              <span style={{
                background: 'linear-gradient(135deg, #fef08a 0%, #fde047 100%)',
                color: '#854d0e',
                border: '1px solid #facc15',
                fontSize: '11.5px',
                fontWeight: 800,
                padding: '3px 10px',
                borderRadius: '999px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px',
                boxShadow: '0 2px 6px rgba(250, 204, 21, 0.25)'
              }}>
                <Zap size={13} color="#854d0e" fill="#854d0e" />
                Next-Gen E-Commerce AI Matchmaker
              </span>
              <span style={{
                background: '#e0f2fe',
                color: '#0369a1',
                border: '1px solid #7dd3fc',
                fontSize: '11px',
                fontWeight: 700,
                padding: '3px 9px',
                borderRadius: '999px'
              }}>
                FastAPI + React 18 + Redux-Saga
              </span>
            </div>
            <h2 style={{ fontSize: '23px', fontWeight: 900, color: '#0f172a', letterSpacing: '-0.03em', margin: 0 }}>
              Purchase Manager Catalog &amp; Style AI Engine
            </h2>
            <p style={{ fontSize: '13.5px', color: '#475569', margin: '6px 0 0 0', maxWidth: '750px', lineHeight: 1.55 }}>
              Upload candidate catalog items and target country men &amp; women lookbook photos to run automated Fashion-MNIST classification, YOLOv8 demographic segmentation, 3-palette density extraction, and CIELAB &Delta;E matching.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <span style={{
              background: '#ffffff',
              border: '2px solid #bbf7d0',
              padding: '8px 14px',
              borderRadius: '12px',
              fontSize: '12px',
              fontWeight: 800,
              color: '#15803d',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              boxShadow: '0 2px 8px rgba(22, 163, 74, 0.12)'
            }}>
              <ShieldCheck size={16} color="#16a34a" />
              Supabase Realtime Sync
            </span>
          </div>
        </div>

        {/* Validation Errors Display */}
        {fileErrors.length > 0 && (
          <div style={{
            background: '#fef2f2',
            border: '2px solid #fca5a5',
            borderRadius: '14px',
            padding: '14px 18px',
            color: '#991b1b',
            fontSize: '13px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <strong>Upload Warnings:</strong>
              <ul style={{ marginLeft: '18px', marginTop: '4px' }}>
                {fileErrors.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
            </div>
            <button
              onClick={() => dispatch(clearFileErrors())}
              style={{ background: 'none', border: 'none', color: '#dc2626', cursor: 'pointer', fontWeight: 800, fontSize: '12px' }}
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Execution Error Banner */}
        {error && (
          <div style={{
            background: '#fef2f2',
            border: '2px solid #f87171',
            borderRadius: '14px',
            padding: '14px 18px',
            color: '#b91c1c',
            fontSize: '13px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <AlertCircle size={18} />
            <div>
              <strong>Execution Error:</strong> {error}
            </div>
          </div>
        )}

        {/* Upload Zones Grid: 3 Zones */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '18px'
        }}>
          {/* 1. Candidate Catalog (Blue Accent) */}
          <FileUploadZone
            title="1. Candidate Product Catalog"
            subtitle="Upload apparel photos or CSV (custom_dataset_start)"
            badgeText="Catalog Items"
            badgeColor="blue"
            files={customDatasetFiles}
            onAddFiles={handleAddDatasetFiles}
            onClearFiles={() => dispatch(clearDatasetFiles())}
            buttonLabel="Select custom_dataset_start"
          />

          {/* 2. Target Market Men Lookbook (Purple Accent) */}
          <FileUploadZone
            title="2. Target Market Men Lookbook"
            subtitle="Upload men reference photos (custom_country_images_man)"
            badgeText="Men Style DNA"
            badgeColor="purple"
            files={customCountryImagesMan}
            onAddFiles={handleAddCountryImagesMan}
            onClearFiles={() => dispatch(clearCountryImagesMan())}
            buttonLabel="Select custom_country_images_man"
          />

          {/* 3. Target Market Women Lookbook (Rose Accent) */}
          <FileUploadZone
            title="3. Target Market Women Lookbook"
            subtitle="Upload women reference photos (custom_country_images_woman)"
            badgeText="Women Style DNA"
            badgeColor="rose"
            files={customCountryImagesWoman}
            onAddFiles={handleAddCountryImagesWoman}
            onClearFiles={() => dispatch(clearCountryImagesWoman())}
            buttonLabel="Select custom_country_images_woman"
          />
        </div>

        {/* Country Selector & Execution Button Bar */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '18px',
          alignItems: 'stretch'
        }}>
          <CountrySelector
            selectedCountry={customCountryName}
            onChangeCountry={(name) => dispatch(setCustomCountryName(name))}
          />

          <div style={{
            background: 'linear-gradient(135deg, #ffffff 0%, #fff7ed 100%)',
            borderRadius: '20px',
            border: '2px solid #fed7aa',
            padding: '24px',
            boxShadow: '0 8px 24px -4px rgba(245, 158, 11, 0.08)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            gap: '16px'
          }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Rocket size={18} color="#ea580c" />
                <h2 style={{ fontSize: '16px', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em', margin: 0 }}>
                  4. Execute ML &amp; Generate DSS Report
                </h2>
              </div>
              <p style={{ fontSize: '13px', color: '#64748b', margin: '4px 0 0 0' }}>
                Runs end-to-end 5-step ML pipeline with live progress streamed via Supabase.
              </p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <button
                id="ExecuteMLButton"
                onClick={handleExecuteML}
                disabled={!isButtonEnabled}
                style={{
                  background: isButtonEnabled
                    ? 'linear-gradient(135deg, #f59e0b 0%, #ea580c 50%, #e11d48 100%)'
                    : '#e2e8f0',
                  color: isButtonEnabled ? '#ffffff' : '#94a3b8',
                  border: isButtonEnabled ? 'none' : '1px solid #cbd5e1',
                  padding: '14px 22px',
                  borderRadius: '14px',
                  fontSize: '15px',
                  fontWeight: 900,
                  letterSpacing: '-0.01em',
                  cursor: isButtonEnabled ? 'pointer' : 'not-allowed',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '10px',
                  boxShadow: isButtonEnabled ? '0 6px 20px rgba(245, 158, 11, 0.4)' : 'none',
                  opacity: isButtonEnabled ? 1 : 0.65,
                  transform: isButtonEnabled ? 'scale(1)' : 'none',
                  transition: 'all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)',
                  width: '100%'
                }}
              >
                {isSubmitting ? (
                  <>
                    <div style={{
                      width: '18px',
                      height: '18px',
                      border: '2.5px solid #ffffff',
                      borderTopColor: 'transparent',
                      borderRadius: '50%',
                      animation: 'spin 0.8s linear infinite'
                    }} />
                    Processing ML Pipeline ({progress.percent}%)...
                  </>
                ) : isButtonEnabled ? (
                  <>
                    <Play size={18} fill="#ffffff" />
                    ExecuteMLButton ({totalFilesAttached} {totalFilesAttached === 1 ? 'file' : 'files'} attached)
                  </>
                ) : (
                  <>
                    <Play size={18} fill="#94a3b8" />
                    ExecuteMLButton (Disabled - Select files first)
                  </>
                )}
              </button>

              {!hasFilesSelected && (
                <span style={{ fontSize: '11.5px', color: '#dc2626', fontWeight: 600, textAlign: 'center' }}>
                  * Attach candidate catalog and/or lookbook files to enable ExecuteMLButton.
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Real-time Progress Visualizer */}
        <ProgressTracker />

        {/* Capstone Report Results Component */}
        {hasResults && <CapstoneReportComponent />}
      </main>

      <footer style={{
        background: '#ffffff',
        borderTop: '2px solid #fef3c7',
        padding: '16px 24px',
        textAlign: 'center',
        fontSize: '12.5px',
        color: '#64748b',
        fontWeight: 500
      }}>
        ✨ CV26 E-Commerce Product Catalog Expertise &bull; Step 81 Frontend (React + TypeScript + Redux-Saga) &bull; Step 82 Backend (FastAPI + Supabase)
      </footer>
    </div>
  );
};

export default App;
