# Scene 05 — MCP Execution Recording Guide

## Duration
2:00–3:30 (90 seconds)

## Visual Target
Hermes terminal showing actual MCP tool execution

## What to Show

### Actual Execution Flow
1. Agent receives prompt
2. Agent calls `search_catalog` with "Sarung Tenun Samarinda"
3. Tool returns: SRG-TNN-04, Rp 520.000, stock 3
4. Agent calls `create_order_draft` with SRG-TNN-04, quantity 1
5. Tool returns: ORD-20260927-35BD8E, pending_approval

## Terminal Setup
- Same terminal as previous scenes
- Font size large enough for 1080p recording
- Scrolling enabled

## What Must Be Visible
- Tool call: `search_catalog` with arguments
- Tool result: product info (SKU, price, stock)
- Tool call: `create_order_draft` with arguments
- Tool result: order ID, status

## What Must Be Hidden
- check_inventory (NOT called in this execution)
- calculate_order_total (NOT called in this execution)
- Any retry/batch attempts (let them happen naturally, don't highlight)

## Narration
> "Agent memahami intent, mencari produk, kemudian membuat draft order. Lihat — agent memanggil `search_catalog`, mendapatkan `SRG-TNN-04` dengan harga Rp520.000. Kemudian agent memanggil `create_order_draft` dan membuat draft order.
>
> Agent menggunakan capability yang diberikan melalui MCP untuk mencari produk dan membuat draft order."

## Important Notes
- Do NOT add check_inventory or calculate_order_total to the visual
- If agent retries or batches, let it happen naturally
- Do NOT call it "agent learning"
- Record actual terminal output only

## Safety Check
- [ ] Actual terminal output only
- [ ] No fake tool calls
- [ ] No hardcoded order IDs
- [ ] No sensitive data
