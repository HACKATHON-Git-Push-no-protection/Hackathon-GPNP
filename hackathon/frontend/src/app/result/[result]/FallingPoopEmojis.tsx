"use client";

import { useEffect, useState } from "react";

interface PoopEmoji {
  id: number;
  x: number;
  y: number;
  size: number;
  speed: number;
  rotation: number;
  rotationSpeed: number;
}

const FallingPoopEmojis = ({ count = 15 }) => {
  const [poops, setPoops] = useState<PoopEmoji[]>([]);

  useEffect(() => {
    const initialPoops: PoopEmoji[] = [];
    for (let i = 0; i < count; i++) {
      initialPoops.push(createNewPoop(i));
    }
    setPoops(initialPoops);

    let animationFrame: number;
    const animate = () => {
      setPoops((prevPoops) =>
        prevPoops.map((poop) => {
          const y = poop.y + poop.speed;
          const rotation = poop.rotation + poop.rotationSpeed;

          if (y > window.innerHeight) {
            return createNewPoop(poop.id);
          }

          return { ...poop, y, rotation };
        })
      );

      animationFrame = requestAnimationFrame(animate);
    };

    animationFrame = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(animationFrame);
  }, [count]);

  function createNewPoop(id: number): PoopEmoji {
    return {
      id,
      x: Math.random() * window.innerWidth,
      y: -50 - Math.random() * 100,
      size: 20 + Math.random() * 30,
      speed: 1 + Math.random() * 3,
      rotation: Math.random() * 360,
      rotationSpeed: -1 + Math.random() * 2,
    };
  }

  return (
    <div className="fixed inset-0 pointer-events-none z-10">
      {poops.map((poop) => (
        <div
          key={poop.id}
          className="absolute select-none"
          style={{
            left: `${poop.x}px`,
            top: `${poop.y}px`,
            fontSize: `${poop.size}px`,
            transform: `rotate(${poop.rotation}deg)`,
            transition: "transform 0.5s ease-out",
          }}
        >
          💩
        </div>
      ))}
    </div>
  );
};

export default FallingPoopEmojis;
