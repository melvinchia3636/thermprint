import type { PrintSettings, PreviewResponse, PrintResponse } from "../types";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-toastify";
import { request } from "./client";

export function usePreview() {
  return useMutation({
    mutationFn: ({
      image,
      settings,
    }: {
      image: File;
      settings: PrintSettings;
    }) => {
      const fd = new FormData();
      fd.append("image", image);
      for (const [k, v] of Object.entries(settings)) {
        fd.append(k, String(v));
      }
      return request<PreviewResponse>("/preview", { method: "POST", body: fd });
    },
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
    }) => {
      const fd = new FormData();
      fd.append("image", image);
      for (const [k, v] of Object.entries(settings)) {
        fd.append(k, String(v));
      }
      return request<PrintResponse>("/print", { method: "POST", body: fd });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["jobs"] });
      toast.success("Image added to print queue");
    },
    onError: (err) => {
      toast.error(err instanceof Error ? err.message : "Failed to print image");
    },
  });
}

export function usePrintQRCode() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ url, size, style, embedImage }: { url: string; size?: number; style?: string; embedImage?: File | null }) => {
      const fd = new FormData();
      fd.append("url", url);
      if (size) fd.append("size", String(size));
      if (style) fd.append("style", style);
      if (embedImage) fd.append("embed_image", embedImage);
      return request<PrintResponse>("/qrcode", { method: "POST", body: fd });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["jobs"] });
      toast.success("QR code added to print queue");
    },
    onError: (err) => {
      toast.error(err instanceof Error ? err.message : "Failed to print QR code");
    },
  });
}

export function useQRPreview() {
  return useMutation({
    mutationFn: ({ url, size, style, embedImage }: { url: string; size?: number; style?: string; embedImage?: File | null }) => {
      const fd = new FormData();
      fd.append("url", url);
      if (size) fd.append("size", String(size));
      if (style) fd.append("style", style);
      if (embedImage) fd.append("embed_image", embedImage);
      return request<PreviewResponse>("/qrcode/preview", { method: "POST", body: fd });
    },
  });
}
