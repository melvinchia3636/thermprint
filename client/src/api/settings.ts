import type { PrintSettings } from "../types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { request } from "./client";

export function useSettings() {
  return useQuery<PrintSettings>({
    queryKey: ["settings"],
    queryFn: () => request("/settings"),
    staleTime: Infinity,
  });
}

export function useUpdateSettings() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (s: PrintSettings) =>
      request("/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(s),
      }),
    onSuccess: (data) => {
      qc.setQueryData(["settings"], data);
    },
  });
}
