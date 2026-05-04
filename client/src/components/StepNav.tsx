import { Icon } from "@iconify/react";

export default function StepNav({
  steps,
  current,
  onChange,
}: {
  steps: readonly { label: string; icon: string }[];
  current: number;
  onChange: (i: number) => void;
}) {
  return (
    <nav aria-label="Step progress"><ul className="flex items-end w-full gap-2">
      {steps.map((s, i) => (
        <li
          key={s.label}
          className="cursor-pointer after:font-semibold w-full"
          onClick={() => onChange(i)}
        >
          <div className="flex items-center text-center mb-1 text-sm gap-1 md:flex-row flex-col">
            <Icon icon={s.icon} className="size-4 shrink-0" />
            {s.label}
          </div>
          <div
            className={`w-full relative h-2 rounded-full border-2 ${
              i < current
                ? "bg-primary border-primary"
                : i === current
                  ? "border-primary after:w-1/2 after:h-1 after:absolute after:top-0 after:left-0 after:bg-primary"
                  : "border-base-content/20"
            }`}
          />
        </li>
      ))}
    </ul></nav>
  );
}
