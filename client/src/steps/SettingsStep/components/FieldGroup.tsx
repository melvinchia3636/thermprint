import type { PrintSettings } from "../../../types";
import type { FieldDef } from "../constants/fields";
import SliderField from "./SliderField";
import SelectField from "./SelectField";
import { Icon } from "@iconify/react";

export default function FieldGroup({
  icon,
  title,
  fields,
  settings,
  onChange,
  alertMsg,
}: {
  icon: string;
  title: string;
  fields: FieldDef[];
  settings: PrintSettings;
  onChange: (key: keyof PrintSettings, value: string) => void;
  alertMsg?: string;
}) {
  return (
    <div>
      <h3 className="text-sm font-semibold text-base-content/70 flex items-center gap-1 mb-3">
        <Icon icon={icon} className="size-4" />
        {title}
      </h3>
      {alertMsg && (
        <div role="alert" className="alert mb-4 alert-info gap-2!">
          <Icon icon="tabler:info-circle" className="size-5 shrink-0" />
          <span>{alertMsg}</span>
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {fields.map((f) =>
          f.type === "select" && f.options ? (
            <SelectField
              key={f.key}
              label={f.label}
              description={f.description}
              value={settings[f.key] as number}
              options={f.options}
              onChange={(v) => onChange(f.key, String(v))}
            />
          ) : (
            <SliderField
              key={f.key}
              label={f.label}
              description={f.description}
              value={settings[f.key] as number}
              min={f.min}
              max={f.max}
              step={f.step}
              onChange={(v) => onChange(f.key, String(v))}
            />
          ),
        )}
      </div>
    </div>
  );
}
