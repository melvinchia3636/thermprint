import { Icon } from "@iconify/react";
import { useApp } from "../../../context/AppContext";

const STEPS = [
  { label: "Select", icon: "tabler:photo" },
  { label: "Settings", icon: "tabler:adjustments" },
  { label: "Preview", icon: "tabler:printer" },
] as const;

export default function StepNav() {
  const { step, setStep } = useApp();

  return (
    <nav aria-label="Step progress"><ul className="flex items-end w-full gap-2">
      {STEPS.map((s, i) => (
        <li
          key={s.label}
          className="cursor-pointer after:font-semibold w-full"
          onClick={() => setStep(i)}
        >
          <div className="flex items-center text-center mb-1 text-sm gap-1 md:flex-row flex-col">
            <Icon icon={s.icon} className="size-4 shrink-0" />
            {s.label}
          </div>
          <div
            className={`w-full relative h-2 rounded-full border-2 ${
              i < step
                ? "bg-primary border-primary"
                : i === step
                  ? "border-primary after:w-1/2 after:h-1 after:absolute after:top-0 after:left-0 after:bg-primary"
                  : "border-base-content/20"
            }`}
          />
        </li>
      ))}
    </ul></nav>
  );
}
