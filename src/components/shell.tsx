'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { ArrowUpRight, Bookmark, Disc3, Menu, Settings2, SlidersHorizontal, UserRound } from 'lucide-react';
import { Dialog } from './dialog';
import s from './demo.module.css';

const utilities = [
  { name: 'Account', path: 'account', Icon: UserRound },
  { name: 'My Concert Taste', path: 'taste', Icon: SlidersHorizontal },
  { name: 'Bookmarks', path: 'bookmarks', Icon: Bookmark },
  { name: 'Settings', path: 'settings', Icon: Settings2 },
];
export function Shell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  const [menu, setMenu] = useState(false);
  const active = path.includes('/concerts/') || path === '/demo/for-you' ? 'For You' : path === '/demo/articles' ? 'Articles' : path === '/demo/reviews' ? 'Reviews' : '';
  return <div className={s.shell}>
    <a className={s.skipLink} href="#content">본문으로 건너뛰기</a>
    <aside className={s.sidebar}>
      <Link href="/demo" className={s.logo} aria-label="Resonance App Home">resonance<span className={s.logoDot} /></Link>
      <nav className={s.navigation} aria-label="주 메뉴">
        {[['For You', 'for-you'], ['Articles', 'articles'], ['Reviews', 'reviews']].map(([name, route]) => <Link key={name} href={`/demo/${route}`} aria-current={active === name ? 'page' : undefined}>{name}{name !== 'For You' && <span className={s.outsideMark} title="이번 데모 범위 밖" aria-label="이번 데모 범위 밖">범위 밖</span>}</Link>)}
      </nav>
      <div className={s.sidebarBottom}><span className={s.shortLine} /><p>MUSIC<br />PEOPLE<br />PLACES</p><span>A deeper listening.</span><div className={s.edition}>PROTOTYPE <span>001</span></div></div>
    </aside>
    <div className={s.body}>
      <header className={s.topbar}><span className={s.topbarLabel}>YOUR NEXT RESONANCE</span><div className={s.topbarRight}><span className={s.demoPill}><span />DEMO</span><span className={s.userStatus}>온보딩 완료</span><button className={s.iconButton} aria-label="유틸리티 메뉴" title="유틸리티 메뉴" aria-haspopup="dialog" aria-expanded={menu} onClick={() => setMenu(true)}><Menu size={23} /></button></div></header>
      <main id="content" className={s.main}>{children}</main>
      <footer className={s.footer}><span><Disc3 size={15} /> Resonance / P-001</span><span>샘플 공연 · 모의 추천 · 실제 관객 근거 없음</span></footer>
    </div>
    <Dialog open={menu} title="내 Resonance" onClose={() => setMenu(false)}><p className={s.muted}>지안 · 온보딩을 완료한 데모 사용자</p><div className={s.utilityLinks}>{utilities.map(({ name, path: route, Icon }) => <Link key={route} href={`/demo/${route}`} onClick={() => setMenu(false)}><Icon size={19} /><span>{name}<small>{route === 'account' || route === 'taste' ? '데모 정보 · 읽기 전용' : '이번 데모 범위 밖'}</small></span><ArrowUpRight size={18} /></Link>)}</div></Dialog>
  </div>;
}
