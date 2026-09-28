import { useState } from "react";
import { loginUser } from "../api";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(e) {
    e.preventDefault();

    setMessage("");
    setError("");

    try {
      const data = await loginUser(email, password);

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user_id", data.user_id);
      localStorage.setItem("user_name", data.name || "User");

      setMessage("Login successful!");

      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 500);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="page">
      <div className="card auth-card">
        <h1>Gene Expression Cancer Analysis</h1>

        <h2>Login</h2>

        <form onSubmit={handleLogin}>
          <label>Email</label>

          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
          />

          <label>Password</label>

          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />

          <button type="submit">
            Login
          </button>
        </form>

        {message && (
          <p className="success">
            {message}
          </p>
        )}

        {error && (
          <p className="error">
            {error}
          </p>
        )}

        <p>
          Don't have an account?{" "}
          <a href="/register">Register</a>
        </p>
      </div>
    </div>
  );
}

export default Login;