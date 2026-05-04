<center><h1 align="center">🧾 ThermPrint</h1></center>

<p align="center">A lightweight, open-source web app for printing images and QR codes to BLE thermal printers. No ads, no bloat, no nonsense.</p>

>[!NOTE]  
> **On Supervised Vibe Coding**  
> This project is built using supervised vibe coding: where intuition drives exploration, and discipline shapes what stays.

## 🤔 The Problem

I bought a random portable thermal image printer from Shopee, planning to print some pictures for my journal. When it arrived, I installed the official app - despite having a beautiful UI, it's extremely bloated with features I don't need. Being a geek, I had to dig deeper. So I downloaded the APK, decompiled it, and with the help of ChatGPT, Claude Opus and Deepseek, I reverse-engineered the BLE data transmission protocol and built my own replacement.

## ✅ The Solution

The result is a lightweight, clean, and minimalistic web app that lets you print images and QR codes directly to your BLE thermal printer from your browser. No ads, no bloat, no nonsense. Open-sourced - tweak it however you want.

## ✨ Features

- **Image Printing** - Upload any image, adjust contrast/gamma/rotation, preview the result, and send it to your printer
- **QR Code Printing** - Generate QR codes from URLs with customizable size, style (square, circle, rounded, gapped, vertical/horizontal bars), and optional embedded logo
- **Real-Time Queue** - Live job status updates via WebSocket with progress bars for active prints
- **Persistent History** - Print jobs survive server restarts thanks to SQLite storage, with paginated browsing and preview thumbnails
- **BLE Device Management** - Scan for nearby printers, select and persist your device name
- **Theme Switcher** - Choose from 35+ built-in daisyUI themes, persisted to localStorage
- **Clean, Minimal UI** - Built with React + Tailwind + DaisyUI, fully responsive for mobile and desktop

## 🖥 Screenshots

<div>
  <img width="49%" alt="image" src="https://github.com/user-attachments/assets/447cd641-7b37-43ac-8164-629715b9a731" />
  <img width="49%" alt="image" src="https://github.com/user-attachments/assets/e99cd99f-a7ae-442b-a420-0dfbd499906a" />
  <img width="49%" alt="image" src="https://github.com/user-attachments/assets/a4df5b8b-5c17-4797-94d5-8be519c08a28" />
  <img width="49%" alt="image" src="https://github.com/user-attachments/assets/fa9c3160-438f-4c1a-a916-2d3d12258094" />
  <img width="49%" alt="image" src="https://github.com/user-attachments/assets/fbc41f2e-6276-44a4-b762-49f6b00b106e" />
  <img width="49%" alt="image" src="https://github.com/user-attachments/assets/f59473a4-2aa3-41e9-81ac-f74a11eb87ee" />
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
- The thermal printer that supports this specific protocol

### Backend

```bash
cd server
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn server.app.main:app --reload --port 8000
```

### Frontend

```bash
cd client
bun install
bun run dev
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

The interactive Swagger UI is available at `http://localhost:8000/docs` when the backend server is running, providing a convenient way to explore and test every endpoint directly from your browser.

## 📈 Status

All the core functions for this project have been completed. If you happen to find any bugs, feel free to file an issue in this GitHub Repo.

## 🙏 Credits

This project wouldn't exist without the help of several AI tools and resources:

- **[ChatGPT](https://chatgpt.com)** - Assisted with initial APK decompilation analysis and BLE protocol discovery
- **[Claude Opus](https://antigravity.ai)** via Antigravity - Codebase deep-dive, algorithm and protocol porting from the decompiled APK
- **[Deepseek](https://opencode.ai)** via OpenCode - Assisted with construction of the backend server and frontend interface
- **[This Article](https://github.com/erkanybekov/BlutoothLan)** - A project similar to mine, but an iOS app built on top of Swift. For giving me motivation and the prove of feasibility

## 🛒 Buy the Printer

This project was built for the [portable thermal printer available on Shopee](https://shopee.com.my/product/12011726/19010120735). If you want to try it yourself, grab one and follow the setup instructions above.

## 📄 License

This project is licensed under the MIT License.
