# Resonance — Decision Log & Open Questions

> 상태: v1.1
> 기준일: 2026-09-15

## 1. 결정 로그

### D-001 전역 1차 메뉴

- **결정:** `For You`, `Articles`, `Reviews`만 사용한다.
- **결과:** `Alerts` 메뉴와 독립 알림 피드는 폐기한다.

### D-002 Reviews의 성격

- **결정:** Reviews는 로그인 사용자의 개인 후기 아카이브다.
- **결과:** 타인 후기 피드, 댓글, 좋아요, 팔로우는 범위 밖이다.

### D-003 App Home

- **결정:** 명시적 로그인 성공 직후 중립적 `App Home`에 도달한다. 이미 로그인된 세션으로 PWA를 재실행하면 마지막 화면과 복원 가능한 상태를 되살린다.
- **결과:** App Home에서는 세 1차 메뉴 중 어느 것도 활성 상태가 아니다. 복원할 수 없는 세션 상태는 안전한 상위 화면으로 fallback한다.

### D-004 Concert Taste 온보딩

- **결정:** 필수이며 전체 Skip은 없다. Apple Music 연결을 첫 선택지로, `취향 직접 입력하기`를 대안으로 제공한다.
- **결과:** Apple Music 없이도 완료할 수 있으며 직접 입력 경로에서는 Preference 최소 1개가 필요하다.

### D-005 Concert Taste의 구성

- **결정:** “무엇을 보고 싶은가”와 “어떻게 경험하고 싶은가”를 모두 포함한다.
- **결과:** Content Preferences는 고정 category 안의 canonical entity 검색·선택과 free-text keyword를 함께 제공한다. Experience Preferences는 자연어 원문을 보존하고 AI 해석 확인은 onboarding 필수 단계로 두지 않는다.

### D-006 관찰된 취향 신호

- **결정:** 사용자가 직접 쓴 취향과 Review·행동에서 추론한 신호를 분리한다.
- **결과:** MVP에서 Learned Experience Signals는 내부 데이터이며 별도 설정으로 노출하지 않는다.

### D-007 유틸리티 메뉴

- **결정:** 햄버거 메뉴에 `Account`, `My Concert Taste`, `Bookmarks`, `Settings`를 둔다.

### D-008 All Events

- **결정:** MVP에서 제거한다.

### D-009 알림 도착점

- **결정:** 알림은 해당 `Concert Detail`로 deep link한다.
- **결과:** 기존 IA/User Flow의 두 후보 분기는 폐기한다.

### D-010 알림의 좌석 정보

- **결정:** 공연 알림에 좌석 추천을 포함하는 방향이다.
- **경계:** 실시간 잔여 좌석을 보장하지 않는다.

### D-011 좌석 추천 단위

- **결정:** 지원 공연장에서는 개별 좌석 번호 또는 번호 범위까지 추천한다.
- **경계:** 실제 구매 가능 여부는 외부 예매처에서 확인한다.

### D-012 복수 추천안

- **결정:** 공연·취향·상황에 따라 복수안을 제공하고 개수를 고정하지 않는다.
- **결과:** `Best value / Center view / Immersive`는 고정 유형이 아니다.

### D-013 추천 기준 입력

- **결정:** 기본 추천을 먼저 제공하고 사용자가 필요할 때 Current Need를 조정한다.

### D-014 Bookmarks

- **결정:** 공연과 아티클을 모두 저장하며 `Concerts`와 `Articles` 탭으로 분리한다.
- **결과:** 공연 북마크는 약한 Concert Taste 신호다.

### D-015 Review의 형식

- **결정:** 구조화된 평가와 자유 텍스트를 함께 제공한다.
- **MVP 잠정:** 공연 전체 만족도, 연주, 프로그램, 좌석 시야, 좌석 음향, 몰입감을 각각 5점으로 받는다.

### D-016 Review 좌석 정보

