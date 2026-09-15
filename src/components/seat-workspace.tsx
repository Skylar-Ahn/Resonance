'use client';
import { useId, useState } from 'react';
import { ArrowRight, Check, Info, RotateCcw, SlidersHorizontal } from 'lucide-react';
import { defaultConcertState, recommendations, seats, type Concert, type Scenario } from '@/lib/demo';
import { useDemo } from './demo-provider';
import { Dialog } from './dialog';
import s from './demo.module.css';

export function SeatWorkspace({ concert, scenario, onScope }: { concert: Concert; scenario: Scenario; onScope: (scope: string) => void }) {
  const { state, dispatch } = useDemo();
  const current = state.byConcert[concert.id] ?? defaultConcertState;
  const options = recommendations(current.need, scenario === 'three');
  const selected = options.find(option => option.id === current.selected) ?? options[0];
  const [editing, setEditing] = useState(false);
  const [zoom, setZoom] = useState(1);
  const mapId = useId();
  const needId = useId();
  const selectedSeats = new Set(selected.seatIds);
  const closeEditor = () => { dispatch({ type: 'draft', concertId: concert.id, draft: current.need }); setEditing(false); };
  return <section aria-label="좌석 추천">
    <div className={s.sectionHeading}><div><p className={s.eyebrow}>A SEAT THAT FEELS RIGHT</p><h2>당신의 자리, 다른 가능성.</h2></div><button className={s.secondaryButton} onClick={() => setEditing(true)}><SlidersHorizontal size={17} />추천 기준 조정</button></div>
    <div className={s.needSummary}><span className={s.smallLabel}>CURRENT NEED</span><p data-testid="current-need">{current.need || '기본 Concert Taste로 비교하고 있어요.'}</p>{current.need && <button className={s.iconButton} aria-label="Current Need 초기화" title="기본 추천으로 초기화" onClick={() => dispatch({ type: 'clear', concertId: concert.id })}><RotateCcw size={16} /></button>}</div>
    <div className={s.seatLayout}>
      <div className={s.options} aria-label="추천안 목록">
        <div className={s.listCaption}><span>추천안 비교</span><span>{String(options.length).padStart(2, '0')} OPTIONS</span></div>
        {options.map((option, index) => <button type="button" key={option.id} className={`${s.option} ${option.id === selected.id ? s.optionActive : ''}`} aria-pressed={option.id === selected.id} aria-label={`${option.name} 추천안`} onClick={() => dispatch({ type: 'select', concertId: concert.id, selected: option.id })} data-testid={`option-${option.id}`}><span className={s.optionTop}><span>{String(index + 1).padStart(2, '0')}</span><span className={s.selectionIndicator}>{option.id === selected.id && <Check size={13} />}</span></span><strong>{option.name}</strong><span className={s.optionSeat}>{option.label}</span><span className={s.optionSummary}>{option.summary}</span></button>)}
        <p className={s.evidenceNote}><Info size={16} /><span>추천 계산과 설명은 모의 데이터입니다.<br />실제 관객 후기 근거는 없습니다.</span></p>
      </div>
      <div className={s.mapColumn}>
        <div className={s.mapTool}>
          <div className={s.mapHeader}><span><strong>{concert.hall}</strong><small>가상 좌석 배치도 · 1층</small></span><label className={s.zoom}>확대<select aria-label="좌석도 확대" value={zoom} onChange={event => setZoom(Number(event.target.value))}><option value={1}>100%</option><option value={1.5}>150%</option><option value={2}>200%</option></select></label></div>
          <div className={s.mapViewport} tabIndex={0} aria-label="좌석 배치도 스크롤 영역"><svg className={s.seatMap} style={{ width: `${zoom * 100}%`, height: `calc(var(--map-height) * ${zoom})` }} viewBox="0 0 540 370" role="img" aria-labelledby={`${mapId}-title ${mapId}-desc`}><title id={`${mapId}-title`}>{concert.hall} 추천 위치</title><desc id={`${mapId}-desc`}>{selected.label}. 파란색 사각 테두리와 밝은 중심이 있는 좌석이 현재 선택한 추천안입니다. 실제 판매 좌석도가 아닙니다.</desc><path d="M135 42 Q270 63 405 42 L405 61 Q270 84 135 61Z" fill="#dcded5" /><text x="270" y="40" textAnchor="middle" className={s.stageText}>STAGE / 무대</text><text x="144" y="93" textAnchor="middle" className={s.blockText}>A 구역</text><text x="398" y="93" textAnchor="middle" className={s.blockText}>B 구역</text>{seats.map(seat => <g key={seat.id} data-seat-id={seat.id} data-highlighted={selectedSeats.has(seat.id) ? 'true' : 'false'}>{selectedSeats.has(seat.id) && <rect x={seat.x - 6} y={seat.y - 6} width="12" height="12" rx="2" fill="var(--blue)" />}<circle cx={seat.x} cy={seat.y} r={selectedSeats.has(seat.id) ? 2.8 : 3.8} fill={selectedSeats.has(seat.id) ? '#ffffff' : '#c5c8be'} /></g>)}{Array.from({ length: 8 }, (_, index) => <text key={index} x="270" y={116 + index * 25} textAnchor="middle" className={s.rowText}>{index + 1}열</text>)}<text x="270" y="348" textAnchor="middle" className={s.rowText}>각 구역 · 왼쪽부터 1번 → 16번</text></svg></div>
          <div className={s.mapLegend}><span><i />선택 추천 위치</span><span>잔여석 미확인</span></div>
        </div>
        <section className={s.reason} aria-live="polite" aria-atomic="true" data-testid="selected-reason"><div className={s.reasonLabel}><span className={s.smallLabel}>YOUR PERSPECTIVE</span><span>{selected.name}</span></div><h3 data-testid="selected-seat-label">{selected.label}</h3><p>{selected.reason}</p><p className={s.tradeoff}>{selected.tradeoff}</p>{scenario === 'partial' && <p role="status" className={s.inlineNotice}>일부 정보 없음 · 프로그램 상세와 관객 근거가 제공되지 않았습니다.</p>}<div className={s.bookingRow}><span>현재 구매 가능 여부는 확인하지 않았습니다.</span><button className={s.textButton} onClick={() => onScope('외부 예매')} aria-label="예매하기 · 이번 데모 범위 밖">예매하기 <ArrowRight size={16} /><small>범위 밖</small></button></div></section>
      </div>
    </div>
    <Dialog open={editing} title="이번 공연의 Current Need" onClose={closeEditor}>
      <form onSubmit={event => { event.preventDefault(); dispatch({ type: 'apply', concertId: concert.id, need: current.draft }); setEditing(false); }}>
        <p className={s.muted}>이번 공연에서 더 중요하게 느끼고 싶은 경험은 무엇인가요?</p>
        <label className={s.fieldLabel} htmlFor={needId}>이번 공연의 관람 기준</label><textarea id={needId} autoFocus maxLength={280} value={current.draft} onChange={event => dispatch({ type: 'draft', concertId: concert.id, draft: event.target.value })} placeholder="예: 전체 음향 균형 우선" rows={3} />
        <button type="button" className={s.textButton} onClick={() => dispatch({ type: 'draft', concertId: concert.id, draft: '전체 음향 균형 우선' })}>균형 우선 예시 입력 <ArrowRight size={15} /></button>
        <div className={s.tasteSnapshot}><span className={s.smallLabel}>장기 CONCERT TASTE · 변경하지 않음</span><p data-testid="taste-original">{state.user.concertTaste.experience}</p><small>Content Preference: {state.user.concertTaste.content}</small></div>
        <p className={s.formNote}>모의 처리: “전체 음향 균형 우선”은 준비된 균형 응답을 표시합니다. 다른 입력은 보존하고 기본 모의 추천을 유지합니다.</p>
        <div className={s.dialogActions}><button type="button" className={s.secondaryButton} onClick={closeEditor}>취소</button><button className={s.primaryButton} type="submit">이번 추천에 적용 <ArrowRight size={17} /></button></div>
      </form>
    </Dialog>
  </section>;
}
