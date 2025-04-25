const API_BASE_URL = "https://localhost:8000";

export const AUTH_CONFIG = {
  // Google OAuth2 endpoints
  google: {
    login: `${API_BASE_URL}/auth/google/login`,
    callback: `${API_BASE_URL}/auth/google/callback`,
    // These scopes match what we defined in the backend
    scope: "openid email profile",
  },
  // Facebook OAuth2 endpoints
  facebook: {
    login: `${API_BASE_URL}/auth/facebook/login`,
    callback: `${API_BASE_URL}/auth/facebook/callback`,
    // These scopes match what we defined in the backend
    scope: "email public_profile",
  },
  // Frontend callback URLs
  frontend: {
    googleCallback: "https://localhost:3000/auth/google/callback",
    facebookCallback: "https://localhost:3000/auth/facebook/callback",
  },
};
