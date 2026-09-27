"use client";
import ShaderAuroraVeil from "./shader-aurora-veil";
export default function ShaderAuroraVeilDemo() {
  return (
    <div className="relative min-h-screen w-full bg-[#0a0a0f]">
      <ShaderAuroraVeil preset="aurora-veil" tone="dark" className="absolute inset-0 h-full w-full" />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <h1 className="text-6xl font-bold text-white tracking-tighter drop-shadow-2xl">Aurora Veil</h1>
      </div>
    </div>
  );
}
