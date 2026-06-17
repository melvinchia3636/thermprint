import StepNav from "../../components/ui/StepNav";
import {
  CalendarPrintingProvider,
  useCalendarPrinting,
} from "./context/CalendarPrintingContext";
import CalendarConfigStep from "./steps/CalendarConfigStep";
import CalendarPreviewStep from "./steps/CalendarPreviewStep";

const STEPS = [
  { component: CalendarConfigStep, label: "Config", icon: "tabler:settings" },
  { component: CalendarPreviewStep, label: "Preview", icon: "tabler:printer" },
] as const;

function CalendarTabInner() {
  const { step } = useCalendarPrinting();

  return (
    <div className="flex-1 min-h-0 flex flex-col space-y-6">
      <StepNav steps={STEPS} current={step} onChange={() => {}} />
      {STEPS.map((s, i) => i === step && <s.component />)}
    </div>
  );
}

export default function CalendarTab() {
  return (
    <CalendarPrintingProvider>
      <CalendarTabInner />
    </CalendarPrintingProvider>
  );
}
