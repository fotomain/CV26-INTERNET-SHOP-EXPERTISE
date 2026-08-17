/**
 * Session Identity Utilities (RUN5)
 * Generates userSessionGUID: UUID() on first app run and persists it in localStorage.
 * Always constant and camelCase.
 */

const STORAGE_KEY = 'userSessionGUID';

function generateUUID(): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export function getUserSessionGUID(): string {
  let guid = localStorage.getItem(STORAGE_KEY);
  if (!guid || guid.trim() === '') {
    guid = generateUUID();
    localStorage.setItem(STORAGE_KEY, guid);
  }
  return guid;
}

export function resetUserSessionGUID(): string {
  const newGuid = generateUUID();
  localStorage.setItem(STORAGE_KEY, newGuid);
  return newGuid;
}
