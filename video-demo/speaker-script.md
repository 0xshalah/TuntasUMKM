# TUNTASUMKM — SPEAKING SCRIPT & DASHBOARD GUIDE
## Video Demo AI HackFest 2026

---

## CARA BUKA VISUAL DASHBOARD

### Prerequisites
1. **Backend running** di port 8765:
   ```bash
   cd C:\Users\Shalahuddin\Downloads\tuntas-lagi-main\backend
   .venv\Scripts\python.exe server.py
   ```
   Tunggu log: `Uvicorn running on http://0.0.0.0:8765`

2. **Frontend running** di port 3000:
   ```bash
   cd C:\Users\Shalahuddin\Downloads\tuntas-lagi-main\frontend
   yarn start
   ```
   Tunggu log: `Compiled successfully!`

3. **Buka browser:**
   ```
   http://localhost:3000
   ```

4. **Verifikasi dashboard:**
   - Header: "TuntasUMKM"
   - Approval queue terlihat
   - Order list muncul

### Untuk Recording
- Buka browser di **fullscreen** (F11)
- Zoom **100%** (Ctrl+0)
- Resolution: **1920x1080**
- Browser: Chrome/Edge (recommended)

---

## FORMAT SKIP

Setiap slide punya **dua bagian yang jelas terpisah**:

```
[SLIDE: n]  →  Visual PPT yang ditampilkan di layar (baca ini)
[DEMO]      →  Demonstrasi langsung (buka dashboard/terminal)
```

**Aturan:**
- Mulai dengan visual PPT dulu untuk konteks
- Lalu pindah ke demonstrasi langsung untuk evidence
- Jangan gabungin — viewer butuh tahu kapan lihat slide, kapan lihat dashboard

---

## 3-LAYER BOUNDARY MODEL

```
┌──────────────────────┐
│     HUMAN / UI       │
│  Approve / Reject    │
└──────────┬───────────┘
           │ authorization
┌──────────▼───────────┐
│       BACKEND        │
│ transaction boundary │
│ stock / notification │
│ audit log            │
└──────────▲───────────┘
           │ MCP tools
┌──────────┴───────────┐
│    HERMES AGENT      │
│                      │
│ search_catalog       │
│ check_inventory      │
│ calculate_total      │
│ create_order_draft   │
└──────────────────────┘
```

**Layer 1 — Human / UI:** Manusia memegang keputusan final melalui UI. Approve / Reject adalah business authorization gate.

**Layer 2 — Backend:** Backend memastikan hanya order berstatus `pending_approval` yang bisa bertransisi. Double approval tidak mungkin. Stock tidak bisa negatif. Transaction effects (stock deduction, notification) dieksekusi di sini.

**Layer 3 — Hermes Agent (MCP Exposure):** Hermes hanya memuat 4 business capabilities. Transactional operations (approve, deduct_stock, send_customer_message) tidak tersedia di MCP tool registry.

**Important note:** Endpoint `/api/v1/orders/{id}/approve` saat ini belum memiliki authentication. Identity-level authorization belum diimplementasikan. Yang di-enforce adalah state-transition validity.

---

## SCENE 0 — HOOK (0:00 - 0:30)

**[SLIDE: 0] — Title slide TUNTASUMKM**

> "Masalahnya bukan AI bisa membuat order. Masalahnya adalah: berapa banyak akses yang seharusnya kita berikan ke AI sebelum AI bisa menghabiskan uang, mengubah stok, atau mengirim sesuatu ke customer?"
>
> "Di TuntasUMKM, AI diberi bounded business tools untuk discovery, calculation, dan draft creation. Transaction effects dijalankan oleh backend setelah human approval."

---

## SCENE 1 — SOLUTION (0:30 - 1:00)

**[SLIDE: 1] — Solution positioning**

> "TuntasUMKM adalah AI-assisted order management, bukan AI-autonomous."
>
> "Kami memisahkan agent capability dari transaction execution. Agent hanya mendapat bounded tools. Backend menjalankan side effects setelah state transition. Semua diaudit."

---

## SCENE 2 — ARCHITECTURE (1:00 - 1:30)

**[SLIDE: 2] — Architecture: 3-layer boundary**

> "Ini arsitektur TuntasUMKM dengan 3-layer boundary."
>
> "Layer 1 — Human / UI: Manusia memegang keputusan final. Layer 2 — Backend: Backend memvalidasi status sebelum menjalankan effects. Layer 3 — Hermes Agent: Hermes hanya memuat 4 business capabilities."

> "Boundary ini berasal dari capability separation, bukan hanya prompt instruction."

---

## SCENE 3 — USER INTENT (1:30 - 2:15)

**[SLIDE: 3] — User intent**

> "Customer mengirim pesan: 'Saya mau pesan Sarung Tenun Samarinda 1 pcs'."
>
> "Agent menerima intent ini dan mulai bekerja."

---

## SCENE 4 — AGENT EXECUTION (2:15 - 3:15)

**[SLIDE: 4] — Agent execution flow**

```
USER INTENT
    ↓
search_catalog
    ↓
check_inventory
    ↓
calculate_order_total
    ↓
create_order_draft
    ↓
PENDING APPROVAL
```

