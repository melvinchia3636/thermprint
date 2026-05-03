import { type ReactNode } from "react";
import { useQueueDrawer } from "../../../context/QueueDrawerContext";
import PrintQueueMobileView from "../views/mobile";

interface Props {
  children: ReactNode;
}

export default function QueueDrawerWrapper({ children }: Props) {
  const { queueOpen, setQueueOpen } = useQueueDrawer();

  return (
    <div className="drawer drawer-end min-h-0 h-dvh">
      <input
        id="queue-drawer"
        type="checkbox"
        className="drawer-toggle"
        checked={queueOpen}
        onChange={(e) => setQueueOpen(e.target.checked)}
      />
      <div className="drawer-content min-h-0 flex flex-col">{children}</div>
      <PrintQueueMobileView />
    </div>
  );
}
