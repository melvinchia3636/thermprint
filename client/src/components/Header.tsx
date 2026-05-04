import { useState } from "react";
import { Icon } from "@iconify/react";
import { useApp } from "../context/AppContext";
import { useQueueDrawer } from "../context/QueueDrawerContext";
import DeviceSelector from "./DeviceSelector";

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

export default function Header() {
  const [showDialog, setShowDialog] = useState(false);
  const { localSettings, defaults, jobsData, connection } = useApp();
  const { queueOpen, setQueueOpen } = useQueueDrawer();
  const deviceName = (localSettings ?? defaults)?.ble_device_name;
  const jobCount = jobsData?.length ?? 0;
  const cfg = STATUS_CONFIG[connection] || STATUS_CONFIG.offline;

  return (
    <>
      <header className="bg-base-200 border-b border-base-300">
        <div className="max-w-6xl mx-auto gap-6 px-6 py-4 flex items-center justify-between">
          <div className="text-lg lg:text-xl font-bold flex items-center gap-2">
            <Icon
              icon="tabler:receipt"
              className="text-primary size-6 lg:size-8"
            />
            <div className="flex flex-col">
              <h1>ThermPrint</h1>
              <small className="text-xs text-base-content/50 font-medium">
                A reverse eng. project
              </small>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div
              className="flex items-center gap-1.5 mr-1 tooltip"
              data-tip={cfg.label}
            >
              <Icon
                icon={cfg.icon}
                className={`size-3 ${cfg.color} ${connection === "connecting" ? "animate-spin" : ""}`}
              />
              <span className="text-xs text-base-content/50 hidden sm:inline">
                {cfg.label}
              </span>
            </div>
            <button
              onClick={() => setShowDialog(true)}
              className="btn btn-ghost btn-sm gap-1"
            >
              <Icon icon="tabler:bluetooth" className="size-5 text-primary" />
              <span className="text-sm truncate max-w-32 hidden sm:inline">
                {deviceName}
              </span>
            </button>
            <button
              onClick={() => setQueueOpen(!queueOpen)}
              className="btn btn-ghost btn-sm btn-square relative lg:hidden"
            >
              <Icon icon="tabler:list" className="size-5" />
              {jobCount > 0 && (
                <span className="badge badge-primary badge-xs absolute -top-1 -right-1">
                  {jobCount}
                </span>
              )}
            </button>
          </div>
        </div>
      </header>
      <DeviceSelector open={showDialog} onClose={() => setShowDialog(false)} />
    </>
  );
}
