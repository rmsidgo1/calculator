---
name: calculator-orchestrator
description: "Python Calculator 에이전트 팀을 조율하는 오케스트레이터. calculator 구현, PRD 기반 코드 생성, 문서 정합성 검증, 테스트 실행, 컴플라이언스 확인, CLI 추가/수정 요청 시 반드시 이 스킬을 사용할 것. 후속 작업: calculator 재실행, 업데이트, 수정, 보완, 부분 재실행, 이전 결과 개선 요청 시에도 반드시 이 스킬을 사용."
---

# Calculator Orchestrator

Python Calculator 에이전트 팀(doc-validator → ai-action → test-verify ‖ compliance-verify)을 조율하여 PRD 기반 완전한 구현을 생성하는 통합 스킬.

## 실행 모드: 하이브리드 (파이프라인 + 팬아웃)

| Phase | 에이전트 | 실행 모드 | 이전 Phase 의존 |
|-------|---------|----------|----------------|
| Phase 1 | doc-validator | 서브 에이전트 (순차) | 없음 |
| Phase 2 | ai-action | 서브 에이전트 (순차) | Phase 1 결과 |
| Phase 3 | test-verify + compliance-verify | 서브 에이전트 (병렬) | Phase 2 결과 |

## 에이전트 구성

| 에이전트 | subagent_type | 역할 | 스킬 | 출력 |
|---------|--------------|------|------|------|
| doc-validator | doc-validator | PRD 정합성 검증 | doc-validator | `_workspace/01_doc_validator_report.md` |
| ai-action | ai-action | Calculator 구현 | ai-action | `calculator.py`, `_workspace/02_ai_action_report.md` |
| test-verify | test-verify | 테스트 작성·실행 | test-verify | `test_calculator.py`, `_workspace/03_test_verify_report.md` |
| compliance-verify | compliance-verify | 비기능 준수 검증 | compliance-verify | `_workspace/04_compliance_verify_report.md` |

## 워크플로우

### Phase 0: 컨텍스트 확인

`_workspace/` 디렉토리 존재 여부 확인:

- **`_workspace/` 미존재** → 초기 실행. Phase 1로 진행
- **`_workspace/` 존재 + 부분 수정 요청** → 해당 에이전트만 재실행:
  - "문서 검증만 다시" → Phase 1만
  - "코드 수정" → Phase 2 + Phase 3
  - "테스트만" → Phase 3 (test-verify만)
- **`_workspace/` 존재 + 새 전체 실행** → `_workspace/`를 `_workspace_{YYYYMMDD_HHMMSS}/`로 이동 후 새 실행

### Phase 1: 준비

1. `C:\reviewer\calculator\_workspace\` 디렉토리 생성 (없으면)
2. `PRD.md` 존재 확인

### Phase 2: doc-validator 실행 (순차)

**실행 모드: 서브 에이전트**

```
Agent(
  name: "doc-validator",
  subagent_type: "doc-validator",
  model: "opus",
  prompt: """
    당신은 doc-validator 에이전트입니다.
    스킬: C:\reviewer\calculator\.claude\skills\doc-validator\SKILL.md를 읽고 따르세요.

    작업 디렉토리: C:\reviewer\calculator
    - PRD.md와 calculator.py(존재 시)의 정합성을 검증하세요.
    - 결과를 C:\reviewer\calculator\_workspace\01_doc_validator_report.md에 저장하세요.
  """
)
```

Phase 2 완료 확인: `_workspace/01_doc_validator_report.md` 생성 여부

### Phase 3: ai-action 실행 (순차, Phase 2 완료 후)

**실행 모드: 서브 에이전트**

```
Agent(
  name: "ai-action",
  subagent_type: "ai-action",
  model: "opus",
  prompt: """
    당신은 ai-action 에이전트입니다.
    스킬: C:\reviewer\calculator\.claude\skills\ai-action\SKILL.md를 읽고 따르세요.

    작업 디렉토리: C:\reviewer\calculator
    1. C:\reviewer\calculator\_workspace\01_doc_validator_report.md를 먼저 읽으세요.
    2. PRD.md를 읽고 calculator.py를 완전히 구현하세요.
    3. C:\reviewer\calculator\_workspace\02_ai_action_report.md를 생성하세요.
  """
)
```

Phase 3 완료 확인: `calculator.py` 생성 여부

### Phase 4: test-verify + compliance-verify 병렬 실행 (Phase 3 완료 후)

**실행 모드: 서브 에이전트 (병렬)**

단일 메시지에서 두 Agent 도구를 동시 호출:

```
# Agent 1 (동시 호출)
Agent(
  name: "test-verify",
  subagent_type: "test-verify",
  model: "opus",
  run_in_background: true,
  prompt: """
    당신은 test-verify 에이전트입니다.
    스킬: C:\reviewer\calculator\.claude\skills\test-verify\SKILL.md를 읽고 따르세요.

    작업 디렉토리: C:\reviewer\calculator
    1. calculator.py를 읽고 test_calculator.py를 작성하세요.
    2. pytest 또는 unittest로 테스트를 실행하세요.
    3. C:\reviewer\calculator\_workspace\03_test_verify_report.md를 생성하세요.
  """
)

