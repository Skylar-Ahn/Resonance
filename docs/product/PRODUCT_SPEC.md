# Resonance — Product Decisions & Feature Specification

> 상태: Working baseline v1.1
> 기준일: 2026-09-15

## 1. 제품 원칙

- 모바일·태블릿·PC는 서로 다른 앱이 아니라 동일한 데이터와 정보 구조를 공유하는 하나의 반응형 웹앱/PWA다.
- 모바일은 알림 확인과 빠른 공연 정보 탐색에, PC·태블릿은 긴 아티클 열람·데이터 확인·키보드 기반 후기 작성에 특히 적합해야 한다.
- 개인적 필요에서 출발한 제품이며, MVP의 네 기능을 임의로 축소하지 않는다.
- AI의 존재 자체보다 사용자가 추천 이유와 근거를 이해하고 다시 확인할 수 있는 것이 중요하다.

## 2. 전역 정보 구조

### 2.1 1차 내비게이션 — 확정

전역 1차 메뉴는 다음 세 개뿐이다.

1. `For You`
2. `Articles`
3. `Reviews`

`Alerts`는 메뉴·목록 화면으로 존재하지 않는다. `App Home`은 1차 메뉴가 아니라 로그인 직후의 중립적 브랜드 홈이다.

### 2.2 유틸리티 내비게이션 — 확정

햄버거 메뉴는 다음 항목을 제공한다.

- `Account`
- `My Concert Taste`
- `Bookmarks`
- `Settings`

데스크톱 목업의 단독 아바타나 검색 아이콘보다 위 구조가 최신 결정이다. 전역 통합 검색은 MVP에서 제외하고 Later 후보로 둔다. My Concert Taste의 preference 검색과 Reviews 내부 탐색처럼 기능 범위가 분명한 검색은 허용한다.

### 2.3 제거된 요소 — 확정

- `All Events`: MVP에서 제거
- 별도 Alerts 메뉴·화면: 제거
- 타인 후기와 커뮤니티 기능: 제거

### 2.4 App Home과 전역 navigation — 확정

- `resonance.` logo는 App Home으로 이동한다. unsaved changes가 있으면 입력 손실 보호 정책을 먼저 적용한다.
- Mobile(`<768px`)과 Tablet(`768–1199px`)에서 primary navigation은 App Home 하단에 있고 모두 비선택이다.
- destination 선택 시 Home 콘텐츠와 같은 navigation이 위로 이동해 content screen의 sticky top navigation이 된다. Home 복귀는 반대로 동작하며 LP가 다시 나타난다.
- Desktop(`>=1200px`)은 left sidebar를 사용한다.
- top navigation 메뉴 직접 선택은 slide 없이 즉시 전환하고, 콘텐츠 swipe는 인접 primary destination으로 gesture에 따라 이동한다.
- Concert, Article, Review Detail은 global top navigation을 중첩하지 않고 compact header와 Back을 사용한다. 이전 list/feed scroll과 복원 가능한 UI state를 유지한다.

## 3. 인증과 초기 설정

### 3.1 인증

`Sign In`과 `Get Started`는 유지한다. MVP 인증 방식은 Google, Sign in with Apple, email magic link다. Resonance 자체 비밀번호를 별도로 관리하지 않는 방향이며 provider 간 계정 연결과 계정 복구 세부는 Open Question이다.

명시적 로그인 성공 직후에는 App Home으로 이동한다. 이미 로그인된 세션으로 PWA를 재실행하면 마지막 화면과 복원 가능한 상태를 되살리고, 유효하지 않거나 복원할 수 없으면 안전한 상위 화면으로 fallback한다. 보호된 deep link의 인증 후 복귀는 별도 Open Question이다.

### 3.2 Concert Taste 온보딩 — 확정

- 신규 사용자는 `Concert Taste` 설정을 완료해야 한다.
- Skip은 제공하지 않는다.
- Apple Music 연결을 온보딩의 첫 선택지로 제시하고 그 아래 `취향 직접 입력하기`를 제공한다.
- Apple Music 연결은 필수가 아니며 외부 음악 서비스 없이도 직접 입력으로 완료할 수 있다.
- 직접 입력 경로에서는 Preference를 최소 한 개 선택·입력해야 다음 단계로 진행할 수 있다.
- Apple Music 연결 시 imported taste 확인을 완료 조건으로 둘지와 어떤 데이터를 가져올지는 Open Question이다.

## 4. My Concert Taste

`Concert Taste`는 단순 관심 키워드 목록이 아니라 다음 두 영역을 포함하는 상위 사용자 모델이다.

### 4.1 Content Preferences — 확정 개념

“무엇을 보고 싶은가?”를 나타낸다.

- 작곡가
- 작품
- 연주자·지휘자
- 악기
- 앙상블·공연 형식
- 음악적 스타일 또는 관심 키워드

