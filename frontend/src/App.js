import React, { useEffect, useState } from "react";
import { getApiSimilarities } from "./services/api";
import { PieChart, Pie, Tooltip, Cell, Legend } from "recharts";
import logo from "./assets/logo.jpeg"; // ✅ logo image

const COLORS = ["#5a287d", "#5e10b1", "#646068", "#FF8042"];

function App() {
  const [apis, setApis] = useState([]);
  const [clusters, setClusters] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getApiSimilarities()
      .then((data) => {
        setApis(data.apis);

        // Group APIs by cluster
        const grouped = data.apis.reduce((acc, api) => {
          acc[api.cluster] = acc[api.cluster] || [];
          acc[api.cluster].push(api.api_name);
          return acc;
        }, {});
        setClusters(grouped);
        setLoading(false);
      })
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  if (loading)
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          backgroundColor: "#f2eaf9",
          color: "#5a287d",
          fontFamily: "sans-serif",
          flexDirection: "column",
        }}
      >
        <h2>🔍 Duplicate Detection Dashboard</h2>
        <p>Loading data...</p>
      </div>
    );

  // Prepare data for pie chart
  const pieData = Object.entries(clusters).map(([cluster, apis]) => ({
    name: `Cluster ${cluster}`,
    value: apis.length,
  }));

  return (
    <div
      style={{
        backgroundColor: "#f2eaf9",
        minHeight: "100vh",
        fontFamily: "'Inter', sans-serif",
        paddingBottom: "2rem",
      }}
    >
      <header
        style={{
          backgroundColor: "#5a287d",
          boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "1rem 2rem",
          position: "sticky",
          top: 0,
          zIndex: 10,
        }}
      >
        <h1 style={{ color: "#fff", fontSize: "1.5rem", fontWeight: 700 }}>
          Duplicate Detection Dashboard
        </h1>
        <img
          src={logo}
          alt="Logo"
          style={{
            width: "55px",
            height: "55px",
            borderRadius: "50%",
            objectFit: "cover",
            boxShadow: "0 0 6px rgba(0,0,0,0.15)",
          }}
        />
      </header>
      <section
        style={{
          marginTop: "3rem",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <div
          style={{
            backgroundColor: "#fff",
            borderRadius: "16px",
            boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
            padding: "2rem",
            maxWidth: "500px",
            width: "90%",
          }}
        >
          <h2
            style={{
              textAlign: "center",
              color: "#5a287d",
              fontWeight: 600,
              marginBottom: "1rem",
            }}
          >
            API Cluster Distribution
          </h2>
          <PieChart width={400} height={300}>
            <Pie
              data={pieData}
              dataKey="value"
              nameKey="name"
              outerRadius={120}
              fill="#8884d8"
              label
            >
              {pieData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
      </section>

      {/* 🧩 Cluster Cards Section */}
      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
          gap: "1.5rem",
          margin: "3rem auto",
          maxWidth: "900px",
          padding: "0 1rem",
        }}
      >
        {Object.entries(clusters).map(([cluster, apis]) => (
          <div
            key={cluster}
            style={{
              backgroundColor: "#fff",
              borderRadius: "12px",
              boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
              padding: "1.5rem",
              transition: "transform 0.2s ease, box-shadow 0.2s ease",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.transform = "translateY(-4px)")
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.transform = "translateY(0)")
            }
          >
            <h3
              style={{
                color: "#5a287d",
                fontWeight: 600,
                marginBottom: "1rem",
              }}
            >
              Cluster {cluster}
            </h3>
            <ul style={{ paddingLeft: "1.2rem", color: "#333" }}>
              {apis.map((api) => (
                <li key={api} style={{ marginBottom: "0.5rem" }}>
                  {api}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </section>
    </div>
  );
}

export default App;
