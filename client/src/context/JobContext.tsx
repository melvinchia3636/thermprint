import { createContext, useContext, type ReactNode } from "react";
import { useJobs, useCancelJob } from "../api/jobs";
import type { JobStatusResponse } from "../types";

interface JobContextValue {
  jobsData: JobStatusResponse[] | undefined;
  cancelJob: ReturnType<typeof useCancelJob>;
}

const JobContext = createContext<JobContextValue | null>(null);

export function useJobContext() {
  const ctx = useContext(JobContext);
  if (!ctx) throw new Error("useJobContext must be used inside JobProvider");
  return ctx;
}

export function JobProvider({ children }: { children: ReactNode }) {
  const { data: jobsData } = useJobs();
  const cancelJob = useCancelJob();

  return (
    <JobContext
      value={{
        jobsData: jobsData?.jobs,
        cancelJob,
      }}
    >
      {children}
    </JobContext>
  );
}
