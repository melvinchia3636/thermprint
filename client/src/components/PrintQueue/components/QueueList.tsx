import { Icon } from "@iconify/react";
import { useJobContext } from "../../../context/JobContext";
import QueueListItem from "./QueueListItem";

export default function QueueList() {
  const { jobsData, cancelJob, deleteJob, hasMore, isLoadingMore, loadMore } =
    useJobContext();

  return (
    <>
      <header className="flex items-center justify-between pt-4 px-4">
        <h2 className="card-title">
          <Icon icon="tabler:list" className="size-6" />
          Print Queue
        </h2>
        <label
          htmlFor="queue-drawer"
          className="btn btn-ghost btn-sm lg:hidden px-0!"
        >
          <Icon icon="tabler:x" className="size-5" />
        </label>
      </header>
      {!jobsData || jobsData.length === 0 ? (
        <p className="text-base-content/30 flex text-lg flex-col flex-1 justify-center items-center gap-2">
          <Icon icon="tabler:file-off" className="size-8" />
          No print jobs yet.
        </p>
      ) : (
        <div className="flex flex-col gap-2 p-4" role="list">
          {jobsData.map((j) => (
            <QueueListItem
              key={j.job_id}
              job={j}
              onCancel={(id) => cancelJob.mutate(id)}
              onDelete={(id) => deleteJob.mutate(id)}
            />
          ))}
          {hasMore && (
            <button
              onClick={loadMore}
              disabled={isLoadingMore}
              className="btn btn-ghost btn-sm w-full mt-2"
            >
              {isLoadingMore && <Icon icon="svg-spinners:ring-resize" />}
              {isLoadingMore ? "Loading..." : "Load more"}
            </button>
          )}
        </div>
      )}
    </>
  );
}
