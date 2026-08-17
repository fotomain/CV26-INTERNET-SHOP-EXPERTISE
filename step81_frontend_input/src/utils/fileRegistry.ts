/**
 * In-memory registry for binary File objects.
 * Keeps Redux state 100% serializable by storing only metadata in Redux
 * and raw File objects in this module registry.
 */

const fileMap = new Map<string, File>();

export function registerFile(id: string, file: File): void {
  fileMap.set(id, file);
}

export function getFile(id: string): File | undefined {
  return fileMap.get(id);
}

export function getFiles(ids: string[]): File[] {
  const result: File[] = [];
  ids.forEach((id) => {
    const f = fileMap.get(id);
    if (f) result.push(f);
  });
  return result;
}

export function removeFile(id: string): void {
  fileMap.delete(id);
}

export function removeFiles(ids: string[]): void {
  ids.forEach((id) => fileMap.delete(id));
}

export function clearAllFiles(): void {
  fileMap.clear();
}
