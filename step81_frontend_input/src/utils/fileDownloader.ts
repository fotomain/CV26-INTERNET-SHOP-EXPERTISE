import { BACKEND_URL } from '../constants/config';

// Track downloaded sessions to avoid duplicate triggers
const downloadedSessions = new Set<string>();

/**
 * Automatically fetches and saves result_good_for_new_marketing.csv and
 * result_not_good_for_new_marketing.csv from step82_backend_exec without prompting the user.
 */
export async function autoDownloadCsvFiles(userSessionGUID: string, backendUrl: string = BACKEND_URL): Promise<void> {
  if (!userSessionGUID || downloadedSessions.has(userSessionGUID)) {
    return;
  }

  downloadedSessions.add(userSessionGUID);

  const filesToDownload = [
    'result_good_for_new_marketing.csv',
    'result_not_good_for_new_marketing.csv'
  ];

  for (const filename of filesToDownload) {
    try {
      const fileUrl = `${backendUrl}/api/download/${userSessionGUID}/${filename}`;
      const response = await fetch(fileUrl);

      if (!response.ok) {
        console.warn(`[AutoDownload] Could not fetch ${filename} from backend: HTTP ${response.status}`);
        continue;
      }

      const blob = await response.blob();
      const objectUrl = window.URL.createObjectURL(blob);

      const downloadAnchor = document.createElement('a');
      downloadAnchor.href = objectUrl;
      downloadAnchor.download = filename;
      downloadAnchor.style.display = 'none';
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();

      // Clean up DOM and memory
      setTimeout(() => {
        window.URL.revokeObjectURL(objectUrl);
        downloadAnchor.remove();
      }, 500);

      console.log(`[AutoDownload] Successfully auto-saved ${filename}`);
    } catch (error) {
      console.warn(`[AutoDownload] Failed auto-download for ${filename}:`, error);
    }
  }
}
