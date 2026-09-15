'use client';
import Image from 'next/image';
import Link from 'next/link';
import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { ArrowLeft, ArrowRight, ArrowUpRight, Bookmark, CalendarDays, Check, ChevronRight, Disc3, Info, MapPin, RotateCcw } from 'lucide-react';
import { concerts, parseScenario, scenarioNames, type Concert } from '@/lib/demo';
import { useDemo } from './demo-provider';
import { Dialog } from './dialog';
import { SeatWorkspace } from './seat-workspace';
import s from './demo.module.css';

function Poster({ concert, compact = false }: { concert: Concert; compact?: boolean }) {
  return <div aria-label={`${concert.title} 데모 포스터`} role="img" className={`${s.poster} ${s[concert.color]} ${compact ? s.posterCompact : ''}`}><span className={s.posterEdition}>RESONANCE<br />LISTENING SERIES</span><div className={s.posterDisc}><Disc3 strokeWidth={0.65} aria-hidden="true" /></div><strong>{concert.english}</strong><span className={s.posterBottom}>{concert.instrument}<span>{concert.day} / {concert.month}</span></span></div>;
}

function Home() {
  const { dispatch } = useDemo();
  useEffect(() => { dispatch({ type: 'reset' }); }, [dispatch]);
  return <>
    <div className={s.breadcrumb}>APP HOME <span>01 / A DEEPER LISTENING</span></div>
    <section className={s.homeScene}>
      <Image src="/images/resonance-vinyl.png" alt="노란 resonance 레이블의 검은 LP, 기본 정지 상태" fill sizes="(max-width: 799px) 100vw, 70vw" priority className={s.homeImage} />
      <div className={s.homeHeading}><p className={s.eyebrow}>MUSIC · PEOPLE · PLACES</p><h1>Music brings<br />us closer.</h1></div>
      <div className={s.homeCaption}><span className={s.shortLine} /><p>좋아하는 음악이<br />당신의 자리가 되는 순간.</p></div>
      <span className={s.recordLabel}>SIDE A / RESONANCE</span>
    </section>
    <div className={s.homeCta}><div><span className={s.eyebrow}>FOR YOUR NEXT EVENING</span><p>나의 취향에서 시작하는 다음 공연</p></div><Link href="/demo/for-you" className={s.primaryButton}>For You 둘러보기 <ArrowRight size={19} /></Link></div>
  </>;
}

function BookmarkButton({ onScope, title }: { onScope: (scope: string) => void; title: string }) {
  return <button className={s.iconButton} title="북마크 · 이번 데모 범위 밖" aria-label={`${title} 북마크 · 이번 데모 범위 밖`} onClick={() => onScope('공연 북마크')}><Bookmark size={20} /></button>;
}

function Feed({ onScope }: { onScope: (scope: string) => void }) {
  return <>
    <div className={s.feedIntro}><div><span className={s.eyebrow}>CURATED FOR YOUR TASTE</span><h1>다음 울림을 만나보세요.</h1><p>실내악, 그리고 가까이에서 느끼는 연주.</p></div><span className={s.count}>03 <small>CONCERTS</small></span></div>
    <div className={s.feedCaption}><span>UPCOMING CONCERTS</span><span>샘플 공연 · 모의 추천</span></div>
    <div className={s.concertList}>{concerts.map(concert => <article className={s.concertRow} key={concert.id}>
      <div className={s.dateBlock}><span>{concert.month}</span><strong>{concert.day}</strong><small>SAT</small></div>
      <Link className={s.posterLink} href={`/demo/concerts/${concert.id}`} tabIndex={-1} aria-hidden="true"><Poster concert={concert} compact /></Link>
      <div className={s.concertInfo}><p className={s.eyebrow}>{concert.instrument}</p><h2><Link href={`/demo/concerts/${concert.id}`}>{concert.title}</Link></h2><p className={s.english}>{concert.english}</p><p className={s.venue}>{concert.hall} <span>·</span> {concert.time}</p><Link className={s.seatTeaser} href={`/demo/concerts/${concert.id}/seat`}><span><small>좌석 추천 · 모의</small><strong>1층 A구역 3열 5번</strong><span>연주자의 움직임을 더 가까이</span></span><ArrowRight size={20} /></Link></div>
      <div className={s.concertActions}><BookmarkButton onScope={onScope} title={concert.title} /><Link className={s.roundLink} href={`/demo/concerts/${concert.id}`} aria-label={`${concert.title} 상세 보기`} title="공연 상세"><ArrowUpRight size={22} /></Link></div>
    </article>)}</div>
    <p className={s.feedFootnote}><Info size={16} />공연, 출연자, 좌석 정보와 추천 이유는 데모용 샘플입니다. 실제 판매 정보가 아닙니다.</p>
  </>;
}

