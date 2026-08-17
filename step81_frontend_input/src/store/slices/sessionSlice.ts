import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { getUserSessionGUID } from '../../utils/session';
import { DEFAULT_FILE_SIZE_LIMIT_BYTES, DEFAULT_NUMBER_OF_FILES } from '../../constants/config';
import { registerFile, removeFiles, clearAllFiles } from '../../utils/fileRegistry';

export interface FileItem {
  id: string;
  name: string;
  size: number;
  type: string;
  lastModified: number;
}

export interface SessionState {
  readonly userSessionGUID: string;
  customCountryName: string;
  customDatasetFiles: FileItem[];
  customCountryImagesMan: FileItem[];
  customCountryImagesWoman: FileItem[];
  fileErrors: string[];
  isSubmitting: boolean;
  error: string | null;
}

const initialState: SessionState = {
  userSessionGUID: getUserSessionGUID(),
  customCountryName: 'United States',
  customDatasetFiles: [],
  customCountryImagesMan: [],
  customCountryImagesWoman: [],
  fileErrors: [],
  isSubmitting: false,
  error: null,
};

export const sessionSlice = createSlice({
  name: 'session',
  initialState,
  reducers: {
    setCustomCountryName: (state, action: PayloadAction<string>) => {
      state.customCountryName = action.payload;
    },
    addDatasetFiles: (state, action: PayloadAction<FileItem[]>) => {
      state.customDatasetFiles.push(...action.payload);
    },
    clearDatasetFiles: (state) => {
      const ids = state.customDatasetFiles.map((f) => f.id);
      removeFiles(ids);
      state.customDatasetFiles = [];
    },
    addCountryImagesMan: (state, action: PayloadAction<FileItem[]>) => {
      state.customCountryImagesMan.push(...action.payload);
    },
    clearCountryImagesMan: (state) => {
      const ids = state.customCountryImagesMan.map((f) => f.id);
      removeFiles(ids);
      state.customCountryImagesMan = [];
    },
    addCountryImagesWoman: (state, action: PayloadAction<FileItem[]>) => {
      state.customCountryImagesWoman.push(...action.payload);
    },
    clearCountryImagesWoman: (state) => {
      const ids = state.customCountryImagesWoman.map((f) => f.id);
      removeFiles(ids);
      state.customCountryImagesWoman = [];
    },
    setFileErrors: (state, action: PayloadAction<string[]>) => {
      state.fileErrors = action.payload;
    },
    clearFileErrors: (state) => {
      state.fileErrors = [];
    },
    startExecution: (state) => {
      state.isSubmitting = true;
      state.error = null;
    },
    executionSuccess: (state) => {
      state.isSubmitting = false;
    },
    executionFailure: (state, action: PayloadAction<string>) => {
      state.isSubmitting = false;
      state.error = action.payload;
    },
  },
});

export const {
  setCustomCountryName,
  addDatasetFiles,
  clearDatasetFiles,
  addCountryImagesMan,
  clearCountryImagesMan,
  addCountryImagesWoman,
  clearCountryImagesWoman,
  setFileErrors,
  clearFileErrors,
  startExecution,
  executionSuccess,
  executionFailure,
} = sessionSlice.actions;

export default sessionSlice.reducer;
