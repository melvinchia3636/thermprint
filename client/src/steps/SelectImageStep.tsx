import { useRef, useState } from "react";
import { Icon } from "@iconify/react";
import { useApp } from "../context/AppContext";
import StepCard from "../components/StepCard";

export default function SelectImageStep() {
  const { image, setImage, setStep } = useApp();
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const handle = (file: File | undefined) => {
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    setImage(file);
  };

  return (
    <StepCard
      title="Select Image"
      icon="tabler:photo"
      onNext={() => setStep(1)}
      nextDisabled={!image}
      nextLabel="Next: Settings"
    >
      <div
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
      </div>
    </StepCard>
  );
}
