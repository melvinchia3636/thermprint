import { DeviceProvider } from "./context/DeviceContext";
import { JobProvider } from "./context/JobContext";
import { QueueDrawerProvider } from "./context/QueueDrawerContext";
import {
  PrintQueueDesktopView,
  QueueDrawerWrapper,
} from "./components/PrintQueue";
import Header from "./components/Header";
import TabbedContent from "./tabs";
import { ToastContainer } from "react-toastify";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

function AppContent() {
  return (
    <QueueDrawerWrapper>
      <Header />
      <main className="flex-1 min-h-0 max-w-6xl mx-auto p-6 flex gap-6 items-stretch w-full">
        <TabbedContent />
        <PrintQueueDesktopView />
      </main>
      <footer className="text-base-content/30 text-center pb-6 text-sm px-8">
        Made with 🖤 by{" "}
        <a
          href="https://melvinchia.dev"
          rel="noreferrer noopener"
          target="_blank"
          className="underline text-secondary"
        >
          Melvin Chia
        </a>
        . 0.087x liver consumed. Project under MIT License.
      </footer>
    </QueueDrawerWrapper>
  );
}

const qc = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={qc}>
      <DeviceProvider>
        <JobProvider>
          <QueueDrawerProvider>
            <AppContent />
          </QueueDrawerProvider>
        </JobProvider>
      </DeviceProvider>
      <ToastContainer position="bottom-center" />
    </QueryClientProvider>
  );
}
