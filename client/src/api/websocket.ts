import { useEffect, useRef, type MutableRefObject } from "react";

export function useWebSocket<T>(
  path: string,
  onMessage: (data: T) => void,
  wsRef: MutableRefObject<WebSocket | null>,
) {
  const cbRef = useRef(onMessage);
  cbRef.current = onMessage;

  useEffect(() => {
    function connect() {
      const protocol = location.protocol === "https:" ? "wss:" : "ws:";
      const ws = new WebSocket(`${protocol}//${location.host}${path}`);
      wsRef.current = ws;

      ws.onmessage = (event) => {
        cbRef.current(JSON.parse(event.data));
      };

      ws.onclose = () => {
        wsRef.current = null;
        setTimeout(connect, 3000);
      };

      ws.onerror = () => ws.close();
    }

    connect();

    return () => {
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [path, wsRef]);
}
