import { DemoProvider } from '@/components/demo-provider';
import { Shell } from '@/components/shell';
export default function DemoLayout({ children }: { children: React.ReactNode }) {
  return <DemoProvider><Shell>{children}</Shell></DemoProvider>;
}