- **결정:** 입력을 쉽게 만들되 선택 항목으로 둔다.
- **결과:** 좌석 번호가 없어도 후기를 저장할 수 있다.

### D-017 여러 후기

- **결정:** 한 공연과 관련된 여러 기록을 허용하는 방향이다.
- **미확정:** `Attendance 1 : Review 1` 모델의 최종 채택.

### D-018 공연 전 메모

- **결정:** MVP에서 제외한다.

### D-019 좌석 추천 근거

- **결정:** 일반적인 음향학 추론보다 실제 관객 후기의 좌석 경험을 중요한 근거로 사용한다.
- **결과:** 후기 텍스트를 aspect별로 구조화하고 공연 맥락과 결합하는 파이프라인이 필요하다.

### D-020 추천 의도 차이

- **결정:** 작품 중심 추천과 연주자 중심 추천은 좌석 가중치가 달라질 수 있다.
- **결과:** 작품 중심은 전체 균형·공간감, 연주자 중심은 가시성·근접감·주법 관찰을 상대적으로 중시한다.

### D-021 YouTube

- **결정:** YouTube 임베딩과 YouTube/YouTube Music 추천 데이터 활용은 폐기한다.
- **보존 목표:** 같은 작품의 다른 연주자·해석에 대한 선호는 first-party 데이터로 파악한다.

### D-022 공연 데이터

- **결정된 방향:** KOPIS를 1차 구조화 소스로 사용하고, 조기 발견은 NOL 공개 오픈예정·공식 공지 등을 후보로 실험한다.
- **경계:** NOL의 로그인·예매·좌석·주문 영역에 자동 접근하지 않는다.

### D-023 상세 이미지 추출

- **결정된 방향:** 낮은 물량에서는 Vision + Structured Output을 기본선으로 삼고 검증 후 저장한다. OCR은 비교·fallback 후보다.

### D-024 Canonical DB

- **결정된 방향:** raw와 normalized provenance를 함께 저장하며 canonical entity와 alias cache를 운영한다.

### D-025 YouTube 폐기 후 음악 재생

- **결정:** LP는 실제 playback UI이며 재생 소스는 Apple Music / Apple Music Classical 계열로 한정한다.
- **결과:** YouTube / YouTube Music과 기타 음원 제공자는 사용하지 않는다.
- **미확정:** MusicKit의 실제 PWA 지원 범위, 권한, catalog mapping과 Apple Music Classical 데이터 경계.

### D-026 디자인 언어

- **결정:** 흰 배경, 검정 구조, 파랑·노랑 포인트, LP 중심의 절제된 neo-brutalism을 유지한다.

### D-027 LP 중앙 상태

- **결정:** Idle/Stop은 노란 `resonance` 레이블이고 Playing/Paused는 흑백 작곡가·연주자 이미지를 유지한다. track 종료 후 노란 레이블로 복귀한다.
- **목적:** Splash와 App Home의 서로 다른 인상을 하나의 상태 시스템으로 연결한다.

## 2. 기존 IA Open Questions 해결표

2026-09-15 점검: 아래는 이전 버전 질문의 해결 이력이다. 현행 [IA](../product/IA.md) v0.4와 [User Flow](../product/USER_FLOW.md) v0.3에는 온보딩, Alerts, All Events, 북마크, 좌석 단위·복수안·Current Need, YouTube 폐기와 D-032~039가 반영되었다. 예전 질문이 모두 현행에도 남아 있다는 의미가 아니다. 상세 감사 결과와 충돌은 6~7절을 참조한다.

