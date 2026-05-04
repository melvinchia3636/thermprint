import InfoPopover from "../tabs/ImageTab/steps/SettingsStep/components/InfoPopover";

export default function SelectField({
  label,
  description,
  value,
  options,
  onChange,
}: {
  label: string;
  description?: string;
  value: number;
  options: { value: number; label: string }[];
  onChange: (v: number) => void;
}) {
  return (
    <label className="flex flex-col gap-1.5 p-3 rounded-box bg-base-300/50">
      <span className="flex items-center gap-1.5 min-w-0">
        <span className="text-sm font-medium text-base-content truncate">
          {label}
        </span>
        {description && <InfoPopover description={description} id={label} />}
      </span>
      <select
        className="select select-bordered w-full"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </label>
  );
}
