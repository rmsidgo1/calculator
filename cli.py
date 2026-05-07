#!/usr/bin/env python3
import math
import sys

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
Meta        : help, quit

Constants   : pi (3.14159...), e (2.71828...)

Examples:
  add 3 4        -> 7
  sin pi         -> 0.0 (approx)
  sin 90 -d      -> 1.0
  log e          -> 0.434...
  multiply e 2   -> 5.436...
  log 1000       -> 3.0
  atan2 1 1 -d   -> 45.0
"""


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
            print(f"Error: invalid number in arguments")
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
