"use client";

import { Power } from "lucide-react";

interface AgentStatusProps {
  running: boolean;
  onToggle: () => void;
}

export function AgentStatus({ running, onToggle }: AgentStatusProps) {
  return (
    <button
      onClick={onToggle}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-all duration-300 ${
        running
          ? "bg-shield-500/10 border-shield-500/30 hover:bg-shield-500/20"
          : "bg-red-500/10 border-red-500/30 hover:bg-red-500/20"
      }`}
    >
      <Power
        className={`w-4 h-4 ${running ? "text-shield-400" : "text-red-400"}`}
      />
      <span
        className={`text-sm font-medium ${
          running ? "text-shield-400" : "text-red-400"
        }`}
      >
        {running ? "Agent Active" : "Agent Paused"}
      </span>
      <div
        className={`w-2 h-2 rounded-full ${
          running ? "bg-shield-500 animate-pulse" : "bg-red-500"
        }`}
      />
    </button>
  );
}
