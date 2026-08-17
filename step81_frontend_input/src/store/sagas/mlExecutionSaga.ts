import { takeLatest, call, put, select, delay } from 'redux-saga/effects';
import { RootState } from '../index';
import {
  startExecution,
  executionSuccess,
  executionFailure,
} from '../slices/sessionSlice';
import {
  setProgressActive,
  setUploadProgress,
  updateProgressData,
} from '../slices/progressSlice';
import { setResultData, clearResults } from '../slices/resultSlice';
import { executeMLApi, uploadBatchApi, clearSessionApi, fetchProgressApi, fetchResultsApi } from '../../services/api';
import { autoDownloadCsvFiles } from '../../utils/fileDownloader';
import { getFiles } from '../../utils/fileRegistry';
import { FILES_PER_1_BATCH } from '../../constants/config';

export const EXECUTE_ML_REQUEST = 'session/EXECUTE_ML_REQUEST';

export const executeMLAction = () => ({
  type: EXECUTE_ML_REQUEST,
});

function* handleExecuteML(): any {
  try {
    const sessionState = yield select((state: RootState) => state.session);
    const {
      userSessionGUID,
      customCountryName,
      customDatasetFiles,
      customCountryImagesMan,
      customCountryImagesWoman,
    } = sessionState;

    yield put(startExecution());
    yield put(clearResults());
    yield put(setProgressActive(true));

    // Clear subfolder custom_data/+userSessionGUID before new ML steps
    yield call(clearSessionApi, userSessionGUID);

    const datasetFiles: File[] = getFiles(customDatasetFiles.map((item: any) => item.id));
    const manFiles: File[] = getFiles(customCountryImagesMan.map((item: any) => item.id));
    const womanFiles: File[] = getFiles(customCountryImagesWoman.map((item: any) => item.id));

    // Chunk into batches (FILES_PER_1_BATCH = 10)
    const datasetBatches: File[][] = [];
    for (let i = 0; i < datasetFiles.length; i += FILES_PER_1_BATCH) {
      datasetBatches.push(datasetFiles.slice(i, i + FILES_PER_1_BATCH));
    }
    const manBatches: File[][] = [];
    for (let i = 0; i < manFiles.length; i += FILES_PER_1_BATCH) {
      manBatches.push(manFiles.slice(i, i + FILES_PER_1_BATCH));
    }
    const womanBatches: File[][] = [];
    for (let i = 0; i < womanFiles.length; i += FILES_PER_1_BATCH) {
      womanBatches.push(womanFiles.slice(i, i + FILES_PER_1_BATCH));
    }

    const totalBatchCount = Math.max(1, datasetBatches.length + manBatches.length + womanBatches.length);
    let currentBatchIndex = 0;
    const totalFilesCount = datasetFiles.length + manFiles.length + womanFiles.length;
    let uploadedFilesCount = 0;

    yield put(
      setUploadProgress({
        isUploading: true,
        currentBatch: 0,
        totalBatches: totalBatchCount,
        uploadedFilesCount: 0,
        totalFilesCount,
        percent: 0,
        statusText: `Preparing ${totalFilesCount} files across ${totalBatchCount} batches (10 files/batch)...`,
        isComplete: false,
      })
    );

    // 1. Upload Dataset Batches
    for (let b = 0; b < datasetBatches.length; b++) {
      currentBatchIndex++;
      uploadedFilesCount += datasetBatches[b].length;
      const uploadPct = Math.round((currentBatchIndex / totalBatchCount) * 100);
      yield put(
        setUploadProgress({
          isUploading: true,
          currentBatch: currentBatchIndex,
          totalBatches: totalBatchCount,
          uploadedFilesCount,
          totalFilesCount,
          percent: uploadPct,
          statusText: `Uploading Catalog Batch ${b + 1}/${datasetBatches.length} (${datasetBatches[b].length} files)...`,
          isComplete: false,
        })
      );
      yield call(uploadBatchApi, {
        userSessionGUID,
        targetType: 'dataset',
        batchIndex: currentBatchIndex,
        totalBatches: totalBatchCount,
        files: datasetBatches[b],
      });
    }

    // 2. Upload Men Lookbook Batches
    for (let b = 0; b < manBatches.length; b++) {
      currentBatchIndex++;
      uploadedFilesCount += manBatches[b].length;
      const uploadPct = Math.round((currentBatchIndex / totalBatchCount) * 100);
      yield put(
        setUploadProgress({
          isUploading: true,
          currentBatch: currentBatchIndex,
          totalBatches: totalBatchCount,
          uploadedFilesCount,
          totalFilesCount,
          percent: uploadPct,
          statusText: `Uploading Men Lookbook Batch ${b + 1}/${manBatches.length} (${manBatches[b].length} files)...`,
          isComplete: false,
        })
      );
      yield call(uploadBatchApi, {
        userSessionGUID,
        targetType: 'man',
        batchIndex: currentBatchIndex,
        totalBatches: totalBatchCount,
        files: manBatches[b],
      });
    }

    // 3. Upload Women Lookbook Batches
    for (let b = 0; b < womanBatches.length; b++) {
      currentBatchIndex++;
      uploadedFilesCount += womanBatches[b].length;
      const uploadPct = Math.round((currentBatchIndex / totalBatchCount) * 100);
      yield put(
        setUploadProgress({
          isUploading: true,
          currentBatch: currentBatchIndex,
          totalBatches: totalBatchCount,
          uploadedFilesCount,
          totalFilesCount,
          percent: uploadPct,
          statusText: `Uploading Women Lookbook Batch ${b + 1}/${womanBatches.length} (${womanBatches[b].length} files)...`,
          isComplete: false,
        })
      );
      yield call(uploadBatchApi, {
        userSessionGUID,
        targetType: 'woman',
        batchIndex: currentBatchIndex,
        totalBatches: totalBatchCount,
        files: womanBatches[b],
      });
    }

    // 4. Mark Batch Upload 100% Complete
    yield put(
      setUploadProgress({
        isUploading: false,
        currentBatch: totalBatchCount,
        totalBatches: totalBatchCount,
        uploadedFilesCount: totalFilesCount,
        totalFilesCount,
        percent: 100,
        statusText: `✓ All ${totalFilesCount} files are at the server. Starting AI ML Pipeline...`,
        isComplete: true,
      })
    );

    // 5. Only when all files are at the server -> Start AI ML Pipeline
    yield put(
      updateProgressData({
        percent: 0,
        stepId: 1,
        stepName: 'Mission 1: Product Ingestion & Classification',
        details: `All files on server. Launching Fashion-MNIST CNN and Style Intelligence for ${customCountryName}...`,
      })
    );

    yield call(executeMLApi, {
      userSessionGUID,
      customCountryName,
    });

    // Polling loop with Supabase & Backend fallback
    let isCompleted = false;
    let attempts = 0;
    const maxAttempts = 300; // 5 minutes timeout

    while (!isCompleted && attempts < maxAttempts) {
      yield delay(1500);
      attempts++;

      try {
        const progressRes = yield call(fetchProgressApi, userSessionGUID);
        if (progressRes && progressRes.progress) {
          yield put(updateProgressData(progressRes.progress));
          if (progressRes.progress.percent >= 100) {
            isCompleted = true;
          }
        }

        const resultsRes = yield call(fetchResultsApi, userSessionGUID);
        if (resultsRes && resultsRes.status === 'completed' && resultsRes.results) {
          yield put(setResultData(resultsRes.results));
          yield put(executionSuccess());
          // Auto download result CSVs
          yield call(autoDownloadCsvFiles, userSessionGUID);
          isCompleted = true;
          break;
        }
      } catch (pollErr) {
        console.warn('Polling status warning:', pollErr);
      }
    }

    if (!isCompleted) {
      throw new Error('Execution timed out after 5 minutes.');
    }
  } catch (error: any) {
    yield put(executionFailure(error.message || 'ML Execution pipeline failed.'));
    yield put(
      updateProgressData({
        percent: 0,
        stepId: -1,
        stepName: 'Execution Error',
        details: error.message || 'Error occurred during processing.',
      })
    );
  }
}

export function* watchMLExecution() {
  yield takeLatest(EXECUTE_ML_REQUEST, handleExecuteML);
}
