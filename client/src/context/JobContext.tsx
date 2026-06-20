import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import { useJobs, useCancelJob, useDeleteJob } from "../api/jobs";
import type { JobStatusResponse } from "../types";

const PAGE_SIZE = 10;

interface JobContextValue {
  jobsData: JobStatusResponse[] | undefined;
  total: number;
  hasMore: boolean;
  isLoadingMore: boolean;
  loadMore: () => void;
  cancelJob: ReturnType<typeof useCancelJob>;
  deleteJob: ReturnType<typeof useDeleteJob>;
}

const JobContext = createContext<JobContextValue | null>(null);

export function useJobContext() {
  const ctx = useContext(JobContext);
  if (!ctx) throw new Error("useJobContext must be used inside JobProvider");
  return ctx;
}

export function JobProvider({ children }: { children: ReactNode }) {
  const [limit, setLimit] = useState(PAGE_SIZE);
  const { data, isFetching } = useJobs(0, limit);
  const cancelJob = useCancelJob();
  const deleteJob = useDeleteJob();

  const total = data?.total ?? 0;
  const hasMore = (data?.jobs.length ?? 0) < total;

  const loadMore = useCallback(() => {
    setLimit((l) => l + PAGE_SIZE);
  }, []);

  return (
    <JobContext
      value={{
        jobsData: data?.jobs,
        total,
        hasMore,
        isLoadingMore: isFetching,
        loadMore,
        cancelJob,
        deleteJob,
      }}
    >
      {children}
    </JobContext>
  );
}