| 기존 번호·주제 | 최신 상태 |
| --- | --- |
| 관심 키워드·좌석 취향을 온보딩에 포함하는가 | 해결: Concert Taste 필수, 전체 Skip 없음, 직접 입력은 최소 1개 |
| 사용자 아바타가 여는 구조 | 대체: 햄버거 메뉴의 Account / My Concert Taste / Bookmarks / Settings |
| All Events 옵션 | 해결: MVP 제거 |
| 알림 도착점 | 해결: Concert Detail |
| 공연·아티클 북마크 | 해결: 둘 다 포함, 탭 분리 |
| 공연 저장과 추천의 관계 | 해결: 공연 bookmark는 약한 행동 신호 |
| 좌석 추천 단위 | 해결: 좌석 번호까지 |
| 단일안 또는 복수안 | 해결: 상황별 복수안 |
| 추천 후보 개수 | 부분 해결: 고정하지 않음 |
| 현재 관람 목적 입력 | 해결: 기본 추천 후 필요 시 조정 |
| 실시간 잔여석 | 해결: MVP 제외, 공식 예매처에서 확인 |
| 후기 필드 | 부분 해결: 6개 5점 항목을 MVP 잠정 채택 + 자유 텍스트 |
| 후기 좌석 번호 | 해결: 선택 입력 |
| 한 공연의 여러 후기 | 부분 해결: 허용 방향, Attendance 모델 미확정 |
| 공연 전 후기·메모 | 해결: MVP 제외 |
| LP 중앙 표현 | 해결: idle 노란 레이블, playing 흑백 인물 |
| YouTube 사용 | 해결: 폐기 |
| 인증 방식 | 해결: Google, Sign in with Apple, email magic link |
| 로그인·세션 재진입 | 해결: 명시적 로그인은 App Home, 로그인 세션 재실행은 마지막 화면 복원 |
| Content Preference 입력 | 해결: 고정 category, canonical 검색·선택, free-text keyword 허용 |
| Experience Preference AI 확인 | 해결: onboarding 필수 아님, My Concert Taste에서 선택 확인 |
| Apple Music onboarding | 해결: 연결 우선, 직접 입력 대안, 전체 Skip 없음 |
| LP 실제 재생과 제공자 | 해결: 실제 playback, Apple Music 계열 한정 |
| logo와 detail navigation | 해결: Home 이동, compact header·Back과 가능한 상태 복원 |
| 전역 검색 | 해결: MVP 제외, 기능 내부 검색 허용, Later 후보 |
| For You 상태·정렬 | 해결: NEW 7일, 의도적 seen 전환, same feed 유지, Taste 중심 ranking |
| breakpoint·Tablet navigation | 해결: `<768 / 768–1199 / >=1200`, Mobile/Tablet bottom→top, Desktop sidebar |

## 3. Open Questions

### 3.1 이번 동기화에서 해결된 기존 질문

| 기존 주제 | 해결 Decision |
| --- | --- |
| 인증 방식 | D-036 |
| 명시적 로그인과 PWA 재실행 도착점 | D-003·D-036 |
| Content Preference category·검색·직접 추가 | D-005·D-037 |
| Experience Preference AI 확인 필수 여부 | D-005·D-037 |
| Apple Music onboarding 포함 여부 | D-004·D-038 |
| LP 실제 재생과 음악 제공자 | D-025·D-039 |
| logo와 detail navigation | D-034 |
| 전역 검색 MVP 포함 | D-035 |
| For You 정렬·NEW·seen 처리 | D-032 |
| breakpoint와 Mobile/Tablet navigation | D-033 |

### 3.2 현재 남은 질문

#### 계정·온보딩·음악

- **OQ-001:** provider 간 계정 연결, 계정 복구와 email 변경 정책은 무엇인가?
- **OQ-002:** Splash의 표시 시간·상태별 도착점과 보호된 deep link의 인증 후 복귀를 어떻게 처리하는가?
- **OQ-003:** Apple Music imported/inferred taste 중 최소 한 개를 사용자가 confirm해야 onboarding이 완료되는가?
- **OQ-004:** recently played, favorites, library, Replay 등 어떤 Apple Music 데이터를 Concert Taste seed로 사용하는가?
- **OQ-005:** classical/non-classical 데이터를 어떤 기준으로 필터링·분류하는가?
- **OQ-006:** MusicKit의 PWA 지원 범위, 권한·catalog mapping·background 전환·오류 처리를 어떻게 구현하는가?

