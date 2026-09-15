# Resonance — Responsive Layout & Navigation

> 상태: Confirmed responsive structure + unresolved implementation details v1.0
> 기준일: 2026-09-15

## 1. 원칙

- Mobile, Tablet, Desktop은 같은 데이터와 정보 구조를 사용한다.
- 화면 크기 변화는 단순 축소가 아니라 navigation, 열 수, 콘텐츠 우선순위와 CTA 위치의 명시적 reflow다.
- fixed pixel 좌표나 absolute positioning을 primary layout으로 사용하지 않는다.
- 기기별 화면을 서로 다른 제품이나 별도 콘텐츠 복제품으로 만들지 않는다.

## 2. 확정 breakpoint

| 구간 | 범위 |
| --- | --- |
| Mobile | `<768px` |
| Tablet | `768–1199px` |
| Desktop | `>=1200px` |

이 수치는 현행 제품 breakpoint다. 컴포넌트 내부의 추가 reflow 지점은 콘텐츠가 깨지지 않도록 둘 수 있지만 전역 기기 분류를 대체하지 않는다.

## 3. Mobile과 Tablet navigation

### App Home

- `For You`, `Articles`, `Reviews` primary navigation은 화면 하단에 위치한다.
- 세 메뉴 중 어느 것도 active가 아니다.
- LP와 stylus home visual을 가리지 않는다.
- 햄버거 유틸리티 메뉴는 `Account`, `My Concert Taste`, `Bookmarks`, `Settings`를 유지한다.

### Primary content

- 사용자가 App Home의 bottom navigation에서 destination을 선택하면 홈 콘텐츠와 navigation이 함께 위로 이동한다.
- 같은 navigation component가 content screen의 top navigation 위치에 도달한다.
- top navigation은 primary content 화면에서 sticky로 유지한다.
- App Home으로 돌아가면 같은 이동을 반대로 실행하고 navigation은 하단으로, LP와 stylus는 다시 화면에 나타난다.

전환의 입력과 timing은 [Interaction](INTERACTION.md)에서 정의한다.

## 4. Desktop navigation

- `For You`, `Articles`, `Reviews`는 left sidebar를 사용한다.
- App Home에서 어느 primary menu도 active가 아닌 의미를 유지한다.
- Mobile/Tablet의 bottom-to-top 이동을 Desktop에 그대로 복제하지 않는다.
- 콘텐츠 열 수, 본문 폭과 보조 정보 배치는 넓은 화면에 맞게 reflow한다.

## 5. Detail과 utility 화면

- `Concert Detail`, `Article Detail`, `Review Detail`에는 global top primary navigation을 중첩하지 않는다.
- detail은 compact header와 Back을 사용하며 논리적 parent primary context를 유지한다.
- Mobile/Tablet에서는 detail header가 좁은 폭에서도 제목과 Back을 가리지 않아야 한다.
- Desktop detail에서도 primary content를 방해하는 중복 top navigation을 만들지 않는다.
- 햄버거 메뉴와 Bookmarks를 포함한 utility IA는 breakpoint 변경으로 폐기하거나 primary menu로 승격하지 않는다.

## 6. Responsive reflow

- For You 카드, Concert Detail, Seat, Articles와 Reviews는 정보 우선순위를 보존하며 열과 CTA를 재배치한다.
- Articles는 화면이 넓어져도 장문 본문의 읽기 가능한 줄 길이를 유지한다.
- Seat 추천안과 좌석도는 각 구간에서 비교와 위치 확인이 가능하도록 배치하되 실제 판매 좌석도처럼 보이게 하지 않는다.
- Loading, Empty, Error, Partial data와 Unsupported 상태도 각 breakpoint에서 레이아웃을 유지한다.

## 7. 화면 크기 변경 시 상태 보존

breakpoint가 바뀌어도 다음 사용자 상태를 임의로 초기화하지 않는다.

- 현재 사용자와 primary destination
- 선택한 공연, detail 탭과 추천안
- Current Need의 적용 상태와 작성 중 입력
- 읽던 Article과 가능한 scroll context
- 작성 중인 Review와 unsaved changes
- 이전 list/feed의 scroll position과 복원 가능한 UI state
- LP의 현재 playback 상태와 position

복원할 수 없는 상태는 [User Flow](../product/USER_FLOW.md)의 안전한 상위 화면 fallback을 따른다.

## 8. Open Questions

- Desktop left sidebar를 인증·utility 화면에서 유지할 정확한 범위
- sticky top navigation과 compact detail header의 높이·scroll 충돌 처리
- 화면 회전과 실시간 resize 중 animation을 생략하거나 단순화할 조건
- Seat map의 구간별 확대·이동·추천안 비교 layout
- reduced motion 환경에서 bottom-to-top 전환과 reflow를 표현하는 정확한 방식
