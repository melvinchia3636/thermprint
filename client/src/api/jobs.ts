import { useRef } from "react";
import type { JobStatusResponse, JobStatus, JobType } from "../types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-toastify";
import { request } from "./client";
import { useWebSocket } from "./websocket";

export function useJobs() {
  const qc = useQueryClient();

  const result = useQuery<{ jobs: JobStatusResponse[] }>({
    queryKey: ["jobs"],
    queryFn: () => request("/jobs"),
    staleTime: Infinity,
  });

  const wsRef = useRef<WebSocket | null>(null);

  useWebSocket<{
    job_id: string;
    type: JobType;
    status: JobStatus;
    progress: string | null;
    error: string | null;
    created_at: string;
  }>(
    "/api/ws/jobs",
    (update) => {
      const prev = qc.getQueryData<{ jobs: JobStatusResponse[] }>(["jobs"]);
      const existing = prev?.jobs.find((j) => j.job_id === update.job_id);
      const wasNotDone = existing && existing.status !== "done";

      qc.setQueryData<{ jobs: JobStatusResponse[] }>(["jobs"], (prev) => {
        if (!prev) return prev;
        const idx = prev.jobs.findIndex((j) => j.job_id === update.job_id);
        const updated: JobStatusResponse = {
          job_id: update.job_id,
          type: update.type,
          status: update.status,
          progress: update.progress,
          error: update.error,
          created_at: update.created_at,
        };
        if (idx >= 0) {
          const next = [...prev.jobs];
          next[idx] = updated;
          return { jobs: next };
        }
        return { jobs: [updated, ...prev.jobs] };
      });

      if (update.status === "done" && wasNotDone) {
        toast.success("Print job completed");
      } else if (update.status === "failed") {
        toast.error(update.error || "Print job failed");
      }
    },
    wsRef,
  );

  return result;
}

export function useCancelJob() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (jobId: string) =>
      request(`/jobs/${jobId}`, { method: "DELETE" }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["jobs"] });
      toast.success("Job cancelled");
    },
    onError: (err) => {
      toast.error(err instanceof Error ? err.message : "Failed to cancel job");
    },
  });
}