#### Navigation과 For You

- **OQ-007:** unsaved changes 보호를 확인, draft 또는 다른 수단 중 무엇으로 구현하는가?
- **OQ-008:** list/feed scroll과 복합 UI state를 어느 기간·범위까지 복원하는가?
- **OQ-009:** Desktop left sidebar를 인증·utility 화면에서 유지할 정확한 범위는 무엇인가?
- **OQ-010:** Concert Taste 적합도, 공연일 임박도와 신규성의 정확한 feature weight·score formula는 무엇인가?
- **OQ-011:** 실제 MVP 알림 채널은 Web Push, Telegram 또는 다른 방식인가?
- **OQ-012:** 알림 읽음 상태를 별도로 보존하는가?
- **OQ-013:** 공연 취소·일시·출연자·프로그램 변경을 어떤 추가 알림으로 전달하는가?

#### 좌석 추천

- **OQ-014:** MVP에서 우선 지원할 공연장·홀의 정확한 목록과 순서는 무엇인가?
- **OQ-015:** 각 홀의 좌석도와 좌표 데이터는 어떤 허용된 소스에서 구축하는가?
- **OQ-016:** 공연별 무대·판매 설정을 어느 수준까지 모델링하는가?
- **OQ-017:** 외부 관객 후기의 허용된 수집·요약·인용 방식은 무엇인가?
- **OQ-018:** 후기 작성자 전문성, 최신성, 좌석 식별 정확도를 어떻게 가중하는가?
- **OQ-019:** 추천안 2~4개 권장 범위를 제품 규칙으로 확정하는가?
- **OQ-020:** 추천 score, confidence, evidence coverage를 어디까지 노출하는가?
- **OQ-021:** 추천 생성 실패·근거 부족·빈 결과에서 어떤 대체 행동을 제공하는가?

#### Reviews

- **OQ-022:** 여섯 평가 필드와 전 항목 5점 척도를 최종 확정하는가?
- **OQ-023:** 좌석 정보가 없을 때 좌석 시야·음향·몰입감 입력을 숨길지 선택 입력으로 둘지?
- **OQ-024:** `Attendance 1 : Review 1` 모델을 채택하는가?
- **OQ-025:** Review의 최소 필수 필드는 무엇인가?
- **OQ-026:** 임시 저장, 작성 취소 확인과 삭제 복구를 제공하는가?
- **OQ-027:** 목록의 검색·정렬·필터는 무엇인가?

#### Articles와 콘텐츠 정책

- **OQ-028:** 아티클의 생성·검수·게시 책임과 승인 단계는 무엇인가?
- **OQ-029:** 원문 링크, 번역·요약, 인용량, 이미지 사용에 관한 콘텐츠 정책은 무엇인가?
- **OQ-030:** 공연 상세 이미지와 프로그램북을 개인 매거진에 재사용할 수 있는 권리 범위는 무엇인가?
- **OQ-031:** Article bookmark 행동을 추천 신호로 사용할 것인가?

#### 데이터와 아키텍처

- **OQ-032:** KOPIS 지연이 좌석 기회에 주는 영향을 어떤 기간·표본으로 실험할 것인가?
- **OQ-033:** Entity resolver의 rule/fuzzy/LLM 조합과 human review 기준은 무엇인가?
- **OQ-034:** Next.js, FastAPI, Supabase/PostgreSQL 제안을 최종 스택으로 확정하는가? D-029에 따라 재논의한다.
- **OQ-035:** background queue, scheduler, object storage, 배포·모니터링 서비스를 무엇으로 정하는가?
- **OQ-036:** 사용자 행동 로그의 동의, 보존 기간과 삭제 정책은 무엇인가?

#### 접근성

- **OQ-037:** 별점·좌석도·LP interaction의 keyboard 및 screen reader 조작을 어떻게 제공하는가?
- **OQ-038:** reduced motion 환경에서 navigation transition과 LP motion을 어떻게 표현하는가?

