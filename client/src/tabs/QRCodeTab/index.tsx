import { Icon } from "@iconify/react";
import { useState } from "react";
import { usePrintQRCode } from "../../api/print";
import SliderField from "../../components/SliderField";

export default function QRCodeTab() {
  const [url, setUrl] = useState("");
  const [size, setSize] = useState(384);
  const printQR = usePrintQRCode();

  const handlePrint = () => {
    if (!url) return;
    printQR.mutate({ url, size });
  };

  return (
    <section className="card bg-base-200 shadow-sm min-h-0 flex-1">
      <div className="card-body flex flex-col min-h-0">
        <header className="flex items-center justify-between mb-2">
          <h2 className="card-title text-base sm:text-xl">
            <Icon icon="tabler:qrcode" className="size-5 sm:size-6" /> QR Code
          </h2>
        </header>
        <div className="form-control w-full space-y-1">
          <label className="label" htmlFor="qr-url">
            <span className="label-text">URL</span>
          </label>
          <input
            id="qr-url"
            type="url"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="input input-bordered w-full"
          />
        </div>
        <SliderField
          label="Size"
          value={size}
          min={50}
          max={384}
          onChange={setSize}
        />
        <footer className="mt-auto">
          <button
            className="btn btn-neutral w-full"
            onClick={handlePrint}
            disabled={!url || printQR.isPending}
          >
            {printQR.isPending ? (
              <span className="loading size-4 loading-spinner" />
            ) : (
              <Icon icon="tabler:printer" className="size-4" />
            )}
            Print QR Code
          </button>
        </footer>
      </div>
    </section>
  );
}
