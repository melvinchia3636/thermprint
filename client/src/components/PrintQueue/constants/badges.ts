export const BADGE: Record<string, { class: string; icon: string }> = {
  queued: { class: "badge badge-soft badge-ghost", icon: "tabler:clock" },
  printing: { class: "badge badge-soft badge-info", icon: "tabler:loader" },
  done: { class: "badge badge-soft badge-success", icon: "tabler:check" },
  failed: {
    class: "badge badge-soft badge-error",
    icon: "tabler:alert-circle",
  },
};
