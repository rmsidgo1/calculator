#!/usr/bin/env python3
import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from calculator import Calculator

TRIG = {"sin", "cos", "tan", "asin", "acos", "atan", "atan2"}
CONSTANTS: dict[str, float] = {"pi": math.pi, "e": math.e}

HELP = """\
Arithmetic  : add, subtract, multiply, divide, modulo, power
Sqrt/Log    : sqrt, cbrt, log [base=10], ln, exp
Trig        : sin, cos, tan, asin, acos, atan, atan2 y x  [-d/--degree]
Hyperbolic  : sinh, cosh, tanh
Number      : factorial, gcd, lcm, abs_val, ceil, floor, round_val [ndigits=0]
History     : history, last, clear
Meta        : help [command], quit

Constants   : pi (3.14159...), e (2.71828...)

Type 'help <command>' for description and examples.
"""

# (usage, description, [(input_example, result_string), ...])
_CmdInfo = tuple[str, str, list[tuple[str, str]]]

COMMAND_INFO: dict[str, _CmdInfo] = {
    # ── Arithmetic ────────────────────────────────────────────────────────
    "add": (
        "add <a> <b>",
        "덧셈: a + b",
        [
            ("add 3 4",       "7"),
            ("add -1.5 2.5",  "1.0"),
            ("add pi e",      "5.8598..."),
        ],
    ),
    "subtract": (
        "subtract <a> <b>",
        "뺄셈: a - b",
        [
            ("subtract 10 3", "7"),
            ("subtract 0 5",  "-5"),
        ],
    ),
    "multiply": (
        "multiply <a> <b>",
        "곱셈: a * b",
        [
            ("multiply 6 7",   "42"),
            ("multiply e 2",   "5.4365..."),
            ("multiply pi 2",  "6.2831..."),
        ],
    ),
    "divide": (
        "divide <a> <b>",
        "나눗셈: a / b  (b=0 이면 ZeroDivisionError)",
        [
            ("divide 10 4", "2.5"),
            ("divide 1 3",  "0.3333..."),
        ],
    ),
    "modulo": (
        "modulo <a> <b>",
        "나머지: a % b  (b=0 이면 ZeroDivisionError)",
        [
            ("modulo 10 3", "1"),
            ("modulo 17 5", "2"),
        ],
    ),
    "power": (
        "power <base> <exp>",
        "거듭제곱: base ** exp",
        [
            ("power 2 10",  "1024"),
            ("power 4 0.5", "2.0"),
            ("power e 2",   "7.3890..."),
        ],
    ),
    # ── Sqrt / Log ────────────────────────────────────────────────────────
    "sqrt": (
        "sqrt <x>",
        "제곱근: sqrt(x)  (x < 0 이면 ValueError)",
        [
            ("sqrt 9", "3.0"),
            ("sqrt 2", "1.4142..."),
            ("sqrt 0", "0.0"),
        ],
    ),
    "cbrt": (
        "cbrt <x>",
        "세제곱근: cbrt(x)  (음수 입력 가능)",
        [
            ("cbrt 8",   "2.0"),
            ("cbrt -27", "-3.0"),
            ("cbrt 2",   "1.2599..."),
        ],
    ),
    "log": (
        "log <x> [base=10]",
        "로그: log_base(x)  기본 base=10 (상용로그)  (x <= 0 이면 ValueError)",
        [
            ("log 100",   "2.0"),
            ("log 8 2",   "3.0"),
            ("log e",     "0.4342..."),
        ],
    ),
    "ln": (
        "ln <x>",
        "자연로그: ln(x) = log_e(x)  (x <= 0 이면 ValueError)",
        [
            ("ln e",   "1.0"),
            ("ln 1",   "0.0"),
            ("ln 100", "4.6051..."),
        ],
    ),
    "exp": (
        "exp <x>",
        "자연 지수: e^x",
        [
            ("exp 0", "1.0"),
            ("exp 1", "2.7182...  (= e)"),
            ("exp 2", "7.3890..."),
        ],
    ),
    # ── Trigonometry ──────────────────────────────────────────────────────
    "sin": (
        "sin <x> [-d/--degree]",
        "사인: 기본 라디안. -d 플래그로 도(degree) 입력 가능.",
        [
            ("sin 0",     "0.0"),
            ("sin 90 -d", "1.0"),
            ("sin pi",    "~0.0  (π 라디안, 부동소수점 근사)"),
        ],
    ),
    "cos": (
        "cos <x> [-d/--degree]",
        "코사인: 기본 라디안. -d 플래그로 도(degree) 입력 가능.",
        [
            ("cos 0",      "1.0"),
            ("cos 180 -d", "-1.0"),
            ("cos pi",     "-1.0"),
        ],
    ),
    "tan": (
        "tan <x> [-d/--degree]",
        "탄젠트: 기본 라디안. -d 플래그로 도(degree) 입력 가능.",
        [
            ("tan 0",     "0.0"),
            ("tan 45 -d", "1.0"),
        ],
    ),
    "asin": (
        "asin <x> [-d/--degree]",
        "역사인(arcsin): 반환값 기본 라디안. -d 로 도(degree) 반환.",
        [
            ("asin 1",      "1.5707...  (= π/2)"),
            ("asin 1 -d",   "90.0"),
            ("asin 0.5 -d", "30.0"),
        ],
    ),
    "acos": (
        "acos <x> [-d/--degree]",
        "역코사인(arccos): 반환값 기본 라디안. -d 로 도(degree) 반환.",
        [
            ("acos -1",     "3.1415...  (= π)"),
            ("acos -1 -d",  "180.0"),
            ("acos 0.5 -d", "60.0"),
        ],
    ),
    "atan": (
        "atan <x> [-d/--degree]",
        "역탄젠트(arctan): 반환값 기본 라디안. -d 로 도(degree) 반환.",
        [
            ("atan 1",    "0.7853...  (= π/4)"),
            ("atan 1 -d", "45.0"),
        ],
    ),
    "atan2": (
        "atan2 <y> <x> [-d/--degree]",
        "2인수 역탄젠트: atan(y/x). 사분면을 고려. 반환값 기본 라디안.",
        [
            ("atan2 1 1",    "0.7853...  (= π/4)"),
            ("atan2 1 1 -d", "45.0"),
            ("atan2 1 0 -d", "90.0"),
        ],
    ),
    # ── Hyperbolic ────────────────────────────────────────────────────────
    "sinh": (
        "sinh <x>",
        "쌍곡선 사인: (e^x - e^-x) / 2",
        [
            ("sinh 0", "0.0"),
            ("sinh 1", "1.1752..."),
        ],
    ),
    "cosh": (
        "cosh <x>",
        "쌍곡선 코사인: (e^x + e^-x) / 2",
        [
            ("cosh 0", "1.0"),
            ("cosh 1", "1.5430..."),
        ],
    ),
    "tanh": (
        "tanh <x>",
        "쌍곡선 탄젠트: sinh(x) / cosh(x)  결과 범위: (-1, 1)",
        [
            ("tanh 0", "0.0"),
            ("tanh 1", "0.7615..."),
        ],
    ),
    # ── Number Theory / Conversion ────────────────────────────────────────
    "factorial": (
        "factorial <n>",
        "팩토리얼: n!  (n은 음이 아닌 정수, 비정수/음수면 ValueError)",
        [
            ("factorial 0",  "1"),
            ("factorial 5",  "120"),
            ("factorial 10", "3628800"),
        ],
    ),
    "gcd": (
        "gcd <a> <b>",
        "최대공약수: a와 b의 GCD",
        [
            ("gcd 12 8",   "4"),
            ("gcd 7 5",    "1"),
            ("gcd 100 75", "25"),
        ],
    ),
    "lcm": (
        "lcm <a> <b>",
        "최소공배수: a와 b의 LCM",
        [
            ("lcm 4 6", "12"),
            ("lcm 7 3", "21"),
        ],
    ),
    "abs_val": (
        "abs_val <x>",
        "절댓값: |x|",
        [
            ("abs_val -5",   "5"),
            ("abs_val 3.14", "3.14"),
        ],
    ),
    "ceil": (
        "ceil <x>",
        "올림: x 이상의 최소 정수",
        [
            ("ceil 2.1",  "3"),
            ("ceil -1.9", "-1"),
        ],
    ),
    "floor": (
        "floor <x>",
        "내림: x 이하의 최대 정수",
        [
            ("floor 2.9",  "2"),
            ("floor -1.1", "-2"),
        ],
    ),
    "round_val": (
        "round_val <x> [ndigits=0]",
        "반올림: x를 ndigits 소수점 자리로 반올림",
        [
            ("round_val 2.567 2", "2.57"),
            ("round_val 2.5",     "2"),
            ("round_val pi 4",    "3.1416"),
        ],
    ),
    # ── History ───────────────────────────────────────────────────────────
    "history": (
        "history",
        "지금까지의 연산 이력을 번호 순으로 출력한다.",
        [
            ("add 1 2",   "= 3"),
            ("multiply 3 4", "= 12"),
            ("history",   "1. add(1, 2) = 3 / 2. multiply(3, 4) = 12"),
        ],
    ),
    "last": (
        "last",
        "가장 최근 연산의 결과를 출력한다. 이력이 없으면 '(no result yet)'.",
        [
            ("add 10 5", "= 15"),
            ("last",     "= 15"),
        ],
    ),
    "clear": (
        "clear",
        "연산 이력을 전부 초기화한다.",
        [
            ("clear", "History cleared."),
        ],
    ),
    # ── Constants ─────────────────────────────────────────────────────────
    "pi": (
        "pi  (숫자 인수 위치에 사용)",
        f"원주율 π = {math.pi}",
        [
            ("sin pi",       "~0.0"),
            ("cos pi",       "-1.0"),
            ("multiply pi 2", "6.2831..."),
        ],
    ),
    "e": (
        "e  (숫자 인수 위치에 사용)",
        f"자연상수 e = {math.e}",
        [
            ("ln e",      "1.0"),
            ("exp 1",     "2.7182..."),
            ("power e 2", "7.3890..."),
        ],
    ),
}


