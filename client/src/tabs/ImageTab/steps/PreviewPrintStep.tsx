import { useEffect, useState } from "react";
import { Icon } from "@iconify/react";
import { useImagePrinting } from "../contexts/ImagePrintingContext";
import { usePreview, usePrint } from "../../../api/print";
import StepCard from "../../../components/ui/StepCard";

export default function PreviewPrintStep() {
  const { image, setStep, setImage, localSettings, defaults } =
    useImagePrinting();
  const settings = localSettings ?? defaults;
  const previewMutation = usePreview();
  const print = usePrint();
  const [lastPreview, setLastPreview] = useState<string | null>(null);

  useEffect(() => {
    if (!image || !settings) return;
    let cancelled = false;
    previewMutation.mutateAsync({ image, settings }).then((data) => {
      if (!cancelled) setLastPreview(data.preview_url);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  const handlePrint = () => {
    if (!image || !settings) return;
    print.mutate({ image, settings });
  };

  return (
    <StepCard
      title="Preview & Print"
      icon="tabler:printer"
      onPrevious={() => setStep(1)}
      onNext={
        lastPreview
          ? () => {
              handlePrint();
              setStep(0);
              setImage(null);
            }
          : undefined
      }
      nextDisabled={!lastPreview}
      nextLabel={print.isPending ? "Printing..." : "Print & Start New"}
    >
      <div className="flex-1 min-h-0 flex items-center justify-center">
        {previewMutation.isPending ? (
          <div className="flex items-center justify-center h-48">
            <span className="loading loading-spinner loading-lg" />
          </div>
        ) : lastPreview ? (
          <figure className="h-full w-full flex items-center justify-center">
            <img
              src={lastPreview}
              alt="print preview"
              className="h-full object-contain"
            />
          </figure>
        ) : (
          <div className="flex items-center justify-center h-48 text-base-content/30 flex-col gap-2">
            <Icon icon="tabler:eye-off" className="text-3xl" />
            Preview will appear here
          </div>
        )}
      </div>
    </StepCard>
  );
}
