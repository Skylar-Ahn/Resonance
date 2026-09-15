# Resonance — Documentation Index

> 상태: Working baseline v1.1  
> 기준일: 2026-09-15  
> 범위: Resonance의 현행 기획·추천·데이터·디자인·협업 기준

## 1. 목적

이 문서 묶음은 최신 IA와 User Flow를 중심으로 제품 결정, 추천 시스템 논리, 데이터 수집·정규화 구조, 기술 아키텍처 방향, 디자인 언어 및 남은 Open Questions를 개발 가능한 수준으로 정리한다.

[IA.md](product/IA.md)와 [USER_FLOW.md](product/USER_FLOW.md)는 각각 기존 문서와 후속 Addendum을 통합한 현행 기준이다.

## 2. 문서 우선순위

1. 사용자가 가장 최근에 명시적으로 내린 결정
2. [IA.md](product/IA.md)와 [USER_FLOW.md](product/USER_FLOW.md)의 `확정` 항목
3. Product Spec과 분야별 상세 문서의 `확정` 항목
4. 목업의 시각적 의도
5. `제안`, `가설`, `MVP 잠정`, `Open Question`

목업에만 있는 요소는 자동으로 기능 범위가 되지 않는다. 조언으로 제시되었으나 사용자가 확정하지 않은 내용도 구현 기준으로 간주하지 않는다.

Decision Log와 이 우선순위의 관계에 대한 문서 간 불일치는 [기존 결정 로그](decisions/DECISION_LOG_AND_OPEN_QUESTIONS.md)의 DR-001에서 검토한다. 충돌 항목을 임의 확정하지 않는다.

## 3. 상태 표기

| 상태 | 의미 |
| --- | --- |
| 확정 | 현재 구현과 후속 문서가 따라야 하는 결정 |
| MVP 잠정 | MVP 기준으로 우선 채택했지만 사용자가 재검토 가능성을 명시한 결정 |
| 기술 방향 | 유지보수성과 현재 요구를 기준으로 정리된 아키텍처 방향. 구현 착수 전 스택 확정 필요 |
| Later | 제품 비전에는 남기되 MVP 구현 대상은 아님 |
| 폐기 | 더 이상 설계·구현 후보로 다루지 않음 |
| Open Question | 아직 결정되지 않아 임의 구현하면 안 되는 항목 |

## 4. 파일 구성

| 파일 | 역할 |
| --- | --- |
| [IA.md](product/IA.md) | 화면·콘텐츠·기능의 존재, 계층 및 연결에 관한 현행 기준 |
| [USER_FLOW.md](product/USER_FLOW.md) | 목표별 시작점, 행동, 분기, 완료 조건에 관한 현행 기준 |
| [PRODUCT_SPEC.md](product/PRODUCT_SPEC.md) | MVP 범위, 화면 구조, 온보딩, Concert Taste, 알림, 저장, 후기 정책 |
| [RECOMMENDATION_SYSTEM.md](recommendation/RECOMMENDATION_SYSTEM.md) | 공연·좌석 추천 입력, 후기 근거화, 복수 추천안, 피드백 루프 |
| [DATA_AND_ARCHITECTURE.md](data/DATA_AND_ARCHITECTURE.md) | 공연 데이터 수집·검증·정규화, 좌석 데이터, 백엔드 구조 |
| [DESIGN_AND_INTERACTION.md](design/DESIGN_AND_INTERACTION.md) | 시각 언어, LP 상태 논리, 반응형·Figma 구현 원칙 |
| [DECISION_LOG_AND_OPEN_QUESTIONS.md](decisions/DECISION_LOG_AND_OPEN_QUESTIONS.md) | 기존 미확정 항목의 해결 상태와 현재 남은 질문 |
| [WORKFLOW_AND_AGENT_HANDOFF.md](process/WORKFLOW_AND_AGENT_HANDOFF.md) | 기획·디자인·개발 에이전트의 역할, 변경 제안 및 문서 갱신 규칙 |
| [AGENTS.md](../AGENTS.md) | Codex 작업 진입 지침 |
| [작업 템플릿](tasks/TEMPLATE.md) / [P-001](tasks/P-001.md) | 반복 실행 입력과 첫 프로토타입 범위 |
| [REFERENCE_MAP.md](design/REFERENCE_MAP.md) | 화면별 기준 자산과 누락 |
| [PWA_SCOPE.md](engineering/PWA_SCOPE.md) | 확정된 PWA 목표와 미결 기능 경계 |

문서 검증은 [협업 문서의 로컬 검증 절차](process/WORKFLOW_AND_AGENT_HANDOFF.md)를 따른다.

## 5. 한 문장 제품 정의

Resonance는 사용자가 보고 싶은 클래식 공연과 원하는 현장 경험을 이해해 공연과 좌석을 설명 가능한 방식으로 추천하고, 감상을 돕는 아티클과 개인 후기 기록을 하나의 흐름으로 연결하는 반응형 웹앱이다.

2026-09-15 사용자 지시로 PWA 개발은 확정되었다(D-028). 상세 기술 스택은 재논의 대상이며 기존 후보는 최종 채택되지 않았다(D-029).

## 6. 현재 MVP의 네 축

1. `For You`: 관심사 기반 공연 추천 피드이자 공연 알림의 도착 영역
2. `Seat Recommendation`: 공연·공연장·사용자 취향에 따른 좌석 번호 수준의 복수 추천
3. `Articles`: 작품·작곡가·연주자·역사·비평 맥락을 제공하는 사전 감상 콘텐츠
4. `Reviews`: 구조화된 평가와 자유 텍스트를 함께 보존하는 개인 후기 아카이브

## 7. 명시적으로 제외하거나 폐기한 것

- 별도 `Alerts` 메뉴와 독립 알림 피드
- 타인의 후기를 탐색하는 커뮤니티형 Reviews
- 댓글·좋아요·팔로우 등 소셜 기능
- Resonance 내부의 좌석 선택·결제·예매 완료
- 실시간 잔여 좌석을 전제로 한 MVP
- `All Events` 컨트롤의 MVP 포함
- 공연 전 메모 기능의 MVP 포함
- YouTube 영상 임베딩 및 YouTube/YouTube Music 데이터를 추천 입력으로 이용하는 구상