function ConcertHeader({ concert, seatTab, onScope }: { concert: Concert; seatTab: boolean; onScope: (scope: string) => void }) {
  return <>
    <div className={s.detailTop}><Link href={seatTab ? `/demo/concerts/${concert.id}` : '/demo/for-you'} className={s.backLink}><ArrowLeft size={16} />{seatTab ? '공연 개요' : 'For You'}</Link><span className={s.smallLabel}>CONCERT / {seatTab ? 'SEAT' : 'OVERVIEW'}</span><BookmarkButton onScope={onScope} title={concert.title} /></div>
    <header className={`${s.concertHeader} ${seatTab ? s.compactHeader : ''} `}><span className={s.eyebrow}>{concert.instrument} <span className={s.sampleTag}>샘플 공연</span></span><h1>{concert.title}</h1><p>{concert.english}</p><div className={s.metadata}><span><CalendarDays size={16} />{concert.date} · {concert.time}</span><span><MapPin size={16} />{concert.hall}</span></div></header>
    <nav className={s.tabs} aria-label="공연 상세 메뉴"><Link href={`/demo/concerts/${concert.id}`} aria-current={!seatTab ? 'page' : undefined}>Overview</Link><Link href={`/demo/concerts/${concert.id}/seat`} aria-current={seatTab ? 'page' : undefined}>Seat</Link>{['Program', 'Articles', 'Reviews'].map(name => <button key={name} onClick={() => onScope(name)} aria-label={`${name} · 이번 데모 범위 밖`}>{name}<small>범위 밖</small></button>)}</nav>
  </>;
}

function Overview({ concert, partial, onScope }: { concert: Concert; partial: boolean; onScope: (scope: string) => void }) {
  return <div className={s.overview}><div className={s.overviewCopy}><p className={s.eyebrow}>ABOUT THIS EVENING</p><h2>서로의 소리에<br />귀 기울이는 시간.</h2><p>{concert.description}</p><dl className={s.facts}><div><dt>출연</dt><dd>{concert.performer}</dd></div><div><dt>프로그램</dt><dd>{partial ? '정보 미제공' : concert.program}</dd></div><div><dt>데이터</dt><dd>가상 공연 · 실제 공연 정보 아님</dd></div></dl><div className={s.overviewRecommend}><div><span className={s.smallLabel}>YOUR SEAT / 모의 추천</span><h3>1층 A구역 3열 5번</h3><p>연주 관찰부터 앙상블 균형까지, 서로 다른 자리.</p></div><Link href={`/demo/concerts/${concert.id}/seat`} className={s.primaryButton}>좌석 추천 보기 <ArrowRight size={18} /></Link></div><div className={s.overviewActions}><button className={s.textButton} onClick={() => onScope('외부 예매')}>예매하기 <ArrowUpRight size={16} /><small>범위 밖</small></button><button className={s.textButton} onClick={() => onScope('후기 작성')}>후기 남기기 <small>범위 밖</small></button></div><p className={s.formNote}>실제 관객 근거와 잔여석 정보는 제공되지 않습니다.</p></div><Poster concert={concert} /></div>;
}

function Utility({ name }: { name: string }) {
  const { state } = useDemo();
  const [tab, setTab] = useState('Concerts');
  const titles: Record<string, string> = { account: 'Account', taste: 'My Concert Taste', bookmarks: 'Bookmarks', settings: 'Settings', articles: 'Articles', reviews: 'Reviews' };
  return <section className={s.utilityPage}><Link href="/demo" className={s.backLink}><ArrowLeft size={16} />App Home</Link><span className={s.eyebrow}>MY RESONANCE</span><h1>{titles[name]}</h1>
    {name === 'account' || name === 'taste' ? <><div className={s.readOnlyNotice}><Check size={17} />온보딩 완료 · 데모 정보 · 읽기 전용</div><dl className={s.profile}><div><dt>사용자</dt><dd>{state.user.name} / {state.user.id}</dd></div><div><dt>Content Preference</dt><dd>{state.user.concertTaste.content}</dd></div><div><dt>Experience Preference</dt><dd data-testid="profile-experience">{state.user.concertTaste.experience}</dd></div></dl><p className={s.muted}>실제 계정 관리와 취향 수정은 이번 데모 범위 밖입니다.</p></> : <>{name === 'bookmarks' && <div className={s.tabs} role="tablist" aria-label="북마크 종류">{['Concerts', 'Articles'].map(label => <button key={label} role="tab" aria-selected={tab === label} onClick={() => setTab(label)}>{label}</button>)}</div>}<div className={s.outsidePanel} {...(name === 'bookmarks' ? { role: 'tabpanel', 'aria-label': tab } : {})}><Bookmark size={30} strokeWidth={1} /><h2>이번 데모 범위 밖입니다.</h2><p>{name === 'bookmarks' ? `${tab === 'Concerts' ? '공연' : '아티클'} 북마크의 저장과 목록 연동은 후속 작업에서 제공합니다.` : `${titles[name]}의 실제 기능은 후속 작업에서 제공합니다.`}</p><Link className={s.textButton} href="/demo/for-you">For You로 이동 <ArrowRight size={16} /></Link></div></>}
  </section>;
}

