import React, { useState, useEffect } from 'react';
import { GlassCard } from './UI';
import { Moon, Info } from 'lucide-react';
import axios from 'axios';

const MoonWidget = () => {
    const [moonData, setMoonData] = useState(null);

    useEffect(() => {
        const fetchMoon = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/services/moon');
                setMoonData(response.data);
            } catch (err) {
                console.error('Failed to fetch moon data');
            }
        };
        fetchMoon();
    }, []);

    if (!moonData) return null;

    return (
        <GlassCard className="border-blue-500/20 bg-blue-500/5 mb-6">
            <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center relative">
                    <Moon className="text-blue-400 w-6 h-6 animate-pulse" />
                    <div className="absolute inset-0 rounded-full border border-blue-400/30 animate-ping opacity-20"></div>
                </div>
                <div className="flex-1">
                    <div className="flex justify-between items-center mb-1">
                        <h4 className="text-blue-300 font-bold text-xs uppercase tracking-tighter">Лунный День: {moonData.lunar_day}</h4>
                        <span className="text-[10px] text-gray-400">{moonData.phase}</span>
                    </div>
                    <p className="text-[11px] text-gray-300 leading-tight italic">
                        {moonData.advice}
                    </p>
                </div>
            </div>
        </GlassCard>
    );
};

export default MoonWidget;
