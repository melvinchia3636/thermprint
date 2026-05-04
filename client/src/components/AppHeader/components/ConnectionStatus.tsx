import { Icon } from "@iconify/react";
import { useDeviceContext } from "../../../context/DeviceContext";

const STATUS_CONFIG: Record<
  string,
  { icon: string; color: string; label: string }
> = {
  online: {
    icon: "tabler:circle-filled",
    color: "text-success",
    label: "Online",
  },
  connecting: {
    icon: "svg-spinners:180-ring",
    color: "text-base-content/30",
    label: "Connecting",
  },
  offline: {
    icon: "tabler:circle-filled",
    color: "text-base-content/30",
    label: "Offline",
  },
};

export default function ConnectionStatus() {
  const { connection } = useDeviceContext();
  const cfg = STATUS_CONFIG[connection] || STATUS_CONFIG.offline;

  return (
    <div className="flex items-center gap-1.5 mr-1 tooltip" data-tip={cfg.label}>
      <Icon
        icon={cfg.icon}
        className={`size-3 ${cfg.color} ${connection === "connecting" ? "animate-spin" : ""}`}
      />
      <span className="text-xs text-base-content/50 hidden sm:inline">
        {cfg.label}
      </span>
    </div>
  );
}
