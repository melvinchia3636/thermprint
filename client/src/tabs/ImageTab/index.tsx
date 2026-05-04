import StepNav from "../../components/StepNav";
import {
  ImagePrintingProvider,
  useImagePrinting,
} from "./contexts/ImagePrintingContext";
import PreviewPrintStep from "./steps/PreviewPrintStep";
import SelectImageStep from "./steps/SelectImageStep";
import SettingsStep from "./steps/SettingsStep";
import LoadingScreen from "../../components/LoadingScreen";

const STEPS = [
  { component: SelectImageStep, label: "Select", icon: "tabler:photo" },
  { component: SettingsStep, label: "Settings", icon: "tabler:adjustments" },
  { component: PreviewPrintStep, label: "Preview", icon: "tabler:printer" },
] as const;

function ImageTabInner() {
  const { step, setStep, defaults } = useImagePrinting();
  if (!defaults) return <LoadingScreen />;

  return (
    <div className="flex-1 min-h-0 flex flex-col space-y-6">
      <StepNav steps={STEPS} current={step} onChange={setStep} />
      {STEPS.map((s, i) => i === step && <s.component />)}
    </div>
  );
}

export default function ImageTab() {
  return (
    <ImagePrintingProvider>
      <ImageTabInner />
    </ImagePrintingProvider>
  );
}