> "Agent memanggil tools secara sequential. Perhatikan output terakhir: bukan approved order. Agent berhenti di draft."

---

### [DEMO] — Live MCP execution (2:45 - 3:15)

**Action:** Buka terminal, jalankan Hermes agent.

**Langkah:**
1. Buka terminal baru
2. Jalankan: `hermes chat -q "Saya mau pesan Sarung Tenun Samarinda 1 pcs"`
3. Tunjukkan agent memanggil `search_catalog` → `create_order_draft`
4. Tunjukkan order ID yang dihasilkan
5. Buka browser ke `http://localhost:3000` — order baru muncul di approval queue

**Narasi:**

> "Ini live execution. Agent menerima intent, mencari produk, membuat draft order. Order baru langsung muncul di dashboard dengan status pending_approval."

---

## SCENE 5 — THE BOUNDARY (3:15 - 3:45)

**[SLIDE: 5] — Boundary: pending_approval**

> "Sampai sini AI berhenti."

> "Status: pending_approval. Tidak ada stock deduction. Tidak ada transaksi final. Order menunggu persetujuan manusia."

> "Di MCP tool registry, tidak ada approve_order, deduct_stock, send_customer_message. Ini bukan kebetulan — ini design decision."

---

## SCENE 6 — HUMAN APPROVAL (3:45 - 4:45)

**[SLIDE: 6] — Human approval flow**

> "Di sini keputusan transaksional berpindah ke manusia. Approval adalah backend operation yang dipicu dari human approval flow."

> "Backend enforce state-transition: hanya order berstatus pending_approval yang bisa bertransisi. Double approval tidak mungkin karena atomic update."

> "Honest note: endpoint approval saat ini belum memiliki authentication. Yang di-enforce adalah state-transition validity, bukan identity-level authorization."

---

### [DEMO] — UI dashboard approval (4:00 - 4:45)

**Action:** Buka browser ke `http://localhost:3000`, tunjukkan approval flow.

**Langkah:**
1. Buka Chrome/Edge ke `http://localhost:3000`
2. Klik order yang baru dibuat agent di approval queue
3. Tunjukkan order detail: product, SKU, quantity, price, status
4. Tunjukkan tombol "Approve" dan "Reject"
5. Klik "Approve"
6. Tunjukkan confirmation dialog dengan konsekuensi
7. Klik "Confirm"
8. Tunjukkan status berubah ke "approved"

**Narasi:**

> "Ini dashboard TuntasUMKM. Order yang dibuat agent muncul di sini. Pemilik UMKM review detail order, lalu approve atau reject. Keputusan ini yang menentukan apakah transaksi dilanjutkan."

---

## SCENE 7 — REAL EFFECT (4:45 - 5:15)

**[SLIDE: 7] — Stock transition: 5 → 4**

> "Setelah human approval, backend menjalankan transaction effects."

> "Stock: 5 → 4. Customer notified. Audit trail tercatat. Ini bukti bahwa side effects hanya terjadi setelah human approval."

---

### [DEMO] — Tampilkan evidence langsung di terminal (5:00 - 5:15)

**Action:** Buka terminal, jalankan query SQLite.

```bash
cd C:\Users\Shalahuddin\Downloads\tuntas-lagi-main\backend
.venv\Scripts\python.exe -c "
import sqlite3
conn = sqlite3.connect('tuntas.db')
cur = conn.cursor()

# Order detail
cur.execute(\"SELECT id, status, total_price FROM orders WHERE id='ORD-20260927-35BD8E'\")
row = cur.fetchone()
print(f'Order: {row[0]}')
print(f'Status: {row[1]}')
print(f'Total: Rp {row[2]:,}')

# Stock transition
cur.execute(\"SELECT stock FROM inventory WHERE sku='SRG-TNN-04'\")
stock = cur.fetchone()[0]
print(f'Current stock SRG-TNN-04: {stock}')

# Audit trail
cur.execute(\"SELECT actor, action, before_state, after_state FROM audit_logs WHERE order_id='ORD-20260927-35BD8E' ORDER BY at\")
for row in cur.fetchall():
    print(f'{row[0]:6} | {row[1]:20} | {row[2]} -> {row[3]}')
"
```

**Narasi:**

> "Ini data langsung dari database. Order sudah approved. Stock sudah deducted. Empat audit entries tercatat lengkap."

**Expected output:**
```
Order: ORD-20260927-35BD8E
Status: approved
Total: Rp 520,000
Current stock SRG-TNN-04: 4
agent  | create_draft         | None -> pending_approval
human  | APPROVE_ORDER        | pending_approval -> approved
agent  | DEDUCT_STOCK         | 5 -> 4
agent  | NOTIFY_CUSTOMER      | None -> sent
```

---

## SCENE 8 — AUDIT TRAIL (5:15 - 6:00)

**[SLIDE: 8] — Audit timeline: 4 entries with actor badges**

