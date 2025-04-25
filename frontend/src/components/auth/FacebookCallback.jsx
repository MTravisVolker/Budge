import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { authService } from "../../services/authService";

const FacebookCallback = () => {
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const response = await authService.handleFacebookCallback();
        authService.setToken(response.token);
        navigate("/dashboard"); // Redirect to dashboard after successful login
      } catch (err) {
        setError(err.message);
        console.error("Facebook OAuth callback error:", err);
      }
    };

    handleCallback();
  }, [navigate]);

  if (error) {
    return (
      <div className="error-container">
        <h2>Authentication Error</h2>
        <p>{error}</p>
        <button onClick={() => navigate("/login")}>Return to Login</button>
      </div>
    );
  }

  return (
    <div className="loading-container">
      <h2>Authenticating with Facebook...</h2>
      <p>Please wait while we complete the authentication process.</p>
    </div>
  );
};

export default FacebookCallback;
