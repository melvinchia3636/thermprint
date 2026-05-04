import { useEffect, useRef, useState } from "react";
import { Icon } from "@iconify/react";
import { useDeviceContext } from "../context/DeviceContext";

export default function DeviceSelector({ open, onClose }: {
  open: boolean;
  onClose: () => void;
}) {
  const { devices, refreshDevices, deviceName, setDeviceName } = useDeviceContext();
  const [scanning, setScanning] = useState(false);
  const ref = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    if (open) ref.current.showModal();
    else ref.current.close();
  }, [open]);

  const selectedName = deviceName;

  const handleScan = async () => {
    setScanning(true);
    await refreshDevices();
    setScanning(false);
  };

  const handleSelect = (name: string) => {
    if (name) setDeviceName(name);
    onClose();
  };

  return (
    <dialog ref={ref} className="modal" onClose={onClose}>
      <div className="modal-box">
        <header className="flex items-center justify-between gap-8">
          <h3 className="font-bold text-xl flex items-center gap-2">
            <Icon icon="tabler:bluetooth" className="size-6 shrink-0" />
            Select Bluetooth Device
          </h3>
          <button onClick={onClose} className="btn btn-ghost">
            <Icon icon="tabler:x" className="size-4 shrink-0" />
          </button>
        </header>

        <div className="py-6">
          {!devices || devices.length === 0 ? (
            <p className="text-base text-base-content/40 text-center py-6">
              No devices found. Click scan to search.
            </p>
          ) : (
            <ul className="flex flex-col gap-2">
              {devices.map((d) => (
                <li key={d.address}>
                  <button
                    onClick={() => d.name && handleSelect(d.name)}
                    className={`btn btn-ghost w-full justify-start gap-3 ${d.name === selectedName ? "bg-primary/10" : ""}`}
                  >
                    <Icon
                      icon={
                        d.name === selectedName
                          ? "tabler:bluetooth-connected"
                          : "tabler:bluetooth"
                      }
                      className="size-5 text-primary"
                    />
                    <span className="truncate text-base">{d.name}</span>
                    {d.name === selectedName && (
                      <span className="badge badge-primary ml-auto">
                        <Icon icon="tabler:check" />
                      </span>
                    )}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="modal-action">
          <button
            onClick={handleScan}
            disabled={scanning}
            className="btn btn-outline w-full"
          >
            {scanning ? (
              <span className="loading size-4 loading-spinner" />
            ) : (
              <Icon icon="tabler:search" className="size-4" />
            )}
            {scanning ? "Scanning..." : "Scan"}
          </button>
        </div>
      </div>
      <form method="dialog" className="modal-backdrop"></form>
    </dialog>
  );
}
