import { Icon } from "@iconify/react";
import { useQueueDrawer } from "../../../context/QueueDrawerContext";

export default function QueueFab() {
  const { queueOpen, setQueueOpen } = useQueueDrawer();

  return (
    <button
      onClick={() => setQueueOpen(!queueOpen)}
      className="btn btn-primary btn-square fixed bottom-6 right-6 shadow-lg lg:hidden z-50"
    >
      <Icon icon="tabler:list" className="size-6" />
    </button>
  );
}
