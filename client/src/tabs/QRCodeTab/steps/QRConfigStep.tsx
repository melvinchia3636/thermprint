import { useRef } from "react";
import { Icon } from "@iconify/react";
import { useQRCodePrinting } from "../context/QRCodePrintingContext";
import SelectField from "../../../components/ui/SelectField";
import SliderField from "../../../components/ui/SliderField";
import StepCard from "../../../components/ui/StepCard";

const STYLES = [
  { value: 0, label: "Square" },
  { value: 1, label: "Gapped" },
  { value: 2, label: "Circle" },
  { value: 3, label: "Rounded" },
  { value: 4, label: "Vertical Bars" },
  { value: 5, label: "Horizontal Bars" },
];

const STYLE_KEYS = [
  "square",
  "gapped",
  "circle",
  "rounded",
  "vertical-bars",
  "horizontal-bars",
];

export default function QRConfigStep() {
  const { form, setForm, setStep } = useQRCodePrinting();
  const inputRef = useRef<HTMLInputElement>(null);

  const handleEmbedImage = (file: File | undefined) => {
    if (!file) {
      setForm({ embedImage: null, embedPreview: null });
      return;
    }
    setForm({ embedImage: file, embedPreview: URL.createObjectURL(file) });
  };

  return (
    <StepCard
      title="QR Code"
      icon="tabler:qrcode"
      onNext={() => setStep(1)}
      nextDisabled={!form.url}
      nextLabel="Preview"
    >
      <div className="form-control w-full space-y-1">
        <label className="label" htmlFor="qr-url">
          <span className="label-text">URL</span>
        </label>
        <input
          id="qr-url"
          type="url"
          placeholder="https://example.com"
          value={form.url}
          onChange={(e) => setForm({ url: e.target.value })}
          className="input input-bordered w-full"
        />
      </div>
      <div className="mt-4">
        <SliderField
          label="Size"
          value={form.size}
          min={50}
          max={384}
          onChange={(v) => setForm({ size: v })}
        />
      </div>
      <div className="mt-4">
        <SelectField
          label="Style"
          value={STYLE_KEYS.indexOf(form.style)}
          options={STYLES}
          onChange={(v) => setForm({ style: STYLE_KEYS[v] })}
        />
      </div>
      <div className="mt-4">
        <div className="flex flex-col gap-1.5 p-3 rounded-box bg-base-300/50">
          <span className="text-sm font-medium text-base-content truncate">
            Embed Image
          </span>
          {form.embedPreview ? (
            <div className="flex flex-col gap-4 items-center">
              <img
                src={form.embedPreview}
                alt="embed preview"
                className="size-32 object-contain rounded-box"
              />
              <button
                className="btn btn-ghost btn-xs w-full h-auto! py-2! btn-error"
                onClick={(e) => {
                  e.stopPropagation();
                  handleEmbedImage(undefined);
                }}
              >
                <Icon icon="tabler:x" className="size-4" />
                Remove
              </button>
            </div>
          ) : (
            <button
              className="btn btn-outline w-full"
              onClick={() => inputRef.current?.click()}
            >
              <Icon icon="tabler:upload" className="size-4" />
              Click to upload
            </button>
          )}
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => handleEmbedImage(e.target.files?.[0])}
          />
        </div>
      </div>
    </StepCard>
  );
}
