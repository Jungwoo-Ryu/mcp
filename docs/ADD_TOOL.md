# MCP Tool 추가 가이드

이 프로젝트는 FastMCP 기준으로 **tool 파일만 추가 → import 한 줄**이면 등록됩니다.  
`server.py`를 건드릴 필요 없이 `tools/`만 확장하면 됩니다.

## 구조

```text
src/demo_mcp/
├── server.py              # FastMCP 인스턴스 + lifespan (보통 수정 안 함)
├── tools/
│   ├── __init__.py        # ← 새 모듈 import 추가
│   ├── echo.py            # 단순 툴 참고
│   ├── calculator.py      # Literal / 검증 참고
│   └── notes.py           # Context / lifespan 참고
├── resources/             # (선택)
└── prompts/               # (선택)
```

등록 흐름:

1. `tools/<name>.py`에서 `@mcp.tool`로 함수 데코레이트  
2. `tools/__init__.py`에서 그 모듈을 import  
3. `server.py`의 `_register_components()`가 `tools` 패키지를 import → 등록 완료  

## 새 툴 추가 (3단계)

### 1) 파일 생성

예: `src/demo_mcp/tools/booking.py`

```python
"""회의실 예약 툴 예시."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from demo_mcp.server import mcp


@mcp.tool
def book_meeting_room(
    room_id: Annotated[str, Field(description="회의실 ID")],
    start: Annotated[str, Field(description="시작 시각 ISO8601")],
    end: Annotated[str, Field(description="종료 시각 ISO8601")],
    title: Annotated[str, Field(description="회의 제목")] = "Untitled",
) -> dict[str, str]:
    """회의실을 예약합니다. 필수 인자가 모두 있을 때만 호출하세요."""
    # TODO: 실제 예약 API 호출
    return {
        "status": "booked",
        "room_id": room_id,
        "start": start,
        "end": end,
        "title": title,
    }
```

한 파일에 `@mcp.tool` 함수를 여러 개 둬도 됩니다.

### 2) import 등록

`src/demo_mcp/tools/__init__.py`에 모듈을 추가합니다.

```python
from demo_mcp.tools import booking, calculator, echo, notes

__all__ = ["booking", "calculator", "echo", "notes"]
```

### 3) 확인

```bash
# HTTP 서버 (기본 URL: http://127.0.0.1:8000/mcp)
uv run demo-mcp

# 테스트
uv run pytest -q
```

클라이언트의 `list_tools`에 `book_meeting_room`이 보이면 성공입니다.

코드 변경 후 서버가 떠 있다면 **재시작**해야 반영됩니다.

## 작성 규칙

| 항목 | 권장 |
|------|------|
| 데코레이터 | `@mcp.tool` |
| mcp 인스턴스 | `from demo_mcp.server import mcp` |
| 인자 설명 | `Annotated[..., Field(description="...")]` |
| docstring | 툴 설명으로 LLM에 노출됨 |
| 반환 타입 | `str` / `dict` / Pydantic 모델 등 JSON 직렬화 가능 타입 |
| 파일 단위 | 도메인별 한 파일 (`booking.py`, `calendar.py` …) |

### lifespan / 공유 상태가 필요할 때

`notes.py`처럼 `Context`를 받으면 됩니다. `ctx`는 클라이언트로 노출되지 않습니다.

```python
from fastmcp import Context

from demo_mcp.server import AppContext, mcp


@mcp.tool
async def my_tool(ctx: Context) -> str:
    app: AppContext = ctx.lifespan_context
    return app.store.get("greeting", "")
```

### 비동기

외부 API·DB 등 I/O가 있으면 `async def` + `@mcp.tool`을 그대로 사용합니다.

### 선택 인자 / 제한된 값

```python
from typing import Literal

@mcp.tool
def calculate(
    a: float,
    b: float,
    op: Annotated[Literal["+", "-", "*", "/"], Field(description="연산자")] = "+",
) -> float:
    """사칙연산."""
    ...
```

## 하지 말 것

- `server.py`에 툴 로직을 직접 몰아넣기  
- `tools/__init__.py` import를 빼먹고 파일이 “안 보이는” 상태 만들기  
- 필수 인자를 숨기거나 대충 채우기 — 스키마를 명확히 두고, 부족한 값은 **오케스트레이터 HITL**에서 수집  
- MCP 서버 안에서 채팅 UI / 승인 플로우를 직접 구현하기 (클라이언트·웹 책임)  

## 체크리스트

- [ ] `src/demo_mcp/tools/<name>.py` 생성  
- [ ] `@mcp.tool` + docstring + `Field(description=...)`  
- [ ] `tools/__init__.py`에 import 추가  
- [ ] 서버 재시작 후 `list_tools`에 이름 확인  
- [ ] (선택) `tests/`에 `Client(mcp)`로 `call_tool` 테스트 추가  

## 참고 구현

| 파일 | 볼 포인트 |
|------|-----------|
| `tools/echo.py` | 최소 형태, 기본값 인자 |
| `tools/calculator.py` | `Literal`, 에러 raise |
| `tools/notes.py` | `async`, `Context`, lifespan store |
| `server.py` | `_register_components()` — tools import만 하면 됨 |

## 테스트 추가 예시

`tests/test_server.py` 스타일:

```python
async def test_book_meeting_room(client):
    result = await client.call_tool(
        "book_meeting_room",
        {
            "room_id": "A-101",
            "start": "2026-07-14T10:00:00",
            "end": "2026-07-14T11:00:00",
            "title": "스탠드업",
        },
    )
    assert result.data["status"] == "booked"
```
