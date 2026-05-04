import { useImagePrinting } from "../../contexts/ImagePrintingContext";
import FieldGroup from "./components/FieldGroup";
import { IMAGE_FIELDS, PRINTER_FIELDS } from "./constants/fields";
import { useUpdateSettings } from "../../../../api/settings";
import StepCard from "../../../../components/ui/StepCard";

export default function SettingsStep() {
  const { setStep, localSettings, setLocalSettings, defaults } =
    useImagePrinting();
  const updateSettings = useUpdateSettings();
  const effective = localSettings ?? defaults;

  const set = (key: string, value: string) => {
    if (!effective) return;
    const n = Number(value);
    setLocalSettings({ ...effective, [key]: isNaN(n) ? value : n });
  };

  const handleNext = () => {
    if (effective)
      updateSettings.mutate(effective, { onSuccess: () => setStep(2) });
  };

  return (
    <StepCard
      title="Settings"
      icon="tabler:adjustments"
      onPrevious={() => setStep(0)}
      onNext={handleNext}
      nextDisabled={updateSettings.isPending}
      nextLabel={updateSettings.isPending ? "Saving..." : "Next: Preview"}
    >
      {effective && (
        <div className="flex flex-col gap-6 overflow-y-auto">
          <FieldGroup
            icon="tabler:photo"
            title="Image Processing"
            fields={IMAGE_FIELDS}
            settings={effective}
            onChange={set}
          />
          <div className="border-t border-base-300" />
          <FieldGroup
            icon="tabler:printer"
            title="Printer"
            fields={PRINTER_FIELDS}
            settings={effective}
            onChange={set}
            alertMsg="Changing these configurations will not affect the preview in the next step."
          />
        </div>
      )}
    </StepCard>
  );
}
