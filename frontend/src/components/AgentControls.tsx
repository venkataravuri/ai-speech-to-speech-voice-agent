import React from 'react';
import { Speaker } from 'lucide-react';

interface AgentControlsProps {
  isPlaying: boolean;
  agentText: string;
}

const AgentControls: React.FC<AgentControlsProps> = ({ isPlaying, agentText }) => {
  return (
    <div className="w-full h-full flex flex-col items-center p-6">
      <div
        className={`p-4 rounded-full bg-gray-200 ${isPlaying ? 'animate-pulse' : ''}`}
      >
        <Speaker size={24} className="text-gray-700" />
      </div>

      <div className="w-full mt-4 p-4 bg-gray-100 rounded-lg min-h-[200px]">
        <p className="text-gray-800">{agentText}</p>
      </div>
    </div>
  );
};

export default AgentControls;