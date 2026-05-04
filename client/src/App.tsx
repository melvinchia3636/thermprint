import { DeviceProvider } from "./context/DeviceContext";
import { JobProvider } from "./context/JobContext";
import { ThemeProvider } from "./context/ThemeContext";
import { QueueDrawerProvider } from "./context/QueueDrawerContext";
import {
  PrintQueueDesktopView,
  QueueDrawerWrapper,
} from "./components/PrintQueue";
import AppHeader from "./components/AppHeader";
import AppFooter from "./components/AppFooter";
import TabbedContent from "./tabs";
import { ToastContainer } from "react-toastify";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import QueueFab from "./components/PrintQueue/components/QueueFab";

function AppContent() {
  return (
    <QueueDrawerWrapper>
      <AppHeader />
      <main className="flex-1 min-h-0 max-w-6xl mx-auto p-6 flex gap-6 items-stretch w-full">
        <TabbedContent />
        <PrintQueueDesktopView />
      </main>
      <QueueFab />
      <AppFooter />
    </QueueDrawerWrapper>
  );
}

const qc = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={qc}>
      <ThemeProvider>
        <DeviceProvider>
          <JobProvider>
            <QueueDrawerProvider>
              <AppContent />
            </QueueDrawerProvider>
          </JobProvider>
        </DeviceProvider>
      </ThemeProvider>
      <ToastContainer position="bottom-center" />
    </QueryClientProvider>
  );
}