## 4. 구현 전 우선 결정 순서

아래 순서는 실제 MVP 구현을 위한 기존 목록이다. 모의 데이터만 사용하는 [P-001](../tasks/P-001.md)의 차단 의존성은 해당 작업 문서에서 별도로 판별한다.

1. MVP 지원 공연장과 좌석 데이터 확보 방식
2. Review 필수 필드와 Attendance 모델
3. 계정 연결·복구와 Concert Taste 저장 스키마
4. 실제 관객 후기 데이터의 허용된 출처와 처리 정책
5. 최종 기술 스택과 배포 구조
6. 알림 채널
7. MusicKit 권한·catalog·재생 오류 처리
8. 핵심 accessibility interaction과 reduced motion

## 5. 문서 갱신 규칙

- Open Question이 해결되면 OQ ID를 재사용하지 않고 해결표에서 Decision ID로 연결한 뒤 현재 질문 목록에서는 제거한다.
- MVP 잠정 항목이 확정되면 데이터 스키마와 User Flow를 동시에 갱신한다.
- Figma 목업이 기능 결정을 앞서가면 목업을 수정하거나 Open Question 주석을 붙인다.
- 추천 로직이 바뀌면 입력 신호, 점수 규칙, 설명 문구, 평가 지표를 함께 갱신한다.

## 6. 2026-09-15 문서 기반 점검

### D-028 PWA 개발 확정

- **상태:** 확정
- **근거:** 이번 사용자 지시: PWA 개발은 확정이다.
- **결정:** 하나의 반응형 PWA를 개발한다.
- **경계:** 설치 유도, 오프라인 기능, 업데이트 UX, 알림 채널의 상세 범위는 자동 확정되지 않는다. [PWA 범위](../engineering/PWA_SCOPE.md) 참조.

### D-029 상세 기술 스택 재논의

- **상태:** 확정된 절차, 상세 스택은 미정
- **근거:** 이번 사용자 지시: 상세 기술 스택은 재논의 예정이며 기존 후보를 최종 채택하지 않는다.
- **결정:** [데이터·아키텍처](../data/DATA_AND_ARCHITECTURE.md) 9~10절의 기술 방향·후보를 보존하고 채택으로 해석하지 않는다.
- **경계:** 이번 Python 문서 검사와 GitHub Actions는 문서 자동화에만 적용한다. 앱 프레임워크·API·DB·배포 결정을 대신하지 않는다.

### D-030 P-001 프로토타입 작업 범위

- **상태:** 확정된 작업 범위, 프로토타입 구현·검증 완료
- **근거:** 이번 사용자 지시의 P-001 정의.
- **결정:** 온보딩 완료 데모 사용자의 App Home → For You → Concert Detail → Seat, 복수 추천안·좌석 번호/범위·위치 강조·선택적 Current Need 조정을 모의 추천으로 검증한다.
- **경계:** 전체 MVP를 이 범위로 축소하지 않는다. [P-001](../tasks/P-001.md)의 임시 선택은 제품 정책과 별개다.

