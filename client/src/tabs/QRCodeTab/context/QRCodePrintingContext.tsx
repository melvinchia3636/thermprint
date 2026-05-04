import { createContext, useContext, useState, type ReactNode } from "react";

interface QRCodeForm {
  url: string;
  size: number;
  style: string;
  embedImage: File | null;
  embedPreview: string | null;
}

interface QRCodePrintingContextValue {
  step: number;
  setStep: (s: number) => void;
  form: QRCodeForm;
  setForm: (f: Partial<QRCodeForm>) => void;
  reset: () => void;
}

const QRCodePrintingContext = createContext<QRCodePrintingContextValue | null>(null);

export function useQRCodePrinting() {
  const ctx = useContext(QRCodePrintingContext);
  if (!ctx) throw new Error("useQRCodePrinting must be used inside QRCodePrintingProvider");
  return ctx;
}

const INITIAL_FORM: QRCodeForm = { url: "", size: 384, style: "square", embedImage: null, embedPreview: null };

export function QRCodePrintingProvider({ children }: { children: ReactNode }) {
  const [step, setStep] = useState(0);
  const [form, setFormState] = useState<QRCodeForm>(INITIAL_FORM);

  const setForm = (patch: Partial<QRCodeForm>) => {
    setFormState((prev) => ({ ...prev, ...patch }));
  };

  const reset = () => {
    setStep(0);
    setFormState(INITIAL_FORM);
  };

  return (
    <QRCodePrintingContext value={{ step, setStep, form, setForm, reset }}>
      {children}
    </QRCodePrintingContext>
  );
}
