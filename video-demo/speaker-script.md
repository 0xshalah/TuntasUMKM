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

## SCENE 0 — HOOK (0:00 - 0:30)

**[SLIDE: 0] — Title slide TUNTASUMKM**

> "Masalahnya bukan AI bisa membuat order. Masalahnya adalah: berapa banyak akses yang seharusnya kita berikan ke AI sebelum AI bisa menghabiskan uang, mengubah stok, atau mengirim sesuatu ke customer?"
>
> "Di TuntasUMKM, AI boleh mencari, menghitung, dan membuat draft. Tapi AI tidak boleh menyelesaikan transaksi."

---

## SCENE 1 — SOLUTION (0:30 - 1:00)

**[SLIDE: 1] — Solution positioning**

> "TuntasUMKM adalah AI-assisted order management, bukan AI-autonomous."
>
> "AI Agent menerima intent customer, mencari produk, membuat draft order. Manusia memegang transaction gate. Backend menjalankan side effects. Semua diaudit."

---

## SCENE 2 — ARCHITECTURE (1:00 - 1:30)

**[SLIDE: 2] — Architecture diagram: flow + capability panel**

> "Ini arsitektur TuntasUMKM. Customer mengirim pesan. Hermes Agent menerima intent. Agent menggunakan bounded business tools untuk mencari produk dan membuat draft."
>
> "Agent TIDAK punya tool untuk approve, reject, deduct stock, atau send message. Authority boundary berasal dari capability access, bukan prompt instruction."

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
>
> "Status: pending_approval. Tidak ada stock deduction. Tidak ada transaksi final. Order menunggu persetujuan manusia."

---

## SCENE 6 — HUMAN APPROVAL (3:45 - 4:45)

**[SLIDE: 6] — Human approval flow**

> "Di sini keputusan transaksional berpindah ke manusia. Agent tidak memiliki capability untuk melakukan approval."

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
>
> "Stock: 5 → 4. Customer notified. Audit trail tercatat."

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
Current stock SRG-TNN-04: 2
agent  | create_draft         | None -> pending_approval
human  | APPROVE_ORDER        | pending_approval -> approved
agent  | DEDUCT_STOCK         | 3 -> 2
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
> "Entry 3: agent — DEDUCT_STOCK. Backend deduct stock setelah approval."
>
> "Entry 4: agent — NOTIFY_CUSTOMER. Backend kirim notification setelah approval."
>
> "Perhatikan: actor untuk DEDUCT_STOCK dan NOTIFY_CUSTOMER adalah agent, karena dieksekusi oleh backend flow setelah human approval. Tapi capability untuk deduct_stock dan send_customer_message tidak tersedia di MCP tool registry."

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

> "Bukan karena prompt-nya melarang agent. Tool-nya memang tidak tersedia."

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

> "Sekarang saya coba minta agent untuk approve order. Perhatikan: agent mencari tool approve_order. Tool tidak tersedia. Agent gagal. Bukan karena prompt melarang. Capability-nya memang tidak ada."

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
- [ ] PPT file: `video-demo/TuntasUMKM-HackFest2026-v4.pptx`
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
| 1:00 - 1:30 | SLIDE 2 | Architecture diagram |
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
