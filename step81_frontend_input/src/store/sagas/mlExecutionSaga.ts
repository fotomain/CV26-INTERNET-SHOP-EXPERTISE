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
    yield put(
      updateProgressData({
        percent: 5,
        stepId: 1,
        stepName: 'Connecting to Backend',
        details: `Submitting ${customDatasetFiles.length} catalog items, ${customCountryImagesMan.length} men photos, and ${customCountryImagesWoman.length} women photos...`,
      })
    );

    const datasetFiles = customDatasetFiles.map((item: any) => item.file);
    const manFiles = customCountryImagesMan.map((item: any) => item.file);
    const womanFiles = customCountryImagesWoman.map((item: any) => item.file);

    yield call(executeMLApi, {
      userSessionGUID,
      customCountryName,
      customDatasetFiles: datasetFiles,
      customCountryImagesMan: manFiles,
      customCountryImagesWoman: womanFiles,
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
            break;
          }
          if (progressRes.progress.stepId === -1) {
            throw new Error(progressRes.progress.details || 'Execution failed on server');
          }
        }
      } catch (err: any) {
        // Continue polling if network glitch
        if (err.message && err.message.includes('failed on server')) {
          throw err;
        }
      }
    }

    // Fetch Final Results JSON
    const resultsRes = yield call(fetchResultsApi, userSessionGUID);
    if (resultsRes && resultsRes.results) {
      yield put(setResultData(resultsRes.results));
    }

    yield put(executionSuccess());
  } catch (error: any) {
    yield put(executionFailure(error.message || 'Execution pipeline encountered an unexpected error.'));
  }
}

export function* watchMLExecution() {
  yield takeLatest(EXECUTE_ML_REQUEST, handleExecuteML);
}

export function* rootSaga() {
  yield takeLatest(EXECUTE_ML_REQUEST, handleExecuteML);
}
