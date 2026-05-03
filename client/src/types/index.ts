export interface PrintSettings {
  ble_device_name: string;
  width: number;
  quality: number;
  speed: number;
  energy: number;
  contrast: number;
  gamma: number;
  rotate: number;
  chunk_rows: number;
  chunk_delay: number;
  feed: number;
}

export type JobStatus = "queued" | "printing" | "done" | "failed";

export interface JobStatusResponse {
  job_id: string;
  status: JobStatus;
  progress: string | null;
  error: string | null;
  created_at: string;
}

export interface PreviewResponse {
  preview_url: string;
  width: number;
  height: number;
}

export interface PrintResponse {
  job_id: string;
  status: JobStatus;
}

export interface DeviceInfo {
  name: string | null;
  address: string;
}
