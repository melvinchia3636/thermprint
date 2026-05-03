import { Icon } from "@iconify/react";
import type { ReactNode } from "react";

interface Props {
  title: string;
  icon: string;
  children: ReactNode;
  onPrevious?: () => void;
  onNext?: () => void;
  nextDisabled?: boolean;
  nextLabel?: string;
  actionButton?: ReactNode;
}

export default function StepCard({
  title,
  icon,
  children,
  onPrevious,
  onNext,
  nextDisabled,
  nextLabel,
  actionButton,
}: Props) {
  return (
    <div className="card bg-base-200 shadow-sm min-h-0 flex-1">
      <div className="card-body flex flex-col min-h-0">
        <div className="flex items-center justify-between mb-2">
          <h2 className="card-title text-base sm:text-xl">
            <Icon icon={icon} className="size-5 sm:size-6" /> {title}
          </h2>
          {actionButton}
        </div>
        <div className="flex-1 min-h-0 flex flex-col">{children}</div>
        <div className="flex justify-between mt-3">
          {onPrevious && (
            <button onClick={onPrevious} className="btn btn-outline">
              <Icon icon="tabler:arrow-left" className="size-4" />
              Back
            </button>
          )}
          {onNext && (
            <button
              onClick={onNext}
              disabled={nextDisabled}
              className={`btn btn-neutral ${!onPrevious && "w-full"}`}
            >
              {nextLabel ?? "Next"}
              <Icon icon="tabler:arrow-right" className="size-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
