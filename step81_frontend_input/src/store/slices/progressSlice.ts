import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface BatchUploadProgress {
  isUploading: boolean;
  currentBatch: number;
  totalBatches: number;
  uploadedFilesCount: number;
  totalFilesCount: number;
  percent: number; // 0% to 100% of batch uploads
  statusText: string;
  isComplete: boolean;
}

export interface ProgressData {
  percent: number;
  stepId: number;
  stepName: string;
  details: string;
  timestamp?: string;
}

export interface ProgressState {
  isActive: boolean;
  uploadProgress: BatchUploadProgress;
  progress: ProgressData;
  history: ProgressData[];
}

const initialUploadProgress: BatchUploadProgress = {
  isUploading: false,
  currentBatch: 0,
  totalBatches: 0,
  uploadedFilesCount: 0,
  totalFilesCount: 0,
  percent: 0,
  statusText: 'Ready to upload',
  isComplete: false,
};

const initialProgressData: ProgressData = {
  percent: 0,
  stepId: 0,
  stepName: 'Ready',
  details: 'Waiting for files upload before starting AI ML pipeline...',
};

const initialState: ProgressState = {
  isActive: false,
  uploadProgress: initialUploadProgress,
  progress: initialProgressData,
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
    setUploadProgress: (state, action: PayloadAction<Partial<BatchUploadProgress>>) => {
      state.uploadProgress = {
        ...state.uploadProgress,
        ...action.payload,
      };
    },
    resetUploadProgress: (state) => {
      state.uploadProgress = initialUploadProgress;
    },
    updateProgressData: (state, action: PayloadAction<ProgressData>) => {
      state.progress = action.payload;
      if (
        action.payload.stepId > 0 &&
        !state.history.some(
          (h) => h.stepId === action.payload.stepId && h.percent === action.payload.percent
        )
      ) {
        state.history.push(action.payload);
      }
    },
    resetProgress: (state) => {
      state.isActive = false;
      state.uploadProgress = initialUploadProgress;
      state.progress = initialProgressData;
      state.history = [];
    },
  },
});

export const {
  setProgressActive,
  setUploadProgress,
  resetUploadProgress,
  updateProgressData,
  resetProgress,
} = progressSlice.actions;

export default progressSlice.reducer;
