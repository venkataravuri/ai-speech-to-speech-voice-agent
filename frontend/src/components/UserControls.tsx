import React, { useState, useRef, useEffect } from 'react';
import { Mic } from 'lucide-react';
import WaveForm from './WaveForm';

interface UserControlsProps {
  onStartRecording: () => void;
  onStopRecording: () => void;
  isRecording: boolean;
  userText: string;
  analyserNode: AnalyserNode | null;
}

const UserControls: React.FC<UserControlsProps> = ({
  onStartRecording,
  onStopRecording,
  isRecording,
  userText,
  analyserNode,
}) => {
  return (
    <div className="w-full h-full flex flex-col items-center p-6">
      <button
        onClick={isRecording ? onStopRecording : onStartRecording}
        className={`p-4 rounded-full transition-colors ${
          isRecording ? 'bg-red-500' : 'bg-gray-200 hover:bg-gray-300'
        }`}
      >
        <Mic size={24} className="text-gray-700" />
      </button>

      <div className="w-full h-32 my-4">
        {isRecording && analyserNode && <WaveForm analyserNode={analyserNode} />}
      </div>

      <div className="w-full mt-4 p-4 bg-gray-100 rounded-lg min-h-[200px]">
        <p className="text-gray-800">{userText}</p>
      </div>
    </div>
  );
};

export default UserControls;