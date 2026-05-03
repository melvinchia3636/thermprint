import { AppProvider, useApp } from "./context/AppContext";
import { QueueDrawerProvider } from "./context/QueueDrawerContext";
import SelectImageStep from "./steps/SelectImageStep";
import SettingsStep from "./steps/SettingsStep";
import PreviewPrintStep from "./steps/PreviewPrintStep";
import {
  PrintQueueDesktopView,
  QueueDrawerWrapper,
} from "./components/PrintQueue";
import Header from "./components/Header";
import StepNav from "./components/StepNav";
import LoadingScreen from "./components/LoadingScreen";

const STEPS = [
  { component: SelectImageStep },
  { component: SettingsStep },
  { component: PreviewPrintStep },
];

function AppContent() {
  const { step, defaults } = useApp();
  if (!defaults) return <LoadingScreen />;

  return (
    <QueueDrawerWrapper>
      <Header />
      <div className="flex-1 min-h-0 max-w-6xl mx-auto p-6 flex gap-6 items-stretch w-full">
        <div className="flex-1 min-h-0 flex flex-col space-y-6">
          <StepNav />
          {STEPS.map((s, i) => i === step && <s.component />)}
        </div>
        <PrintQueueDesktopView />
      </div>
    </QueueDrawerWrapper>
  );
}

export default function App() {
  return (
    <AppProvider>
      <QueueDrawerProvider>
        <AppContent />
      </QueueDrawerProvider>
    </AppProvider>
  );
}
