# Tistory Custom Skin

개인 디자인 아카이브를 하나의 웹사이트처럼 운영하기 위해 제작한 Tistory 커스텀 스킨 프로젝트입니다.

## Overview

- **Role**: Design / Structure / Front-end customization
- **Platform**: Tistory
- **Stack**: HTML / CSS / JavaScript
- **Focus**: Editorial layout, Responsive Web, TOC, Interaction, Design System

## Why

기본 스킨을 단순히 꾸미는 수준이 아니라, 디자이너의 작업 기록과 아카이브를 한눈에 볼 수 있는 개인 브랜드 공간으로 만들고 싶었습니다.

핵심 목표는 다음과 같았습니다.

- 블로그보다 웹사이트에 가까운 첫인상
- 콘텐츠를 방해하지 않는 에디토리얼 레이아웃
- 글·프로젝트·아카이브가 자연스럽게 연결되는 구조
- 데스크톱부터 모바일까지 안정적인 반응형
- Tistory의 실제 데이터 구조와 예외 상태까지 고려한 UI

## Design Direction

전체 톤은 White / Black / Cobalt Blue를 중심으로 정리했습니다.

포인트 컬러는 `#0037FF`를 사용했고, 버튼·링크·선택 상태처럼 행동을 유도하는 요소에 집중했습니다.

## What I Built

- Landing-style home
- Custom header
- 2-column post grid
- Custom post detail layout
- Left-side TOC
- Automatic heading-based TOC generation
- Responsive long-title handling
- Previous / Next post navigation
- Category page redesign
- Guestbook CTA
- Text button system
- Responsive layout
- Scroll interaction
- Empty / delayed-rendering / missing-content states

## Key Problems & Solutions

### 1. Tistory template structure

일반 HTML과 달리 Tistory 치환자와 조건 태그가 실제 콘텐츠 렌더링에 관여하기 때문에, 디자인만 보고 수정할 수 없었습니다.

필요한 영역부터 치환자와 DOM 구조를 파악하고, 본문·댓글·관련 글·카테고리 등 각 블록이 문서 흐름에 어떻게 참여하는지 확인하면서 구조를 정리했습니다.

### 2. Post layout and grid alignment

게시글 상세 페이지에서 목차와 본문의 기준선이 어긋나는 문제가 있었습니다.

- TOC는 로고 컬럼 기준
- 게시글 본문은 타이틀 컬럼 기준

으로 그리드를 명확하게 나누고, 페이지 전체의 바깥 셸도 공통 기준으로 통일했습니다.

### 3. TOC exceptions

초기 TOC는 페이지 전체의 heading을 수집해 본문 밖 제목까지 포함되는 문제가 있었습니다.

본문 컨테이너 내부 heading만 선택하도록 selector 범위를 제한하고, 게시글마다 DOM 차이가 있어도 레이아웃이 흔들리지 않도록 구조를 안정화했습니다.

### 4. Empty states

이전글·다음글 중 하나가 없거나, 관련 글이 비어 있거나, 콘텐츠가 늦게 렌더링되는 경우 레이아웃이 무너지는 문제가 있었습니다.

존재 여부와 렌더링 시점을 확인하는 예외 처리를 추가하고, 커스텀 블록이 비어 있을 때는 Tistory 기본 목록을 fallback으로 사용하도록 보완했습니다.

### 5. Responsive design

데스크톱 레이아웃을 단순히 축소하지 않고, 화면 크기에 따라 구조 자체가 자연스럽게 바뀌도록 조정했습니다.

특히 긴 제목, TOC, 태그 그리드, 카드 목록, 버튼과 푸터 타이포를 모바일 환경에서 다시 설계했습니다.

### 6. Interaction and polish

스크롤 이동 버튼의 버벅임, pagination 상태 오류, 화살표 정렬, 댓글 UI, 공감 도구, 태그 라인, 카드 그라디언트 등 실제 사용 중 거슬리는 디테일을 반복적으로 수정했습니다.

## What I Learned

- HTML 구조와 DOM 흐름 읽기
- CSS Grid / Flex / spacing / specificity
- JavaScript selector와 상태 처리
- Responsive Web은 단순 축소가 아니라 구조 재설계라는 점
- 실제 서비스에서는 empty state와 delayed rendering까지 디자인해야 한다는 점
- AI를 활용해도 무엇이 문제인지 정의하고 결과를 판단하는 디렉팅 능력이 중요하다는 점

## Project Logs

- [2026-09-10 · Final Polish](../../logs/2026/09/2026-09-10-tistory-skin-final-polish.md)
- [2026-09-10 · Version History v1.43–v1.48](../../logs/2026/09/2026-09-10-tistory-skin-version-history.md)

## Retrospective

처음에는 폰트와 컬러 정도만 수정하려고 시작했지만, 결국 홈·목록·상세·카테고리·댓글·관련 글·반응형·인터랙션까지 거의 하나의 스킨을 새로 만드는 수준으로 확장되었습니다.

가장 크게 느낀 점은 디자인과 구현이 완전히 별개의 일이 아니라는 것입니다. 구현 방식을 이해할수록 디자인 단계에서 고려해야 할 상태와 구조가 더 많이 보이기 시작했습니다.

이제 Tistory를 보면 그냥 블로그보다, 또 뜯어고칠 곳부터 보입니다.
