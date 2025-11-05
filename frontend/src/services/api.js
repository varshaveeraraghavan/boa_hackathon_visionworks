const API_BASE_URL = "http://127.0.0.1:8000";

export async function getApiSimilarities() {
  const response = await fetch(`${API_BASE_URL}/api/similarity`);
  if (!response.ok) throw new Error("Failed to fetch API data");
  return response.json();
}
