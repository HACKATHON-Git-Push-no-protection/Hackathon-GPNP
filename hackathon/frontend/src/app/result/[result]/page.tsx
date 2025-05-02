"use client";

import { notFound } from "next/navigation";
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

interface PageProps {
  params: { result: string };
}

const FallingPoopEmojis = ({ count = 15 }) => {
  const [poops, setPoops] = useState<PoopEmoji[]>([]);

  useEffect(() => {
    // Create initial poop emojis
    const initialPoops: PoopEmoji[] = [];
    for (let i = 0; i < count; i++) {
      initialPoops.push(createNewPoop(i));
    }
    setPoops(initialPoops);

    // Animation loop
    const animationFrame = requestAnimationFrame(animate);

    function animate() {
      setPoops((prevPoops) =>
        prevPoops.map((poop) => {
          // Update position
          const y = poop.y + poop.speed;
          const rotation = poop.rotation + poop.rotationSpeed;

          // Reset if out of screen
          if (y > window.innerHeight) {
            return createNewPoop(poop.id);
          }

          return { ...poop, y, rotation };
        })
      );

      requestAnimationFrame(animate);
    }

    // Cleanup
    return () => cancelAnimationFrame(animationFrame);
  }, [count]);

  function createNewPoop(id: number): PoopEmoji {
    return {
      id,
      x: Math.random() * window.innerWidth,
      y: -50 - Math.random() * 100, // Start above the screen at random positions
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

export default function ResultPage({ params }: PageProps) {
  const { result } = params;

  const number = Number(result);
  if (isNaN(number)) return notFound();

  return (
    <div className="flex items-center justify-center h-screen flex-col bg-gray-100">
      <FallingPoopEmojis />
      <div className="text-9xl font-bold text-orange-600">{number}</div>
      <div className="text-3xl font-bold text-gray-600 mt-4 text-center px-4">
        (you need to wipe at least {number} times)
      </div>
    </div>
  );
}
