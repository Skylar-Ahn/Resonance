# Resonance — Design System

> 상태: Confirmed visual direction + unresolved token details v1.0
> 기준일: 2026-09-15

## 1. 디자인 철학과 visual language

Resonance는 클래식 음악을 보수적인 장식으로 재현하기보다 LP와 에디토리얼 그래픽을 이용한 절제된 neo-brutalism으로 표현한다.

- 미니멀하고 고대비인 구조
- 충분한 흰 여백과 단단한 검정 타이포그래피·선
- 선명한 Resonance Blue와 상징적인 노랑
- LP와 stylus를 잇는 일관된 브랜드 오브젝트
- Articles와 개인 매거진으로 확장 가능한 에디토리얼 감각

목업은 시각적 의도를 제공하지만 제품 범위와 상태 규칙을 확정하지 않는다. 화면별 자산과 목업 차이는 [Reference Map](REFERENCE_MAP.md)에서 관리한다.

## 2. Color roles와 token 방향

| 역할 | 용도 |
| --- | --- |
| White | 기본 화면·seen 공연 카드 배경과 여백 |
| Black | LP, 핵심 타이포그래피, 구조선 |
| Resonance Blue | 디지털 제품성, 활성 상태, CTA, glow, `NEW` 텍스트 |
| Yellow | LP 레이블, 클래식 음반의 기억점, 브랜드 정체성 |
| Cool blue/lavender tint | unseen 공연 카드의 매우 옅은 배경 |
| Stronger pastel tint | Seat recommendation surface의 강조 배경 |

파랑만 브랜드색으로 취급하지 않는다. 노랑은 전통적인 클래식 음반 커버의 인상을 연결하는 핵심 색이다. 정확한 token 값과 각 조합의 명암 대비는 Open Question이다.

향후 색상, 타이포그래피, 간격, 모서리, 선 굵기는 역할 기반 design token으로 관리한다. 상태마다 임의의 유사 색을 추가하지 않는다.

## 3. Typography hierarchy

- 핵심 제목은 검정과 충분한 대비를 사용한다.
- Articles 본문은 장문 읽기에 적합한 줄 길이·행간·문단 간격을 사용한다.
- 상태·분류·제목은 정보 역할을 시각적으로 구분하되 같은 의미를 중복 표기하지 않는다.

For You 공연 카드의 수직 계층은 다음 순서를 사용하고 세 텍스트의 왼쪽 시작선을 맞춘다.

1. `NEW`
2. 공연 분류, 예: `STRING QUARTET`
3. 공연 제목

글자 크기 우선순위는 `공연 제목 > NEW > 공연 분류`다. `NEW`는 pill이나 badge가 아닌 Resonance Blue 텍스트로 표시한다.

## 4. Spacing, border, radius와 line

- 흰 여백은 콘텐츠 계층과 에디토리얼 리듬을 만드는 구조로 사용한다.
- 검정 선과 border는 영역 구분에 필요한 만큼만 사용한다.
- radius와 선 굵기는 token으로 관리하며 화면마다 임의 값을 늘리지 않는다.
- fixed pixel 좌표나 absolute positioning을 primary layout으로 사용하지 않는다.
- 긴 텍스트와 번역문이 컴포넌트 경계를 침범하지 않도록 유연한 높이와 reflow를 허용한다.

정확한 spacing scale, border width와 radius 값은 아직 확정하지 않는다.

## 5. Component visual rules와 variants

- 반복 요소는 component와 variant로 만든다.
- 최소 상태 후보는 `default`, `active`, `hover/focus`, `loading`, `empty`, `error`, `disabled`다.
- 상태는 색 하나에만 의존하지 않고 텍스트, 구조, 아이콘 또는 접근 가능한 상태 정보와 함께 구분한다.
- CTA는 화면의 핵심 정보보다 시각적으로 과도하게 우세하지 않게 한다.
- 동일한 콘텐츠를 기기별 별도 복제품으로 만들지 않는다.

### Navigation

- App Home에서는 `For You`, `Articles`, `Reviews` 어느 메뉴도 active가 아니다.
- primary content 화면에서는 현재 메뉴 하나만 active다.
- Mobile/Tablet의 bottom navigation과 top navigation은 같은 component의 위치·상태 변화다.
- Desktop left sidebar에서도 동일한 메뉴명과 active 의미를 유지한다.
- 상세 화면은 global top primary navigation을 중첩하지 않고 compact header와 Back을 사용한다.

위치와 전환은 [Responsive](RESPONSIVE.md)와 [Interaction](INTERACTION.md)에서 정의한다.

## 6. For You 카드 상태

`NEW`와 `unseen`은 독립 상태다.

