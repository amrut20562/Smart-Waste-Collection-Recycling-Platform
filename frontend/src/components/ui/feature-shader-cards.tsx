"use client"

import type React from "react"
import { Warp } from "@paper-design/shaders-react"

interface Feature {
  title: string
  description: string
  icon: React.ReactNode
}

const features: Feature[] = [
  {
    title: "AI Waste Identification",
    description: "YOLO11n object detection with CLIP zero-shot fallback classifies any waste item from a photo.",
    icon: (
      <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" /></svg>
    ),
  },
  {
    title: "Geographic Clustering",
    description: "DBSCAN groups nearby pickup requests into clusters for efficient multi-stop routes.",
    icon: (
      <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M17 1H7c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-2-2-2zM7 4V3h10v1H7zM7 18V6h10v12H7z" /></svg>
    ),
  },
  {
    title: "Route Optimization",
    description: "OR-Tools solves capacity-constrained CVRP to minimize vehicle distance and fuel use.",
    icon: (
      <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M7 2v11h3v9l7-12h-4l4-8z" /></svg>
    ),
  },
  {
    title: "Priority Scoring",
    description: "Waste type, urgency, and proximity produce a priority score that orders every pickup.",
    icon: (
      <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" /></svg>
    ),
  },
  {
    title: "Deterministic Disposal",
    description: "Every category maps to verified disposal rules — no LLM policy guesses, just clean instructions.",
    icon: (
      <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z" /></svg>
    ),
  },
  {
    title: "Operations Command Center",
    description: "Real-time admin dashboard with cluster view, route optimization, and priority queue.",
    icon: (
      <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" /></svg>
    ),
  },
]

export default function FeaturesCards() {
  const getShaderConfig = (index: number) => {
    const configs = [
      { proportion: 0.3, softness: 0.8, distortion: 0.15, swirl: 0.6, swirlIterations: 8, shape: "checks" as const, shapeScale: 0.08, colors: ["hsl(280,100%,30%)","hsl(320,100%,60%)","hsl(340,90%,40%)","hsl(300,100%,70%)"] },
      { proportion: 0.4, softness: 1.2, distortion: 0.2, swirl: 0.9, swirlIterations: 12, shape: "stripes" as const, shapeScale: 0.12, colors: ["hsl(200,100%,25%)","hsl(180,100%,65%)","hsl(160,90%,35%)","hsl(190,100%,75%)"] },
      { proportion: 0.35, softness: 0.9, distortion: 0.18, swirl: 0.7, swirlIterations: 10, shape: "checks" as const, shapeScale: 0.1, colors: ["hsl(120,100%,25%)","hsl(140,100%,60%)","hsl(100,90%,30%)","hsl(130,100%,70%)"] },
      { proportion: 0.45, softness: 1.1, distortion: 0.22, swirl: 0.8, swirlIterations: 15, shape: "stripes" as const, shapeScale: 0.09, colors: ["hsl(30,100%,35%)","hsl(50,100%,65%)","hsl(40,90%,40%)","hsl(45,100%,75%)"] },
      { proportion: 0.38, softness: 0.95, distortion: 0.16, swirl: 0.85, swirlIterations: 11, shape: "checks" as const, shapeScale: 0.11, colors: ["hsl(250,100%,30%)","hsl(270,100%,65%)","hsl(260,90%,35%)","hsl(265,100%,70%)"] },
      { proportion: 0.42, softness: 1.0, distortion: 0.19, swirl: 0.75, swirlIterations: 9, shape: "stripes" as const, shapeScale: 0.13, colors: ["hsl(330,100%,30%)","hsl(350,100%,60%)","hsl(340,90%,35%)","hsl(345,100%,75%)"] },
    ]
    return configs[index % configs.length]
  }

  return (
    <section className="min-h-screen py-24 px-4 bg-transparent">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-6xl font-light text-white mb-6 tracking-[-0.03em]">Smart Waste <span className="text-eco-400">AI</span></h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">Computer vision, clustering, and route optimization for cleaner cities.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const shaderConfig = getShaderConfig(index)
            return (
              <div key={index} className="relative h-[420px] rounded-3xl overflow-hidden shadow-2xl shadow-black/40 group">
                <div className="absolute inset-0">
                  <Warp
                    style={{ height: "100%", width: "100%" }}
                    proportion={shaderConfig.proportion}
                    softness={shaderConfig.softness}
                    distortion={shaderConfig.distortion}
                    swirl={shaderConfig.swirl}
                    swirlIterations={shaderConfig.swirlIterations}
                    shape={shaderConfig.shape}
                    shapeScale={shaderConfig.shapeScale}
                    scale={1}
                    rotation={0}
                    speed={0.8}
                    colors={shaderConfig.colors}
                  />
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent z-10" />
                <div className="relative z-20 p-8 h-full flex flex-col justify-end">
                  <div className="mb-4">{feature.icon}</div>
                  <h3 className="text-2xl font-bold mb-3 text-white tracking-tight">{feature.title}</h3>
                  <p className="leading-relaxed text-gray-200">{feature.description}</p>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
