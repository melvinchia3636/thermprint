import { useRef, useState, useCallback } from "react";
import { Icon } from "@iconify/react";
import { useImagePrinting } from "../contexts/ImagePrintingContext";
import StepCard from "../../../components/ui/StepCard";

export default function SelectImageStep() {
  const { image, setImage, setStep } = useImagePrinting();
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const handle = useCallback(
    (file: File | undefined) => {
      if (!file) return;
      setPreview(URL.createObjectURL(file));
      setImage(file);
    },
    [setImage],
  );

  const handlePaste = useCallback(async () => {
    try {
      const items = await navigator.clipboard.read();
      for (const item of items) {
        for (const type of item.types) {
          if (type.startsWith("image/")) {
            const blob = await item.getType(type);
            const file = new File(
              [blob],
              `clipboard.${type.split("/")[1] || "png"}`,
              { type },
            );
            handle(file);
            return;
          }
        }
      }
    } catch {
      // clipboard empty or permission denied — silently ignore
    }
  }, [handle]);

  return (
    <StepCard
      title="Select Image"
      icon="tabler:photo"
      onNext={() => setStep(1)}
      nextDisabled={!image}
      nextLabel="Next: Settings"
    >
      <figure
        className="border-2 border-dashed flex-1 border-base-content/30 rounded-box w-full cursor-pointer min-h-0 flex flex-col items-center justify-center p-4"
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => handle(e.target.files?.[0])}
        />
        {preview ? (
          <img
            src={preview}
            alt="preview"
            className="w-full object-contain min-h-0 rounded-2xl"
          />
        ) : (
          <span className="text-base-content/30 flex xl:text-lg flex-col items-center gap-2">
            <Icon icon="meteor-icons:upload" className="size-12 xl:size-20" />
            Click to select an image
          </span>
        )}
      </figure>
      <button className="btn btn-outline w-full mt-4" onClick={handlePaste}>
        <Icon icon="tabler:clipboard" className="size-5" />
        Paste from clipboard
      </button>
    </StepCard>
  );
}
