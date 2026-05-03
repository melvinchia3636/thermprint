import InfoPopover from "./InfoPopover";

interface Props {
  label: string;
  description?: string;
  value: number;
  options: { value: number; label: string }[];
  onChange: (v: number) => void;
}

export default function SelectField({
  label,
  description,
  value,
  options,
  onChange,
}: Props) {
  return (
    <div className="flex flex-col gap-1.5 p-3 rounded-box bg-base-300/50">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-1.5 min-w-0">
          <span className="text-sm font-medium text-base-content truncate">
            {label}
          </span>
          {description && <InfoPopover description={description} id={label} />}
        </div>
      </div>
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
    </div>
  );
}
