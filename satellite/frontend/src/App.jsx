import { useState, useEffect } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  Navigate,
  useNavigate,
} from "react-router-dom";
import "./index.css";

/* =====================================================
   LOGIN
===================================================== */

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    localStorage.setItem(
      "satelliteUser",
      JSON.stringify({
        email: email,
        name: email.split("@")[0],
      })
    );

    navigate("/dashboard");
  };

  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="logo-large">🛰️</div>

        <h1>Satellite Vision</h1>

        <p className="auth-subtitle">
          Satellite Image Analysis Platform
        </p>

        <form onSubmit={handleLogin}>

          <label>Email</label>

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label>Password</label>

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="primary-btn">
            Login
          </button>

        </form>

        <p className="auth-link">
          Don't have an account?
          <Link to="/register"> Create Account</Link>
        </p>

      </div>

    </div>
  );
}


/* =====================================================
   REGISTER
===================================================== */

function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = (e) => {
    e.preventDefault();

    if (!name || !email || !password) {
      alert("Please fill all fields");
      return;
    }

    localStorage.setItem(
      "satelliteRegisteredUser",
      JSON.stringify({
        name,
        email,
        password,
      })
    );

    alert("Registration successful!");

    navigate("/");
  };

  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="logo-large">🌍</div>

        <h1>Create Account</h1>

        <p className="auth-subtitle">
          Start analyzing satellite images
        </p>

        <form onSubmit={handleRegister}>

          <label>Full Name</label>

          <input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <label>Email</label>

          <input
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label>Password</label>

          <input
            type="password"
            placeholder="Create password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="primary-btn">
            Register
          </button>

        </form>

        <p className="auth-link">
          Already have an account?
          <Link to="/"> Login</Link>
        </p>

      </div>

    </div>
  );
}


/* =====================================================
   NAVBAR
===================================================== */

function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("satelliteUser");
    navigate("/");
  };

  return (
    <nav className="navbar">

      <Link to="/dashboard" className="brand">
        🛰️ Satellite Vision
      </Link>

      <div className="nav-links">

        <Link to="/dashboard">
          Dashboard
        </Link>

        <Link to="/analysis">
          Analysis
        </Link>

        <Link to="/enhancement">
          Enhancement
        </Link>

        <Link to="/history">
          History
        </Link>

        <button
          className="logout-btn"
          onClick={logout}
        >
          Logout
        </button>

      </div>

    </nav>
  );
}


/* =====================================================
   LAYOUT
===================================================== */

function Layout({ children }) {
  return (
    <>
      <Navbar />
      <main>{children}</main>
    </>
  );
}


/* =====================================================
   DASHBOARD
===================================================== */

