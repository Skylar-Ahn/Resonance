export const demoUser = Object.freeze({
  id: 'demo-user-001', name: '지안', onboardingCompleted: true,
  concertTaste: Object.freeze({ content: '실내악', experience: '연주자의 움직임을 가까이 보고 싶다' }),
});

export const concerts = [
  { id: 'concert-demo-001', title: '데모 실내악 공연', english: 'An evening of chamber music', day: '24', month: 'OCT', date: '2026. 10. 24. SAT', time: '19:30', hall: 'Resonance 데모홀', performer: '데모 스트링 콰르텟', program: '가상의 현악 사중주 프로그램', instrument: 'STRING QUARTET', description: '네 개의 현이 주고받는 대화. 가까운 자리에서 작은 움직임까지 함께하는 실내악의 저녁.', color: 'yellow' },
  { id: 'concert-demo-002', title: '데모 피아노 리사이틀', english: 'Between the notes', day: '07', month: 'NOV', date: '2026. 11. 07. SAT', time: '17:00', hall: 'Resonance 데모홀', performer: '데모 피아니스트', program: '가상의 피아노 독주 프로그램', instrument: 'PIANO RECITAL', description: '음과 음 사이의 여백에 귀 기울이는 오후. 피아노의 선율과 연주자의 호흡을 따라가 보세요.', color: 'blue' },
  { id: 'concert-demo-003', title: '데모 앙상블 나이트', english: 'A shared resonance', day: '21', month: 'NOV', date: '2026. 11. 21. SAT', time: '19:00', hall: 'Resonance 데모홀', performer: '데모 챔버 앙상블', program: '가상의 앙상블 프로그램', instrument: 'CHAMBER ENSEMBLE', description: '서로 다른 악기가 만드는 하나의 울림. 무대 전체를 느끼는 시간을 만나보세요.', color: 'ink' },
] as const;

export type Concert = typeof concerts[number];
export type Seat = { id: string; section: string; row: number; number: number; x: number; y: number };
export const seats: Seat[] = ['A', 'B'].flatMap((section, sectionIndex) =>
  Array.from({ length: 8 }, (_, rowIndex) => Array.from({ length: 16 }, (_, index) => ({
    id: `${section}-${rowIndex + 1}-${index + 1}`, section, row: rowIndex + 1, number: index + 1,
    x: 43 + sectionIndex * 252 + index * 13,
    y: 106 + rowIndex * 25 + Math.abs(index - 7.5) * 1.1,
  }))).flat(),
);

export type Recommendation = { id: string; name: string; label: string; seatIds: string[]; summary: string; reason: string; tradeoff: string };
const options: Recommendation[] = [
  { id: 'close', name: '연주 관찰', label: '1층 A구역 3열 5번', seatIds: ['A-3-5'], summary: '연주자의 움직임을 더 가까이', reason: '실내악을 좋아하고 연주자의 움직임을 가까이 보고 싶다는 데모 취향에 맞춰, 무대 앞쪽의 한 좌석을 제안하는 모의 예시입니다.', tradeoff: '근접한 시야를 우선한 예시로, 무대 전체를 바라보는 관점과는 차이가 있습니다.' },
  { id: 'balance', name: '앙상블 균형', label: '1층 B구역 7열 11~14번', seatIds: ['B-7-11', 'B-7-12', 'B-7-13', 'B-7-14'], summary: '한 걸음 뒤에서 느끼는 전체의 호흡', reason: '선택한 데모 공연의 전체적인 균형을 우선하는 비교안입니다. 뒤쪽의 좌석 범위를 보여 주는 모의 예시이며, 실제 음향을 측정한 결과가 아닙니다.', tradeoff: '전체적인 감상을 우선한 예시로, 연주자의 작은 동작은 가까운 안보다 덜 보일 수 있습니다.' },
  { id: 'wide', name: '무대의 대화', label: '1층 A구역 5열 9~10번', seatIds: ['A-5-9', 'A-5-10'], summary: '다른 거리에서 비교하는 무대', reason: '중간 거리에서 무대의 대화를 바라보는 세 번째 모의 비교안입니다. 실제 관객 평가나 검증된 시야 데이터는 없습니다.', tradeoff: '실제 시야·음향 특성은 확인되지 않았습니다.' },
];

export function recommendations(need = '', three = false): Recommendation[] {
  const result = options.slice(0, three ? 3 : 2).map(option => ({ ...option, seatIds: [...option.seatIds] }));
  if (need.trim() === '전체 음향 균형 우선') {
    const balance = result.find(option => option.id === 'balance')!;
    balance.reason = '이번 Current Need인 “전체 음향 균형 우선”에 대응하는 미리 작성된 모의 응답입니다. 앙상블 균형 안을 앞에 배치하며 장기 Concert Taste는 바꾸지 않습니다.';
    return [balance, ...result.filter(option => option.id !== 'balance')];
  }
  return result;
}

export type ConcertState = { need: string; selected: string; draft: string };
export type DemoState = { user: typeof demoUser; byConcert: Record<string, ConcertState> };
export const initialState: DemoState = { user: demoUser, byConcert: {} };
export const defaultConcertState: ConcertState = { need: '', selected: 'close', draft: '' };
export type DemoAction =
  | { type: 'reset' }
  | { type: 'select'; concertId: string; selected: string }
  | { type: 'draft'; concertId: string; draft: string }
  | { type: 'apply'; concertId: string; need: string }
  | { type: 'clear'; concertId: string };

export function demoReducer(state: DemoState, action: DemoAction): DemoState {
  if (action.type === 'reset') return initialState;
  const current = state.byConcert[action.concertId] ?? defaultConcertState;
  let next: ConcertState;
  switch (action.type) {
    case 'select': next = { ...current, selected: action.selected }; break;
    case 'draft': next = { ...current, draft: action.draft }; break;
    case 'clear': next = { ...defaultConcertState }; break;
    case 'apply': {
      const need = action.need.trim();
      next = { need, draft: need, selected: recommendations(need)[0].id };
      break;
    }
  }
  return { ...state, byConcert: { ...state.byConcert, [action.concertId]: next } };
}

export const scenarioNames = ['normal', 'three', 'loading', 'empty', 'error', 'partial', 'unsupported'] as const;
export type Scenario = typeof scenarioNames[number];
export function parseScenario(value: string | null): Scenario {
  return scenarioNames.includes(value as Scenario) ? value as Scenario : 'normal';
}
