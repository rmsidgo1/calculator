---
name: ai-action
description: "PRD.md 명세를 기반으로 calculator.py를 구현한다. calculator 구현, 코드 작성, Python Calculator 클래스 생성 요청 시 반드시 이 스킬을 사용할 것. doc-validator 리포트가 있으면 반드시 반영한다."
---

# AI Action 스킬

PRD.md를 읽고 완전한 Calculator 클래스를 구현한다.

## 구현 규칙

### 필수 제약
- 표준 라이브러리만: `import math`, `import cmath` 허용, 그 외 외부 패키지 금지
- Python 3.10+: 반환 타입에 `float | None`, 파라미터에 소문자 제네릭(`list[dict]`) 사용
- 타입 힌트: 모든 public 메서드의 파라미터·반환 타입 100% 적용
- `__init__`: `history_limit: int = 100` 파라미터, `_history: list[dict]` 초기화

### 히스토리 관리
- 모든 연산 메서드는 완료 후 히스토리에 `{"expression": "메서드명(인수)", "result": 결과값}` 추가
- `history_limit` 초과 시 가장 오래된 항목 자동 제거 (`pop(0)`)
- `last_result()`: 히스토리가 비어있으면 `None` 반환

### 예외 처리 (PRD 섹션 5 기준)
```python
# 메시지 예시 (정확히 이 형식 사용)
raise ZeroDivisionError("Division by zero")
raise ValueError("sqrt of negative number")
raise ValueError("factorial requires non-negative integer")
raise ValueError("log requires positive number")
raise TypeError("operands must be numeric")
```

### 삼각함수 degree 변환
```python
if degree:
    x = math.radians(x)  # 입력 변환
# 역함수 (asin/acos/atan/atan2)
result = math.asin(x)
if degree:
    result = math.degrees(result)  # 결과 변환
```

## 구현 순서

1. `_workspace/01_doc_validator_report.md` 읽기 (존재 시)
2. `PRD.md` 전체 읽기
3. calculator.py 작성 (섹션 순서대로)
4. `_workspace/02_ai_action_report.md` 생성

## 이전 산출물 처리

`calculator.py`가 이미 존재하면:
- doc-validator 리포트의 불일치 항목만 수정
- 기존 구현이 정합성을 통과했으면 최소 변경 원칙 적용
