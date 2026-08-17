import { BACKEND_URL } from '../constants/config';

export interface ExecuteMLParams {
  userSessionGUID: string;
  customCountryName: string;
  customDatasetFiles?: File[];
  customCountryImagesMan?: File[];
  customCountryImagesWoman?: File[];
}

export async function clearSessionApi(userSessionGUID: string): Promise<any> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/clear-session/${userSessionGUID}`, {
      method: 'POST',
    });
    return response.json();
  } catch (e) {
    console.warn(`Could not clear session subfolder for ${userSessionGUID}:`, e);
    return null;
  }
}

export interface UploadBatchParams {
  userSessionGUID: string;
  targetType: 'dataset' | 'man' | 'woman';
  batchIndex: number;
  totalBatches: number;
  files: File[];
}

export async function uploadBatchApi(params: UploadBatchParams): Promise<any> {
  const formData = new FormData();
  formData.append('userSessionGUID', params.userSessionGUID);
  formData.append('targetType', params.targetType);
  formData.append('batchIndex', params.batchIndex.toString());
  formData.append('totalBatches', params.totalBatches.toString());

  params.files.forEach((file) => {
    formData.append('files', file);
  });

  const response = await fetch(`${BACKEND_URL}/api/upload-batch`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorDetail = 'Failed to upload batch';
    try {
      const err = await response.json();
      errorDetail = err.detail || errorDetail;
    } catch {
      errorDetail = `HTTP ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export async function executeMLApi(params: ExecuteMLParams): Promise<any> {
  const formData = new FormData();
  formData.append('userSessionGUID', params.userSessionGUID);
  formData.append('custom_country_name', params.customCountryName);

  if (params.customDatasetFiles) {
    params.customDatasetFiles.forEach((file) => {
      formData.append('custom_dataset_start', file);
    });
  }

  if (params.customCountryImagesMan) {
    params.customCountryImagesMan.forEach((file) => {
      formData.append('custom_country_images_man', file);
    });
  }

  if (params.customCountryImagesWoman) {
    params.customCountryImagesWoman.forEach((file) => {
      formData.append('custom_country_images_woman', file);
    });
  }

  const response = await fetch(`${BACKEND_URL}/api/execute-ml`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorDetail = 'Failed to execute ML pipeline';
    try {
      const err = await response.json();
      errorDetail = err.detail || errorDetail;
    } catch {
      errorDetail = `HTTP ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export async function fetchProgressApi(userSessionGUID: string): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/api/progress/${userSessionGUID}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch progress for ${userSessionGUID}`);
  }
  return response.json();
}

export async function fetchResultsApi(userSessionGUID: string): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/api/results/${userSessionGUID}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch results for ${userSessionGUID}`);
  }
  return response.json();
}
