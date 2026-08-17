import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from './store';
import {
  setCustomCountryName,
  addDatasetFiles,
  clearDatasetFiles,
  addCountryImages,
  clearCountryImages,
  clearFileErrors,
} from './store/slices/sessionSlice';
import { updateProgressData } from './store/slices/progressSlice';
import { setResultData } from './store/slices/resultSlice';
import { executeMLAction } from './store/sagas/mlExecutionSaga';
import { subscribeToProgress, subscribeToResults } from './services/supabaseClient';
import { Header } from './components/Header';
import { FileUploadZone } from './components/FileUploadZone';
import { CountrySelector } from './components/CountrySelector';
import { ProgressTracker } from './components/ProgressTracker';
import { CapstoneReportComponent } from './components/CapstoneReportComponent';
import { Play, AlertCircle, Sparkles, CheckCircle2, ShieldCheck } from 'lucide-react';

export const App: React.FC = () => {
  const dispatch = useDispatch();
  const {
    userSessionGUID,
    customCountryName,
    customDatasetFiles,
    customCountryImages,
    fileErrors,
    isSubmitting,
    error,
  } = useSelector((state: RootState) => state.session);

  const { progress } = useSelector((state: RootState) => state.progress);
  const { hasResults } = useSelector((state: RootState) => state.result);

  // Subscribe to Supabase Realtime Channels for userSessionGUID
  useEffect(() => {
    if (!userSessionGUID) return;

    const unsubscribeProgress = subscribeToProgress(userSessionGUID, (p) => {
      dispatch(updateProgressData(p));
    });

    const unsubscribeResults = subscribeToResults(userSessionGUID, (r) => {
      dispatch(setResultData(r));
    });

    return () => {
      unsubscribeProgress();
      unsubscribeResults();
    };
  }, [userSessionGUID, dispatch]);

  const handleExecuteML = () => {
    dispatch(executeMLAction());
  };

  const totalFilesAttached = customDatasetFiles.length + customCountryImages.length;
  const isButtonEnabled = !isSubmitting;

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#f8fafc' }}>
      <Header />

      <main style={{
        flex: 1,
        maxWidth: '1280px',
        width: '100%',
        margin: '0 auto',
        padding: '24px 16px',
        display: 'flex',
        flexDirection: 'column',
        gap: '24px',
        minWidth: '350px'
      }}>
        {/* Scenario Banner */}
        <div style={{
          background: 'linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%)',
          border: '1px solid #bfdbfe',
          borderRadius: '16px',
          padding: '20px 24px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '16px'
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Sparkles size={18} color="#2563eb" />
              <h2 style={{ fontSize: '16px', fontWeight: 800, color: '#1e3a8a', margin: 0 }}>
                Custom ML Life Cycle Execution
              </h2>
            </div>
            <p style={{ fontSize: '13px', color: '#475569', margin: '4px 0 0 0', maxWidth: '750px' }}>
              Upload candidate catalog files and target country lookbook photos to run automated Fashion-MNIST classification, YOLOv8 + OpenCV demographic exclusions, 3-palette density extraction, and DSS marketing scoring.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <span style={{
              background: '#ffffff',
              border: '1px solid #cbd5e1',
              padding: '6px 12px',
              borderRadius: '8px',
              fontSize: '12px',
              fontWeight: 600,
              color: '#334155',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}>
              <ShieldCheck size={14} color="#16a34a" />
              Supabase Realtime Sync
            </span>
          </div>
        </div>

        {/* Validation Errors Display */}
        {fileErrors.length > 0 && (
          <div style={{
            background: '#fef2f2',
            border: '1px solid #fecaca',
            borderRadius: '12px',
            padding: '14px 18px',
            color: '#991b1b',
            fontSize: '13px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <strong>File Upload Warnings:</strong>
              <ul style={{ marginLeft: '20px', marginTop: '4px' }}>
                {fileErrors.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
            </div>
            <button
              onClick={() => dispatch(clearFileErrors())}
              style={{ background: 'none', border: 'none', color: '#dc2626', cursor: 'pointer', fontWeight: 700 }}
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Execution Error Banner */}
        {error && (
          <div style={{
            background: '#fef2f2',
            border: '1px solid #f87171',
            borderRadius: '12px',
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

        {/* Step 1 & Step 2 Upload Zones Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '20px'
        }}>
          {/* Custom Candidate Catalog */}
          <FileUploadZone
            title="1. Candidate Product Catalog"
            subtitle="Upload candidate apparel photos or CSV catalog (custom_dataset_start)"
            badgeText="Input Catalog"
            files={customDatasetFiles}
            onAddFiles={(files) => dispatch(addDatasetFiles(files))}
            onClearFiles={() => dispatch(clearDatasetFiles())}
            buttonLabel="Select custom_dataset_start"
          />

          {/* Custom Target Country Images */}
          <FileUploadZone
            title="2. Target Market Lookbook"
            subtitle="Upload authentic country fashion reference photos (custom_country_images)"
            badgeText="Style DNA"
            files={customCountryImages}
            onAddFiles={(files) => dispatch(addCountryImages(files))}
            onClearFiles={() => dispatch(clearCountryImages())}
            buttonLabel="Select custom_country_images"
          />
        </div>

        {/* Country Selector & Execution Button Bar */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '20px',
          alignItems: 'stretch'
        }}>
          <CountrySelector
            selectedCountry={customCountryName}
            onChangeCountry={(name) => dispatch(setCustomCountryName(name))}
          />

          <div style={{
            background: '#ffffff',
            borderRadius: '16px',
            border: '1px solid #e2e8f0',
            padding: '24px',
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            gap: '16px'
          }}>
            <div>
              <h2 style={{ fontSize: '16px', fontWeight: 700, color: '#0f172a', margin: 0 }}>
                3. Execute ML &amp; Generate DSS Report
              </h2>
              <p style={{ fontSize: '13px', color: '#64748b', margin: '4px 0 0 0' }}>
                Runs end-to-end 5-step ML pipeline with live step progress streamed via Supabase.
              </p>
            </div>

            <button
              id="ExecuteMLButton"
              onClick={handleExecuteML}
              disabled={!isButtonEnabled}
              style={{
                background: isButtonEnabled
                  ? 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)'
                  : '#94a3b8',
                color: '#ffffff',
                border: 'none',
                padding: '14px 24px',
                borderRadius: '12px',
                fontSize: '15px',
                fontWeight: 800,
                cursor: isButtonEnabled ? 'pointer' : 'not-allowed',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '10px',
                boxShadow: isButtonEnabled ? '0 4px 14px rgba(37, 99, 235, 0.35)' : 'none',
                transition: 'all 0.2s ease',
                width: '100%'
              }}
            >
              {isSubmitting ? (
                <>
                  <div style={{
                    width: '18px',
                    height: '18px',
                    border: '2px solid #ffffff',
                    borderTopColor: 'transparent',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite'
                  }} />
                  Processing ML Pipeline ({progress.percent}%)...
                </>
              ) : (
                <>
                  <Play size={18} fill="#ffffff" />
                  ExecuteMLButton ({totalFilesAttached > 0 ? `${totalFilesAttached} custom files attached` : 'Default Dataset Mode'})
                </>
              )}
            </button>
          </div>
        </div>

        {/* Real-time Progress Visualizer */}
        <ProgressTracker />

        {/* Capstone Report Results Component */}
        {hasResults && <CapstoneReportComponent />}
      </main>

      <footer style={{
        background: '#ffffff',
        borderTop: '1px solid #e2e8f0',
        padding: '16px 24px',
        textAlign: 'center',
        fontSize: '12px',
        color: '#64748b'
      }}>
        CV26 E-Commerce Product Catalog Expertise &bull; Step 81 Frontend (React + TypeScript + Tamagui + Redux-Saga) &bull; Step 82 Backend (FastAPI + Supabase)
      </footer>
    </div>
  );
};

export default App;
