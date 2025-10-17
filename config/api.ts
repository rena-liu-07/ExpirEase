// API Configuration
import { Platform } from 'react-native';

// Development API base URL
const getBaseUrl = (): string => {
  if (__DEV__) {
    // For development
    if (Platform.OS === 'android') {
      // Android emulator uses 10.0.2.2 to reach host machine
      return 'http://10.0.2.2:5000';
    } else if (Platform.OS === 'ios') {
      // iOS simulator can use localhost
      return 'http://localhost:5000';
    } else {
      // Web or other platforms
      return 'http://localhost:5000';
    }
  } else {
    // Production URL - replace with your actual production API URL
    return 'https://your-production-api.com';
  }
};

export const API_BASE_URL = getBaseUrl();

// API endpoints
export const API_ENDPOINTS = {
  EXPIRING_INGREDIENTS: `${API_BASE_URL}/expiring-ingredients`,
  GENERATE_RECIPE: `${API_BASE_URL}/generate-recipe`,
  ALL_INGREDIENTS: `${API_BASE_URL}/all-ingredients`,
  SEARCH: `${API_BASE_URL}/search`,
  ADD_INGREDIENT: `${API_BASE_URL}/add-ingredient`,
  DELETE_INGREDIENT: `${API_BASE_URL}/delete-ingredient`,
} as const;

// Utility function for making API calls with error handling
export const apiCall = async (url: string, options?: RequestInit) => {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call failed:', url, error);
    throw error;
  }
};