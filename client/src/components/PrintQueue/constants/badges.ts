export const BADGE: Record<string, { class: string; icon: string }> = {
  queued: { class: "badge badge-ghost", icon: "tabler:clock" },
  connecting: { class: "badge badge-secondary", icon: "tabler:bluetooth" },
  printing: { class: "badge badge-info", icon: "svg-spinners:180-ring" },
  done: { class: "badge badge-success", icon: "tabler:check" },
  failed: {
    class: "badge badge-error",
    icon: "tabler:alert-circle",
  },
  cancelled: {
    class: "badge badge-warning",
    icon: "tabler:x",
  },
};
