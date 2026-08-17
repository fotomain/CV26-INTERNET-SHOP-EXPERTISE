import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { SupabaseResultPayload } from '../../services/supabaseClient';

export interface ResultState {
  hasResults: boolean;
  resultData: SupabaseResultPayload | null;
  selectedCategoryFilter: string;
  selectedTierFilter: string;
  selectedApprovalFilter: string;
  searchQuery: string;
}

const initialState: ResultState = {
  hasResults: false,
  resultData: null,
  selectedCategoryFilter: 'ALL',
  selectedTierFilter: 'ALL',
  selectedApprovalFilter: 'ALL',
  searchQuery: '',
};

export const resultSlice = createSlice({
  name: 'result',
  initialState,
  reducers: {
    setResultData: (state, action: PayloadAction<SupabaseResultPayload>) => {
      state.resultData = action.payload;
      state.hasResults = true;
    },
    clearResults: (state) => {
      state.hasResults = false;
      state.resultData = null;
    },
    setCategoryFilter: (state, action: PayloadAction<string>) => {
      state.selectedCategoryFilter = action.payload;
    },
    setTierFilter: (state, action: PayloadAction<string>) => {
      state.selectedTierFilter = action.payload;
    },
    setApprovalFilter: (state, action: PayloadAction<string>) => {
      state.selectedApprovalFilter = action.payload;
    },
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
    },
  },
});

export const {
  setResultData,
  clearResults,
  setCategoryFilter,
  setTierFilter,
  setApprovalFilter,
  setSearchQuery,
} = resultSlice.actions;

export default resultSlice.reducer;
