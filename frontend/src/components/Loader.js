import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './Loader.css';

const Loader = ({ onLoadComplete, theme }) => {
  const [showLoader, setShowLoader] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowLoader(false);
      setTimeout(() => {
        onLoadComplete();
      }, 800);
    }, 4500);

    return () => clearTimeout(timer);
  }, [onLoadComplete]);

  return (
    <AnimatePresence>
      {showLoader && (
        <motion.div
          className={`loader-container ${theme}`}
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.8 }}
        >
          {/* Animated grid background */}
          <div className="grid-bg">
            <motion.div
              className="grid-lines"
              animate={{
                opacity: [0.05, 0.15, 0.05],
                scale: [1, 1.1, 1]
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />
          </div>

          {/* Animated waves */}
          <div className="waves">
            {[...Array(3)].map((_, i) => (
              <motion.div
                key={i}
                className="wave"
                animate={{
                  x: ['-100%', '100%'],
                  opacity: [0.1, 0.3, 0.1]
                }}
                transition={{
                  duration: 8 + i * 2,
                  repeat: Infinity,
                  ease: "linear",
                  delay: i * 0.5
                }}
                style={{
                  top: `${30 + i * 15}%`,
                  animationDelay: `${i * 0.5}s`
                }}
              />
            ))}
          </div>

          {/* Enhanced particles */}
          <div className="particles">
            {[...Array(40)].map((_, i) => (
              <motion.div
                key={i}
                className="particle"
                initial={{
                  x: Math.random() * window.innerWidth,
                  y: Math.random() * window.innerHeight,
                  scale: 0
                }}
                animate={{
                  x: [
                    Math.random() * window.innerWidth,
                    Math.random() * window.innerWidth,
                    Math.random() * window.innerWidth
                  ],
                  y: [
                    Math.random() * window.innerHeight,
                    Math.random() * window.innerHeight,
                    Math.random() * window.innerHeight
                  ],
                  scale: [0, 1, 0.5, 1, 0],
                  opacity: [0, 1, 0.5, 1, 0]
                }}
                transition={{
                  duration: 4 + Math.random() * 3,
                  repeat: Infinity,
                  delay: Math.random() * 3,
                  ease: "easeInOut"
                }}
              />
            ))}
          </div>

          {/* Orbiting circles */}
          <div className="orbit-container">
            {[...Array(3)].map((_, i) => (
              <motion.div
                key={i}
                className="orbit"
                animate={{
                  rotate: 360
                }}
                transition={{
                  duration: 20 - i * 5,
                  repeat: Infinity,
                  ease: "linear"
                }}
                style={{
                  width: `${300 + i * 150}px`,
                  height: `${300 + i * 150}px`
                }}
              >
                <div className="orbit-dot" />
              </motion.div>
            ))}
          </div>

          {/* Animated lines background */}
          <div className="lines-bg">
            {[...Array(8)].map((_, i) => (
              <motion.div
                key={i}
                className="line"
                initial={{ x: '-100%' }}
                animate={{ x: '200%' }}
                transition={{
                  duration: 4,
                  repeat: Infinity,
                  delay: i * 0.5,
                  ease: "linear"
                }}
                style={{ top: `${10 + i * 12}%` }}
              />
            ))}
          </div>

          {/* Floating geometric shapes */}
          <div className="shapes">
            {[...Array(6)].map((_, i) => (
              <motion.div
                key={i}
                className={`shape shape-${i % 3}`}
                animate={{
                  y: [0, -30, 0],
                  rotate: [0, 180, 360],
                  scale: [1, 1.2, 1]
                }}
                transition={{
                  duration: 5 + Math.random() * 3,
                  repeat: Infinity,
                  delay: i * 0.8,
                  ease: "easeInOut"
                }}
                style={{
                  left: `${10 + i * 15}%`,
                  top: `${20 + (i % 3) * 30}%`
                }}
              />
            ))}
          </div>

          {/* Logo and text container */}
          <div className="loader-content">
            {/* Logo animation - Simple entrance in circle */}
            <motion.div
              className="logo-wrapper"
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{
                duration: 0.8,
                type: "spring",
                stiffness: 100
              }}
            >
              <motion.div
                className="logo-circle"
                animate={{
                  boxShadow: [
                    '0 0 20px rgba(255, 255, 255, 0.3)',
                    '0 0 40px rgba(255, 255, 255, 0.5)',
                    '0 0 20px rgba(255, 255, 255, 0.3)'
                  ]
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              >
                <img
                  src="/fluid-ai.png"
                  alt="Fluid AI"
                  className="loader-logo"
                />
              </motion.div>
            </motion.div>

            {/* Company name animation */}
            <div className="text-wrapper">
              <motion.h1
                className="company-name"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5, duration: 0.8 }}
              >
                {'Fluid AI'.split('').map((char, index) => (
                  <motion.span
                    key={index}
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                      delay: 0.8 + index * 0.1,
                      duration: 0.5,
                      type: "spring",
                      stiffness: 120
                    }}
                  >
                    {char === ' ' ? '\u00A0' : char}
                  </motion.span>
                ))}
              </motion.h1>

              <motion.p
                className="tagline"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.8, duration: 0.6 }}
              >
                Enterprise AI Assistant
              </motion.p>
            </div>

            {/* Loading bar */}
            <motion.div
              className="loading-bar-container"
              initial={{ opacity: 0, width: 0 }}
              animate={{ opacity: 1, width: '300px' }}
              transition={{ delay: 2.2, duration: 0.5 }}
            >
              <motion.div
                className="loading-bar"
                initial={{ width: '0%' }}
                animate={{ width: '100%' }}
                transition={{ delay: 2.5, duration: 2, ease: "easeInOut" }}
              />
            </motion.div>
          </div>

          {/* Multiple ripple effects */}
          {[...Array(3)].map((_, i) => (
            <motion.div
              key={i}
              className="ripple"
              initial={{ scale: 0, opacity: 0.6 }}
              animate={{
                scale: [0, 4],
                opacity: [0.6, 0]
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                delay: i * 1,
                ease: "easeOut"
              }}
            />
          ))}

          {/* Glowing center point */}
          <motion.div
            className="glow-center"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.3, 0.6, 0.3]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />

          {/* Scanning line effect */}
          <motion.div
            className="scan-line"
            animate={{
              y: ['-100%', '200%']
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: "linear"
            }}
          />
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default Loader;
