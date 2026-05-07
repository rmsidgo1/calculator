---
name: test-verify
description: "test_calculator.py를 작성하고 pytest로 실행하여 Calculator 테스트를 검증한다. 테스트 작성, 단위 테스트 실행, 테스트 결과 확인 요청 시 반드시 이 스킬을 사용할 것."
---

# Test Verify 스킬

Calculator 클래스의 모든 메서드에 대한 단위 테스트를 작성하고 실행한다.

## 테스트 작성 원칙

### 정상 케이스
- 각 메서드마다 최소 2개 테스트 (일반값 + 경계값)
- 부동소수점 비교: `pytest.approx()` 또는 `assertAlmostEqual(places=10)` 사용
- 삼각함수: 라디안 모드 + degree=True 모드 각 1개씩

### 예외 케이스
```python
def test_divide_by_zero(self):
    with self.assertRaises(ZeroDivisionError):
        self.calc.divide(1, 0)

def test_sqrt_negative(self):
    with self.assertRaises(ValueError):
        self.calc.sqrt(-1)
```

### 히스토리 테스트
- 연산 후 `history()` 길이 확인
- `last_result()` 값 확인
- `clear_history()` 후 빈 리스트 확인
- `history_limit` 초과 시 오래된 항목 자동 제거 확인

## 실행 방법

```bash
# pytest 우선 시도
python -m pytest test_calculator.py -v --tb=short

# pytest 미설치 시
python -m unittest test_calculator -v
```

## 커버리지 기준

| 섹션 | 최소 테스트 수 |
|------|--------------|
| 사칙연산 (6개) | 12개 (정상 2 × 6) + 예외 3개 |
| 제곱근·로그 (5개) | 10개 + 예외 4개 |
| 삼각함수 (7개) | 14개 (rad/deg 각 1) + 예외 0 |
| 쌍곡선 (3개) | 6개 |
| 수이론·변환 (7개) | 14개 + 예외 2개 |
| 히스토리 (3개) | 6개 |

## 이전 산출물 처리

`test_calculator.py`가 이미 존재하면:
- 실행만 하고 결과 리포트 생성
- 실패 테스트가 있으면 원인 분석 후 리포트에 포함
- calculator.py가 변경되었으면 테스트 재작성 여부 판단
