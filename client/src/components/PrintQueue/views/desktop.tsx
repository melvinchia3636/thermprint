import QueueList from "../components/QueueDetails";

export default function PrintQueueDesktopView() {
  return (
    <div className="hidden lg:flex w-80 shrink-0">
      <div className="card bg-base-200 shadow-sm flex-1 min-w-0">
        <QueueList />
      </div>
    </div>
  );
}
