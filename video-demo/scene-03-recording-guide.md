# Scene 03 — Runtime / Infrastructure Recording Guide

## Duration
1:10–1:30 (20 seconds)

## Visual Target
Hermes terminal showing runtime information

## What to Show

### Command 1: Hermes Version
```bash
hermes --version
```
Expected output:
```
Hermes Agent v0.21.5+3432.gf039f02 (2026.9.24) · upstream f039f028
```

### Command 2: MCP Server List
```bash
hermes mcp list
```
Expected output:
```
MCP Servers:

  Name             Transport                      Tools        Status    
  ──────────────── ────────────────────────────── ──────────── ──────────
  tuntasumkm       C:\Users\Shalahuddin\Down...   4 selected   ✓ enabled
```

## Terminal Setup
- Font: JetBrains Mono or Fira Code
- Font size: 14-16px
- Background: Dark (#0a0a0a or default terminal)
- Window size: 1200×400 minimum

## What Must Be Visible
- Hermes version number
- MCP server name "tuntasumkm"
- "4 selected" tools count
- "✓ enabled" status

## What Must Be Hidden
- API keys
- .env contents
- Credentials
- Personal file paths (crop if needed)
- Password manager overlays

## Narration
> "Di sisi runtime, Hermes menjalankan agent loop dan MCP server terhubung sebagai subprocess. Backend TuntasUMKM berjalan sebagai service aplikasi dengan FastAPI dan SQLite."

## Safety Check
- [ ] No secrets visible
- [ ] No .env content
- [ ] No credentials
- [ ] No personal paths (or cropped)
- [ ] Clean terminal (no previous commands with sensitive data)
