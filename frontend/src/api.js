const API_URL = "http://127.0.0.1:8000";

export async function registerUser(name, email, password) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      name,
      email,
      password
    })
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Registration failed");
  }

  return data;
}

export async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email,
      password
    })
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  return data;
}

export async function predictCancer(userId, sampleName, file) {
  const formData = new FormData();

  formData.append("user_id", userId);
  formData.append("sample_name", sampleName);
  formData.append("file", file);

  const response = await fetch(`${API_URL}/prediction/csv`, {
    method: "POST",
    body: formData
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Prediction failed");
  }

  return data;
}

export async function getHistory(userId) {
  const response = await fetch(
    `${API_URL}/prediction/history/${userId}`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Unable to load history");
  }

  return data;
}