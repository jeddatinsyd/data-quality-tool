/**
 * API configuration utility
 * Uses environment variable for API URL, falls back to localhost for development
 */
<<<<<<< HEAD
const getApiUrl = (): string => {
  // In browser/client-side, use NEXT_PUBLIC_ prefix
  let url: string;
  if (typeof window !== 'undefined') {
    url = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  } else {
    // Server-side
    url = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  }
  // Remove trailing slash to prevent double slashes
  return url.replace(/\/+$/, '');
=======
export const getApiUrl = (): string => {
  // In browser/client-side, use NEXT_PUBLIC_ prefix
  if (typeof window !== 'undefined') {
    return process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  }
  // Server-side
  return process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
>>>>>>> e8b800629f67e72a170ac77ac0aca737245dc9f2
};

export const API_BASE_URL = getApiUrl();

<<<<<<< HEAD
/**
 * Helper function to construct API URLs safely
 * Ensures no double slashes regardless of how API_BASE_URL is set
 */
export const apiUrl = (path: string): string => {
  const base = API_BASE_URL.replace(/\/+$/, ''); // Remove trailing slashes
  const cleanPath = path.startsWith('/') ? path : `/${path}`; // Ensure path starts with /
  return `${base}${cleanPath}`;
};
=======
>>>>>>> e8b800629f67e72a170ac77ac0aca737245dc9f2
