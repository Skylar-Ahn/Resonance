# Resonance — Design Language & Interaction Specification

> 상태: Confirmed direction + unresolved implementation details v1.0  
> 기준일: 2026-09-14

## 1. 디자인 목표

Resonance의 시각 언어는 클래식 음악을 보수적인 장식으로 재현하기보다, LP와 에디토리얼 그래픽을 이용한 절제된 neo-brutalism으로 표현한다.

핵심 인상:

- 미니멀하고 고대비
- 충분한 흰 여백
- 단단한 검정 타이포그래피와 선
- 선명한 파랑과 상징적인 노랑
- LP라는 일관된 브랜드 오브젝트
- 아티클과 개인 매거진으로 확장 가능한 에디토리얼 감각

## 2. 색상 역할 — 확정

| 색 | 역할 |
| --- | --- |
| White | 기본 배경과 여백 |
| Black | LP, 핵심 타이포그래피, 구조선 |
| Blue | 디지털 제품성, 활성 상태, CTA, glow |
| Yellow | 클래식 음악의 상징성, LP 레이블, 브랜드 기억점 |

파랑만 브랜드색으로 취급하지 않는다. 노랑은 전통적인 클래식 음반 커버의 인상을 연결하는 핵심 정체성 색이다.

## 3. Splash와 App Home의 관계

두 화면의 디자인 논리 중 하나를 버리지 않는다. 동일한 LP 오브젝트가 상태에 따라 역할을 바꾸는 시스템으로 통합한다.

### 3.1 Splash / idle state — 확정

- 화면 구성은 최대한 간결하게 유지한다.
- LP 한 장이 중심 오브젝트다.
- LP 중앙은 노란 레이블이다.
- 레이블에는 `resonance`가 표시된다.
- 작곡가 사진이나 여러 카드·기능 설명을 추가하지 않는다.

의미: 브랜드, 클래식, 아직 재생되지 않은 잠재 상태.

### 3.2 App Home / playing state — 확정된 시각 방향

- 기본 상태에서는 노란 LP 레이블을 유지한다.
- 사용자가 바늘을 LP 위에 올려 재생 상태가 되면 중앙이 흑백 작곡가 또는 연주자 사진으로 전환된다.
- LP 회전과 blue glow 강화로 재생 상태를 표현할 수 있다.
- playing 상태에서도 얇은 yellow ring이나 center dot 등 노란 흔적을 남겨 Splash와의 연속성을 유지하는 방향이 권장된다.

실제 음원 재생 제공자와 재생 권한은 미확정이므로 시각 프로토타입의 interaction과 제품의 음악 재생 기능을 동일시하지 않는다.

## 4. LP 상태 모델

| 상태 | 중앙 | 바늘 | 움직임 | 색 강조 |
| --- | --- | --- | --- | --- |
| Idle | 노란 `resonance` 레이블 | LP 밖 또는 준비 상태 | 정지 | Yellow 중심 |
| Hover/Focus | 노란 레이블 | 접근 상태 | 미세 반응 | Blue glow 증가 가능 |
| Playing | 흑백 작곡가·연주자 이미지 | LP 위 | LP 회전 | Blue 강화 + Yellow 잔존 |
| Paused | 마지막 콘텐츠 이미지 또는 레이블 | 정지 위치 | 회전 정지 | 낮은 glow |
| Error/Unavailable | 임의 이미지 생성 금지 | 안전한 기본 상태 | 정지 | 기본 대비 |

Idle과 Playing은 방향이 확정되었으나 Hover, Paused, Error의 정확한 표현은 interaction spec에서 최종 확정한다.

## 5. 화면별 시각 원칙

### 5.1 App Home

- LP와 브랜드 메시지가 주인공이다.
- 정보 카드나 목록을 억지로 추가하지 않는다.
- `For You`, `Articles`, `Reviews` 어디도 활성 상태로 표시하지 않는다.
- 햄버거 메뉴를 유틸리티 진입점으로 사용한다.

### 5.2 For You

- `For You`라는 큰 중복 제목과 `All Events` 컨트롤을 제거한다.
- 날짜, 공연명, 장소·시간, 좌석 추천 요약, 추천 이유를 빠르게 훑을 수 있어야 한다.
- 추천 CTA는 공연 정보보다 시각적으로 우세하지 않게 한다.

