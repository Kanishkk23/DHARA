import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FloodFlash | Flood Intelligence Platform",
  description:
    "FloodFlash is an intelligent flood-risk monitoring and early-warning platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}