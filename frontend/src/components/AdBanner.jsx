import React from 'react';
import { GlassCard, MysticButton } from './UI';
import { ExternalLink, Play, X } from 'lucide-react';

const AdBanner = ({ variant = 'native', className = '', onClose }) => {
    // Placeholder content for demo
    const adContent = {
        title: 'Магические Свечи',
        desc: 'Очистите ауру вашего дома с нашими руническими свечами.',
        cta: 'Купить',
        image: 'https://images.unsplash.com/photo-1602523961358-f9f03dd557db?auto=format&fit=crop&q=80&w=200&h=200'
    };

    if (variant === 'sticky-bottom') {
        return (
            <div className={`fixed bottom-[72px] left-0 right-0 z-40 px-4 ${className}`}>
                <div className="max-w-md mx-auto relative group">
                    <div className="absolute -top-2 -right-2 z-10" onClick={onClose}>
                        <div className="bg-black/80 rounded-full p-1 cursor-pointer border border-white/20">
                            <X size={12} className="text-white/70" />
                        </div>
                    </div>
                    <GlassCard className="flex items-center gap-3 p-3 !bg-black/90 !border-purple-500/50 shadow-[0_-4px_20px_rgba(168,85,247,0.2)]">
                        <img src={adContent.image} alt="Ad" className="w-12 h-12 rounded object-cover" />
                        <div className="flex-1">
                            <h4 className="text-xs font-bold text-white mb-0.5 flex items-center gap-1">
                                <span className="bg-yellow-500/20 text-yellow-300 text-[8px] px-1 rounded">РЕКЛАМА</span>
                                {adContent.title}
                            </h4>
                            <p className="text-[10px] text-gray-400 leading-tight line-clamp-1">{adContent.desc}</p>
                        </div>
                        <MysticButton className="text-xs px-3 py-1.5 h-auto whitespace-nowrap bg-purple-600 hover:bg-purple-500">
                            {adContent.cta}
                        </MysticButton>
                    </GlassCard>
                </div>
            </div>
        );
    }

    if (variant === 'rewarded') {
        return (
            <GlassCard className={`relative overflow-hidden group cursor-pointer border-yellow-500/30 ${className}`}>
                <div className="absolute inset-0 bg-gradient-to-r from-yellow-500/10 to-transparent opacity-50" />
                <div className="relative z-10 flex items-center justify-between">
                    <div>
                        <h3 className="font-bold text-sm text-yellow-300 mb-1 flex items-center gap-2">
                            <Play size={14} fill="currentColor" /> Восстановить энергию
                        </h3>
                        <p className="text-xs text-gray-400">Посмотрите короткое видео, чтобы получить +1 ⚡️</p>
                    </div>
                    <div className="bg-yellow-500/20 p-2 rounded-full border border-yellow-500/50">
                        <span className="text-lg">⚡️</span>
                    </div>
                </div>
            </GlassCard>
        );
    }

    // Default 'native'
    return (
        <GlassCard className={`relative overflow-hidden !border-dashed !border-gray-700/50 ${className}`}>
            <span className="absolute top-2 right-2 text-[8px] text-gray-600 uppercase tracking-widest border border-gray-700 rounded px-1">Реклама</span>
            <div className="flex gap-4">
                <div className="w-20 h-20 shrink-0 rounded-lg overflow-hidden bg-gray-800">
                    <img src={adContent.image} alt="Ad" className="w-full h-full object-cover opacity-80" />
                </div>
                <div className="flex flex-col justify-center">
                    <h4 className="font-bold text-sm text-gray-200 mb-1">{adContent.title}</h4>
                    <p className="text-xs text-gray-400 mb-3 line-clamp-2">{adContent.desc}</p>
                    <div className="flex items-center gap-2 text-purple-400 text-xs font-medium group cursor-pointer hover:text-purple-300 transition-colors">
                        Открыть <ExternalLink size={12} />
                    </div>
                </div>
            </div>
        </GlassCard>
    );
};

export default AdBanner;
