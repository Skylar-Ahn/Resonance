import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = { title: 'Resonance | A deeper listening', description: 'Resonance P-001: 모의 공연과 좌석 추천 프로토타입', robots: { index: false, follow: false } };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="ko"><body>{children}</body></html>;
}
