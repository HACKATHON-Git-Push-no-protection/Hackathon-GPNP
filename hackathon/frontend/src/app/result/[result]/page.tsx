import { notFound } from "next/navigation";
import FallingPoopEmojis from "./FallingPoopEmojis";

interface PageProps {
	params: Promise<{ result: string }>;
}

export default async function ResultPage({ params }: PageProps) {
	const { result } = await params;
	const number = Number(result);
	if (isNaN(number)) return notFound();

	return (
		<div className="flex items-center justify-center h-screen flex-col bg-gray-100">
			<FallingPoopEmojis />
			<div className="text-9xl font-bold text-orange-600">{number}</div>
			<div className="text-3xl font-bold text-gray-600 mt-4 text-center px-4">
				(you need to wipe exactly {number} times)
			</div>
		</div>
	);
}
