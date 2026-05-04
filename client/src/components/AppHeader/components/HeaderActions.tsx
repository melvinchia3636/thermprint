import { useState } from "react";
import { Icon } from "@iconify/react";
import ProjectDescModal from "../../ProjectDescModal";
import ThemeSelectorModal from "../../ThemeSelectorModal";

export default function HeaderActions() {
  const [showProjectDesc, setShowProjectDesc] = useState(false);
  const [showThemeSelector, setShowThemeSelector] = useState(false);

  return (
    <>
      <div className="flex items-center gap-2">
        <button
          onClick={() => setShowProjectDesc(true)}
          className="btn btn-ghost btn-square text-base-content/50 hover:text-base-content"
        >
          <Icon icon="tabler:info-circle" className="size-5" />
        </button>
        <a
          href="https://github.com/melvinchia3636/thermprint"
          className="btn btn-ghost btn-square text-base-content/50 hover:text-base-content"
          rel="noreferrer noopener"
          target="_blank"
        >
          <Icon icon="mdi:github" className="size-5" />
        </a>
      </div>
      <ProjectDescModal
        open={showProjectDesc}
        onClose={() => setShowProjectDesc(false)}
        onChangeTheme={() => setShowThemeSelector(true)}
      />
      <ThemeSelectorModal
        open={showThemeSelector}
        onClose={() => setShowThemeSelector(false)}
      />
    </>
  );
}
