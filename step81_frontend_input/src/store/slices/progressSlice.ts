import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface ProgressData {
  percent: number;
  stepId: number;
  stepName: string;
  details: string;
  timestamp?: string;
}

export interface ProgressState {
  isActive: boolean;
  progress: ProgressData;
  history: ProgressData[];
}

const initialState: ProgressState = {
  isActive: false,
  progress: {
    percent: 0,
    stepId: 0,
    stepName: 'Ready',
    details: 'Attach files and select country to start ML pipeline.',
  },
  history: [],
};

export const progressSlice = createSlice({
  name: 'progress',
  initialState,
  reducers: {
    setProgressActive: (state, action: PayloadAction<boolean>) => {
      state.isActive = action.payload;
      if (action.payload) {
        state.history = [];
      }
    },
    updateProgressData: (state, action: PayloadAction<ProgressData>) => {
      state.progress = action.payload;
      if (
        !state.history.some(
          (h) => h.stepId === action.payload.stepId && h.percent === action.payload.percent
        )
      ) {
        state.history.push(action.payload);
      }
    },
    resetProgress: (state) => {
      state.isActive = false;
      state.progress = initialState.progress;
      state.history = [];
    },
  },
});

export const { setProgressActive, updateProgressData, resetProgress } = progressSlice.actions;
export default progressSlice.reducer;
