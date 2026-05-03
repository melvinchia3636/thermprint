import { createContext, useContext, useState, type ReactNode } from "react";

interface QueueDrawerContextValue {
  queueOpen: boolean;
  setQueueOpen: (v: boolean) => void;
}

const QueueDrawerContext = createContext<QueueDrawerContextValue | null>(null);

export function useQueueDrawer() {
  const ctx = useContext(QueueDrawerContext);
  if (!ctx) throw new Error("useQueueDrawer must be used inside QueueDrawerProvider");
  return ctx;
}

export function QueueDrawerProvider({ children }: { children: ReactNode }) {
  const [queueOpen, setQueueOpen] = useState(false);
  return (
    <QueueDrawerContext.Provider value={{ queueOpen, setQueueOpen }}>
      {children}
    </QueueDrawerContext.Provider>
  );
}
