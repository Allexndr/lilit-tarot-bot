import React, { useState } from 'react';
import { motion } from 'framer-motion';

const TarotCard = ({ card, isReversed, index, isRevealed, onReveal }) => {
    // If external control (isRevealed) is not provided, use local state (click to flip)
    const [localFlipped, setLocalFlipped] = useState(false);

    const isFlipped = isRevealed !== undefined ? isRevealed : localFlipped;

    const handleClick = () => {
        if (onReveal) {
            onReveal();
        } else {
            setLocalFlipped(!localFlipped);
        }
    };

    return (
        <div
            className="perspective-1000 w-32 h-52 cursor-pointer group"
            onClick={handleClick}
        >
            <motion.div
                className="relative w-full h-full transition-all duration-700 preserve-3d"
                animate={{ rotateY: isFlipped ? 180 : 0 }}
                transition={{ type: 'spring', stiffness: 120, damping: 14, delay: index * 0.15 }} // Staggered delay
            >
                {/* Back of Card - Mystical Design */}
                <div className="absolute inset-0 backface-hidden rounded-xl overflow-hidden shadow-lg group-hover:shadow-purple-500/40 transition-shadow duration-300">
                    <div className="w-full h-full bg-[#1a1a2e] border-2 border-purple-500/40 p-1.5 flex items-center justify-center">
                        <div className="w-full h-full border border-purple-500/20 rounded-lg bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] bg-purple-900/10 flex flex-col items-center justify-center gap-2">
                            <div className="w-20 h-20 rounded-full border border-purple-400/30 flex items-center justify-center relative">
                                <div className="absolute inset-0 border border-purple-500/20 rounded-full animate-ping-slow"></div>
                                <span className="text-3xl text-purple-300 opacity-60 filter drop-shadow-[0_0_5px_rgba(168,85,247,0.5)]">👁</span>
                            </div>
                            <div className="text-[9px] tracking-[0.2em] text-purple-500/50 uppercase font-medium mt-2">Lilit Tarot</div>
                        </div>
                    </div>
                </div>

                {/* Front of Card */}
                <div
                    className={`absolute inset-0 backface-hidden rounded-xl overflow-hidden rotate-y-180 shadow-2xl shadow-purple-500/10 ${isReversed ? 'rotate-180' : ''}`}
                >
                    <div className="absolute inset-0 bg-gradient-to-br from-black to-purple-950/80 -z-10" />

                    {/* Glowing border effect */}
                    <div className="absolute inset-0 border-2 border-purple-400/50 rounded-xl box-border shadow-[inset_0_0_20px_rgba(168,85,247,0.2)]"></div>

                    <img
                        src={card.image || 'https://via.placeholder.com/128x208?text=Tarot'}
                        alt={card.name}
                        className="w-full h-full object-cover p-1.5 rounded-xl opacity-90 hover:opacity-100 transition-opacity"
                    />

                    {/* Card Label Overlay */}
                    <div className="absolute bottom-3 left-2 right-2 flex justify-center">
                        <div className="bg-black/70 backdrop-blur-md px-3 py-1 rounded-full border border-purple-500/30 shadow-lg">
                            <p className="text-[9px] text-yellow-100 font-bold uppercase tracking-wider whitespace-nowrap">
                                {card.name} {isReversed && '(Пер)'}
                            </p>
                        </div>
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default TarotCard;