| 점검 대상 | 근거와 판정 | 처리 |
| --- | --- | --- |
| 숫자 접두사 문서 참조 | 인덱스의 01/02/03/04/06/07 파일명은 실제 경로와 다름 | 실제 상대 링크로 수정; 파일 이동 없음 |
| 과거 구조 제안과 Addendum | 협업 2절 트리의 파일 대부분은 없고 IA·Flow는 이미 통합됨 | 제안 트리·역사적 원본명으로 명시; 현행 입력은 통합 문서로 연결 |
| 문서 우선순위 | 최신 명시적 사용자 결정이 최우선이며 확정 Decision과 IA/Flow를 함께 갱신 | DR-001 Accepted; 이번 Checkpoint 범위에 적용 |
| 해결된 질문 | 현행 IA 14절·Flow 28절과 D-001~D-027 해결표 대조 | 완료된 질문을 재개하지 않음 |
| 부분 해결된 질문 | 추천 개수 비고정과 권장 2~4개 채택 여부, 실제 LP와 MusicKit 구현, 후기 복수 기록과 Attendance 모델 | 제품 결정과 구현 세부를 분리해 OQ-006·019·024 유지 |
| 재진입 도착점 | 명시적 로그인은 App Home, 로그인 세션 PWA 재실행은 마지막 화면 복원 | D-003·D-036, DR-002 Accepted in part; 보호된 deep link는 OQ-002 |
| 후기 완료 도착점 | UF-12 저장·UF-13 수정은 Review Detail, Flow 현재 질문 33은 저장·수정·삭제를 모두 미정으로 둠 | DR-003 Proposed; 이번 Checkpoint에서 결정하지 않음 |
| 작성 취소와 입력 손실 | 입력 손실 보호 목표는 유지하고 확인·draft 수단은 미정 | DR-004 Proposed, OQ-007·026 |
| Splash 도착점 | UF-01의 일반 진입과 Splash 이후 상태별 전환 조건은 구체성이 다름 | DR-002에 경계 포함; 타이밍·인증 후 딥링크 복귀는 미결 유지 |

### D-031 P-001 프로토타입 기술 구성과 가역적 UI 선택 승인

- **상태:** P-001에 한해 확정 (2026-09-15 사용자 지시)
- **근거:** 사용자가 추천한 최소 프런트엔드 구성으로 P-001을 구현하고, 가역적인 UI 선택은 데모 가정으로 기록해 진행하도록 승인했다.
- **결정:** Node.js 24 LTS, npm, Next.js App Router, React, TypeScript, CSS Modules·CSS 토큰, React 상태, Playwright와 Vitest를 프로토타입에 사용한다. 정확한 설치 버전은 루트 package-lock.json으로 재현한다.
- **경계:** D-029의 최종 제품 스택 재논의는 유지한다. API·DB·인증·배포·서비스 워커·알림 도구와 DR-001~004의 제품 정책은 채택하지 않는다.
- **영향:** [P-001](../tasks/P-001.md)의 T-01 차단을 해제한다. UI 임시 가정과 검증 결과는 같은 작업 문서에 기록한다.

### D-032 For You의 NEW·seen과 기본 ranking

- **상태:** 확정
- **결정:** `NEW`는 공연 최초 수집 후 7일간 유지하며 사용자별 unseen/seen과 독립적이다. 공연 정보 수정으로 NEW 기간을 다시 시작하지 않는다. viewport 노출은 seen으로 만들지 않고 상세 열기·좌석 추천 확인 등 의도적 행동에서 seen으로 전환한다.
- **결과:** seen 공연도 숨기거나 강등하지 않고 같은 피드 위치에 둔다. 기본 ranking은 Concert Taste 적합도를 주축으로 하고 공연일 임박도와 신규성을 보조 신호로 사용한다.
- **미확정:** 정확한 feature weight와 score formula는 OQ-010.

### D-033 Responsive breakpoint와 primary navigation

- **상태:** 확정
- **결정:** Mobile `<768px`, Tablet `768–1199px`, Desktop `>=1200px`를 사용한다. Mobile/Tablet App Home은 bottom navigation, primary content는 같은 component의 sticky top navigation, Desktop은 left sidebar다.
- **결과:** Home↔content는 vertical transition, 직접 menu 선택은 즉시 전환, 콘텐츠 swipe는 인접 menu로 gesture에 따라 slide한다. Desktop에는 swipe를 강제하지 않는다.

### D-034 Logo와 detail navigation

- **상태:** 확정
- **결정:** `resonance.` logo는 App Home으로 이동한다. Concert/Article/Review Detail은 global top navigation을 중첩하지 않고 compact header와 Back을 사용한다.
- **결과:** 논리적 parent context와 이전 list/feed scroll 및 가능한 UI state를 복원한다. unsaved changes 보호가 필요한 화면에서는 보호 정책이 우선한다.

