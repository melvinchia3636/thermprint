import StepNav from "../../components/ui/StepNav";
import {
  QRCodePrintingProvider,
  useQRCodePrinting,
} from "./context/QRCodePrintingContext";
import QRConfigStep from "./steps/QRConfigStep";
import QRPreviewStep from "./steps/QRPreviewStep";

const STEPS = [
  { component: QRConfigStep, label: "Config", icon: "tabler:settings" },
  { component: QRPreviewStep, label: "Preview", icon: "tabler:printer" },
] as const;

function QRCodeTabInner() {
  const { step } = useQRCodePrinting();

  return (
    <div className="flex-1 min-h-0 flex flex-col space-y-6">
      <StepNav steps={STEPS} current={step} onChange={() => {}} />
      {STEPS.map((s, i) => i === step && <s.component />)}
    </div>
  );
}

export default function QRCodeTab() {
  return (
    <QRCodePrintingProvider>
      <QRCodeTabInner />
    </QRCodePrintingProvider>
  );
}
