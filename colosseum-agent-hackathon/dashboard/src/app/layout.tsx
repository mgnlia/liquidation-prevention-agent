import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { WalletContextProvider } from "@/components/WalletProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SolShield — AI Liquidation Prevention",
  description:
    "Autonomous AI agent monitoring your Solana DeFi positions to prevent liquidations",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-gray-950 text-white min-h-screen`}>
        <WalletContextProvider>{children}</WalletContextProvider>
      </body>
    </html>
  );
}
