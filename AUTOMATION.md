# Design Log Automation

이 저장소는 기록을 귀찮은 별도 업무로 만들지 않기 위해 세 가지 입력 경로를 사용합니다.

## 1. ChatGPT — 가장 권장

대화 중 `/log`, `기록해줘`, `깃허브에 남겨줘`처럼 말하면 현재 작업 맥락을 짧게 정리해 `logs/YYYY/MM/YYYY-MM-DD.md`에 기록합니다.

이 방식의 장점은 제목·요약·배운 점을 다시 입력할 필요가 없다는 점입니다. 이미 대화에 있는 맥락을 사용하되, 공개 저장소에 부적절한 개인 정보는 제외합니다.

## 2. GitHub 버튼 — 대화 밖 작업용

GitHub Actions의 **Add Work Log**를 실행하면 폼처럼 제목, 카테고리, 요약, 상세, 링크를 입력할 수 있습니다.

→ [Add Work Log 실행](https://github.com/bini-s2/Design-log/actions/workflows/add-work-log.yml)

입력된 내용은 한국 시간 기준 하루 로그에 추가되고 README의 Recent Activity도 갱신됩니다.

## 3. Tistory — 자동 기록

`https://bini-s2.tistory.com/rss`를 6시간마다 확인합니다.

- 처음 실행할 때는 현재 RSS 항목을 기준점으로만 저장하고 기존 글을 소급 기록하지 않습니다.
- 이후 새 글이 발견되면 발행일 기준 하루 로그에 제목, 링크, 짧은 요약을 추가합니다.
- 같은 글은 다시 기록하지 않습니다.
- 새 글이 없으면 커밋하지 않습니다.

자동 동기화는 GitHub Actions의 **Sync Tistory**에서 수동 실행할 수도 있습니다.

## 기록 구조

```text
Design-log/
├─ README.md
├─ AGENTS.md
├─ AUTOMATION.md
├─ .automation/
│  └─ tistory-state.json
├─ .github/workflows/
│  ├─ add-work-log.yml
│  └─ sync-tistory.yml
├─ scripts/
│  ├─ log_activity.py
│  ├─ rebuild_readme.py
│  └─ sync_tistory.py
└─ logs/
   └─ YYYY/MM/
      └─ YYYY-MM-DD.md
```

## 왜 하루 단위 로그인가

자동화를 자주 쓰면 주제별 파일이 너무 많이 생길 수 있습니다. 그래서 새 자동 기록은 하루 한 파일에 시간순으로 모읍니다. 세부 프로젝트 기록은 각 프로젝트 저장소에 남기고, Design-log는 전체 작업 흐름을 빠르게 훑는 역할을 합니다.

## 공개 저장소 안전 원칙

이 저장소는 공개입니다. 자동 기록 대상은 디자인, UX/UI, 프론트엔드 학습, 블로그, AI 활용, 자동화, 창작 프로젝트에 한정합니다. 건강, 연애, 사적 관계, 상세 위치, 연락처, 계정 정보, 인증 정보 등 개인적인 내용은 기록하지 않습니다.
