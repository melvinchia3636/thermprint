import { useState } from "react";
import { Icon } from "@iconify/react";
import { useDeviceContext } from "../context/DeviceContext";
import { useQueueDrawer } from "../context/QueueDrawerContext";
import DeviceSelector from "./DeviceSelector";
import ProjectDescModal from "./ProjectDescModal";

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
  const [showProjectDesc, setShowProjectDesc] = useState(false);
  const { connection, deviceName } = useDeviceContext();
  const { queueOpen, setQueueOpen } = useQueueDrawer();
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
              onClick={() => setShowProjectDesc(true)}
              className="btn btn-ghost btn-square text-base-content/50 hover:text-base-content"
            >
              <Icon icon="tabler:info-circle" className="size-5" />
            </button>
            <a
              href="https://github.com/melvinchia3636/thermprint"
              className="btn btn-ghost btn-square text-base-content/50 hover:text-base-content"
              rel="noreferrer noopener"
              target="_blank"
            >
              <Icon icon="mdi:github" className="size-5" />
            </a>
          </div>
        </div>
      </header>
      <button
        onClick={() => setQueueOpen(!queueOpen)}
        className="btn btn-primary btn-square fixed bottom-6 right-6 shadow-lg lg:hidden z-50"
      >
        <Icon icon="tabler:list" className="size-6" />
      </button>
      <DeviceSelector open={showDialog} onClose={() => setShowDialog(false)} />
      <ProjectDescModal
        open={showProjectDesc}
        onClose={() => setShowProjectDesc(false)}
      />
    </>
  );
}
