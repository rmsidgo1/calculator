---
name: compliance-verify
description: "PRD 비기능 요구사항과 Definition of Done 준수 여부를 코드 레벨에서 검증한다. 컴플라이언스 확인, 외부 라이브러리 검사, 타입 힌트 점검, DoD 체크 요청 시 반드시 이 스킬을 사용할 것."
---

# Compliance Verify 스킬

calculator.py의 비기능 요구사항 준수 여부를 체계적으로 검증한다.

## 검증 체크리스트

### 1. 외부 라이브러리 검사

허용 목록: `math`, `cmath`, Python 내장 모듈
```bash
# import 구문 추출
grep -n "^import\|^from" calculator.py
```
- `math`, `cmath`, `__future__` 이외 패키지 발견 시 → NON-COMPLIANT

### 2. Python 3.10+ 문법 검증

체크 항목:
- `float | None` 형식의 유니온 타입 (구식 `Optional[float]` 사용 금지는 아니지만 권고)
- 소문자 제네릭: `list[dict]`, `list[str]` (구식 `List[Dict]` 대신)
- 반환 타입에 `X | Y` 표기 권장

### 3. 타입 힌트 완전성

모든 public 메서드에 파라미터 타입과 반환 타입이 있어야 한다:
```python
# 올바른 예
def add(self, a: float, b: float) -> float: ...
def last_result(self) -> float | None: ...
def history(self) -> list[dict]: ...

# 위반 예
def add(self, a, b): ...  # 타입 힌트 없음
```

체크 방법: `def ` 로 시작하는 라인에 `->` 반환 타입이 있는지 확인

### 4. Definition of Done (PRD 섹션 7)

| 항목 | 검증 방법 |
|------|----------|
| 모든 메서드 구현 완료 | 31개 메서드 존재 여부 |
| 정상 케이스 테스트 통과 | test_calculator.py 존재 + 실행 결과 |
| 예외 케이스 테스트 통과 | assertRaises 패턴 존재 여부 |
| 타입 힌트 전체 적용 | 모든 def 라인에 -> 존재 |
| 외부 라이브러리 미사용 | import 목록 검사 |

## 판정 기준

- 외부 라이브러리 위반: 즉시 NON-COMPLIANT
- 타입 힌트 누락 5개 이상: NON-COMPLIANT
- 타입 힌트 누락 1~4개: PARTIAL-COMPLIANT (목록 명시)
- 모든 항목 통과: COMPLIANT

## 이전 산출물 처리

`_workspace/04_compliance_verify_report.md`가 이미 존재하면:
- calculator.py 수정 여부 확인 (파일 크기/mtime 비교)
- 변경되었으면 재검증, 변경 없으면 기존 리포트 재사용