# Agent 2 (동시 호출)
Agent(
  name: "compliance-verify",
  subagent_type: "compliance-verify",
  model: "opus",
  run_in_background: true,
  prompt: """
    당신은 compliance-verify 에이전트입니다.
    스킬: C:\reviewer\calculator\.claude\skills\compliance-verify\SKILL.md를 읽고 따르세요.

    작업 디렉토리: C:\reviewer\calculator
    1. calculator.py, test_calculator.py, PRD.md를 읽으세요.
    2. 비기능 요구사항 및 DoD 준수 여부를 검증하세요.
    3. C:\reviewer\calculator\_workspace\04_compliance_verify_report.md를 생성하세요.
  """
)
```

### Phase 5: 결과 종합 및 보고

1. 4개 리포트 수집:
   - `_workspace/01_doc_validator_report.md`
   - `_workspace/02_ai_action_report.md`
   - `_workspace/03_test_verify_report.md`
   - `_workspace/04_compliance_verify_report.md`
2. 최종 요약 보고 (콘솔 출력):

```
## 실행 결과 요약

| 단계 | 에이전트 | 결과 |
|------|---------|------|
| Phase 1 | doc-validator | PASS/FAIL |
| Phase 2 | ai-action | 완료/실패 |
| Phase 3 | test-verify | N/M 통과 |
| Phase 3 | compliance-verify | COMPLIANT/NON-COMPLIANT |

## 산출물
- calculator.py: [생성됨/실패]
- test_calculator.py: [생성됨/실패]

## 다음 조치 (있는 경우)
- [불합격 항목 및 권장 조치]
```

## 데이터 흐름

```
PRD.md
  │
  ▼
[doc-validator] ──→ _workspace/01_doc_validator_report.md
                                │
                                ▼
                          [ai-action] ──→ calculator.py
                                              │
                          ┌───────────────────┤
                          ▼                   ▼
                   [test-verify]    [compliance-verify]
                          │                   │
                          ▼                   ▼
              _workspace/03_*.md    _workspace/04_*.md
                          │                   │
                          └─────────┬─────────┘
                                    ▼
                             [최종 요약 보고]
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| doc-validator 실패 | 리포트 없이 ai-action으로 진행, 보고서에 "검증 생략" 명시 |
| ai-action 실패 (calculator.py 미생성) | Phase 4 건너뜀, 사용자에게 알림 |
| test-verify 실패 | 오류 메시지를 리포트에 포함, compliance-verify는 계속 진행 |
| compliance-verify 실패 | 오류 메시지를 리포트에 포함, 나머지 결과로 종합 보고 |
| 에이전트 1개 실패 | 1회 재시도 후 재실패 시 "N/A"로 표시하고 진행 |

## 테스트 시나리오

### 정상 흐름
1. `PRD.md` 존재, `calculator.py` 미존재 상태에서 실행
2. Phase 2: doc-validator가 "구현 파일 없음" 리포트 생성
3. Phase 3: ai-action이 31개 메서드 구현 완료
4. Phase 4: test-verify N개 통과 + compliance-verify COMPLIANT
5. 예상 산출물: `calculator.py`, `test_calculator.py`, 4개 리포트

### 에러 흐름 (ai-action 실패)
1. Phase 3에서 ai-action이 부분 구현만 완료
2. doc-validator 리포트에 미구현 메서드 목록 존재
3. Phase 4에서 test-verify가 ImportError 또는 AttributeError 감지
4. 리포트에 "미구현 메서드: [목록]" 명시
5. 사용자에게 "ai-action 재실행 권고" 보고
