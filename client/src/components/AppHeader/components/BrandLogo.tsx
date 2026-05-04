import { Icon } from "@iconify/react";

export default function BrandLogo() {
  return (
    <div className="text-lg lg:text-xl font-bold flex items-center gap-2">
      <Icon icon="tabler:receipt" className="text-primary size-6 lg:size-8" />
      <div className="flex flex-col">
        <h1>ThermPrint</h1>
        <small className="text-xs text-base-content/50 font-medium">
          A reverse eng. project
        </small>
      </div>
    </div>
  );
}
