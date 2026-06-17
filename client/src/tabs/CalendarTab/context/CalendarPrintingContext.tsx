import { createContext, useContext, useState, type ReactNode } from "react";

interface CalendarForm {
  year: number;
  month: number;
}

interface CalendarPrintingContextValue {
  step: number;
  setStep: (s: number) => void;
  form: CalendarForm;
  setForm: (f: Partial<CalendarForm>) => void;
  reset: () => void;
}

const CalendarPrintingContext = createContext<CalendarPrintingContextValue | null>(null);

export function useCalendarPrinting() {
  const ctx = useContext(CalendarPrintingContext);
  if (!ctx) throw new Error("useCalendarPrinting must be used inside CalendarPrintingProvider");
  return ctx;
}

const now = new Date();
const INITIAL_FORM: CalendarForm = {
  year: now.getFullYear(),
  month: now.getMonth() + 1,
};

export function CalendarPrintingProvider({ children }: { children: ReactNode }) {
  const [step, setStep] = useState(0);
  const [form, setFormState] = useState<CalendarForm>(INITIAL_FORM);

  const setForm = (patch: Partial<CalendarForm>) => {
    setFormState((prev) => ({ ...prev, ...patch }));
  };

  const reset = () => {
    setStep(0);
    setFormState(INITIAL_FORM);
  };

  return (
    <CalendarPrintingContext value={{ step, setStep, form, setForm, reset }}>
      {children}
    </CalendarPrintingContext>
  );
}
