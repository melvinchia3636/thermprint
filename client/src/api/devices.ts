import { useRef } from "react";
import type { DeviceInfo, DeviceStatusResponse } from "../types";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { request } from "./client";
import { useWebSocket } from "./websocket";

export function useDevices() {
  return useQuery<{ devices: DeviceInfo[] }>({
    queryKey: ["devices"],
    queryFn: () => request("/devices"),
    staleTime: 0,
  });
}

export function useConnectionStatus() {
  const qc = useQueryClient();

  const result = useQuery<DeviceStatusResponse>({
    queryKey: ["connection-status"],
    queryFn: () => request("/status"),
    staleTime: Infinity,
  });

  const wsRef = useRef<WebSocket | null>(null);

  useWebSocket<{ connection: "offline" | "connecting" | "online" }>(
    "/api/ws/status",
    (update) => {
      qc.setQueryData<DeviceStatusResponse>(["connection-status"], update);
    },
    wsRef,
  );

  return result;
}