예: `Piazzolla`, `Sibelius`, `Violin`, `Bandoneon`, `Chamber Music`.

카테고리는 작곡가, 작품, 연주자·지휘자, 악기, 앙상블·공연 형식, 음악적 스타일·관심 키워드로 고정한다. canonical entity가 있으면 검색 결과에서 선택하고 DB에 없는 맥락적 관심사는 free-text keyword로 추가할 수 있다.

### 4.2 Experience Preferences — 확정 개념

“공연장에서 어떻게 경험하고 싶은가?”를 자연어로 받는다.

예:

> 바이올린이나 실내악은 연주자의 움직임까지 가까이서 보는 것을 좋아하지만, 오케스트라는 전체적인 음향 밸런스를 더 중요하게 생각한다.

단순 체크박스나 고정 태그만으로 조건부 취향을 표현하게 하지 않는다. 자연어 원문은 보존한다.

### 4.3 AI 해석 결과 — 확정 경계

자연어 원문은 그대로 보존한다. AI는 추천 계산을 위해 구조화된 해석을 생성할 수 있지만 결과 확인을 onboarding 필수 단계로 두지 않는다. `My Concert Taste`에서 “Resonance가 이렇게 이해했어요”와 같은 형태로 선택적으로 확인·수정할 수 있다. 해석 schema와 정확한 편집 UI는 아직 미확정이다.

### 4.4 Learned Experience Signals — 확정 개념

후기와 행동에서 관찰된 취향 신호는 사용자가 직접 입력한 Experience Preferences와 분리한다.

- 사용자에게 보이는 명시적 입력: `Experience Preferences`
- 백엔드에서 축적하는 관찰 신호: `Learned Experience Signals`

MVP에서는 학습된 프로필을 별도 설정 화면으로 노출하지 않는다. 충분한 데이터가 쌓인 뒤 Taste Insight 형태로 보여주는 것은 Later다.

## 5. For You와 알림

### 5.1 For You — 확정

- 관심 키워드와 Concert Taste 기반의 개인화 공연 피드다.
- 알림된 공연이 앱 안에서 이어지는 도착 영역이다.
- 공연 카드에서 공연 상세, 좌석 추천, 외부 예매, 후기 작성으로 이동할 수 있다.
- `NEW`는 공연 최초 수집 후 7일간 유지하며 사용자별 unseen/seen과 독립적이고 공연 정보 수정으로 기간을 다시 시작하지 않는다.
- viewport 노출만으로 seen 처리하지 않고 상세 열기·좌석 추천 확인 등 의도적 행동에서 seen 처리한다.
- seen 공연도 숨기거나 강등하지 않고 같은 피드 위치에 둔다. seen/unseen은 ranking 신호가 아니다.
- 기본 ranking은 Concert Taste 적합도를 주축으로 하고 공연일 임박도와 신규성을 보조 신호로 사용한다. 정확한 가중치는 Open Question이다.

### 5.2 알림 도착점 — 최신 확정

알림을 선택하면 해당 `Concert Detail`로 바로 이동한다. 기존 문서의 “For You 카드 또는 Concert Detail” 분기는 폐기한다.

### 5.3 알림 내용 — 확정 방향

공연 알림에는 단순 공연 발견뿐 아니라 해당 공연의 좌석 추천 정보가 포함되어야 한다. 단, 실시간 잔여석을 보장하는 표현은 사용하지 않는다.

### 5.4 전달 채널 — Open Question

모바일 중심 Push/Web Push 또는 Telegram 등의 실제 MVP 채널은 아직 확정하지 않는다.

## 6. Concert Detail

공연 상세는 다음을 연결하는 허브다.

- `Overview`
- `Seat`
- `Program`
- `Articles`
- `Reviews` — 해당 공연과 연결된 내 후기만

Overview는 공연 일시·장소·연주자·프로그램 요약, 좌석 추천 요약, 추천 이유, 외부 예매 CTA를 제공한다.

상세 화면은 compact header와 Back을 사용한다. global primary navigation을 중첩하지 않으며, Back 시 이전 list/feed scroll과 가능한 UI state를 복원한다.

## 7. Bookmarks — 확정

### 7.1 구조

`Bookmarks` 안에서 저장 대상을 탭으로 분리한다.

- `Concerts`
- `Articles`

공연 상세와 공연 카드의 저장 행동은 `Concerts`로, Article Detail의 저장 행동은 `Articles`로 연결한다.

### 7.2 추천 신호

공연 북마크는 Concert Taste 추론에 활용하는 약한 행동 신호로 기록한다. 명시적 취향 입력이나 실제 관람 후기와 같은 강도의 신호로 취급하지 않는다.

아티클 북마크를 공연 취향 신호로 사용할지는 Open Question이다.