function Dashboard() {
  const user = JSON.parse(
    localStorage.getItem("satelliteUser")
  );

  const openBiologyProject = () => {
    // Change this port if your Biology frontend runs on another port
    window.location.href = "http://localhost:5174";
  };

  return (
    <Layout>

      <section className="dashboard">

        {/* =========================
            WELCOME SECTION
        ========================= */}

        <div className="hero">

          <div>

            <p className="welcome">
              Welcome back 👋
            </p>

            <h1>
              AI & Data Science
              <span> Project Portal</span>
            </h1>

            <p>
              Explore our Biology and Geo Science
              applications developed using machine
              learning, data analysis, image processing
              and modern web technologies.
            </p>

          </div>

          <div className="earth">
            🌍
          </div>

        </div>


        {/* =========================
            PROJECTS
        ========================= */}

        <h2 className="section-title">
          🚀 Our Projects
        </h2>

        <p className="section-description">
          Select a project to explore its features
          and functionality.
        </p>


        <div className="project-grid">

          {/* =========================
              PART A
          ========================= */}

          <div className="project-card biology-card">

            <div className="project-number">
              PART A
            </div>

            <div className="project-icon">
              🧬
            </div>

            <h2>
              Biology
            </h2>

            <h3>
              Gene Expression Data Analysis
              for Cancer Diagnosis
            </h3>

            <p>
              Analyze high-dimensional gene expression
              data and use machine learning techniques
              to classify different cancer types based
              on gene expression patterns.
            </p>


            <div className="project-tags">

              <span>Python</span>
              <span>Machine Learning</span>
              <span>Scikit-learn</span>
              <span>FastAPI</span>
              <span>MySQL</span>

            </div>


            <div className="project-features">

              <p>✓ Gene Expression Analysis</p>
              <p>✓ Data Preprocessing</p>
              <p>✓ Feature Selection</p>
              <p>✓ Cancer Classification</p>
              <p>✓ Prediction Probability</p>

            </div>


            <button
              className="project-btn biology-btn"
              onClick={openBiologyProject}
            >
              Open Biology Project →
            </button>

          </div>


          {/* =========================
              PART B
          ========================= */}

          <div className="project-card satellite-card">

            <div className="project-number">
              PART B
            </div>

            <div className="project-icon">
              🛰️
            </div>

            <h2>
              Geo Science
            </h2>

            <h3>
              Satellite Image Application
            </h3>

            <p>
              Upload, visualize, analyze and enhance
              satellite images using image processing
              techniques and an interactive web
              application.
            </p>


            <div className="project-tags">

              <span>React</span>
              <span>FastAPI</span>
              <span>Python</span>
              <span>Pillow</span>
              <span>MySQL</span>

            </div>


            <div className="project-features">

              <p>✓ Satellite Image Upload</p>
              <p>✓ Image Preview</p>
              <p>✓ RGB Analysis</p>
              <p>✓ Brightness Analysis</p>
              <p>✓ Image Enhancement</p>

            </div>


            <button
              className="project-btn satellite-btn"
              onClick={() =>
                window.location.href = "/analysis"
              }
            >
              Open Satellite Project →
            </button>

          </div>

        </div>


        {/* =========================
            TECHNOLOGY SECTION
        ========================= */}

        <h2 className="section-title">
          🛠️ Technologies Used
        </h2>


        <div className="technology-grid">

          <div className="technology-card">
            <div>🐍</div>
            <h3>Python</h3>
            <p>
              Data analysis, machine learning
              and image processing
            </p>
          </div>


          <div className="technology-card">
            <div>⚛️</div>
            <h3>React</h3>
            <p>
              Interactive frontend
              development
            </p>
          </div>


          <div className="technology-card">
            <div>⚡</div>
            <h3>FastAPI</h3>
            <p>
              Backend APIs and
              application services
            </p>
          </div>


          <div className="technology-card">
            <div>🗄️</div>
            <h3>MySQL</h3>
            <p>
              Structured data and
              user information
            </p>
          </div>


          <div className="technology-card">
            <div>🤖</div>
            <h3>Machine Learning</h3>
            <p>
              Prediction and
              classification
            </p>
          </div>


          <div className="technology-card">
            <div>☁️</div>
            <h3>AWS</h3>
            <p>
              Cloud deployment and
              application hosting
            </p>
          </div>

        </div>


        {/* =========================
            ACCOUNT
        ========================= */}

        <div className="info-card">

          <h2>
            👤 Current User
          </h2>

          <p>
            <strong>Name:</strong>{" "}
            {user?.name || "User"}
          </p>

          <p>
            <strong>Email:</strong>{" "}
            {user?.email || "Not available"}
          </p>

        </div>

      </section>

    </Layout>
  );
}

/* =====================================================
   ANALYSIS PAGE
===================================================== */

