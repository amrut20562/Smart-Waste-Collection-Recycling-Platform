import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Recycle } from 'lucide-react';
import FeaturesCards from '../components/ui/feature-shader-cards';
import { LiquidMetalButton } from '../components/ui/liquid-metal-button';
import ShaderAuroraVeil from '../components/ui/shader-aurora-veil';

export const LandingPage: React.FC = () => {
  return (
    <div className="relative min-h-screen bg-[#0a0a0f] text-[#e8e8ec]">
      {/* Aurora veil background — full page shader */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <ShaderAuroraVeil preset="aurora-veil" tone="dark" className="h-full w-full" />
      </div>

      {/* Dark hero */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 md:px-12 pt-12 pb-6">
        <div className="flex items-center justify-between flex-wrap gap-4 mb-6">
          <div className="flex items-center gap-2 text-eco-400">
            <Recycle className="h-6 w-6" />
            <span className="font-semibold tracking-tight">Smart Waste AI</span>
          </div>
          <div className="flex gap-3">
            <LiquidMetalButton label="Citizen Portal" onClick={() => window.location.href = '/citizen'} />
            <LiquidMetalButton label="Operations Center" onClick={() => window.location.href = '/admin'} />
          </div>
        </div>
        <h1 className="text-5xl md:text-7xl font-bold tracking-[-0.03em] leading-[0.92] text-white mb-4">Smart Waste <span className="text-eco-400">AI</span></h1>
        <p className="text-lg text-gray-400 max-w-xl leading-relaxed">Computer vision, geographic clustering, and capacity-constrained routing for cleaner cities.</p>
      </section>

      {/* Feature shader cards become the hero - no cards above */}
      <div className="relative z-10">
        <FeaturesCards />
      </div>

      {/* Footer */}
      <footer className="relative z-10 max-w-7xl mx-auto px-6 md:px-12 py-8 border-t border-white/10">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <Recycle className="h-5 w-5 text-eco-400" />
            <span>Smart Waste AI</span>
          </div>
          <div className="flex gap-6 text-sm text-gray-400">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
};
