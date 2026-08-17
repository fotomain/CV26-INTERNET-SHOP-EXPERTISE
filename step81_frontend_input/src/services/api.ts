import { BACKEND_URL } from '../constants/config';

export interface ExecuteMLParams {
  userSessionGUID: string;
  customCountryName: string;
  customDatasetFiles: File[];
  customCountryImagesMan: File[];
  customCountryImagesWoman: File[];
}

export async function executeMLApi(params: ExecuteMLParams): Promise<any> {
  const formData = new FormData();
  formData.append('userSessionGUID', params.userSessionGUID);
  formData.append('custom_country_name', params.customCountryName);

  params.customDatasetFiles.forEach((file) => {
    formData.append('custom_dataset_start', file);
  });

  params.customCountryImagesMan.forEach((file) => {
    formData.append('custom_country_images_man', file);
  });

  params.customCountryImagesWoman.forEach((file) => {
    formData.append('custom_country_images_woman', file);
  });

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
