// app/result/[result]/page.tsx
import { notFound } from "next/navigation";

interface PageProps {
  params: { result: string };
}

export default function ResultPage({ params }: PageProps) {
  const { result } = params;

  const number = Number(result);
  if (isNaN(number)) return notFound();

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-6xl font-bold text-blue-600">{number}</div>
    </div>
  );
}
