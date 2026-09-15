# Codex Working Instructions

## 시작 순서

1. [기존 문서 인덱스](docs/00_README.md)와 [협업·인계 규칙](docs/process/WORKFLOW_AND_AGENT_HANDOFF.md)을 읽는다.
2. [기존 결정 로그](docs/decisions/DECISION_LOG_AND_OPEN_QUESTIONS.md)에서 최신 결정과 관련 DR 상태를 확인한다. 인덱스의 우선순위와 DR-001의 미해결 관계를 확인한다.
3. 대상 작업 문서를 읽고 [IA](docs/product/IA.md)와 [User Flow](docs/product/USER_FLOW.md)의 관련 영역·UF를 대조한다. 작업이 없으면 [템플릿](docs/tasks/TEMPLATE.md)으로 입력을 정리한다.
4. `git status --short --branch`와 `git rev-parse HEAD`로 기존 변경·브랜치·HEAD를 확인하고, 이전 실행의 검증·남은 일을 읽는다. 이미 완료된 작업을 재생성하지 않는다.

## 필요한 분야 선택

| 작업 | 추가 입력 |
| --- | --- |
| 화면·사용자 입력·저장 | [Product Spec](docs/product/PRODUCT_SPEC.md)의 해당 기능 |
| 시각 언어·컴포넌트 | [Design System](docs/design/DESIGN_SYSTEM.md), [Reference Map](docs/design/REFERENCE_MAP.md) |
| 반응형·내비게이션 위치 | [Responsive](docs/design/RESPONSIVE.md) |
| 제스처·전환·상태 | [Interaction](docs/design/INTERACTION.md) |
| 공연·좌석 추천 | [Recommendation System](docs/recommendation/RECOMMENDATION_SYSTEM.md), [Data/Architecture](docs/data/DATA_AND_ARCHITECTURE.md)의 좌석·근거 데이터 |
| 데이터·인증·API | [Data/Architecture](docs/data/DATA_AND_ARCHITECTURE.md)와 관련 제품 정책 |
| PWA·설치·캐시·라우팅 | [PWA Scope](docs/engineering/PWA_SCOPE.md) |

관련 Decision ID, UF ID와 읽은 절을 작업 문서에 남긴다. 이 파일에 제품 정책을 복사하거나 새 인덱스·결정 로그·협업 문서를 만들지 않는다.

## 상태별 처리

- `확정`: 최신 사용자 지시와 적용 범위를 확인하고 구현 기준으로 사용한다.
- `MVP 잠정`: 작업 범위에 필요할 때 잠정 상태를 유지해 사용한다. 고정 데이터 계약으로 승격하지 않는다.
- `기술 방향`, `제안`, `가설`: 후보로 읽는다. D-029에 따라 상세 스택 선택은 재논의한다.
- `Open Question`, `Proposed` DR: 제품 결정을 추측하지 않는다. 충돌은 기존 로그의 Decision Request 형식으로 기록하고 해당 부분만 차단한다.
- `Later`, `폐기`, `Deferred`, `Rejected`: 현재 작업에 자동 포함하지 않는다. 사용자가 재개하면 관련 근거·상태를 갱신한다.
- 프로토타입 임시 선택: 작업 문서에서 식별자·범위·이유·교체 조건을 명시한다. 제품 확정 또는 MVP 잠정 결정과 구분한다.

## 구현과 검증

- 작업 문서의 범위·의존성·수용 기준을 따라 최소 변경한다. 관계없는 기존 변경을 되돌리지 않는다.
- 문서만 요청된 작업에서 앱 구현으로 넘어가지 않는다. 앱 구현은 승인된 작업 범위를 따르며, [P-001](docs/tasks/P-001.md)의 프로토타입 기술 선택을 최종 제품 스택으로 확장하지 않는다.
- 파일 참조는 해당 문서 기준 상대 Markdown 링크로 작성한다. 역사적 원본·미생성 후보는 그렇게 표시하고 가짜 링크를 만들지 않는다.
- 자산은 실제 존재와 공유 가능 여부를 확인한다. 대화 첨부·다른 환경의 scratch 경로·미추적 로컬 자산을 필수 의존성으로 쓰지 않는다.
- 구현 시 관련 loading/empty/error/partial/unsupported 상태, 입력 보존, 접근성, 화면 크기별 동작을 검증한다. 모의 데이터와 실제 근거를 구분하고 외부 API·추천 계산은 작업에서 승인한 범위만 연결한다.
- [협업 문서의 검증 명령](docs/process/WORKFLOW_AND_AGENT_HANDOFF.md)을 실행한다. 앱 작업에서는 해당 수용 기준에 맞는 테스트와 화면 확인을 추가한다.
- 문서 충돌을 발견하면 관련 본문·Open Question에 기존 DR을 연결한다. 승인이 필요한 제품 변경과 독립적으로 가능한 구현·검증은 진행한다.

## 상태와 보고

작업 상태는 `Draft` → `Ready` → `In Progress` → `Done`으로 관리한다. 차단 의존성이 있으면 `Blocked`로 기록하고 원인·해제 조건을 적는다. 문서 작성 완료만으로 앱 작업을 Done으로 표시하지 않는다.

마지막에 작업 문서에 변경 범위, 실제 검증 명령과 결과, 미실행 항목, 남은 결정, 재개할 첫 단계를 기록한다. 사용자에게 변경 파일, 검증 증거, 남은 결정과 정확한 재현 경로를 보고한다. 실행 가능한 앱이 생긴 작업에서는 실제 실행 명령과 URL도 검증해 제공한다.

## Git 실행 규칙

[협업 문서의 Git 정책](docs/process/WORKFLOW_AND_AGENT_HANDOFF.md#13-git-커밋과-파일-추적-정책)과 [검사 자동화 절차](docs/process/WORKFLOW_AND_AGENT_HANDOFF.md#136-로컬-훅과-검사기)를 따른다.

- 작업 전후 `git status --short --branch`를 확인하고, 작업 관련 경로만 `git add <path>`로 선택적으로 스테이징한다. `git add .`과 `git add -A`를 기본 절차로 사용하지 않는다.
- 새 clone이나 새 Codex 실행 환경에서는 `python3 scripts/install_gitleaks.py`와 `python3 scripts/install_git_hooks.py`를 실행하고 `git config --local --get core.hooksPath`를 확인한다. 훅 파일이 추적되어 있어도 설치 전에는 자동 활성화되지 않는다.
- 커밋 전 `git diff --cached`, `git diff --cached --check`, `python3 scripts/run_git_checks.py pre-commit`으로 Git index의 실제 blob을 검사한다. `pre-commit`은 파일 정책·크기·비밀정보, `commit-msg`는 메시지 형식, `pre-push`는 실제 push ref의 모든 신규 커밋을 검사한다.
- 푸시 전 대상 브랜치와 비교한 커밋·파일 범위 및 스테이징 내용을 검토한다. 검사기가 없거나 버전이 다르면 실패가 정상이며 [고정 설치 절차](docs/process/WORKFLOW_AND_AGENT_HANDOFF.md#136-로컬-훅과-검사기)로 복구한다.
- `git add -f`, `--no-verify`, 검사 비활성화로 정책을 우회하지 않는다.
- 비밀 값은 응답·로그·문서·커밋 메시지에 출력하지 않는다. 의심 파일은 내용을 노출하지 않고 경로·추적 여부만 확인한다.
- 필수 검증 실패를 해결하지 않은 채 커밋하거나 푸시하지 않는다. 과거 커밋을 재작성하거나 공유 이력에 force push하지 않는다.
