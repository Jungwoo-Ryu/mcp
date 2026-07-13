# Demo FastMCP Server

로컬에서 FastMCP 서버 구조(tools / resources / prompts / lifespan)를 실험하기 위한 더미 프로젝트입니다.

**툴만 추가하려면 → [docs/ADD_TOOL.md](docs/ADD_TOOL.md)**

## 구조

```
src/demo_mcp/
├── server.py          # FastMCP 인스턴스 + lifespan + 등록 진입점
├── config.py          # 설정/시드 데이터
├── tools/             # @mcp.tool
│   ├── echo.py
│   ├── calculator.py
│   └── notes.py       # lifespan context 예시
├── resources/         # @mcp.resource
│   ├── config.py
│   └── notes.py
└── prompts/           # @mcp.prompt
    └── assistant.py
tests/
└── test_server.py     # Client(mcp) 인메모리 테스트
```

## 설치

```bash
uv sync --extra dev
```

## 테스트

```bash
uv run pytest -q
```

인메모리 `Client(mcp)`로 transport 없이 tools/resources/prompts를 검증합니다.

## 서버 실행

HTTP (기본):

```bash
uv run demo-mcp
```

서버 URL: `http://127.0.0.1:8000/mcp`

환경변수로 바꿀 수 있습니다.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DEMO_MCP_TRANSPORT` | `http` | `http` 또는 `stdio` |
| `DEMO_MCP_HOST` | `127.0.0.1` | 바인드 호스트 |
| `DEMO_MCP_PORT` | `8000` | 포트 |
| `DEMO_MCP_PATH` | `/mcp` | MCP 엔드포인트 경로 |

stdio:

```bash
DEMO_MCP_TRANSPORT=stdio uv run demo-mcp
```

## Cursor MCP 연결 예시

HTTP (서버를 먼저 `uv run demo-mcp`로 실행한 뒤):

```json
{
  "mcpServers": {
    "demo-mcp": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

이미 `.cursor/mcp.json`에 위 설정이 들어 있습니다.

## 포함된 더미 기능

| 종류 | 이름 | 설명 |
|------|------|------|
| tool | `echo`, `greet` | 단순 문자열 |
| tool | `add`, `calculate` | 사칙연산 |
| tool | `save_note`, `get_note`, `list_notes` | lifespan store |
| resource | `config://app` | 서비스 메타 |
| resource | `notes://{key}` | 시드 노트 |
| prompt | `summarize`, `code_review` | 프롬프트 템플릿 |
# mcp