function Analysis() {

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const selectFile = (e) => {

    const selected = e.target.files[0];

    if (!selected) return;

    setFile(selected);

    setPreview(
      URL.createObjectURL(selected)
    );

    setAnalysis(null);
    setUploadResult(null);
  };


  const uploadImage = async () => {

    if (!file) {
      alert("Please select an image");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      const response = await fetch(
        "http://127.0.0.1:8001/image/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setUploadResult(data);

    } catch {

      alert("Backend connection failed");

    }
  };


  const analyzeImage = async () => {

    if (!file) {
      alert("Please select an image");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8001/image/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setAnalysis(data);

      if (data.success) {

        const oldHistory =
          JSON.parse(
            localStorage.getItem(
              "satelliteHistory"
            )
          ) || [];

        oldHistory.push({
          filename: file.name,
          width: data.image.width,
          height: data.image.height,
          format: file.type,
          brightness:
            data.brightness.value,
          level:
            data.brightness.level,
          date:
            new Date().toLocaleString(),
        });

        localStorage.setItem(
          "satelliteHistory",
          JSON.stringify(oldHistory)
        );
      }

    } catch {

      alert("Analysis backend connection failed");

    }

    setLoading(false);
  };


  return (
    <Layout>

      <section className="page">

        <h1>📊 Satellite Image Analysis</h1>

        <p className="page-description">
          Upload a satellite image and analyze
          its visual characteristics.
        </p>


        <div className="upload-panel">

          <input
            type="file"
            accept=".jpg,.jpeg,.png,.tif,.tiff"
            onChange={selectFile}
          />

          {file && (
            <p>
              Selected:
              <strong> {file.name}</strong>
            </p>
          )}

          <div className="button-row">

            <button
              className="primary-btn"
              onClick={uploadImage}
            >
              Upload Image
            </button>

            <button
              className="success-btn"
              onClick={analyzeImage}
            >
              {loading
                ? "Analyzing..."
                : "Analyze Image"}
            </button>

          </div>

        </div>


        {preview && (

          <div className="image-card">

            <h2>
              Satellite Image Preview
            </h2>

            <img
              src={preview}
              className="satellite-preview"
              alt="Satellite"
            />

          </div>

        )}


        {uploadResult?.success && (

          <div className="result-card">

            <h2>
              ✅ Upload Successful
            </h2>

            <p>
              File: {uploadResult.filename}
            </p>

            <p>
              Size: {uploadResult.width} ×{" "}
              {uploadResult.height}
            </p>

            <p>
              Format: {uploadResult.format}
            </p>

          </div>

        )}


        {analysis?.success && (

          <div className="analysis-card">

            <h2>
              🔬 Analysis Results
            </h2>

            <div className="stats-grid">

              <Stat
                title="Image Size"
                value={`${analysis.image.width} × ${analysis.image.height}`}
              />

              <Stat
                title="Format"
                value={file?.type}
              />

              <Stat
                title="Average Red"
                value={analysis.rgb.average_red}
              />

              <Stat
                title="Average Green"
                value={analysis.rgb.average_green}
              />

              <Stat
                title="Average Blue"
                value={analysis.rgb.average_blue}
              />

              <Stat
                title="Brightness"
                value={analysis.brightness.value}
              />

            </div>


            <div className="brightness-result">

              <h3>
                Brightness Level
              </h3>

              <div className="brightness-value">

                {analysis.brightness.level ===
                "Bright"
                  ? "☀️ Bright"
                  : analysis.brightness.level ===
                    "Dark"
                  ? "🌑 Dark"
                  : "🌤️ Moderate"}

              </div>

            </div>

          </div>

        )}

      </section>

    </Layout>
  );
}


/* =====================================================
   STAT COMPONENT
===================================================== */

function Stat({ title, value }) {

  return (

    <div className="stat-card">

      <h3>{title}</h3>

      <p>{value}</p>

    </div>

  );
}


/* =====================================================
   IMAGE ENHANCEMENT
===================================================== */

function Enhancement() {

  const [file, setFile] = useState(null);

  const [preview, setPreview] =
    useState(null);

  const [brightness, setBrightness] =
    useState(100);

  const [contrast, setContrast] =
    useState(100);

  const [grayscale, setGrayscale] =
    useState(0);


  const selectImage = (e) => {

    const selected =
      e.target.files[0];

    if (!selected) return;

    setFile(selected);

    setPreview(
      URL.createObjectURL(selected)
    );
  };


  const downloadImage = () => {

    if (!preview) {
      alert("Please select an image");
      return;
    }

    const link =
      document.createElement("a");

    link.href = preview;

    link.download =
      `enhanced_${file.name}`;

    link.click();
  };


  return (
    <Layout>

      <section className="page">

        <h1>
          🎨 Image Enhancement
        </h1>

        <p className="page-description">
          Improve satellite image visualization
          using brightness, contrast and grayscale.
        </p>


        <div className="upload-panel">

          <input
            type="file"
            accept=".jpg,.jpeg,.png"
            onChange={selectImage}
          />

        </div>


        {preview && (

          <>

            <div className="enhancement-preview">

              <img
                src={preview}
                alt="Enhanced"
                style={{
                  filter: `
                    brightness(${brightness}%)
                    contrast(${contrast}%)
                    grayscale(${grayscale}%)
                  `,
                }}
              />

            </div>


            <div className="controls">

              <label>
                Brightness: {brightness}%
              </label>

              <input
                type="range"
                min="50"
                max="150"
                value={brightness}
                onChange={(e) =>
                  setBrightness(e.target.value)
                }
              />


              <label>
                Contrast: {contrast}%
              </label>

              <input
                type="range"
                min="50"
                max="150"
                value={contrast}
                onChange={(e) =>
                  setContrast(e.target.value)
                }
              />


              <label>
                Grayscale: {grayscale}%
              </label>

              <input
                type="range"
                min="0"
                max="100"
                value={grayscale}
                onChange={(e) =>
                  setGrayscale(e.target.value)
                }
              />


              <button
                className="primary-btn"
                onClick={downloadImage}
              >
                📥 Download Image
              </button>

            </div>

          </>

        )}

      </section>

    </Layout>
  );
}


/* =====================================================
   HISTORY
===================================================== */

function History() {

  const [history, setHistory] =
    useState([]);

  useEffect(() => {

    const data =
      JSON.parse(
        localStorage.getItem(
          "satelliteHistory"
        )
      ) || [];

    setHistory(data);

  }, []);


  const clearHistory = () => {

    localStorage.removeItem(
      "satelliteHistory"
    );

    setHistory([]);

  };


  return (

    <Layout>

      <section className="page">

        <div className="history-header">

          <div>

            <h1>
              📜 Analysis History
            </h1>

            <p className="page-description">
              Your previously analyzed satellite images.
            </p>

          </div>

          {history.length > 0 && (

            <button
              className="danger-btn"
              onClick={clearHistory}
            >
              Clear History
            </button>

          )}

        </div>


        {history.length === 0 ? (

          <div className="empty-card">

            <div>
              📭
            </div>

            <h2>
              No analysis history
            </h2>

            <p>
              Analyze your first satellite image
              to see results here.
            </p>

          </div>

        ) : (

          <div className="history-table">

            <div className="table-header">

              <span>File</span>
              <span>Size</span>
              <span>Brightness</span>
              <span>Level</span>
              <span>Date</span>

            </div>


            {history.map(
              (item, index) => (

                <div
                  className="table-row"
                  key={index}
                >

                  <span>
                    {item.filename}
                  </span>

                  <span>
                    {item.width} ×{" "}
                    {item.height}
                  </span>

                  <span>
                    {item.brightness}
                  </span>

                  <span>
                    {item.level}
                  </span>

                  <span>
                    {item.date}
                  </span>

                </div>

              )
            )}

          </div>

        )}

      </section>

    </Layout>

  );
}


/* =====================================================
   PROTECTED ROUTE
===================================================== */

function ProtectedRoute({ children }) {

  const user =
    localStorage.getItem(
      "satelliteUser"
    );

  if (!user) {
    return <Navigate to="/" replace />;
  }

  return children;
}


/* =====================================================
   APP
===================================================== */

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/analysis"
          element={
            <ProtectedRoute>
              <Analysis />
            </ProtectedRoute>
          }
        />

        <Route
          path="/enhancement"
          element={
            <ProtectedRoute>
              <Enhancement />
            </ProtectedRoute>
          }
        />

        <Route
          path="/history"
          element={
            <ProtectedRoute>
              <History />
            </ProtectedRoute>
          }
        />

      </Routes>

    </BrowserRouter>

  );
}

export default App;