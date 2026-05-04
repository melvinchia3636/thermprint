import InfoPopover from "../tabs/ImageTab/steps/SettingsStep/components/InfoPopover";

export default function SliderField({
  label,
  description,
  value,
  min,
  max,
  step,
  onChange,
}: {
  label: string;
  description?: string;
  value: number;
  min?: number;
  max?: number;
  step?: number;
  onChange: (v: number) => void;
}) {
  return (
    <label className="flex flex-col gap-1.5 p-3 rounded-box bg-base-300/50">
      <span className="flex items-center justify-between gap-2">
        <span className="flex items-center gap-1.5 min-w-0">
          <span className="text-sm font-medium text-base-content truncate">
            {label}
          </span>
          {description && <InfoPopover description={description} id={label} />}
        </span>
        <span className="text-sm font-mono font-semibold text-base-content shrink-0 min-w-[3ch] text-right">
          {value}
        </span>
      </span>
      <input
        type="range"
        value={value}
        min={min}
        max={max}
        step={step ?? 1}
        onChange={(e) => onChange(Number(e.target.value))}
        className="range w-full range-sm"
      />
    </label>
  );
}
