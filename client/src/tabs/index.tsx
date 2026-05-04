import { useState } from "react";
import { Icon } from "@iconify/react";
import ImageTab from "./ImageTab";
import QRCodeTab from "./QRCodeTab";

const TABS: {
  id: string;
  label: string;
  icon: string;
  component: React.ReactNode;
}[] = [
  {
    id: "image",
    label: "Image",
    icon: "tabler:photo",
    component: <ImageTab />,
  },
  {
    id: "qrcode",
    label: "QR Code",
    icon: "tabler:qrcode",
    component: <QRCodeTab />,
  },
];

export default function TabbedContent() {
  const [active, setActive] = useState(TABS[0].id);

  return (
    <section className="flex flex-col w-full min-h-0">
      <nav role="tablist" aria-label="Content tabs" className="tabs tabs-border">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            className={`tab flex-1 before:w-full! text-base before:left-0! pb-2 gap-1.5 ${active === tab.id ? "tab-active" : ""}`}
            onClick={() => setActive(tab.id)}
          >
            <Icon icon={tab.icon} className="size-5" />
            {tab.label}
          </button>
        ))}
      </nav>
      {TABS.map((tab) => (
        <div
          key={tab.id}
          className={`flex-1 min-h-0 mt-6 flex flex-col ${active === tab.id ? "flex" : "hidden"}`}
        >
          {tab.component}
        </div>
      ))}
    </section>
  );
}
