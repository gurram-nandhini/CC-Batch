import { useEffect, useState } from "react";
import { getHistory } from "../api";

function History() {
  const userName =
    localStorage.getItem("user_name") || "User";

  const userId =
    localStorage.getItem("user_id");

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    try {
      setLoading(true);
      setError("");

      if (!userId) {
        setError("Please login again.");
        return;
      }

      const data = await getHistory(userId);

      console.log("HISTORY RESPONSE:", data);

      setHistory(
        Array.isArray(data) ? data : []
      );

    } catch (err) {
      console.error("History error:", err);

      setError(
        err.message || "Unable to load history."
      );
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    localStorage.clear();
    window.location.href = "/login";
  }

  return (
    <div className="dashboard">

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
              window.location.href = "/dashboard";
            }}
          >
            Dashboard
          </button>

          <button
            className="logout-button"
            onClick={logout}
          >
            Logout
          </button>

        </div>

      </header>

      <main>

        <section className="card">

          <h2>Prediction History</h2>

          {loading && (
            <p>Loading history...</p>
          )}

          {error && (
            <p className="error-box">
              {error}
            </p>
          )}

          {!loading &&
            !error &&
            history.length === 0 && (
              <p>
                No prediction history found.
              </p>
            )}

          {!loading &&
            !error &&
            history.length > 0 && (

              <div className="history-table">

                <table>

                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Sample Name</th>
                      <th>Prediction</th>
                      <th>Probability</th>
                      <th>Date</th>
                    </tr>
                  </thead>

                  <tbody>

                    {history.map((item) => (

                      <tr key={item.id}>

                        <td>
                          {item.id}
                        </td>

                        <td>
                          {item.sample_name}
                        </td>

                        <td>
                          <strong>
                            {item.prediction}
                          </strong>
                        </td>

                        <td>
                          {Number(
                            item.probability
                          ).toFixed(2)}
                          %
                        </td>

                        <td>
                          {item.created_at
                            ? new Date(
                                item.created_at
                              ).toLocaleString()
                            : "-"}
                        </td>

                      </tr>

                    ))}

                  </tbody>

                </table>

              </div>

            )}

        </section>

      </main>

    </div>
  );
}

export default History;