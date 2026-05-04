import { useState } from "react";
import { Icon } from "@iconify/react";
import { useDeviceContext } from "../../../context/DeviceContext";
import DeviceSelector from "../../DeviceSelector";

export default function BluetoothButton() {
  const { deviceName } = useDeviceContext();
  const [showDialog, setShowDialog] = useState(false);

  return (
    <>
      <button
        onClick={() => setShowDialog(true)}
        className="btn btn-ghost btn-sm gap-1"
      >
        <Icon icon="tabler:bluetooth" className="size-5 text-primary" />
        <span className="text-sm truncate max-w-32 hidden sm:inline">
          {deviceName}
        </span>
      </button>
      <DeviceSelector
        open={showDialog}
        onClose={() => setShowDialog(false)}
      />
    </>
  );
}
