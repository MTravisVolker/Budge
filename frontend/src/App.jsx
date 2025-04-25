import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import FacebookCallback from "./components/auth/FacebookCallback";
import GoogleCallback from "./components/auth/GoogleCallback";

function App() {
  return (
    <Router>
      <Routes>
        {/* OAuth Callback Routes */}
        <Route path="/auth/google/callback" element={<GoogleCallback />} />
        <Route path="/auth/facebook/callback" element={<FacebookCallback />} />

        {/* Other routes will go here */}
        <Route path="/" element={<div>Home Page</div>} />
        <Route path="/login" element={<div>Login Page</div>} />
        <Route path="/dashboard" element={<div>Dashboard</div>} />
      </Routes>
    </Router>
  );
}

export default App;
