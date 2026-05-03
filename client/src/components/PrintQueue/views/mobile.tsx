import QueueList from "../components/QueueDetails";

export default function PrintQueueMobileView() {
  return (
    <div className="drawer-side z-50">
      <label htmlFor="queue-drawer" className="drawer-overlay" />
      <div className="w-full sm:w-96 flex flex-col min-h-full bg-base-200">
        <QueueList />
      </div>
    </div>
  );
}
