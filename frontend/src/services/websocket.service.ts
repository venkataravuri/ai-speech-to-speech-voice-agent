class WebSocketService {
  private url: string;
  private ws: WebSocket | null = null;
  private messageHandlers = new Map<string, (data: any) => void>();

  constructor(url: string) {
    this.url = url;
  }

  connect() {
    console.log(this.url);
    this.ws = new WebSocket(this.url);

    this.ws.onmessage = (event) => {
      const response = JSON.parse(event.data.toString());
      const handler = this.messageHandlers.get(response.type);
      if (handler) {
        handler(response);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket connection closed');
      // Implement reconnection logic if needed
    };
  }

  sendAudio(audioData: string) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(
        JSON.stringify({
          type: 'audio',
          content: audioData,
        })
      );
    }
  }

  onMessage(type: string, handler: (data: any) => void) {
    this.messageHandlers.set(type, handler);
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

export default WebSocketService;
