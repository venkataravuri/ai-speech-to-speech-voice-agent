import React, { useState, useEffect, useRef } from 'react';
import UserControls from './components/UserControls';
import AgentControls from './components/AgentControls';
import WebSocketService from './services/websocket.service';

const App: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [userText, setUserText] = useState('');
  const [agentText, setAgentText] = useState('');
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserNodeRef = useRef<AnalyserNode | null>(null);
  const webSocketService = useRef<WebSocketService | null>(null);

  useEffect(() => {
    webSocketService.current = new WebSocketService(process.env.REACT_APP_WS_URL!);
    webSocketService.current.connect();

    webSocketService.current.onMessage('text', (response) => {
      if (response.source === 'user') {
        setUserText(response.content);
      } else {
        setAgentText(response.content);
      }
    });

    webSocketService.current.onMessage('audio', (response) => {
      playAudioResponse(response.content);
    });

    return () => {
      webSocketService.current?.disconnect();
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioContextRef.current = new AudioContext();
      analyserNodeRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserNodeRef.current);
      setIsRecording(true);

      const intervalId = setInterval(() => {
        const audioData = getAudioData();
        webSocketService.current?.sendAudio(audioData);
      }, 100);

      return () => {
        clearInterval(intervalId);
        stopRecording();
      };
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (audioContextRef.current) {
      audioContextRef.current.close();
      setIsRecording(false);
    }
  };

  const getAudioData = (): string => {
    if (analyserNodeRef.current) {
      const bufferLength = analyserNodeRef.current.fftSize;
      const dataArray = new Uint8Array(bufferLength);
      analyserNodeRef.current.getByteTimeDomainData(dataArray);
      return arrayBufferToBase64(dataArray.buffer);
    }
    return '';
  };

  const playAudioResponse = async (audioData: string) => {
    try {
      setIsPlaying(true);
      const audioContext = new AudioContext();
      const audioBuffer = await audioContext.decodeAudioData(
        base64ToArrayBuffer(audioData)
      );
      const source = audioContext.createBufferSource();
      source.buffer = audioBuffer;
      source.connect(audioContext.destination);
      source.onended = () => setIsPlaying(false);
      source.start(0);
    } catch (error) {
      console.error('Error playing audio:', error);
      setIsPlaying(false);
    }
  };

  return (
    <div className="flex h-screen">
      <UserControls
        onStartRecording={startRecording}
        onStopRecording={stopRecording}
        isRecording={isRecording}
        userText={userText}
        analyserNode={analyserNodeRef.current}
      />
      <AgentControls isPlaying={isPlaying} agentText={agentText} />
    </div>
  );



  function base64ToArrayBuffer(base64: string) {
    var binaryString = atob(base64);
    var bytes = new Uint8Array(binaryString.length);
    for (var i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
  }

  function arrayBufferToBase64(buffer: ArrayBuffer): string {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
  }


};

export default App;