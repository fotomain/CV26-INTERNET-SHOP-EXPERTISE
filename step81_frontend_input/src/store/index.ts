import { configureStore } from '@reduxjs/toolkit';
import createSagaMiddleware from 'redux-saga';
import sessionReducer from './slices/sessionSlice';
import progressReducer from './slices/progressSlice';
import resultReducer from './slices/resultSlice';
import { rootSaga } from './sagas/rootSaga';

const sagaMiddleware = createSagaMiddleware();

export const store = configureStore({
  reducer: {
    session: sessionReducer,
    progress: progressReducer,
    result: resultReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false, // File objects are stored for binary upload
    }).concat(sagaMiddleware),
});

sagaMiddleware.run(rootSaga);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
