import { useEffect, useState } from "react";
import { Icon } from "@iconify/react";
import { useCalendarPreview, usePrintCalendar } from "../../../api/print";
import { useCalendarPrinting } from "../context/CalendarPrintingContext";
import StepCard from "../../../components/ui/StepCard";

export default function CalendarPreviewStep() {
  const {
    form: { year, month },
    setStep,
    reset,
  } = useCalendarPrinting();
  const previewMutation = useCalendarPreview();
  const printMutation = usePrintCalendar();
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!year || !month) return;
    let cancelled = false;
    previewMutation.mutateAsync({ year, month }).then((data) => {
      if (!cancelled) setPreviewUrl(data.preview_url);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  const handlePrint = () => {
    if (!year || !month) return;
    printMutation.mutate({ year, month }, { onSuccess: reset });
  };

  return (
    <StepCard
      title="Preview & Print"
      icon="tabler:printer"
      onPrevious={() => setStep(0)}
      onNext={previewUrl ? handlePrint : undefined}
      nextDisabled={!previewUrl || printMutation.isPending}
      nextLabel={printMutation.isPending ? "Printing..." : "Print & Start New"}
    >
      <div className="flex-1 min-h-0 flex items-center justify-center">
        {previewMutation.isPending ? (
          <div className="flex items-center justify-center h-48">
            <span className="loading loading-spinner loading-lg" />
          </div>
        ) : previewUrl ? (
          <figure className="h-full w-full flex items-center justify-center p-4 bg-white rounded-box">
            <img
              src={previewUrl}
              alt="Calendar preview"
              className="max-h-full object-contain"
              style={{ maxWidth: "384px" }}
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
