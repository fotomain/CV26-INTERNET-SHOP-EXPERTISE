import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { getUserSessionGUID } from '../../utils/session';
import { DEFAULT_FILE_SIZE_LIMIT_BYTES, DEFAULT_NUMBER_OF_FILES } from '../../constants/config';

export interface FileItem {
  id: string;
  name: string;
  size: number;
  type: string;
  file: File;
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
    addDatasetFiles: (state, action: PayloadAction<File[]>) => {
      const newErrors: string[] = [];
      const validFiles: FileItem[] = [];

      action.payload.forEach((file) => {
        if (file.size > DEFAULT_FILE_SIZE_LIMIT_BYTES) {
          newErrors.push(`"${file.name}" exceeds 1MB limit (${(file.size / (1024 * 1024)).toFixed(2)}MB).`);
        } else if (state.customDatasetFiles.length + validFiles.length >= DEFAULT_NUMBER_OF_FILES) {
          newErrors.push(`Exceeded maximum limit of ${DEFAULT_NUMBER_OF_FILES} files.`);
        } else {
          validFiles.push({
            id: `${file.name}-${file.size}-${Date.now()}-${Math.random()}`,
            name: file.name,
            size: file.size,
            type: file.type,
            file: file,
          });
        }
      });

      state.customDatasetFiles.push(...validFiles);
      state.fileErrors = newErrors;
    },
    clearDatasetFiles: (state) => {
      state.customDatasetFiles = [];
    },
    addCountryImagesMan: (state, action: PayloadAction<File[]>) => {
      const newErrors: string[] = [];
      const validFiles: FileItem[] = [];

      action.payload.forEach((file) => {
        if (file.size > DEFAULT_FILE_SIZE_LIMIT_BYTES) {
          newErrors.push(`"${file.name}" exceeds 1MB limit (${(file.size / (1024 * 1024)).toFixed(2)}MB).`);
        } else if (state.customCountryImagesMan.length + validFiles.length >= DEFAULT_NUMBER_OF_FILES) {
          newErrors.push(`Exceeded maximum limit of ${DEFAULT_NUMBER_OF_FILES} files.`);
        } else {
          validFiles.push({
            id: `${file.name}-${file.size}-${Date.now()}-${Math.random()}`,
            name: file.name,
            size: file.size,
            type: file.type,
            file: file,
          });
        }
      });

      state.customCountryImagesMan.push(...validFiles);
      state.fileErrors = newErrors;
    },
    clearCountryImagesMan: (state) => {
      state.customCountryImagesMan = [];
    },
    addCountryImagesWoman: (state, action: PayloadAction<File[]>) => {
      const newErrors: string[] = [];
      const validFiles: FileItem[] = [];

      action.payload.forEach((file) => {
        if (file.size > DEFAULT_FILE_SIZE_LIMIT_BYTES) {
          newErrors.push(`"${file.name}" exceeds 1MB limit (${(file.size / (1024 * 1024)).toFixed(2)}MB).`);
        } else if (state.customCountryImagesWoman.length + validFiles.length >= DEFAULT_NUMBER_OF_FILES) {
          newErrors.push(`Exceeded maximum limit of ${DEFAULT_NUMBER_OF_FILES} files.`);
        } else {
          validFiles.push({
            id: `${file.name}-${file.size}-${Date.now()}-${Math.random()}`,
            name: file.name,
            size: file.size,
            type: file.type,
            file: file,
          });
        }
      });

      state.customCountryImagesWoman.push(...validFiles);
      state.fileErrors = newErrors;
    },
    clearCountryImagesWoman: (state) => {
      state.customCountryImagesWoman = [];
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
  clearFileErrors,
  startExecution,
  executionSuccess,
  executionFailure,
} = sessionSlice.actions;

export default sessionSlice.reducer;
