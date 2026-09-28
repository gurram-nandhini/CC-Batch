import { useState } from "react";
import { registerUser } from "../api";

function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleRegister(e) {
    e.preventDefault();

    setMessage("");
    setError("");

    try {
      await registerUser(name, email, password);

      setMessage("Registration successful!");

      setTimeout(() => {
        window.location.href = "/login";
      }, 1000);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="page">
      <div className="card auth-card">
        <h1>Gene Expression Cancer Analysis</h1>

        <h2>Create Account</h2>

        <form onSubmit={handleRegister}>
          <label>Name</label>

          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
            required
          />

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
            placeholder="Enter password"
            required
          />

          <button type="submit">
            Register
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
          Already have an account?{" "}
          <a href="/login">Login</a>
        </p>
      </div>
    </div>
  );
}

export default Register;