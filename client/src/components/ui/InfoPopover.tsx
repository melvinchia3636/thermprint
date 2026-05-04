import { Tooltip } from "react-tooltip";
import { Icon } from "@iconify/react";

export default function InfoPopover({ description, id }: { description: string; id: string }) {
  return (
    <>
      <span
        data-tooltip-id={id}
        data-tooltip-content={description}
        data-tooltip-place="right"
        className="cursor-pointer text-base-content/30 hover:text-base-content/60 transition-colors inline-flex"
      >
        <Icon icon="tabler:info-circle" className="size-4" />
      </span>
      <Tooltip
        id={id}
        className="max-w-80 z-50"
        style={{
          backgroundColor: "var(--color-base-100)",
          color: "var(--color-base-content)",
          border: "1px solid var(--color-base-300)",
          borderRadius: "var(--radius-box)",
          fontSize: "0.875rem",
          lineHeight: "1.5",
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
          opacity: 1,
        }}
      />
    </>
  );
}
