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
    <fieldset className="flex flex-col gap-1.5 p-3 rounded-box bg-base-300/50">
      <legend className="flex items-center gap-1.5 min-w-0 px-0">
        <span className="text-sm font-medium text-base-content truncate">
          {label}
        </span>
        {description && <InfoPopover description={description} id={label} />}
      </legend>
      <div className="flex gap-2">
        {options.map((opt) => (
          <button
            key={opt.value}
            onClick={() => onChange(opt.value)}
            className={`btn btn-sm flex-1 ${value === opt.value ? "btn-primary" : "btn-ghost border border-base-content/10"}`}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </fieldset>
  );
}
