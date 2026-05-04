import { createContext, useContext, type ReactNode } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { request } from "../api/client";
import { useDevices, useConnectionStatus } from "../api/devices";
import type { DeviceInfo } from "../types";

interface DeviceContextValue {
  devices: DeviceInfo[] | undefined;
  refreshDevices: () => void;
  connection: "offline" | "connecting" | "online";
  deviceName: string | undefined;
  setDeviceName: (name: string) => void;
}

const DeviceContext = createContext<DeviceContextValue | null>(null);

export function useDeviceContext() {
  const ctx = useContext(DeviceContext);
  if (!ctx)
    throw new Error("useDeviceContext must be used inside DeviceProvider");
  return ctx;
}

export function DeviceProvider({ children }: { children: ReactNode }) {
  const qc = useQueryClient();

  const { data: deviceData } = useQuery<{ ble_device_name: string }>({
    queryKey: ["device"],
    queryFn: () => request("/device"),
    staleTime: Infinity,
  });

  const updateDevice = useMutation({
    mutationFn: (name: string) =>
      request("/device", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ble_device_name: name }),
      }),
    onSuccess: (data) => {
      qc.setQueryData(["device"], data);
    },
  });

  const { data: devicesData, refetch: refreshDevices } = useDevices();
  const { data: statusData } = useConnectionStatus();

  return (
    <DeviceContext
      value={{
        devices: devicesData?.devices,
        refreshDevices,
        connection: statusData?.connection ?? "offline",
        deviceName: deviceData?.ble_device_name,
        setDeviceName: (name) => updateDevice.mutate(name),
      }}
    >
      {children}
    </DeviceContext>
  );
}
