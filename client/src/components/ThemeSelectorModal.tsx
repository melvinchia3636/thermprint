import { Icon } from "@iconify/react";
import { THEMES, useTheme } from "../context/ThemeContext";

export default function ThemeSelectorModal({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  const { theme, setTheme } = useTheme();

  return (
    <dialog className="modal" open={open} onClose={onClose}>
      <div className="modal-box max-h-[90dvh] max-w-[90vw] lg:max-w-[50vw] overflow-y-auto">
        <h3 className="font-bold text-lg flex items-center gap-2">
          <Icon icon="tabler:palette" className="size-5" />
          Select Theme
        </h3>
        <div className="py-4 grid grid-cols-[repeat(auto-fit,minmax(140px,1fr))] gap-3">
          {THEMES.map((t) => (
            <div
              className={`rounded-md overflow-hidden ${theme === t && "ring-2 ring-primary ring-offset-base-100 ring-offset-2"}`}
              data-theme={t}
              key={t}
              onClick={() => setTheme(t)}
            >
              <div className="grid grid-cols-5 grid-rows-3">
                <div className="row-span-2 bg-base-200" />
                <div className="row-span-3 col-span-4 bg-base-100 p-2">
                  <p className="font-semibold text-base mb-1">{t}</p>
                  <div className="flex items-center gap-1">
                    {[
                      ["bg-primary", "text-primary-content"],
                      ["bg-secondary", "text-secondary-content"],
                      ["bg-accent", "text-accent-content"],
                      ["bg-neutral", "text-neutral-content"],
                    ].map((e) => (
                      <div
                        className={`rounded-sm flex-1 aspect-square flex items-center justify-center font-semibold ${e[0]} ${e[1]}`}
                      >
                        A
                      </div>
                    ))}
                  </div>
                </div>
                <div className="row-span-1 col-span-1 bg-base-300" />
              </div>
            </div>
          ))}
        </div>
        <div className="modal-action">
          <button className="btn" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
      <form method="dialog" className="modal-backdrop" onClick={onClose}>
        <button>close</button>
      </form>
    </dialog>
  );
}