> "Empat entry audit trail. Setiap action tercatat dengan actor yang jelas."
>
> "Entry 1: agent — create_draft. Agent membuat draft order."
>
> "Entry 2: human — APPROVE_ORDER. Manusia approve via UI."
>
> "Entry 3: agent — DEDUCT_STOCK. Stock deduction 5 → 4 dieksekusi backend setelah approval."

> "Entry 4: agent — NOTIFY_CUSTOMER. Notifikasi dikirim backend setelah approval."

> "Actor agent untuk DEDUCT_STOCK dan NOTIFY_CUSTOMER merepresentasikan origin workflow — backend mengeksekusi side effects atas otorisasi human approval. Physical executor adalah backend, logical origin adalah agent workflow."

---

## SCENE 9 — ATTACK THE BOUNDARY (6:00 - 6:40)

**[SLIDE: 9] — Available vs Not Available tools**

```
Available tools:
✓ search_catalog
✓ check_inventory
✓ calculate_order_total
✓ create_order_draft

✗ approve_order
✗ deduct_stock
✗ send_customer_message
```

> "Bukan karena prompt-nya melarang agent. Tool-nya memang tidak ada di MCP registry."

> "Honest limitation: agent memiliki akses ke execute_code dan terminal. Secara teknis, agent bisa gunakan Python atau curl untuk HTTP request langsung ke backend. Ini known limitation — MCP boundary adalah model-awareness layer, bukan absolute security boundary. Security boundary yang sebenarnya ada di backend state-transition enforcement."

---

### [DEMO] — Coba minta agent approve order (6:15 - 6:40)

**Action:** Buka terminal, minta agent untuk approve order.

**Langkah:**
1. Buka terminal baru
2. Jalankan: `hermes chat -q "Approve order ORD-20260927-35BD8E"`
3. Tunjukkan agent mencari tool approve_order
4. Tunjukkan agent gagal karena tool tidak tersedia
5. Tunjukkan agent tidak bisa bypass

**Narasi:**

> "Sekarang saya coba minta agent untuk approve order. Perhatikan: agent mencari tool approve_order. Tool tidak tersedia di MCP registry. Agent tidak bisa approve melalui business tools."

---

## SCENE 10 — CLOSING (6:40 - 7:00)

**[SLIDE: 10] — Closing slide TUNTASUMKM**

> "TuntasUMKM tidak mencoba membuat AI melakukan semuanya. Kami membuat AI melakukan hal yang tepat, dan berhenti di tempat yang tepat."
>
> "Build Agent, Deliver Impact."

---

## RECORDING CHECKLIST

- [ ] Backend running di port 8765
- [ ] Frontend running di port 3000
- [ ] Browser fullscreen (F11)
- [ ] Zoom 100% (Ctrl+0)
- [ ] Resolution 1920x1080
- [ ] PPT file: `video-demo/TuntasUMKM-HackFest2026-v7.pptx`
- [ ] Script: `video-demo/speaker-script.md`
- [ ] No secrets visible di screen
- [ ] No .env files visible
- [ ] No API keys visible

---

## TIMING GUIDE

| Scene | Title | Duration | Cumulative |
|---|---|---|---|
| 0 | Hook | 0:30 | 0:00 |
| 1 | Solution | 0:30 | 0:30 |
| 2 | Architecture | 0:30 | 1:00 |
| 3 | User Intent | 0:45 | 1:30 |
| 4 | Agent Execution | 1:00 | 2:15 |
| 5 | The Boundary | 0:30 | 3:15 |
| 6 | Human Approval | 1:00 | 3:45 |
| 7 | Real Effect | 0:30 | 4:45 |
| 8 | Audit Trail | 0:45 | 5:15 |
| 9 | Attack the Boundary | 0:40 | 6:00 |
| 10 | Closing | 0:20 | 6:40 |

**Total: ~7:00 minutes**

---

## SLIDE vs DEMO REFERENCE

| Timestamp | Mode | What Viewer Sees |
|---|---|---|
| 0:00 - 0:30 | SLIDE 0 | Title slide |
| 0:30 - 1:00 | SLIDE 1 | Solution positioning |
| 1:00 - 1:30 | SLIDE 2 | Architecture: 3-layer boundary |
| 1:30 - 2:15 | SLIDE 3 | User intent |
| 2:15 - 2:45 | SLIDE 4 | Agent execution flow |
| 2:45 - 3:15 | DEMO | Terminal — live MCP execution |
| 3:15 - 3:45 | SLIDE 5 | Boundary: pending_approval |
| 3:45 - 4:00 | SLIDE 6 | Human approval flow |
| 4:00 - 4:45 | DEMO | UI dashboard — approval flow |
| 4:45 - 5:00 | SLIDE 7 | Stock transition |
| 5:00 - 5:15 | DEMO | Terminal — live DB query |
| 5:15 - 6:00 | SLIDE 8 | Audit timeline |
| 6:00 - 6:15 | SLIDE 9 | Available vs Not Available |
| 6:15 - 6:40 | DEMO | Terminal — attack the boundary |
| 6:40 - 7:00 | SLIDE 10 | Closing slide |

---

*Script generated: 2026-09-28*
*Project: TuntasUMKM — AI HackFest 2026*
