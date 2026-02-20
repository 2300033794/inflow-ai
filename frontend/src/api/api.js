import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

export async function sendChat(query) {
  const response = await client.post('/chat', { query });
  return response.data;
}

export async function checkHealth() {
  const response = await client.get('/health');
  return response.data;
}

export async function triggerIngest() {
  const response = await client.post('/ingest');
  return response.data;
}
