import { all, fork } from 'redux-saga/effects';
import { watchMLExecution } from './mlExecutionSaga';

export function* rootSaga() {
  yield all([fork(watchMLExecution)]);
}
