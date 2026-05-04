<center><h1 align="center">🧾 ThermPrint</h1></center>

<p align="center">A lightweight, open-source web app for printing images and QR codes to BLE thermal printers. No ads, no bloat, no nonsense.</p>

## The Problem

I bought a random portable thermal image printer from Shopee and the official app that comes with it sucks — it's bloated, full of ads, and barely functional. So I downloaded the APK, decompiled it, reverse-engineered the BLE data transmission protocol, and built my own replacement.

## The Solution

ThermPrint is a lightweight web app that lets you print images and QR codes directly to your BLE thermal printer from your browser. Zero ads, zero bloat, fully open-source.

## ✨ Features

- **Image Printing** — Upload any image, adjust contrast/gamma/rotation, preview the result, and send it to your printer
- **QR Code Printing** — Generate QR codes from URLs with customizable size, style (square, circle, rounded, gapped, vertical/horizontal bars), and optional embedded logo
- **Real-Time Queue** — Live job status updates via WebSocket with progress bars for active prints
- **Persistent History** — Print jobs survive server restarts thanks to SQLite storage
- **Paginated History** — Browse past jobs with load-more pagination, preview thumbnails, and job deletion
- **BLE Device Management** — Scan for nearby printers, select and persist your device name
- **Theme Switcher** — Choose from 35+ built-in daisyUI themes, persisted to localStorage
- **Clean, Minimal UI** — Built with React + Tailwind + DaisyUI, fully responsive for mobile and desktop

## 🖥 Screenshots

<div>
  <img width="49%" alt="ThermPrint preview" src="https://placehold.co/800x600/1a1a2e/eaeaea?text=ThermPrint+Screenshot">
  <img width="49%" alt="ThermPrint queue" src="https://placehold.co/800x600/16213e/eaeaea?text=Print+Queue">
</div>

## 🔬 Technologies Used

![skills](https://img.shields.io/badge/-TYPESCRIPT-FF0000?style=for-the-badge&logo=typescript&logoColor=white&color=blue)
![skills](https://img.shields.io/badge/-REACT-FF0000?style=for-the-badge&logo=react&logoColor=white&color=38BDF8)
![skills](https://img.shields.io/badge/-TAILWIND_CSS-FF0000?style=for-the-badge&logo=tailwindcss&logoColor=white&color=22D3EE)
![skills](https://img.shields.io/badge/-DAISYUI-FF0000?style=for-the-badge&logo=daisyui&logoColor=white&color=5A0EF8)
![skills](https://img.shields.io/badge/-PYTHON-FF0000?style=for-the-badge&logo=python&logoColor=white&color=3776AB)
![skills](https://img.shields.io/badge/-FASTAPI-FF0000?style=for-the-badge&logo=fastapi&logoColor=white&color=009688)
![skills](https://img.shields.io/badge/-SQLITE-FF0000?style=for-the-badge&logo=sqlite&logoColor=white&color=003B57)
![skills](https://img.shields.io/badge/-BLEAK-FF0000?style=for-the-badge&logo=bluetooth&logoColor=white&color=0082FC)

**Frontend:** React, TypeScript, Tailwind CSS, DaisyUI, TanStack Query  
**Backend:** Python, FastAPI, Uvicorn, Bleak (BLE), Pillow (image processing), aiosqlite  
**Protocol:** Reverse-engineered BLE GATT communication from the official APK

## ⌨️ Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- A BLE-compatible thermal printer

### Backend

```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn server.app.main:app --reload --port 8000
```

### Frontend

```bash
cd client
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## 🧪 Running Tests

```bash
cd server
source .venv/bin/activate
pytest
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/print` | Print an image |
| `POST` | `/api/preview` | Preview an image |
| `POST` | `/api/qrcode` | Print a QR code |
| `POST` | `/api/qrcode/preview` | Preview a QR code |
| `GET` | `/api/jobs` | List print jobs (paginated) |
| `DELETE` | `/api/jobs/{id}` | Cancel a job |
| `DELETE` | `/api/jobs/{id}/delete` | Delete a job |
| `GET` | `/api/device` | Get configured device name |
| `PUT` | `/api/device` | Update device name |
| `GET` | `/api/devices` | Scan for BLE printers |
| `GET` | `/api/status` | Get connection status |
| `GET` | `/api/settings` | Get print settings |
| `PUT` | `/api/settings` | Update print settings |
| `WS` | `/api/ws/jobs` | Real-time job updates |
| `WS` | `/api/ws/status` | Real-time connection status |

## 📈 Status

This project is actively maintained. If any bugs are found, please file an issue on GitHub, and I'll resolve it ASAP.

## 🛒 Buy the Printer

This project was built for the [portable thermal printer available on Shopee](https://shopee.com.my/product/12011726/19010120735). If you want to try it yourself, grab one and follow the setup instructions above.

## 📄 License

Copyright © 2026 Melvin Chia  
Licensed under MIT.
