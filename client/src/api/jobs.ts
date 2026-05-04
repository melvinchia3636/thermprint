import { useRef } from "react";
import type { JobStatusResponse, JobStatus, JobType } from "../types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-toastify";
import { request } from "./client";
import { useWebSocket } from "./websocket";

export function useJobs(offset = 0, limit = 10) {
  const qc = useQueryClient();

  const result = useQuery<{ jobs: JobStatusResponse[]; total: number }>({
    queryKey: ["jobs", { offset, limit }],
    queryFn: () => request(`/jobs?offset=${offset}&limit=${limit}`),
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
    preview_url?: string | null;
  }>(
    "/api/ws/jobs",
    (update) => {
      const existing = result.data?.jobs.find(
        (j) => j.job_id === update.job_id,
      );
      const wasNotDone = existing && existing.status !== "done";

      qc.setQueryData<{ jobs: JobStatusResponse[]; total: number }>(["jobs", { offset, limit }], (prev) => {
        if (!prev) return prev;
        const idx = prev.jobs.findIndex((j) => j.job_id === update.job_id);
        const updated: JobStatusResponse = {
          job_id: update.job_id,
          type: update.type,
          status: update.status,
          progress: update.progress,
          error: update.error,
          created_at: update.created_at,
          preview_url: update.preview_url ?? undefined,
        };
        if (idx >= 0) {
          const next = [...prev.jobs];
          next[idx] = updated;
          return { jobs: next, total: prev.total };
        }
        if (offset === 0) {
          return { jobs: [updated, ...prev.jobs], total: prev.total + 1 };
        }
        return prev;
      });

      if (update.status === "done" && wasNotDone) {
        toast.success("Print job completed");
      } else if (update.status === "failed") {
        toast.error(update.error || "Print job failed");
      }
    },
    wsRef,
    () => qc.invalidateQueries({ queryKey: ["jobs"] }),
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

export function useDeleteJob() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (jobId: string) =>
      request(`/jobs/${jobId}/delete`, { method: "DELETE" }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["jobs"] });
      toast.success("Job deleted");
    },
    onError: (err) => {
      toast.error(err instanceof Error ? err.message : "Failed to delete job");
    },
  });
}
