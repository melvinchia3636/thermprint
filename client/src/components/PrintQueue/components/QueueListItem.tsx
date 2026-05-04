import { Icon } from "@iconify/react";
import { BADGE } from "../constants/badges";
import { JobStatusResponse } from "../../../types";
import dayjs from "dayjs";

import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(relativeTime);

function chunkProgress(progress: string | null) {
  const m = progress?.match(/^(\d+)\/(\d+) chunks$/);
  if (!m) return null;
  return { current: Number(m[1]), total: Number(m[2]) };
}

export default function QueueListItem({
  job,
  onCancel,
}: {
  job: JobStatusResponse;
  onCancel: (jobId: string) => void;
}) {
  const badge = BADGE[job.status] || {
    class: "badge",
    icon: "tabler:question-mark",
  };

  const typeIcon = job.type === "qr_code" ? "tabler:qrcode" : "tabler:photo";
  const typeLabel = job.type === "qr_code" ? "QR Code" : "Image";

  const progress = chunkProgress(job.progress);

  return (
    <div
      role="listitem"
      className="flex flex-col gap-1.5 bg-base-300 rounded-box p-3"
    >
      <div className="flex items-start justify-between gap-2">
        <span className="flex items-center gap-2">
          <span className={`${badge.class} gap-1`}>
            <Icon icon={badge.icon} className="size-4" />
            {job.status}
          </span>
        </span>
        <div className="items-end flex flex-col">
          <span className="text-xs text-base-content/50 flex items-center gap-1">
            <Icon icon={typeIcon} className="size-3.5" />
            {typeLabel}
          </span>
          <span className="text-xs text-base-content/50 whitespace-nowrap">
            {dayjs(job.created_at).fromNow()}
          </span>
        </div>
      </div>
      {progress ? (
        <div className="flex flex-col gap-0.5 mt-2">
          <progress
            className="progress progress-primary w-full"
            value={progress.current}
            max={progress.total}
          />
          <span className="text-xs text-base-content/50">{job.progress}</span>
        </div>
      ) : (
        (job.progress || job.error) && (
          <span className="text-sm min-w-0 truncate">
            {job.progress || job.error}
          </span>
        )
      )}
      {!["done", "cancelled"].includes(job.status) && (
        <button
          onClick={() => onCancel(job.job_id)}
          className="btn btn-ghost btn-error w-full"
        >
          <Icon icon="tabler:x" className="size-4" />
          Cancel
        </button>
      )}
    </div>
  );
}
