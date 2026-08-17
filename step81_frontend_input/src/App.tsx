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
import { Play, AlertCircle, Sparkles, ShieldCheck, Zap } from 'lucide-react';

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
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#fafafa' }}>
      <Header />

      <main style={{
        flex: 1,
        maxWidth: '1240px',
        width: '100%',
        margin: '0 auto',
        padding: '24px 16px',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        minWidth: '350px'
      }}>
        {/* Tamagui.dev Style Hero Card */}
        <div style={{
          background: '#ffffff',
          border: '1px solid rgba(0, 0, 0, 0.08)',
          borderRadius: '20px',
          padding: '28px 32px',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.02), 0 10px 30px -4px rgba(0, 0, 0, 0.05)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '20px'
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <span style={{
                background: '#f4f4f5',
                color: '#18181b',
                border: '1px solid #e4e4e7',
                fontSize: '11px',
                fontWeight: 700,
                padding: '2px 8px',
                borderRadius: '999px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                <Zap size={12} color="#f59e0b" fill="#f59e0b" />
                Next-Gen E-Commerce Style DSS
              </span>
              <span style={{
                background: '#f4f4f5',
                color: '#71717a',
                border: '1px solid #e4e4e7',
                fontSize: '11px',
                fontWeight: 600,
                padding: '2px 8px',
                borderRadius: '999px'
              }}>
                FastAPI + Tamagui
              </span>
            </div>
            <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#09090b', letterSpacing: '-0.03em', margin: 0 }}>
              Purchase Manager Catalog &amp; Style AI Engine
            </h2>
            <p style={{ fontSize: '13px', color: '#71717a', margin: '6px 0 0 0', maxWidth: '720px', lineHeight: 1.5 }}>
              Upload candidate catalog items and target country lookbook photos to run automated Fashion-MNIST classification, YOLOv8 + OpenCV demographic segmentation, 3-palette density extraction, and CIELAB &Delta;E matching.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <span style={{
              background: '#ffffff',
              border: '1px solid #e4e4e7',
              padding: '6px 12px',
              borderRadius: '8px',
              fontSize: '11px',
              fontWeight: 600,
              color: '#3f3f46',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              boxShadow: '0 1px 2px rgba(0, 0, 0, 0.03)'
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
            padding: '12px 16px',
            color: '#991b1b',
            fontSize: '12px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <strong>Upload Warnings:</strong>
              <ul style={{ marginLeft: '16px', marginTop: '3px' }}>
                {fileErrors.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
            </div>
            <button
              onClick={() => dispatch(clearFileErrors())}
              style={{ background: 'none', border: 'none', color: '#dc2626', cursor: 'pointer', fontWeight: 700, fontSize: '11px' }}
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
            padding: '12px 16px',
            color: '#b91c1c',
            fontSize: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <AlertCircle size={16} />
            <div>
              <strong>Execution Error:</strong> {error}
            </div>
          </div>
        )}

        {/* Upload Zones Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '16px'
        }}>
          {/* Custom Candidate Catalog */}
          <FileUploadZone
            title="1. Candidate Product Catalog"
            subtitle="Upload apparel photos or CSV catalog (custom_dataset_start)"
            badgeText="Input Catalog"
            files={customDatasetFiles}
            onAddFiles={(files) => dispatch(addDatasetFiles(files))}
            onClearFiles={() => dispatch(clearDatasetFiles())}
            buttonLabel="Select custom_dataset_start"
          />

          {/* Custom Target Country Images */}
          <FileUploadZone
            title="2. Target Market Lookbook"
            subtitle="Upload authentic reference lookbook photos (custom_country_images)"
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
          gap: '16px',
          alignItems: 'stretch'
        }}>
          <CountrySelector
            selectedCountry={customCountryName}
            onChangeCountry={(name) => dispatch(setCustomCountryName(name))}
          />

          <div style={{
            background: '#ffffff',
            borderRadius: '16px',
            border: '1px solid rgba(0, 0, 0, 0.08)',
            padding: '24px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.02), 0 6px 24px -4px rgba(0, 0, 0, 0.04)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            gap: '16px'
          }}>
            <div>
              <h2 style={{ fontSize: '15px', fontWeight: 700, color: '#09090b', letterSpacing: '-0.02em', margin: 0 }}>
                3. Execute ML &amp; Generate DSS Report
              </h2>
              <p style={{ fontSize: '12px', color: '#71717a', margin: '4px 0 0 0' }}>
                Runs end-to-end 5-step ML pipeline with live progress streamed via Supabase.
              </p>
            </div>

            <button
              id="ExecuteMLButton"
              onClick={handleExecuteML}
              disabled={!isButtonEnabled}
              style={{
                background: isButtonEnabled ? '#09090b' : '#a1a1aa',
                color: '#ffffff',
                border: 'none',
                padding: '13px 20px',
                borderRadius: '10px',
                fontSize: '14px',
                fontWeight: 700,
                letterSpacing: '-0.01em',
                cursor: isButtonEnabled ? 'pointer' : 'not-allowed',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                boxShadow: isButtonEnabled ? '0 4px 14px rgba(0, 0, 0, 0.15)' : 'none',
                transition: 'all 0.15s ease',
                width: '100%'
              }}
            >
              {isSubmitting ? (
                <>
                  <div style={{
                    width: '16px',
                    height: '16px',
                    border: '2px solid #ffffff',
                    borderTopColor: 'transparent',
                    borderRadius: '50%',
                    animation: 'spin 0.8s linear infinite'
                  }} />
                  Processing ML Pipeline ({progress.percent}%)...
                </>
              ) : (
                <>
                  <Play size={16} fill="#ffffff" />
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
        borderTop: '1px solid rgba(0, 0, 0, 0.07)',
        padding: '14px 24px',
        textAlign: 'center',
        fontSize: '12px',
        color: '#71717a'
      }}>
        CV26 E-Commerce Product Catalog Expertise &bull; Step 81 Frontend (React + TypeScript + Tamagui Light + Redux-Saga) &bull; Step 82 Backend (FastAPI + Supabase)
      </footer>
    </div>
  );
};

export default App;
