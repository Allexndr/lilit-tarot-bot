import React, { useEffect, useRef } from 'react';
import { useTheme } from '../context/ThemeContext';

const BackgroundEffect = () => {
    const canvasRef = useRef(null);
    const { theme } = useTheme();

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        let animationFrameId;

        let width = window.innerWidth;
        let height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;

        const stars = [];
        const starCount = width < 768 ? 80 : 200;

        // Initialize stars with drifting vectors and twinkle offsets
        for (let i = 0; i < starCount; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * (theme === 'light' ? 2 : 1.5) + 0.2,
                vx: Math.random() * 0.4 - 0.2,
                vy: Math.random() * 0.4 - 0.2,
                twinkle: Math.random() * Math.PI * 2,
                twinkleSpeed: Math.random() * 0.03 + 0.01,
                // Light mode: Violet/Indigo. Dark mode: White/Gold.
                color: theme === 'light'
                    ? (Math.random() > 0.5 ? '124, 58, 237' : '30, 27, 75')
                    : (Math.random() > 0.8 ? '253, 230, 138' : '255, 255, 255')
            });
        }

        const animate = () => {
            // Subtle clear for trail effect if needed, but here we do full clear
            ctx.clearRect(0, 0, width, height);

            stars.forEach(star => {
                // Update position
                star.x += star.vx;
                star.y += star.vy;

                // Wrap around edges
                if (star.x < 0) star.x = width;
                if (star.x > width) star.x = 0;
                if (star.y < 0) star.y = height;
                if (star.y > height) star.y = 0;

                // Twinkle logic using Sine
                star.twinkle += star.twinkleSpeed;
                const opacity = Math.sin(star.twinkle) * 0.4 + 0.6;

                // Draw star
                ctx.fillStyle = `rgba(${star.color}, ${opacity})`;
                ctx.beginPath();
                ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
                ctx.fill();

                // Add subtle glow in dark mode
                if (theme === 'dark' && star.radius > 1) {
                    ctx.shadowBlur = 5;
                    ctx.shadowColor = `rgba(${star.color}, 0.3)`;
                } else {
                    ctx.shadowBlur = 0;
                }
            });

            animationFrameId = requestAnimationFrame(animate);
        };

        const handleResize = () => {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
        };

        window.addEventListener('resize', handleResize);
        animate();

        return () => {
            window.removeEventListener('resize', handleResize);
            cancelAnimationFrame(animationFrameId);
        };
    }, [theme]);

    return (
        <canvas
            ref={canvasRef}
            className="fixed inset-0 pointer-events-none z-[-1]"
            style={{ filter: theme === 'light' ? 'blur(0.5px)' : 'none' }}
        />
    );
};

export default BackgroundEffect;
