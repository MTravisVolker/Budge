import { AUTH_CONFIG } from "../config/auth";

class AuthService {
  constructor() {
    this.googleLoginUrl = AUTH_CONFIG.google.login;
    this.facebookLoginUrl = AUTH_CONFIG.facebook.login;
  }

  // Google OAuth2
  initiateGoogleLogin() {
    window.location.href = this.googleLoginUrl;
  }

  handleGoogleCallback() {
    // This will be called by the callback component
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (!code) {
      throw new Error("No authorization code received");
    }

    return this.exchangeCodeForToken("google", code);
  }

  // Facebook OAuth2
  initiateFacebookLogin() {
    window.location.href = this.facebookLoginUrl;
  }

  handleFacebookCallback() {
    // This will be called by the callback component
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (!code) {
      throw new Error("No authorization code received");
    }

    return this.exchangeCodeForToken("facebook", code);
  }

  async exchangeCodeForToken(provider, code) {
    try {
      const response = await fetch(
        `${AUTH_CONFIG[provider].callback}?code=${code}`,
        {
          method: "GET",
          credentials: "include", // Important for cookies
        }
      );

      if (!response.ok) {
        throw new Error(
          `Failed to exchange code for token: ${response.statusText}`
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error exchanging code for token:", error);
      throw error;
    }
  }

  // Store the token in localStorage
  setToken(token) {
    localStorage.setItem("auth_token", token);
  }

  // Get the token from localStorage
  getToken() {
    return localStorage.getItem("auth_token");
  }

  // Remove the token from localStorage
  removeToken() {
    localStorage.removeItem("auth_token");
  }

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.getToken();
  }
}

export const authService = new AuthService();