### D-035 Global Search

- **상태:** 확정
- **결정:** 전역 통합 검색은 MVP에서 제외하고 Later 후보로 둔다.
- **경계:** My Concert Taste preference 검색과 Reviews 내부 탐색처럼 기능 내부 검색은 허용한다.

### D-036 MVP 인증과 재진입

- **상태:** 확정
- **결정:** MVP 인증은 Google, Sign in with Apple, email magic link를 사용한다. 명시적 로그인 성공 직후 App Home으로 이동하고, 로그인 세션으로 PWA를 재실행하면 마지막 화면을 복원한다.
- **결과:** 복원할 수 없는 상태는 안전한 상위 화면으로 fallback한다.
- **미확정:** 계정 연결·복구는 OQ-001, 보호된 deep link 인증 후 복귀는 OQ-002.

### D-037 Concert Taste 입력과 AI 해석

- **상태:** 확정
- **결정:** Content Preference category는 Composer, Work, Performer/Conductor, Instrument, Ensemble/Performance Type, Musical Style/Interest Keyword로 고정한다. canonical entity는 검색·선택하며 DB에 없는 관심사는 free-text keyword로 허용한다. Experience Preference 자연어 원문은 보존한다.
- **결과:** AI 구조화 해석은 가능하지만 onboarding 확인 필수 단계가 아니다. My Concert Taste에서 선택적으로 확인·수정한다.

### D-038 Apple Music onboarding과 authorization 경계

- **상태:** 확정
- **결정:** Apple Music 연결을 onboarding의 첫 선택지로 제시하고 `취향 직접 입력하기`를 대안으로 둔다. 전체 Skip은 없고 직접 입력 경로는 Preference 최소 1개가 필요하다.
- **경계:** Sign in with Apple은 identity 인증이며 Apple Music 데이터·재생 권한은 별도 MusicKit authorization과 consent가 필요하다.
- **미확정:** imported taste confirm은 OQ-003, seed 데이터는 OQ-004, classical 분류는 OQ-005.

### D-039 LP playback interaction

- **상태:** 확정
- **결정:** stylus를 play zone에 옮기면 Play, LP tap/click은 Pause/Resume, stylus를 resting position으로 돌리면 Stop한다. track 종료 시 자동 Stop한다.
- **결과:** Stop은 playback position, stylus와 노란 `resonance` label을 초기 상태로 복원한다. Mobile/Tablet은 touch-drag, Desktop은 mouse/trackpad drag를 사용한다.
- **경계:** keyboard·screen-reader 대체 조작은 OQ-037, MusicKit 구현은 OQ-006.

## 7. Decision Requests

다음 요청은 [기존 협업 형식](../process/WORKFLOW_AND_AGENT_HANDOFF.md)으로 기록한다. `Accepted`는 이번 동기화에 반영한 결정, `Accepted in part`는 결정된 부분과 남은 OQ를 분리한 상태, `Proposed`는 아직 채택되지 않은 상태다.

### DR-001 문서 우선순위와 결정 기록 위치

- 상태: Accepted (2026-09-15)
- 배경: 인덱스 2절, IA 1절, 협업 8·10절의 우선순위가 서로 다르다. 협업은 스택을 ADR로 확정하도록 서술하지만 현재 지시는 동등한 결정 로그 신설을 금한다.
- 결정: 최신 명시적 사용자 지시를 최우선으로 하고, 근거와 적용 범위가 확인된 확정 Decision을 IA/Flow 및 관련 분야 문서에 함께 반영한다. 기술 결정도 이 로그에 기록하고 상세 설명은 분야 문서로 연결한다.
- 제품 영향: 충돌이 없는 확정 범위는 진행하고, 충돌 부분의 제품 정책은 결정을 기다린다.
- 디자인 영향: 목업이 범위나 정책을 대신 확정하지 않는다.
- 데이터·개발 영향: 문서의 나이·번호만으로 스키마나 스택을 고정하지 않는다.
- 영향받는 문서: [인덱스](../00_README.md), [IA](../product/IA.md), [협업](../process/WORKFLOW_AND_AGENT_HANDOFF.md), 이 로그.

