import { Icon } from "@iconify/react";

export default function ProjectDescModal({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  return (
    <dialog className="modal" open={open} onClose={onClose}>
      <div className="modal-box">
        <h3 className="font-bold text-lg flex items-center gap-2">
          <Icon icon="tabler:info-circle" className="size-5" />
          About ThermPrint
        </h3>
        <div className="py-4 space-y-4 text-sm">
          <p>
            The reason why this project exists? Well, I bought a random portable
            thermal image printer from Shopee, and was planning to use it to
            print some pictures that I could paste in my journal. When it
            finally arrived, I installed the official app, following the
            instruction manual that contains dozens of grammatical and spelling
            errors.
          </p>
          <p>
            Despite having beautiful and clean UI, it's extremely bloated with
            features that I do not need in my use cases. Being a geek myself, of
            course I have to allocate some brain cells into it. So I downloaded
            the APK, decompiled it, and with the help of ChatGPT, Claude Opus
            and Deepseek, I was able to reverse-engineer the BLE data
            transmission protocol, therefore build my own replacement.
          </p>
          <p>
            The result, as you can see here, is a lightweight, clean, and
            minimalistic web app that lets you print images and QR codes
            directly to the printer from your browser.
          </p>
          <p>
            No ads, no bloat, no nonsense. Open-sourced, tweak it however you
            want.
          </p>
          <p>
            By the way, here is the link if you want to{" "}
            <a
              href="https://shopee.com.my/product/12011726/19010120735?gads_t_sig=gqRjZGVrxHCFomtpsTE0MjUxOnRzc19zZGtfa2V5omt20QABpGFsZ2_SAAAAZKNkZWvAomN0xEAAAAAMRoz0ZUjQw0QlRa--FjB0AKnHQPF7xv4DyGj9-GQwqn4zSdB6gztmw7ebmtsZs9FPJxlVqctc57WUE3IRqmNpcGhlcnRleHTEcAAAAAyMGtBJHztyrUMs5ClTtYvPdJx9Evq8VaLSgihEiLWjGUHY_cFOUTDkkN8Dgb0H_-gEaeBD5SUPgQ5llU_E-Bsha5ng6y7hwqpowrr9rWealDjgWSSKC3B5MCukqABr3QJ1m2pAs4iOyzjnU2c"
              rel="noreferrer noopener"
              target="_blank"
              className="link link-primary"
            >
              buy this printer on Shopee
            </a>
          </p>

          <div className="divider mt-0" />
          <div className="space-y-2">
            <h4 className="font-semibold">Tech Stack</h4>
            <ul className="list-disc list-inside text-base-content/70 space-y-1">
              <li>FastAPI (Python) — backend API & WebSocket</li>
              <li>React + TypeScript — frontend</li>
              <li>Bleak — BLE communication</li>
              <li>Pillow — image processing</li>
              <li>SQLite — job history persistence</li>
              <li>DaisyUI + Tailwind — UI styling</li>
            </ul>
          </div>

          <div className="divider mt-0" />

          <p>
            Licensed under MIT. Source code available on{" "}
            <a
              href="https://github.com/melvinchia3636/thermprint"
              rel="noreferrer noopener"
              target="_blank"
              className="link link-secondary"
            >
              GitHub
            </a>
            .
          </p>
          <p>
            Made with 🖤 by{" "}
            <a
              href="https://melvinchia.dev"
              rel="noreferrer noopener"
              target="_blank"
              className="underline text-secondary"
            >
              Melvin Chia
            </a>
            .
          </p>
        </div>
        <div className="modal-action">
          <button className="btn btn-secondary" onClick={onClose}>
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
