import { Icon } from "@iconify/react";
import { useApp } from "../../../context/AppContext";
import { BADGE } from "../constants/badges";

export default function QueueList() {
  const { jobsData, cancelJob } = useApp();

  return (
    <>
      <div className="flex items-center justify-between pt-4 px-4">
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
      </div>
      {!jobsData || jobsData.length === 0 ? (
        <p className="text-base-content/30 flex text-lg flex-col flex-1 justify-center items-center gap-2">
          <Icon icon="tabler:file-off" className="size-8" />
          No print jobs yet.
        </p>
      ) : (
        <div className="overflow-x-auto min-w-0">
          <table className="table table-sm">
            <thead>
              <tr>
                <th>Status</th>
                <th>Progress</th>
                <th>Created</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {jobsData.map((j) => {
                const badge = BADGE[j.status] || {
                  class: "badge",
                  icon: "tabler:question-mark",
                };
                return (
                  <tr key={j.job_id}>
                    <td>
                      <span className={`${badge.class} gap-1`}>
                        <Icon icon={badge.icon} className="size-4" />
                        {j.status}
                      </span>
                    </td>
                    <td className="text-sm">{j.progress || j.error || "-"}</td>
                    <td className="text-sm whitespace-nowrap">
                      {new Date(j.created_at).toLocaleTimeString()}
                    </td>
                    <td>
                      <button
                        onClick={() => cancelJob.mutate(j.job_id)}
                        className="btn btn-ghost btn-xs text-error"
                      >
                        <Icon icon="tabler:x" className="size-4" />
                        Cancel
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