## 8. Reviews — 확정 및 MVP 잠정

### 8.1 성격 — 확정

- 로그인한 사용자의 개인 아카이브다.
- 공개 커뮤니티가 아니다.
- 작성·조회·수정·삭제를 제공한다.
- 구조화된 평가와 자유 텍스트를 함께 저장한다.

### 8.2 MVP 평가 필드 — MVP 잠정

모든 항목은 우선 5점 척도로 둔다.

| 구분 | 필드 |
| --- | --- |
| 공연 | 공연 전체 만족도, 연주, 프로그램 |
| 좌석 경험 | 좌석 시야, 좌석 음향, 몰입감 |
| 서술 | 자유 텍스트 |

사용자가 평가 항목과 척도를 더 고민할 필요가 있다고 명시했으므로 고정 데이터 계약으로 확정하기 전 재검토한다.

### 8.3 좌석 정보 — 확정

- 구역·열·좌석 번호 입력은 선택 사항이다.
- 좌석 정보를 쓰지 않아도 후기를 저장할 수 있어야 한다.
- 좌석 정보가 있는 후기는 향후 좌석 추천 품질을 높이는 피드백 데이터로 활용할 수 있다.

편의를 위한 입력 방식 후보는 직접 입력, 좌석도 선택, 이전 Resonance 추천 불러오기다. 어떤 방식을 MVP에 넣을지는 미확정이다.

### 8.4 후기 개수와 관람 기록 — 부분 확정

한 공연에 여러 기록을 허용하는 방향이다. 동일 공연의 재관람과 다른 좌석 경험을 정확히 표현하려면 `Concert`에 후기를 바로 여러 개 붙이기보다 `Attendance` 하나당 `Review` 하나를 두는 모델이 권장된다. `Attendance` 도입은 아직 최종 확정하지 않는다.

### 8.5 MVP 제외

공연 전에 기대 곡이나 사전 감상 노트를 쓰는 기능은 MVP에서 제외한다.

## 9. Articles

- 작품·작곡가·연주자·공연 프로그램뿐 아니라 생애, 역사, 음악사, 국가·사회적 맥락, 해석과 비평을 다룬다.
- 사용자에게 원문과 근거를 다시 확인할 수 있는 출처 정보를 제공한다.
- 무료로 접근 가능한 자료를 우선 활용하고, 영어·스페인어 등 외국어 자료를 번역·요약할 수 있다.
- Article bookmark는 MVP에 포함한다.
- 생성·검수·게시 기준과 저작권 정책은 별도 확정이 필요하다.

## 10. 음악 서비스 및 미디어

### 10.1 YouTube — 폐기

YouTube 영상 임베딩과 YouTube/YouTube Music 데이터를 Resonance의 추천 입력으로 사용하는 구상은 폐기한다. 같은 작품의 서로 다른 연주·해석에 대한 사용자 선호를 이해한다는 목적은 유지하되 Resonance의 직접 입력과 앱 내 행동 데이터로 해결한다.

### 10.2 LP playback과 Apple Music — 확정 제품 정책

App Home LP는 단순한 시각 prototype이 아니라 실제 playback UI다. stylus를 LP play zone으로 이동하면 Play, LP tap/click은 Pause/Resume, stylus를 resting position으로 되돌리면 Stop한다. track 종료 시 자동 Stop하고 playback position, stylus와 노란 `resonance` label을 초기 상태로 복원한다.

재생 소스는 Apple Music / Apple Music Classical 계열로 한정하며 YouTube / YouTube Music 및 기타 음원 제공자는 사용하지 않는다. 실제 PWA 통합은 MusicKit / Apple Music API의 지원 범위, 권한, catalog mapping과 Apple Music Classical 데이터 경계를 engineering 단계에서 검증한다. 제품 차원에서 실제 재생 여부와 제공자 범위는 더 이상 Open Question이 아니다.

### 10.3 Apple identity와 Music authorization — 확정 경계

Sign in with Apple은 Resonance 계정 인증에 사용한다. 이것만으로 Apple Music 개인 데이터나 재생 권한이 생긴다고 가정하지 않는다. Apple Music 연결 단계에서 MusicKit의 별도 사용자 authorization과 consent가 필요하다.

Concert Taste seed에 사용할 Apple Music 데이터, imported/inferred taste confirm 여부와 classical/non-classical 분류 기준은 Open Question이다.

## 11. Later 범위

- 전역 통합 검색
- Learned Experience Signals를 설명하는 Taste Insight
- 후기·아티클·프로그램북·공연 상세 이미지를 조합한 개인 매거진
- 개인 후기의 선택적 공유
- 다수 사용자 후기 기반 좌석 점수와 신뢰도 모델
- 실시간 예매 재고와의 공식 연동
- 뮤지컬 좌석 평가로의 확장
