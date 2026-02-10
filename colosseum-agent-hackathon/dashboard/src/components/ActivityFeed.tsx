"use client";

import { ActivityEntry, getRiskColor } from "@/types";
import { Activity, ExternalLink } from "lucide-react";

function timeAgo(ts: number): string {
  const seconds = Math.round((Date.now() - ts) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.round(minutes / 60);
  return `${hours}h ago`;
}

export function ActivityFeed({ entries }: { entries: ActivityEntry[] }) {
  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      {entries.map((entry) => (
        <div
          key={entry.id}
          className="flex gap-3 p-3 rounded-lg bg-white/5 hover:bg-white/8 transition"
        >
          <div className="mt-0.5">
            <Activity
              className={`w-4 h-4 ${
                entry.riskLevel
                  ? getRiskColor(entry.riskLevel)
                  : "text-gray-400"
              }`}
            />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium text-white">{entry.action}</p>
              <span className="text-[10px] text-gray-500 whitespace-nowrap ml-2">
                {timeAgo(entry.timestamp)}
              </span>
            </div>
            <p className="text-xs text-gray-400 mt-0.5 leading-relaxed">
              {entry.details}
            </p>
            {entry.txSignature && (
              <a
                href={`https://explorer.solana.com/tx/${entry.txSignature}?cluster=devnet`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-[10px] text-shield-400 hover:text-shield-300 mt-1"
              >
                <ExternalLink className="w-3 h-3" />
                {entry.txSignature}
              </a>
            )}
          </div>
        </div>
      ))}
      {entries.length === 0 && (
        <p className="text-sm text-gray-500 text-center py-4">
          No activity yet
        </p>
      )}
    </div>
  );
}
