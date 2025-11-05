import React from "react";

function ClusterTable({ clusters }) {
  return (
    <div className="card mt-4 shadow-sm">
      <div className="card-body">
        <h5 className="card-title">API Clusters</h5>
        <table className="table table-hover">
          <thead>
            <tr>
              <th>Cluster #</th>
              <th>Category</th>
              <th>APIs</th>
              <th>Recommendation</th>
            </tr>
          </thead>
          <tbody>
            {clusters.map((cluster, idx) => (
              <tr key={idx}>
                <td>{idx + 1}</td>
                <td>{cluster.category}</td>
                <td>{cluster.apis.join(", ")}</td>
                <td>{cluster.recommended_action}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ClusterTable;
