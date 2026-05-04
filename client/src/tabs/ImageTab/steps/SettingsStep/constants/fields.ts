import type { PrintSettings } from "../../../../../types";

export interface FieldDef {
  key: keyof PrintSettings;
  label: string;
  description?: string;
  type?: "slider" | "select";
  min?: number;
  max?: number;
  step?: number;
  options?: { value: number; label: string }[];
}

export const IMAGE_FIELDS: FieldDef[] = [
  {
    key: "width",
    label: "Width (px)",
    description:
      "Output image width in pixels. The image is resized to this width using Lanczos resampling, maintaining aspect ratio. Typical thermal printer widths are 384 (default), 512, or 576 pixels.",
    min: 64,
    max: 1000,
  },
  {
    key: "contrast",
    label: "Contrast",
    description:
      "Contrast multiplier applied via (pixel - 128) * contrast + 128. Values > 1.0 increase contrast. Values < 1.0 reduce contrast, flattening the image.",
    min: 0,
    max: 5,
    step: 0.1,
  },
  {
    key: "gamma",
    label: "Gamma",
    description:
      "Gamma correction: output = 255 * (input/255)^(1/gamma). Higher values produce a brighter image by expanding midtones. Lower values darken the image.",
    min: 0.1,
    max: 5,
    step: 0.1,
  },
  {
    key: "rotate",
    label: "Rotate",
    description:
      "Rotates the image clockwise before resizing. The canvas expands to fit the rotated image.",
    type: "select",
    options: [
      { value: 0, label: "0\u00b0" },
      { value: 90, label: "90\u00b0" },
      { value: 180, label: "180\u00b0" },
      { value: 270, label: "270\u00b0" },
    ],
  },
];

export const PRINTER_FIELDS: FieldDef[] = [
  {
    key: "quality",
    label: "Quality",
    description:
      "Printer heat quality setting (0x31–0x35). Higher values produce darker, more saturated prints at the cost of slower printing and more battery usage. 0x32 is a balanced default.",
    min: 0x31,
    max: 0x35,
  },
  {
    key: "speed",
    label: "Speed",
    description:
      "Paper feed speed. Lower values = faster feed but may reduce print quality. Higher values slow the feed, allowing more heat dwell time for darker output. Range 0x01–0xFF.",
    min: 1,
    max: 255,
  },
  {
    key: "energy",
    label: "Energy",
    description:
      "Thermal energy applied to the print head (0x0000–0xFFFF). Higher values produce darker prints. 0 = auto, letting the printer decide the optimal energy level.",
    min: 0,
    max: 65535,
  },
  {
    key: "chunk_rows",
    label: "Chunk Rows",
    description:
      "Number of pixel rows to send per BLE data chunk. Larger chunks reduce BLE overhead but may cause timeouts on slow connections. Each chunk is compressed with LZO before sending.",
    min: 1,
    max: 100,
  },
  {
    key: "chunk_delay",
    label: "Chunk Delay",
    description:
      "Delay in seconds between sending each data chunk to the printer. A longer delay gives the printer more time to process and print each chunk, reducing the risk of buffer overflow. 0.2s is a safe default.",
    min: 0,
    max: 10,
    step: 0.1,
  },
  {
    key: "feed",
    label: "Feed",
    description:
      "Number of additional pixel rows to feed (advance) the paper after the print completes. Cuts or tears often leave a margin; this feeds the paper so the image is fully visible before tear-off.",
    min: 0,
    max: 5000,
  },
];