### 5.3 Concert Detail

- 공연 정보와 하위 탭의 계층을 명확히 한다.
- Seat는 추천안과 좌석도 시각화를 함께 제공한다.
- 실시간 판매 좌석도처럼 보이게 하지 않는다.
- 추천 이유와 잔여석 미확인 경계를 가까이 배치한다.

### 5.4 Articles

- 장문 읽기에 적합한 줄 길이·행간·문단 간격을 사용한다.
- 대표 비주얼은 본문을 방해하지 않는 에디토리얼 요소로 사용한다.
- 출처와 관련 공연 연결을 숨기지 않는다.

### 5.5 Reviews

- 평점 입력과 자유 텍스트를 명확히 분리한다.
- 개인 기록의 차분한 아카이브 느낌을 유지한다.
- 타인 프로필, 좋아요 수, 소셜 반응처럼 커뮤니티로 오해할 요소를 넣지 않는다.

## 6. 반응형 원칙 — 확정

- 정보 구조와 기능 이름은 모든 기기에서 동일하다.
- fixed pixel 좌표나 absolute positioning을 primary layout으로 사용하지 않는다.
- breakpoint 변화 시 단순 축소가 아니라 내비게이션, 열 수, 콘텐츠 우선순위, CTA 위치를 명시적으로 재배치한다.
- 작성 중 후기, 현재 공연, 선택한 추천안, 스크롤 맥락이 화면 크기 변화로 사라지지 않아야 한다.

### 현재 확인된 내비게이션 표현

| 화면 | 전역 내비게이션 방향 |
| --- | --- |
| Mobile | 콘텐츠 상단의 간결한 가로 메뉴 |
| Desktop | 좌측 사이드 내비게이션 |
| Tablet | 미확정. 콘텐츠 폭과 입력 작업을 기준으로 결정 |

과거 제안된 `<768 / 768–1199 / ≥1200` 구간은 예시일 뿐 확정 breakpoint가 아니다.

## 7. 컴포넌트 원칙

- Figma에서는 Auto Layout과 constraints를 사용한다.
- 반복 요소는 component와 variant로 만든다.
- 최소 variant 후보: default, active, hover/focus, loading, empty, error, disabled.
- 색상, 타이포그래피, 간격, 모서리, 선 굵기는 token으로 관리한다.
- 동일한 콘텐츠가 모바일·태블릿·데스크톱에서 별도 복제품이 되지 않도록 한다.

## 8. Figma와 Markdown의 역할

| 도구 | source of truth |
| --- | --- |
| Markdown | 제품 범위, IA, User Flow, 상태 규칙, 반응형 규칙, 데이터·추천 정책 |
| Figma | 화면 구성, 컴포넌트, variant, Auto Layout, 주요 breakpoint, 프로토타입 |
| 목업 이미지 | 시각적 의도와 분위기 |

Figma가 문서에 없는 기능을 생성하면 확정 기능으로 받아들이지 않는다. 문서와 목업이 충돌하면 IA/User Flow와 최신 제품 결정을 우선한다.

## 9. Figma 산출물 요구

- 편집 가능한 native layer
- component 및 variant
- Auto Layout
- 모바일·태블릿·데스크톱 대표 화면
- 핵심 흐름 prototype
- Loading, Empty, Error, Partial data 상태
- `Open Questions` 페이지 또는 주석
- 화면 이름과 컴포넌트 이름의 일관성

## 10. 남은 디자인 결정

- 실제 breakpoint 수치와 태블릿 내비게이션
- App Home LP가 실제 음악을 재생하는지, 시각적 인터랙션만 제공하는지
- LP hover/focus, pause, 오류 상태
- 모바일 전역 메뉴와 햄버거의 고정·스크롤 동작
- 상세 화면에서 상위 전역 메뉴의 active 처리
- 좌석도 확대·이동·선택 interaction
- 추천안 비교 방식
- Review의 5점 입력 컴포넌트와 접근성 표현
- Blue·Yellow의 정확한 token 값과 명암 대비