def _show_command_help(cmd: str) -> None:
    info = COMMAND_INFO.get(cmd)
    if info is None:
        print(f"  '{cmd}' 에 대한 도움말이 없습니다. 'help' 로 전체 목록을 확인하세요.")
        return
    usage, desc, examples = info
    print(f"\n  {cmd}")
    print(f"  사용법 : {usage}")
    print(f"  설명   : {desc}")
    print("  예시   :")
    for expr, result in examples:
        print(f"    {expr:<26}->  {result}")
    print()


def to_num(s: str) -> int | float:
    if s.lower() in CONSTANTS:
        return CONSTANTS[s.lower()]
    f = float(s)
    return int(f) if f == int(f) else f


def main() -> None:
    calc = Calculator()
    print("Calculator CLI -- type 'help' for commands, 'quit' to exit.\n")

    while True:
        try:
            line = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)

        if not line:
            continue

        cmd, *rest = line.split()
        cmd = cmd.lower()

        if cmd in ("quit", "exit", "q"):
            sys.exit(0)

        if cmd in ("help", "h", "?"):
            if rest:
                _show_command_help(rest[0].lower())
            else:
                print(HELP)
            continue

        if cmd == "history":
            hist = calc.history()
            if not hist:
                print("  (empty)")
            else:
                for i, entry in enumerate(hist, 1):
                    print(f"  {i:3}. {entry['expression']} = {entry['result']}")
            continue

        if cmd == "last":
            r = calc.last_result()
            print(f"= {r}" if r is not None else "  (no result yet)")
            continue

        if cmd == "clear":
            calc.clear_history()
            print("  History cleared.")
            continue

        degree = "-d" in rest or "--degree" in rest
        nums_str = [t for t in rest if t not in ("-d", "--degree")]

        try:
            nums = [to_num(s) for s in nums_str]
        except ValueError:
            print("Error: invalid number in arguments")
            continue

        method = getattr(calc, cmd, None)
        if method is None:
            print(f"Error: unknown command '{cmd}'  (type 'help' for list)")
            continue

        try:
            result = method(*nums, degree=degree) if cmd in TRIG else method(*nums)
            print(f"= {result}")
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
