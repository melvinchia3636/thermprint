import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import * as api from "../api/printer";
import type { PrintSettings, DeviceInfo } from "../types";

export function useSettings() {
  return useQuery<PrintSettings>({
    queryKey: ["settings"],
    queryFn: api.getSettings,
    staleTime: Infinity,
  });
}

export function useUpdateSettings() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: api.updateSettings,
    onSuccess: (data) => {
      qc.setQueryData(["settings"], data);
    },
  });
}

export function usePreview() {
  return useMutation({
    mutationFn: ({
      image,
      settings,
    }: {
      image: File;
      settings: PrintSettings;
    }) => api.getPreview(image, settings),
  });
}

export function usePrint() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      image,
      settings,
    }: {
      image: File;
      settings: PrintSettings;
    }) => api.printImage(image, settings),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["jobs"] });
    },
  });
}

export function useJobs() {
  return useQuery({
    queryKey: ["jobs"],
    queryFn: api.listJobs,
    refetchInterval: 2000,
  });
}

export function useCancelJob() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: api.cancelJob,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["jobs"] });
    },
  });
}

export function useDevices() {
  return useQuery<{
    devices: DeviceInfo[];
  }>({
    queryKey: ["devices"],
    queryFn: api.listDevices,
    staleTime: 0,
  });
}

export function useConnectionStatus() {
  return useQuery({
    queryKey: ["connection-status"],
    queryFn: api.getStatus,
    refetchInterval: 3000,
  });
}
