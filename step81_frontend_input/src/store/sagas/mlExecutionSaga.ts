import { takeLatest, call, put, select, delay } from 'redux-saga/effects';
import { RootState } from '../index';
import {
  startExecution,
  executionSuccess,
  executionFailure,
} from '../slices/sessionSlice';
import {
  setProgressActive,
  updateProgressData,
} from '../slices/progressSlice';
import { setResultData, clearResults } from '../slices/resultSlice';
import { executeMLApi, fetchProgressApi, fetchResultsApi } from '../../services/api';

export const EXECUTE_ML_REQUEST = 'session/EXECUTE_ML_REQUEST';

export const executeMLAction = () => ({
  type: EXECUTE_ML_REQUEST,
});

function* handleExecuteML(): any {
  try {
    const sessionState = yield select((state: RootState) => state.session);
    const { userSessionGUID, customCountryName, customDatasetFiles, customCountryImages } = sessionState;

    yield put(startExecution());
    yield put(clearResults());
    yield put(setProgressActive(true));
    yield put(
      updateProgressData({
        percent: 5,
        stepId: 1,
        stepName: 'Connecting to Backend',
        details: `Submitting ${customDatasetFiles.length} catalog items and ${customCountryImages.length} country images...`,
      })
    );

    const datasetFiles = customDatasetFiles.map((item: any) => item.file);
    const countryFiles = customCountryImages.map((item: any) => item.file);

    yield call(executeMLApi, {
      userSessionGUID,
      customCountryName,
      customDatasetFiles: datasetFiles,
      customCountryImages: countryFiles,
    });

    // Polling loop with Supabase & Backend fallback
    let isCompleted = false;
    let attempts = 0;
    const maxAttempts = 300; // 5 minutes timeout

    while (!isCompleted && attempts < maxAttempts) {
      yield delay(1000);
      attempts++;

      try {
        const progressRes = yield call(fetchProgressApi, userSessionGUID);
        if (progressRes && progressRes.progress) {
          yield put(updateProgressData(progressRes.progress));
          if (progressRes.progress.percent >= 100) {
            isCompleted = true;
          }
        }

        if (isCompleted || attempts % 2 === 0) {
          const resultsRes = yield call(fetchResultsApi, userSessionGUID);
          if (resultsRes && resultsRes.results && resultsRes.results.kpis) {
            yield put(setResultData(resultsRes.results));
            yield put(executionSuccess());
            return;
          }
        }
      } catch (pollErr) {
        console.warn('Polling progress error:', pollErr);
      }
    }

    if (!isCompleted) {
      throw new Error('Pipeline execution timed out. Please check backend logs.');
    }
  } catch (error: any) {
    yield put(executionFailure(error.message || 'Execution failed'));
    yield put(
      updateProgressData({
        percent: 0,
        stepId: -1,
        stepName: 'Execution Error',
        details: error.message || 'Failed to complete ML pipeline.',
      })
    );
  }
}

export function* watchMLExecution() {
  yield takeLatest(EXECUTE_ML_REQUEST, handleExecuteML);
}
