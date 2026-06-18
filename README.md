# Resume-JD Match MCP Server

An MCP server that compares your resume against a job description using
sentence embeddings (semantic similarity) + skill keyword matching, and
generates a visual skill-gap chart.

## Features

- **`match_score`** — Returns semantic similarity (0-100) plus matched/missing/extra skills
- **`generate_gap_chart_tool`** — Creates a PNG chart showing which JD skills you have vs. are missing
- **`suggest_bullet_points`** — Helps Claude draft resume bullet suggestions based on your real experience

## Setup

```bash
cd resume-mcp
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

First run will download the `all-MiniLM-L6-v2` embedding model (~80MB) —
needs internet access once.

## Test it locally (without Claude Desktop)

```bash
python test_local.py
```

## Connect to Claude Desktop

Edit your Claude Desktop config file:

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add this entry (use the FULL absolute path to your venv's python):

```json
{
  "mcpServers": {
    "resume-matcher": {
      "command": "/full/path/to/resume-mcp/venv/Scripts/python",
      "args": ["/full/path/to/resume-mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop. You should now be able to ask things like:

> "Compare my resume against this job description and show me the skill gap"

Claude will call `match_score` and `generate_gap_chart_tool` automatically.