export function DemoScreen({ route }: { route: string[] }) {
  const pathname = usePathname();
  const params = useSearchParams();
  const router = useRouter();
  const scenario = parseScenario(params.get('scenario'));
  const [loading, setLoading] = useState(scenario === 'loading');
  const [scope, setScope] = useState('');
  const home = route.length === 0;
  const feed = route.join('/') === 'for-you';
  const concert = route[0] === 'concerts' ? concerts.find(item => item.id === route[1]) : undefined;
  const seatTab = route[2] === 'seat';
  const validConcert = concert && (route.length === 2 || (route.length === 3 && seatTab));
  const utility = route.length === 1 && ['account', 'taste', 'bookmarks', 'settings', 'articles', 'reviews'].includes(route[0]);
  useEffect(() => {
    if (scenario !== 'loading') { setLoading(false); return; }
    setLoading(true);
    const timer = setTimeout(() => setLoading(false), 850);
    return () => clearTimeout(timer);
  }, [scenario, pathname]);
  const recover = () => router.replace(pathname, { scroll: false });
  const gate = (feed || validConcert) && (loading || ['error', 'empty', 'unsupported'].includes(scenario));
  return <>
    {home ? <Home /> : <>
      {validConcert && <ConcertHeader concert={concert} seatTab={seatTab} onScope={setScope} />}
      {gate ? <section className={s.statePanel} role={scenario === 'error' ? 'alert' : 'status'}>{loading ? <><Disc3 className={s.spinning} size={36} /><h1>모의 추천을 준비하고 있어요.</h1><p>잠시 후 샘플 결과가 표시됩니다.</p></> : <><Info size={30} /><span className={s.eyebrow}>DEMO SCENARIO</span><h1>{scenario === 'error' ? '추천을 불러오지 못했어요.' : scenario === 'empty' ? '아직 추천할 결과가 없어요.' : '이 홀의 좌석도는 준비 중이에요.'}</h1><p>{scenario === 'unsupported' ? '좌석 위치를 추정해 표시하지 않습니다.' : '오류와 빈 결과를 확인하기 위한 모의 상태입니다.'}</p><div className={s.dialogActions}><button className={s.primaryButton} onClick={recover}><RotateCcw size={17} />{scenario === 'error' ? '다시 시도' : '기본 데모로 돌아가기'}</button><Link className={s.backLink} href={concert ? `/demo/concerts/${concert.id}` : '/demo'}>{concert ? '공연 개요' : 'App Home'}<ArrowRight size={16} /></Link></div></>}</section>
        : feed ? <Feed onScope={setScope} /> : validConcert ? seatTab ? <SeatWorkspace concert={concert} scenario={scenario} onScope={setScope} /> : <Overview concert={concert} partial={scenario === 'partial'} onScope={setScope} /> : utility ? <Utility name={route[0]} /> : <div className={s.statePanel}><h1>공연을 찾을 수 없어요.</h1><p>이 주소에 해당하는 데모 화면이 없습니다.</p><Link className={s.primaryButton} href="/demo/for-you">For You로 이동 <ArrowRight size={16} /></Link></div>}
    </>}
    {(feed || validConcert) && <details className={s.scenarios}><summary>데모 상태 확인 <ChevronRight size={14} /></summary><label>모의 응답<select aria-label="모의 응답 상태" value={scenario} onChange={event => router.replace(`${pathname}${event.target.value === 'normal' ? '' : `?scenario=${event.target.value}`}`, { scroll: false })}>{scenarioNames.map(name => <option key={name} value={name}>{{ normal: '기본 추천', three: '3개 추천안', loading: '로딩 후 성공', empty: '빈 결과', error: '실패', partial: '일부 정보 없음', unsupported: '좌석도 미지원' }[name]}</option>)}</select></label><p>실제 추천 엔진·관객 후기·예매 API에 연결하지 않습니다.</p></details>}
    <Dialog open={!!scope} title={`${scope} · 범위 안내`} onClose={() => setScope('')}><div className={s.scopeContent}><span className={s.sampleTag}>P-001 범위 밖</span><h3>{scope} 기능은 아직 연결하지 않았어요.</h3><p>이번 데모는 공연 탐색과 모의 좌석 추천 비교까지 제공합니다. 저장·예매·후기 등의 실제 처리는 실행되지 않습니다.</p><button className={s.primaryButton} onClick={() => setScope('')}>확인 <Check size={17} /></button></div></Dialog>
  </>;
}