- `NEW`: 공연 최초 수집 시점부터 7일 동안 유지하는 공연 상태다. 사용자가 공연을 확인해도 기간은 줄지 않으며 공연 정보 수정으로 다시 시작하지 않는다.
- `unseen`: 사용자별 상태다. 단순 렌더링·스크롤·viewport 노출만으로 해제하지 않는다.
- `seen`: 상세 열기나 좌석 추천 확인처럼 공연에 대한 의도적 행동 뒤에 전환한다.

unseen 카드는 매우 옅은 cool blue/lavender, seen 카드는 white를 사용한다. seen 공연도 같은 피드 위치에 남으며 숨김이나 강등을 시각적으로 암시하지 않는다. Seat recommendation surface는 unseen보다 강한 같은 계열의 pastel tint를 사용할 수 있다.

## 7. LP와 stylus의 시각 구성

Splash와 App Home은 동일한 LP 오브젝트를 상태에 따라 다르게 보여준다.

### Idle / Stop

- LP 한 장을 중심 오브젝트로 사용한다.
- LP 중앙은 노란 `resonance` 레이블이다.
- stylus는 LP 밖의 resting position에 있다.
- LP 회전과 재생 위치는 초기 상태다.

### Playing

- stylus가 LP의 play zone 위에 있다.
- LP가 회전하고 blue glow를 강화할 수 있다.
- 중앙 노란 원의 정체성을 유지하면서 흑백 작곡가 또는 연주자 portrait를 표시한다.
- 얇은 yellow ring이나 center dot처럼 Splash와의 연속성을 남길 수 있다.

### Paused

- portrait와 stylus 위치는 유지한다.
- LP 회전은 멈추고 glow는 Playing보다 낮출 수 있다.
- 재생 위치가 유지되고 있음을 Stop과 구분해야 한다.

### Track ended

Stop의 시각 상태로 돌아간다. stylus는 resting position, LP는 정지, portrait는 제거되고 노란 `resonance` 레이블이 복귀한다.

정확한 hover/focus, paused, unavailable/error 표현과 portrait 자산 정책은 Open Question이다. 상태 전환과 입력은 [Interaction](INTERACTION.md)을 따른다.

## 8. 화면별 시각 원칙

### App Home

- LP와 브랜드 메시지가 주인공이다.
- 정보 카드나 목록을 억지로 추가하지 않는다.
- primary menu는 모두 비선택이다.
- 햄버거 메뉴를 유틸리티 진입점으로 유지한다.

### For You

- 큰 중복 제목과 `All Events` 컨트롤을 두지 않는다.
- 날짜, 공연명, 장소·시간, 좌석 추천 요약과 이유를 빠르게 훑을 수 있어야 한다.
- 추천 CTA는 공연 정보보다 시각적으로 우세하지 않게 한다.

### Concert Detail / Seat

- 공연 정보와 하위 탭의 계층을 명확히 한다.
- Seat는 추천안과 좌석도 시각화를 함께 제공한다.
- 실시간 판매 좌석도처럼 보이게 하지 않는다.
- 추천 이유와 잔여석 미확인 경계를 가까이 배치한다.

### Articles

- 장문 읽기에 적합한 본문 리듬을 사용한다.
- 대표 비주얼은 본문을 방해하지 않는 에디토리얼 요소다.
- 출처와 관련 공연 연결을 숨기지 않는다.

### Reviews

- 평점 입력과 자유 텍스트를 명확히 분리한다.
- 개인 기록의 차분한 아카이브 인상을 유지한다.
- 타인 프로필, 좋아요 수, 소셜 반응처럼 커뮤니티로 오해할 요소를 넣지 않는다.

## 9. Figma와 Markdown의 역할

| 도구 | 담당 |
| --- | --- |
| Markdown | 제품 범위, IA, User Flow, 상태·반응형·데이터·추천 정책 |
| Figma | 화면 구성, component, variant, Auto Layout, 대표 breakpoint, prototype |
| 목업 이미지 | 시각적 의도와 분위기 |

Figma가 문서에 없는 기능을 생성하면 확정 기능으로 받아들이지 않는다. Figma 산출물은 편집 가능한 native layer, component/variant, Auto Layout, Mobile·Tablet·Desktop 대표 화면, 핵심 흐름 prototype, Loading·Empty·Error·Partial data 상태와 일관된 이름을 포함해야 한다. 미확정 항목은 `Open Questions` 페이지 또는 주석으로 구분한다.

## 10. Open Questions

- Blue·Yellow·상태 tint의 정확한 token 값과 명암 대비
- typography scale, spacing, radius와 line token의 실제 값
- LP hover/focus, paused, unavailable/error의 최종 시각 표현
- portrait의 선정·출처·권리와 fallback 자산
- Review 5점 입력 component의 최종 시각·접근성 표현
- 좌석 추천안 비교와 좌석도 선택 상태의 최종 visual hierarchy
