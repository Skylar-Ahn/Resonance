import { Suspense } from 'react';
import { DemoScreen } from '@/components/demo-screen';

export const dynamic = 'force-dynamic';
export default async function Page({ params }: { params: Promise<{ path?: string[] }> }) {
  const { path = [] } = await params;
  return <Suspense fallback={<p role="status">화면을 준비하고 있어요.</p>}><DemoScreen route={path} /></Suspense>;
}
