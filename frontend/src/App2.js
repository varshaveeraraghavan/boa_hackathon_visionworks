import React, { useEffect, useState } from "react";
import { getApiSimilarities } from "./services/api";
import { PieChart, Pie, Tooltip, Cell, Legend } from "recharts";

const COLORS = ["#5a287d", "#5e10b1", "#646068", "#3c1053"];

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
      <h3>
        🔍 API Similarity Dashboard
        <br />
        Loading data...
      </h3>
    );

  // Prepare data for pie chart
  const pieData = Object.entries(clusters).map(([cluster, apis]) => ({
    name: `Cluster ${cluster}`,
    value: apis.length,
  }));

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h2 className="text-2xl font-bold mb-4">Duplicate detection dashboard</h2>

      {/* Pie Chart for cluster distribution */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginBottom: "2rem",
        }}
      >
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

      {/* Cluster table */}
      <div style={{ display: "grid", gap: "1rem" }}>
        {Object.entries(clusters).map(([cluster, apis]) => (
          <div
            key={cluster}
            style={{
              border: "1px solid #ccc",
              borderRadius: 8,
              padding: "1rem",
            }}
          >
            <h3>🧩 Cluster {cluster}</h3>
            <ul>
              {apis.map((api) => (
                <li key={api}>🔸 {api}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
