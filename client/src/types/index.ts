export interface PrintSettings {
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
  split_cols: number;
  split_rows: number;
}

export type JobStatus = "queued" | "connecting" | "printing" | "done" | "failed" | "cancelled";

export type JobType = "image" | "qr_code" | "calendar";

export interface JobStatusResponse {
  job_id: string;
  type: JobType;
  status: JobStatus;
  progress: string | null;
  error: string | null;
  created_at: string;
  preview_url?: string;
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

export interface DeviceConfig {
  ble_device_name: string;
}

export interface DeviceStatusResponse {
  connection: "offline" | "connecting" | "online";
}
