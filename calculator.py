import math


class Calculator:
    def __init__(self, history_limit: int = 100) -> None:
        self._history: list[dict] = []
        self._history_limit = history_limit

    def _record(self, expression: str, result: float | int | None) -> None:
        self._history.append({"expression": expression, "result": result})
        if len(self._history) > self._history_limit:
            self._history.pop(0)

    # 2.1 기본 사칙연산

    def add(self, a: float, b: float) -> float:
        result = a + b
        self._record(f"add({a}, {b})", result)
        return result

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self._record(f"subtract({a}, {b})", result)
        return result

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self._record(f"multiply({a}, {b})", result)
        return result

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        result = a / b
        self._record(f"divide({a}, {b})", result)
        return result

    def modulo(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        result = a % b
        self._record(f"modulo({a}, {b})", result)
        return result

    def power(self, base: float, exp: float) -> float:
        result = base ** exp
        self._record(f"power({base}, {exp})", result)
        return result

    # 2.2 제곱근 및 로그

    def sqrt(self, x: float) -> float:
        if x < 0:
            raise ValueError("sqrt of negative number")
        result = math.sqrt(x)
        self._record(f"sqrt({x})", result)
        return result

    def cbrt(self, x: float) -> float:
        result = math.copysign(abs(x) ** (1 / 3), x)
        self._record(f"cbrt({x})", result)
        return result

    def log(self, x: float, base: float = 10) -> float:
        if x <= 0:
            raise ValueError("log requires positive number")
        result = math.log(x, base)
        self._record(f"log({x}, {base})", result)
        return result

    def ln(self, x: float) -> float:
        if x <= 0:
            raise ValueError("log requires positive number")
        result = math.log(x)
        self._record(f"ln({x})", result)
        return result

    def exp(self, x: float) -> float:
        result = math.exp(x)
        self._record(f"exp({x})", result)
        return result

    # 2.3 삼각함수

    def sin(self, x: float, degree: bool = False) -> float:
        if degree:
            x = math.radians(x)
        result = math.sin(x)
        self._record(f"sin({x}, degree={degree})", result)
        return result

    def cos(self, x: float, degree: bool = False) -> float:
        if degree:
            x = math.radians(x)
        result = math.cos(x)
        self._record(f"cos({x}, degree={degree})", result)
        return result

    def tan(self, x: float, degree: bool = False) -> float:
        if degree:
            x = math.radians(x)
        result = math.tan(x)
        self._record(f"tan({x}, degree={degree})", result)
        return result

    def asin(self, x: float, degree: bool = False) -> float:
        result = math.asin(x)
        if degree:
            result = math.degrees(result)
        self._record(f"asin({x}, degree={degree})", result)
        return result

    def acos(self, x: float, degree: bool = False) -> float:
        result = math.acos(x)
        if degree:
            result = math.degrees(result)
        self._record(f"acos({x}, degree={degree})", result)
        return result

    def atan(self, x: float, degree: bool = False) -> float:
        result = math.atan(x)
        if degree:
            result = math.degrees(result)
        self._record(f"atan({x}, degree={degree})", result)
        return result

    def atan2(self, y: float, x: float, degree: bool = False) -> float:
        result = math.atan2(y, x)
        if degree:
            result = math.degrees(result)
        self._record(f"atan2({y}, {x}, degree={degree})", result)
        return result

    # 2.4 쌍곡선 함수

    def sinh(self, x: float) -> float:
        result = math.sinh(x)
        self._record(f"sinh({x})", result)
        return result

    def cosh(self, x: float) -> float:
        result = math.cosh(x)
        self._record(f"cosh({x})", result)
        return result

    def tanh(self, x: float) -> float:
        result = math.tanh(x)
        self._record(f"tanh({x})", result)
        return result

    # 2.5 수 이론 및 변환

    def factorial(self, n: int) -> int:
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            raise ValueError("factorial requires non-negative integer")
        result = math.factorial(n)
        self._record(f"factorial({n})", result)
        return result

    def gcd(self, a: int, b: int) -> int:
        result = math.gcd(a, b)
        self._record(f"gcd({a}, {b})", result)
        return result

    def lcm(self, a: int, b: int) -> int:
        result = math.lcm(a, b)
        self._record(f"lcm({a}, {b})", result)
        return result

    def abs_val(self, x: float) -> float:
        result = abs(x)
        self._record(f"abs_val({x})", result)
        return result

    def ceil(self, x: float) -> int:
        result = math.ceil(x)
        self._record(f"ceil({x})", result)
        return result

    def floor(self, x: float) -> int:
        result = math.floor(x)
        self._record(f"floor({x})", result)
        return result

    def round_val(self, x: float, ndigits: int = 0) -> float:
        result = round(x, ndigits)
        self._record(f"round_val({x}, {ndigits})", result)
        return result

    # 2.6 연산 히스토리

    def history(self) -> list[dict]:
        return list(self._history)

    def clear_history(self) -> None:
        self._history.clear()

    def last_result(self) -> float | None:
        if not self._history:
            return None
        return self._history[-1]["result"]
