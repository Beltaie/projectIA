import { BackendHealth } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function checkBackendHealth(): Promise<BackendHealth> {
  const startTime = performance.now();
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);

    // Try direct port 8000 or proxied /api/health
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    const latencyMs = Math.round(performance.now() - startTime);

    if (response.ok) {
      const data = await response.json();
      return {
        status: 'online',
        serviceName: data.service || 'SmartCampus AI API',
        version: data.version || '1.0.0',
        environment: data.environment || 'development',
        latencyMs,
        lastChecked: new Date().toLocaleTimeString(),
      };
    } else {
      return {
        status: 'offline',
        errorMessage: `Status HTTP ${response.status}`,
        latencyMs,
        lastChecked: new Date().toLocaleTimeString(),
      };
    }
  } catch (err: unknown) {
    const latencyMs = Math.round(performance.now() - startTime);
    const message = err instanceof Error ? err.message : 'Connexion impossible';
    return {
      status: 'offline',
      errorMessage: message,
      latencyMs,
      lastChecked: new Date().toLocaleTimeString(),
    };
  }
}
