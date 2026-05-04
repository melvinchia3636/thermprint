import { createContext, useContext, useState, type ReactNode } from "react";
import { useSettings } from "../../../api/settings";
import type { PrintSettings } from "../../../types";

interface ImagePrintingContextValue {
  step: number;
  setStep: (s: number) => void;
  image: File | null;
  setImage: (f: File | null) => void;
  localSettings: PrintSettings | null;
  setLocalSettings: (s: PrintSettings | null) => void;
  defaults: PrintSettings | undefined;
}

const ImagePrintingContext = createContext<ImagePrintingContextValue | null>(null);

export function useImagePrinting() {
  const ctx = useContext(ImagePrintingContext);
  if (!ctx) throw new Error("useImagePrinting must be used inside ImagePrintingProvider");
  return ctx;
}

export function ImagePrintingProvider({ children }: { children: ReactNode }) {
  const { data: defaults } = useSettings();
  const [image, setImage] = useState<File | null>(null);
  const [step, setStep] = useState(0);
  const [localSettings, setLocalSettings] = useState<PrintSettings | null>(null);

  return (
    <ImagePrintingContext
      value={{
        step,
        setStep,
        image,
        setImage,
        localSettings,
        setLocalSettings,
        defaults,
      }}
    >
      {children}
    </ImagePrintingContext>
  );
}
