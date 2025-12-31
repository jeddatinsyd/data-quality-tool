/**
 * API configuration utility
 * Uses environment variable for API URL, falls back to localhost for development
 */
export const getApiUrl = (): string => {
  // In browser/client-side, use NEXT_PUBLIC_ prefix
  if (typeof window !== 'undefined') {
    return process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  }
  // Server-side
  return process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
};

export const API_BASE_URL = getApiUrl();
