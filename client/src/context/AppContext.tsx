import { createContext, useContext, useState, type ReactNode } from "react";
import { useSettings } from "../api/settings";
import { useJobs, useCancelJob } from "../api/jobs";
import { useDevices, useConnectionStatus } from "../api/devices";
import type { PrintSettings, DeviceInfo, JobStatusResponse } from "../types";

interface AppContextValue {
  step: number;
  setStep: (s: number) => void;
  image: File | null;
  setImage: (f: File | null) => void;
  localSettings: PrintSettings | null;
  setLocalSettings: (s: PrintSettings | null) => void;
  defaults: PrintSettings | undefined;
  jobsData: JobStatusResponse[] | undefined;
  cancelJob: ReturnType<typeof useCancelJob>;
  devices: DeviceInfo[] | undefined;
  refreshDevices: () => void;
  connection: "offline" | "connecting" | "online";
}

const AppContext = createContext<AppContextValue | null>(null);

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used inside AppProvider");
  return ctx;
}

export function AppProvider({ children }: { children: ReactNode }) {
  const { data: defaults } = useSettings();
  const { data: jobsData } = useJobs();
  const cancelJob = useCancelJob();
  const { data: devicesData, refetch: refreshDevices } = useDevices();
  const { data: statusData } = useConnectionStatus();
  const [image, setImage] = useState<File | null>(null);
  const [step, setStep] = useState(0);
  const [localSettings, setLocalSettings] = useState<PrintSettings | null>(
    null,
  );

  return (
    <AppContext
      value={{
        step,
        setStep,
        image,
        setImage,
        localSettings,
        setLocalSettings,
        defaults,
        jobsData: jobsData?.jobs,
        cancelJob,
        devices: devicesData?.devices,
        refreshDevices,
        connection: statusData?.connection ?? "offline",
      }}
    >
      {children}
    </AppContext>
  );
}
