/**
 * API configuration utility
 * Uses environment variable for API URL, falls back to localhost for development
 */

export const getApiUrl = (): string => {
  let url: string;
  // In browser/client-side, use NEXT_PUBLIC_ prefix
  if (typeof window !== 'undefined') {
    url = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  } else {
    // Server-side
    url = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  }
  // Remove trailing slash to prevent double slashes
  return url.replace(/\/+$/, '');
};

export const API_BASE_URL = getApiUrl();

/**
 * Helper function to construct API URLs safely
 * Ensures no double slashes regardless of how API_BASE_URL is set
 */
export const apiUrl = (path: string): string => {
  const base = API_BASE_URL.replace(/\/+$/, ''); // Remove trailing slashes
  const cleanPath = path.startsWith('/') ? path : `/${path}`; // Ensure path starts with /
  return `${base}${cleanPath}`;
};
