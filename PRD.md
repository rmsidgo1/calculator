

# PRD: Python 공학용 Calculator 클래스

## 1. 개요

### 목적
Python으로 구현하는 공학용 계산기 클래스. 기본 사칙연산부터 삼각함수, 로그, 지수 등 고급 수학 연산을 지원하며, 재사용 가능한 클래스 형태로 제공한다.

### 배경
직접 수식 처리 로직을 매번 작성하는 대신 단일 클래스로 캡슐화하여 코드 재사용성과 테스트 용이성을 높인다.

---

## 2. 기능 요구사항

### 2.1 기본 사칙연산

| 메서드 | 설명 | 예외 처리 |
|---|---|---|
| `add(a, b)` | 덧셈 `a + b` | - |
| `subtract(a, b)` | 뺄셈 `a - b` | - |
| `multiply(a, b)` | 곱셈 `a * b` | - |
| `divide(a, b)` | 나눗셈 `a / b` | `b == 0` → `ZeroDivisionError` |
| `modulo(a, b)` | 나머지 `a % b` | `b == 0` → `ZeroDivisionError` |
| `power(base, exp)` | 거듭제곱 `base ** exp` | - |

### 2.2 제곱근 및 로그

| 메서드 | 설명 | 예외 처리 |
|---|---|---|
| `sqrt(x)` | 제곱근 `√x` | `x < 0` → `ValueError` |
| `cbrt(x)` | 세제곱근 `∛x` | - |
| `log(x, base=10)` | 로그 (기본: 상용로그) | `x <= 0` → `ValueError` |
| `ln(x)` | 자연로그 `ln(x)` | `x <= 0` → `ValueError` |
| `exp(x)` | 자연 지수 `e^x` | - |

### 2.3 삼각함수

각도 입력 단위는 기본값 **라디안(radian)**이며, `degree=True` 옵션으로 도(degree) 입력도 지원한다.

| 메서드 | 설명 |
|---|---|
| `sin(x, degree=False)` | 사인 |
| `cos(x, degree=False)` | 코사인 |
| `tan(x, degree=False)` | 탄젠트 |
| `asin(x, degree=False)` | 역사인 (arcsin) |
| `acos(x, degree=False)` | 역코사인 (arccos) |
| `atan(x, degree=False)` | 역탄젠트 (arctan) |
| `atan2(y, x, degree=False)` | 2인수 역탄젠트 |

### 2.4 쌍곡선 함수

| 메서드 | 설명 |
|---|---|
| `sinh(x)` | 쌍곡선 사인 |
| `cosh(x)` | 쌍곡선 코사인 |
| `tanh(x)` | 쌍곡선 탄젠트 |

### 2.5 수 이론 및 변환

| 메서드 | 설명 | 예외 처리 |
|---|---|---|
| `factorial(n)` | 팩토리얼 `n!` | `n < 0` 또는 비정수 → `ValueError` |
| `gcd(a, b)` | 최대공약수 | - |
| `lcm(a, b)` | 최소공배수 | - |
| `abs_val(x)` | 절댓값 | - |
| `ceil(x)` | 올림 | - |
| `floor(x)` | 내림 | - |
| `round_val(x, ndigits=0)` | 반올림 | - |

### 2.6 연산 히스토리

| 메서드 | 설명 |
|---|---|
| `history()` | 최근 연산 목록 반환 (연산식 + 결과) |
| `clear_history()` | 히스토리 초기화 |
| `last_result()` | 마지막 연산 결과 반환 |

---

## 3. 비기능 요구사항

- **언어**: Python 3.10 이상
- **의존성**: 표준 라이브러리만 사용 (`math`, `cmath` 허용), 외부 패키지 없음
- **정밀도**: 부동소수점 연산은 Python 기본 `float` 정밀도 (IEEE 754) 준수
- **스레드 안전성**: 단일 인스턴스 단일 스레드 사용 기준 (멀티스레드 미지원)
- **테스트**: 각 메서드에 대한 단위 테스트 작성 (`unittest` 또는 `pytest`)

---

## 4. 클래스 인터페이스 (설계 초안)

```python
class Calculator:
    def __init__(self, history_limit: int = 100): ...

    # 사칙연산
    def add(self, a: float, b: float) -> float: ...
    def subtract(self, a: float, b: float) -> float: ...
    def multiply(self, a: float, b: float) -> float: ...
    def divide(self, a: float, b: float) -> float: ...
    def modulo(self, a: float, b: float) -> float: ...
    def power(self, base: float, exp: float) -> float: ...

    # 제곱근 및 로그
    def sqrt(self, x: float) -> float: ...
    def cbrt(self, x: float) -> float: ...
    def log(self, x: float, base: float = 10) -> float: ...
    def ln(self, x: float) -> float: ...
    def exp(self, x: float) -> float: ...

    # 삼각함수
    def sin(self, x: float, degree: bool = False) -> float: ...
    def cos(self, x: float, degree: bool = False) -> float: ...
    def tan(self, x: float, degree: bool = False) -> float: ...
    def asin(self, x: float, degree: bool = False) -> float: ...
    def acos(self, x: float, degree: bool = False) -> float: ...
    def atan(self, x: float, degree: bool = False) -> float: ...
    def atan2(self, y: float, x: float, degree: bool = False) -> float: ...

    # 쌍곡선 함수
    def sinh(self, x: float) -> float: ...
    def cosh(self, x: float) -> float: ...
    def tanh(self, x: float) -> float: ...

    # 수 이론 및 변환
    def factorial(self, n: int) -> int: ...
    def gcd(self, a: int, b: int) -> int: ...
    def lcm(self, a: int, b: int) -> int: ...
    def abs_val(self, x: float) -> float: ...
    def ceil(self, x: float) -> int: ...
    def floor(self, x: float) -> int: ...
    def round_val(self, x: float, ndigits: int = 0) -> float: ...

    # 히스토리
    def history(self) -> list[dict]: ...
    def clear_history(self) -> None: ...
    def last_result(self) -> float | None: ...
```

---

## 5. 예외 정책

| 상황 | 예외 타입 | 메시지 예시 |
|---|---|---|
| 0으로 나누기 | `ZeroDivisionError` | `"Division by zero"` |
| 음수 제곱근 | `ValueError` | `"sqrt of negative number"` |
| 비정수 팩토리얼 | `ValueError` | `"factorial requires non-negative integer"` |
| 로그의 비양수 입력 | `ValueError` | `"log requires positive number"` |
| 잘못된 타입 | `TypeError` | `"operands must be numeric"` |

---

## 6. 파일 구조

```
calculator/
├── PRD.md
├── calculator.py        # Calculator 클래스 구현
├── test_calculator.py   # 단위 테스트
├── cli.py               # 대화형 CLI (REPL)
└── README.md            # 사용 예시
```

---

## 7. 완료 기준 (Definition of Done)

- [x] 모든 메서드 구현 완료
- [x] 각 메서드에 대한 정상 케이스 단위 테스트 통과
- [x] 각 예외 케이스에 대한 단위 테스트 통과
- [x] 타입 힌트 전체 적용
- [x] 외부 라이브러리 미사용
- [x] CLI (cli.py) 제공 — `pi`, `e` 상수 지원
