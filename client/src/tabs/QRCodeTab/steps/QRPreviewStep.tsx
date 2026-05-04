import { useEffect, useState } from "react";
import { Icon } from "@iconify/react";
import StepCard from "../../../components/StepCard";
import { useQRPreview, usePrintQRCode } from "../../../api/print";
import { useQRCodePrinting } from "../context/QRCodePrintingContext";

export default function QRPreviewStep() {
  const {
    form: { url, size, style, embedImage },
    setStep,
    reset,
  } = useQRCodePrinting();
  const previewMutation = useQRPreview();
  const printMutation = usePrintQRCode();
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!url) return;
    let cancelled = false;
    previewMutation.mutateAsync({ url, size, style, embedImage }).then((data) => {
      if (!cancelled) setPreviewUrl(data.preview_url);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  const handlePrint = () => {
    if (!url) return;
    printMutation.mutate({ url, size, style, embedImage }, { onSuccess: reset });
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
      <div role="alert" className="alert mb-4 alert-warning gap-2!">
        <Icon icon="tabler:info-circle" className="size-5 shrink-0" />
        <span>
          Make sure the QRCode is scannable by your preferred QRCode scanner
          before proceeding to printing it out.
        </span>
      </div>
      <div className="flex-1 min-h-0 flex items-center justify-center">
        {previewMutation.isPending ? (
          <div className="flex items-center justify-center h-48">
            <span className="loading loading-spinner loading-lg" />
          </div>
        ) : previewUrl ? (
          <figure className="h-full w-full flex items-center justify-center p-4">
            <img
              src={previewUrl}
              alt="QR code preview"
              className="max-h-full object-contain"
              style={{ maxWidth: `${size}px` }}
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
