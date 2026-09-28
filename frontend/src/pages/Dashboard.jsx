import { useState } from "react";
import { predictCancer } from "../api";

function Dashboard() {
  const userName = localStorage.getItem("user_name") || "User";
  const userId = localStorage.getItem("user_id");

  const [sampleName, setSampleName] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function logout() {
    localStorage.clear();
    window.location.href = "/login";
  }

  async function handlePrediction(event) {
    event.preventDefault();

    setError("");
    setResult(null);

    if (!sampleName.trim()) {
      setError("Please enter sample name.");
      return;
    }

    if (!file) {
      setError("Please select a CSV file.");
      return;
    }

    if (!file.name.toLowerCase().endsWith(".csv")) {
      setError("Only CSV files are allowed.");
      return;
    }

    if (!userId) {
      setError("Please login again.");
      return;
    }

    try {
      setLoading(true);

      const response = await predictCancer(
        userId,
        sampleName,
        file
      );

      console.log("BACKEND RESPONSE:", response);

      /*
       * Convert different possible backend response
       * formats into one simple object.
       */

      let predictionData = response;

      // If response is an array
      if (Array.isArray(predictionData)) {
        predictionData = predictionData[0];
      }

      // If response contains "result"
      if (
        predictionData &&
        typeof predictionData.result === "object"
      ) {
        predictionData = predictionData.result;
      }

      // If response contains "predictions"
      if (
        predictionData &&
        Array.isArray(predictionData.predictions)
      ) {
        predictionData = predictionData.predictions[0];
      }

      /*
       * Create a clean result object.
       */
      if (
        predictionData &&
        typeof predictionData === "object"
      ) {
        const prediction =
          predictionData.prediction ||
          predictionData.cancer_type ||
          predictionData.label ||
          predictionData.predicted_class ||
          predictionData.class_name ||
          predictionData.cancer ||
          predictionData.type ||
          "Unknown";

        const probability =
          predictionData.probability ??
          predictionData.confidence ??
          predictionData.score ??
          null;

        setResult({
          prediction: String(prediction),
          probability: probability
        });
      } else {
        setResult({
          prediction: String(predictionData),
          probability: null
        });
      }

    } catch (err) {
      console.error("Prediction error:", err);

      setError(
        err.message || "Prediction failed."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="dashboard">

      {/* HEADER */}

      <header className="topbar">

        <div>
          <h1>Gene Expression Cancer Analysis</h1>

          <p>
            Welcome, {userName}
          </p>
        </div>

        <div>

          <button
            className="secondary-button"
            onClick={() => {
              window.location.href = "/history";
            }}
          >
            History
          </button>

          <button
            className="logout-button"
            onClick={logout}
          >
            Logout
          </button>

        </div>

      </header>


      {/* MAIN */}

      <main>

        {/* PREDICTION CARD */}

        <section className="card">

          <h2>Cancer Prediction</h2>

          <p>
            Upload gene expression data to predict
            the cancer type.
          </p>


          <form onSubmit={handlePrediction}>

            {/* SAMPLE NAME */}

            <label>
              Sample Name
            </label>

            <input
              type="text"
              value={sampleName}
              onChange={(event) =>
                setSampleName(event.target.value)
              }
              placeholder="Example: Cancer_Sample_001"
            />


            {/* CSV FILE */}

            <label>
              Gene Expression CSV
            </label>

            <input
              type="file"
              accept=".csv"
              onChange={(event) => {

                const selectedFile =
                  event.target.files[0];

                setFile(selectedFile);
                setError("");
                setResult(null);

              }}
            />


            {/* FILE NAME */}

            {file && (
              <p>
                Selected file: {file.name}
              </p>
            )}


            {/* PREDICT BUTTON */}

            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Predicting..."
                : "Predict Cancer Type"}
            </button>

          </form>


          {/* ERROR */}

          {error && (
            <div className="error-box">
              {error}
            </div>
          )}

        </section>


        {/* RESULT */}

        {result && (
          <section className="card result-card">

            <h2>Prediction Result</h2>

            <p>
              Sample: {sampleName}
            </p>

            <h1>
              {result.prediction}
            </h1>

            {result.probability !== null &&
              result.probability !== undefined && (
                <p>
                  Probability:{" "}
                  {Number(result.probability).toFixed(2)}%
                </p>
              )}

          </section>
        )}

      </main>

    </div>
  );
}

export default Dashboard;