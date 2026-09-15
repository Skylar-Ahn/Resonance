# 화면별 Reference Map

> 점검일: 2026-09-15
> 기준: 저장소 실제 파일과 Git 추적 목록, 로컬 이미지의 육안 확인

[Design System](DESIGN_SYSTEM.md), [Responsive](RESPONSIVE.md), [Interaction](INTERACTION.md)과 [IA](../product/IA.md)를 화면 구조·시각·상호작용의 기준으로 사용한다. 아래 자산은 시각 참고이며 제품 정책을 확정하지 않는다. 관련 결정은 [기존 로그](../decisions/DECISION_LOG_AND_OPEN_QUESTIONS.md)의 D-026~027과 D-032~039, 작업 범위는 [P-001](../tasks/P-001.md)을 따른다.

## 1. 자산 가용성

사용자가 안내한 원격 커밋 `7364437`을 반영하여 아래 목업 5장을 실제로 열어 확인했다. 모두 Git에 추적된 저장소 자산이며, 개발 시 화면별 시각 참고로 사용한다. 이전 기반 작업의 이미지 누락 판정은 이 확인으로 갱신한다. 목업은 화면 예시이며 개별 사진·폰트의 배포용 원본이나 실제 홀 좌석 좌표 데이터는 아니다.

| ID | 저장소 기준 자산 | 관찰 |
| --- | --- | --- |
| L-01 | [Splash](references/rs_mockupex_splash_screen.png) | 모바일 Splash, 노란 레이블 LP |
| L-02 | [좌석 추천](references/rs_mockupex_seat_recommend.png) | 모바일 공연 상세·3개 추천·좌석 위치 축약도 |
| L-03 | [모바일 화면](references/rs_mockupex_mobileapp.png) | Splash·For You·Overview·App Home의 4화면 합성 |
| L-04 | [Article Detail](references/rs_mockupex_ai_article.png) | 모바일 Article Detail 예시 |
| L-05 | [데스크톱 화면](references/rs_mockupex_webapp.png) | Public Landing·App Home·For You·Overview의 4화면 합성 |

출처는 사용자가 제공한 Resonance 저장소의 목업 예시이며 사용 범위는 디자인 참고다. 위 상대 링크는 로컬 문서 검사와 CI의 자산 존재 검사 대상이다. 대화 첨부나 다른 환경의 scratch 파일을 전제로 하지 않는다.

## 2. 화면별 기준과 누락

| 화면 | 현재 재현 가능한 기준 | 참고 자산 ID | 누락·불일치와 P-001 처리 |
| --- | --- | --- | --- |
| Splash | [Design System](DESIGN_SYSTEM.md) 7절 | L-01, L-03 첫 화면 | 시각 예시 확보; P-001 범위 밖 |
| App Home | [Design System](DESIGN_SYSTEM.md) 7~8절, [Responsive](RESPONSIVE.md) 3~4절, [Interaction](INTERACTION.md) 2·5절 | L-03 마지막, L-05 오른쪽 위 | 목업은 For You 활성·playing 이미지이나 기본 홈은 메뉴 비선택·idle 노란 LP; 단독 검색·아바타는 햄버거 유틸리티 구조를 대체하지 않음 |
| For You | [IA](../product/IA.md) 8.1절, [Design System](DESIGN_SYSTEM.md) 3·6·8절 | L-03 두 번째, L-05 왼쪽 아래 | 데스크톱의 중복 큰 제목·All Events는 제외; NEW/unseen/seen 표현과 빈·오류 상태의 기준 화면은 추가 설계 |
| Concert Detail / Overview | [IA](../product/IA.md) 8.2절, [Flow](../product/USER_FLOW.md) UF-07 | L-02, L-03 세 번째, L-05 오른쪽 아래 | 배포용 공연 이미지 원본·출처 미확보; 단일 추천 강조는 복수안 제품 규칙을 대체하지 않음; All Events 복귀 문구 제외 |
| Seat | [추천 명세](../recommendation/RECOMMENDATION_SYSTEM.md) 6~11절, [Flow](../product/USER_FLOW.md) UF-08 | L-02 축약 좌석도만 참고 | 완성된 Seat 화면, Current Need 조정, 좌석 번호별 좌표·실제 홀 도면 없음; P-001은 가상 좌표 fixture와 자체 도면 필요 |
| Program | [IA](../product/IA.md) 8.2절 | 없음 | 화면·데이터 샘플 누락; P-001 범위 밖 |
| Articles / Article Detail | [Design System](DESIGN_SYSTEM.md) 8절, [Responsive](RESPONSIVE.md) 5~6절 | L-04 | 목록·태블릿·데스크톱·출처 자산 누락; P-001 범위 밖 |
| Reviews / 작성·수정·상세 | [IA](../product/IA.md) 8.4절 | 없음 | 현행 개인 후기 화면 누락; 과거 타인 후기 표현을 되살리지 않음 |
| 온보딩 / My Concert Taste | [Flow](../product/USER_FLOW.md) UF-02·04 | 없음 | 화면·입력 상태 누락; P-001은 온보딩 완료 fixture만 사용 |
| Bookmarks / Account / Settings | [IA](../product/IA.md) 8.5~8.8절 | 없음 | 화면·상태 자산 누락; 별도 작업 |
| 공통 내비게이션·상태 | [Responsive](RESPONSIVE.md) 2~7절, [Interaction](INTERACTION.md) 2~7절, [Flow](../product/USER_FLOW.md) 23~24절 | L-03 모바일, L-05 데스크톱 | 확정 breakpoint와 Mobile/Tablet bottom→top 전환을 반영한 기준 화면, 키보드·오류·미지원 화면은 누락; P-001 캡처는 이전 프로토타입 증거 |

L-02의 `Best value / Center view / Immersive`는 고정 추천 유형이 아니다. 문서의 확정 구조를 우선하고 모의 좌석을 실제 공연장의 판매 좌석처럼 표시하지 않는다.

## 3. 다음 자산 인계

P-001 구현 자산: [LP 비트맵](../../public/images/resonance-vinyl.png)은 Image Gen으로 새로 생성한 데모 이미지다. 사용 화면은 App Home이며 검은 LP·노란 resonance 레이블·흰 배경의 정면 사진을 요청했다. 저장소 목업을 UI에 직접 붙여 넣지 않았다. 프롬프트 핵심은 `top-down black vinyl LP, concentric grooves, yellow label with lowercase resonance, whole circular record on pure white, no turntable or interface`이다. 실물 음반이나 제품 사진이 아니다.

공연 포스터는 [화면 코드](../../src/components/demo-screen.tsx)와 [CSS](../../src/components/demo.module.css)로 만든 샘플 타이포그래피이며, [Seat 코드](../../src/components/seat-workspace.tsx)의 도면은 [좌표 fixture](../../src/lib/demo.ts)를 렌더링한다. 실제 홀 도면·배포용 공연 사진은 여전히 누락이다. 완성 화면의 세 크기 캡처는 [P-001](../tasks/P-001.md) 7절에 연결한다.

P-001 구현 시 위 목업을 참고하여 LP·가상 좌석도·공연 데모 비주얼을 실제 저장소 파일 또는 자체 렌더링 코드로 만들고 이 문서에서 상대 링크로 연결한다. 스크린샷 자체를 화면 UI로 붙여 넣지 않는다. 파일 위치, 제작/출처, 데모 여부, 사용 화면, 누락 상태를 갱신한 후 문서 검사를 실행한다. 미추적 파일이 없어도 빌드·검증이 가능해야 한다.
