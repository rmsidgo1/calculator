---
name: doc-validator
description: "PRD.md와 calculator.py를 대조하여 메서드 누락·시그니처 불일치·예외 정책 위반을 탐지한다. calculator 문서 검증, PRD 정합성 확인, 구현 검토 요청 시 반드시 이 스킬을 사용할 것."
---

# Doc Validator 스킬

PRD.md(진실의 원본)와 calculator.py(구현)를 교차 비교하여 정합성을 검증한다.

## 검증 흐름

1. `PRD.md` 섹션 4(클래스 인터페이스)에서 전체 메서드 목록 추출
2. `calculator.py`에서 실제 구현된 메서드 목록 추출 (Grep 활용)
3. 교차 비교: 누락 메서드, 추가 메서드, 시그니처 불일치 식별
4. 섹션 5(예외 정책) 기준으로 예외 처리 검증
5. 결과를 `_workspace/01_doc_validator_report.md`에 저장

## 검증 기준

### 메서드 완전성 (31개)
- 사칙연산: add, subtract, multiply, divide, modulo, power (6)
- 제곱근·로그: sqrt, cbrt, log, ln, exp (5)
- 삼각함수: sin, cos, tan, asin, acos, atan, atan2 (7)
- 쌍곡선: sinh, cosh, tanh (3)
- 수이론·변환: factorial, gcd, lcm, abs_val, ceil, floor, round_val (7)
- 히스토리: history, clear_history, last_result (3)

### 시그니처 핵심 체크
- `divide(a, b)`: ZeroDivisionError 발생 가능성
- `log(x, base=10)`: 기본값 존재 여부
- `sin/cos/tan(x, degree=False)`: degree 파라미터 존재 여부
- `atan2(y, x, degree=False)`: 파라미터 순서 y, x 확인
- `factorial(n)`: 반환 타입 `int`
- `last_result()`: 반환 타입 `float | None`

### 예외 정책 (PRD 섹션 5)
| 메서드 | 예외 타입 | 트리거 조건 |
|--------|-----------|------------|
| divide, modulo | ZeroDivisionError | b == 0 |
| sqrt | ValueError | x < 0 |
| log, ln | ValueError | x <= 0 |
| factorial | ValueError | n < 0 또는 비정수 |

## 이전 산출물 처리

`_workspace/01_doc_validator_report.md`가 이미 존재하면:
- 읽고 이전 불일치 목록 확인
- calculator.py가 수정되었으면 재검증
- 변경 없으면 기존 리포트 재사용 가능 (상단에 "재사용됨" 표기)