### DR-002 기존 사용자 진입과 복원 정책

- 상태: Accepted in part (2026-09-15)
- 배경: 명시적 로그인 성공과 이미 로그인된 PWA 재실행은 서로 다른 진입이다.
- 결정: 명시적 로그인 성공 직후는 App Home, 로그인 세션 재실행은 마지막 화면 복원, 복원 불가능하면 안전한 상위 화면 fallback을 사용한다.
- 남은 질문: Splash의 정확한 분기와 보호된 deep link 인증 후 복귀는 OQ-002로 유지한다.
- 제품 영향: 로그인과 재진입 도착점에 영향을 준다. P-001은 이미 로그인한 데모 사용자의 App Home에서 시작하므로 인증 정책 구현에 의존하지 않는다.
- 디자인 영향: Splash·로그인 완료·복원 화면 분기 필요.
- 데이터·개발 영향: 세션 상태·복귀 URL 저장과 검증은 실제 인증 작업에서 결정한다.
- 영향받는 문서: [IA](../product/IA.md) 5·10·12절, [Flow](../product/USER_FLOW.md) UF-01·26절, [PWA 범위](../engineering/PWA_SCOPE.md), D-003·D-036.

### DR-003 후기 저장·수정·삭제 완료 도착점

- 상태: Proposed
- 배경: UF-12와 UF-13은 저장·수정 후 Review Detail로 이동하지만 기존 Flow Q37은 이 도착점도 미정으로 포함했다. 삭제 도착점은 UF-14에서도 미정이다.
- 결정이 필요한 질문: 현재 질문 33을 삭제 완료 도착점만 남기도록 좁힐지, 저장·수정 도착점도 재검토할지?
- 선택지: 저장·수정은 본문 유지, 삭제만 미결 / 세 동작의 도착점을 모두 재논의.
- 권장안과 이유: 본문에 명시된 저장·수정 흐름을 보존하고 삭제만 미결로 둔다. 다만 명시적 결정 확인 전에는 질문을 삭제하지 않는다.
- 제품 영향: 후기 탐색 연속성에 영향; P-001 범위 밖.
- 디자인 영향: 성공 후 상세 화면과 삭제 후 목록 상태 구분.
- 데이터·개발 영향: 성공 시 라우팅·캐시 갱신 테스트에 영향.
- 영향받는 문서: [Flow](../product/USER_FLOW.md) UF-12~14·현재 질문 33, 이 로그.

### DR-004 입력 손실 보호와 취소 확인의 경계

- 상태: Proposed
- 배경: 공통 상태는 이탈 전 입력 손실 방지를 요구하지만 후기 작성 취소 확인과 임시 저장은 Open Question이다.
- 결정이 필요한 질문: 입력 손실 보호의 최소 요구와 이를 구현할 확인창·임시 저장의 범위는 무엇인가?
- 선택지: 보호 목표를 유지하고 수단을 후속 확정 / 후기 작성에서 취소 확인을 필수로 확정.
- 권장안과 이유: 보호 목표와 수단을 구분하고 임시 저장을 자동 추가하지 않는다.
- 제품 영향: 후기·Taste 편집 정책에 영향; P-001 Current Need의 임시 상태는 작업 문서에 한정한다.
- 디자인 영향: 이탈·취소·오류 시 입력 보존 상태 정의 필요.
- 데이터·개발 영향: 서버 초안 저장과 보존 기간은 확정 전 구현하지 않는다.
- 영향받는 문서: [IA](../product/IA.md) 12.2절 질문 8·28, [Flow](../product/USER_FLOW.md) 23절·현재 질문 30, OQ-007·026.
