import StepNav from "./components/StepNav";
import { useApp } from "../../context/AppContext";
import PreviewPrintStep from "./steps/PreviewPrintStep";
import SelectImageStep from "./steps/SelectImageStep";
import SettingsStep from "./steps/SettingsStep";

const STEPS = [
  { component: SelectImageStep },
  { component: SettingsStep },
  { component: PreviewPrintStep },
];

function ImageTab() {
  const { step } = useApp();

  return (
    <div className="flex-1 min-h-0 flex flex-col space-y-6">
      <StepNav />
      {STEPS.map((s, i) => i === step && <s.component />)}
    </div>
  );
}

export default ImageTab;
