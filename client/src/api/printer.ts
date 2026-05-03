import type {
  PrintSettings,
  PreviewResponse,
  PrintResponse,
  JobStatusResponse,
  DeviceInfo,
} from "../types";

const BASE = "/api";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, options);
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    const detail = body?.detail;
    const msg = Array.isArray(detail)
      ? detail.join("; ")
      : detail || `HTTP ${res.status}`;
    throw new Error(msg);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export async function getSettings(): Promise<PrintSettings> {
  return request("/settings");
}

export async function updateSettings(s: PrintSettings): Promise<PrintSettings> {
  return request("/settings", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(s),
  });
}

export async function getPreview(
  image: File,
  settings: PrintSettings,
): Promise<PreviewResponse> {
  const fd = new FormData();
  fd.append("image", image);
  for (const [k, v] of Object.entries(settings)) {
    fd.append(k, String(v));
  }
  return request("/preview", { method: "POST", body: fd });
}

export async function printImage(
  image: File,
  settings: PrintSettings,
): Promise<PrintResponse> {
  const fd = new FormData();
  fd.append("image", image);
  for (const [k, v] of Object.entries(settings)) {
    fd.append(k, String(v));
  }
  return request("/print", { method: "POST", body: fd });
}

export async function listJobs(): Promise<{
  jobs: JobStatusResponse[];
}> {
  return request("/jobs");
}

export async function getJob(jobId: string): Promise<JobStatusResponse> {
  return request(`/jobs/${jobId}`);
}

export async function cancelJob(jobId: string): Promise<void> {
  return request(`/jobs/${jobId}`, { method: "DELETE" });
}

export async function listDevices(): Promise<{
  devices: DeviceInfo[];
}> {
  return request("/devices");
}

export interface StatusResponse {
  connection: "offline" | "connecting" | "online";
}

export async function getStatus(): Promise<StatusResponse> {
  return request("/status");
}
