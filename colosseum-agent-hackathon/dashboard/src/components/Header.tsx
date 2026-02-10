"use client";

import { Shield } from "lucide-react";

export function Header() {
  return (
    <header className="border-b border-white/10 bg-gray-950/80 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="relative">
              <Shield className="w-8 h-8 text-shield-500" />
              <div className="absolute inset-0 animate-shield-glow rounded-full" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">
                Sol<span className="text-shield-400">Shield</span>
              </h1>
              <p className="text-xs text-gray-500">Liquidation Prevention Agent</p>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-6">
            <a href="#" className="text-sm text-shield-400 font-medium">
              Dashboard
            </a>
            <a href="#" className="text-sm text-gray-400 hover:text-white transition">
              Positions
            </a>
            <a href="#" className="text-sm text-gray-400 hover:text-white transition">
              Activity
            </a>
            <a href="#" className="text-sm text-gray-400 hover:text-white transition">
              Settings
            </a>
          </nav>

          <div className="flex items-center gap-2">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-shield-500/10 border border-shield-500/20">
              <div className="w-2 h-2 rounded-full bg-shield-500 animate-pulse" />
              <span className="text-xs text-shield-400 font-medium">Devnet</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
