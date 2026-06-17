import React from 'react';
import { motion } from 'framer-motion';

export const GlassCard = ({ children, className = "", onClick, hover = true }) => {
    return (
        <motion.div
            className={`glass-panel p-6 ${className} ${hover ? 'cursor-pointer' : ''}`}
            whileHover={hover ? { scale: 1.02, y: -4 } : {}}
            whileTap={hover ? { scale: 0.98 } : {}}
            onClick={onClick}
            transition={{ duration: 0.2 }}
        >
            {children}
        </motion.div>
    );
};

export const MysticalButton = ({ children, onClick, variant = "primary", className = "", icon: Icon }) => {
    return (
        <motion.button
            className={`mystic-btn ${variant === "secondary" ? "secondary" : variant === "accent" ? "accent" : ""} ${className} flex items-center justify-center gap-2 overflow-hidden relative group`}
            onClick={onClick}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
        >
            <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
            {Icon && <Icon className="w-5 h-5" />}
            <span className="relative z-10">{children}</span>
        </motion.button>
    );
};

export const PageTransition = ({ children }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
        >
            {children}
        </motion.div>
    );
};
