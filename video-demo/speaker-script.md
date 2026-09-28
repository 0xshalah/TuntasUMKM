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
- Resolution: **1920×1080**
- Browser: Chrome/Edge (recommended)

---

## SPEAKING SCRIPT PER SLIDE

---

### SLIDE 0 — TITLE (0:00 - 0:30)

**[Visual: Title slide — TUNTASUMKM]**

> "Halo, selamat datang di demo TuntasUMKM. Nama saya Shalahuddin, dan saya akan mendemonstrasikan AI Agent-assisted order management untuk UMKM dengan bounded authority dan Human-in-the-Loop approval."
>
> "TuntasUMKM adalah sistem pemesanan yang menggunakan AI Agent untuk memahami intent customer, mencari produk, dan membuat draft order — tetapi keputusan transaksional tetap di tangan manusia."
>
> "Mari kita lihat masalahnya."

---

### SLIDE 1 — THE PROBLEM (0:30 - 1:15)

**[Visual: Problem flow — Channels → Chaos → Solution]**

> "UMKM menerima pesanan dari berbagai channel — WhatsApp, Instagram, Tokopedia. Setiap channel punya format berbeda, dan proses manual membuat pemilik UMKM kewalahan."
>
> "Automation bisa membantu memahami dan menyiapkan pesanan. Tapi keputusan transaksional — seperti approve order, deduct stock, kirim WhatsApp — membutuhkan kontrol yang jelas."
>
> "AI chatbot biasa bisa menghasilkan jawaban, tapi tidak bisa menjalankan workflow bisnis secara aman."
>
> "Solusinya: AI Agent dengan bounded authority dan Human-in-the-Loop."

---

### SLIDE 2 — ARCHITECTURE (1:15 - 2:15)

**[Visual: Architecture diagram — flow + capability panel]**

> "Ini arsitektur TuntasUMKM. Customer mengirim pesan — misalnya 'Saya mau pesan Sarung Tenun Samarinda 1 pcs'."
>
> "Hermes Agent menerima intent, lalu menggunakan MCP — Model Context Protocol — untuk mengakses bounded business tools."
>
> "Agent bisa: search_catalog, check_inventory, calculate_order_total, dan create_order_draft."
>
> "Agent TIDAK bisa: approve_order, reject_order, deduct_stock, send_customer_message. Semua transaksi final membutuhkan persetujuan manusia."
>
> "Setelah agent membuat draft, order masuk status pending_approval. Manusia review dan approve. Backend menjalankan transaction effect dan mencatat audit trail."

---

### SLIDE 3 — BOUNDED AUTHORITY (2:15 - 3:00)

**[Visual: Bounded authority — Agent zone vs Human zone]**

> "Ini yang membuat TuntasUMKM berbeda. Agent punya authority zone yang jelas — bisa query data bisnis dan membuat draft order, tapi berhenti di approval gate."
>
> "Human authority zone: approve atau reject order, deduct stock, send customer message. Semua keputusan transaksional ada di sini."
>
> "Agent tidak bisa override keputusan manusia. Agent tidak bisa langsung mutate database. Agent tidak bisa commit transaksi."
>
> "Ini bukan fully autonomous AI. Ini AI-assisted dengan human control."

---

### SLIDE 4 — HUMAN-IN-THE-LOOP (3:00 - 3:45)

**[Visual: HITL flow — Agent → Human → Backend]**

> "Ini alur Human-in-the-Loop. Agent membuat draft order dengan status pending_approval. Tidak ada stock deduction, tidak ada transaksi final."
>
> "Manusia review order detail di dashboard. Manusia approve atau reject. Keputusan manusia final."
>
> "Setelah approval, backend menjalankan: deduct stock, send customer notification, write audit log. Semua dalam satu transactional commit."
>
> "Agent tidak pernah menyentuh transaction lifecycle."

---

### SLIDE 5 — MCP TOOLS (3:45 - 4:30)

**[Visual: MCP tools — 4 tool cards + P2.5 usage]**

> "Ini 4 MCP tools yang tersedia untuk agent. Tiga read-only: search_catalog, check_inventory, calculate_order_total. Satu bounded write: create_order_draft."
>
> "create_order_draft hanya membuat order dengan status pending_approval. Tidak ada stock deduction, tidak ada approval, tidak ada WhatsApp."
>
> "Pada execution P2.5 yang sudah kita verifikasi, agent hanya menggunakan search_catalog dan create_order_draft. check_inventory dan calculate_order_total tersedia tapi tidak digunakan."
>
> "Agent memilih tool berdasarkan intent dan reasoning — bukan hardcoded sequence."

---

### SLIDE 6 — VERIFIED DEMO EVIDENCE (4:30 - 5:15)

**[Visual: Evidence — order card + stock transition + audit]**

> "Ini evidence dari P2.5 execution yang sudah diverifikasi. Order ID: ORD-20260927-35BD8E. Product: Sarung Tenun Samarinda, SKU: SRG-TNN-04, quantity 1, price Rp 520.000."
>
> "Pre-approval: status pending_approval, stock masih 3. Human approval: YES. Post-approval: stock 3 menjadi 2."
>
> "Audit trail: 4 entries. Agent create_draft, human APPROVE_ORDER, agent DEDUCT_STOCK, agent NOTIFY_CUSTOMER."
>
> "Semua tercatat. Semua bisa diaudit."

---

### SLIDE 7 — AUDIT TRAIL (5:15 - 6:00)

**[Visual: Audit timeline — 4 entries with actor badges]**

> "Ini audit trail lengkap. Empat entry dengan actor yang jelas."
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

### SLIDE 8 — SECURITY & SAFETY (6:00 - 6:45)

**[Visual: Security boundary — safe zone vs forbidden zone]**

> "Ini security boundary. Agent boundary: read-only queries, create draft orders, stop at approval gate."
>
> "Forbidden zone: direct database access, transactional commits, stock mutation, customer communication. Semua butuh human approval."
>
> "Agent tidak bisa bypass approval. Agent tidak bisa inject SQL. Agent tidak bisa access database langsung."
>
> "Ini design principle: least privilege, bounded authority, human gate."

---

### SLIDE 9 — WHY DIFFERENT (6:45 - 7:15)

**[Visual: Comparison — chatbot vs agent]**

> "Kenapa ini berbeda dari chatbot biasa? Chatbot generates text responses. TuntasUMKM Agent menjalankan workflow bisnis."
>
> "Chatbot: no tool integration, no business logic, no audit trail, cannot execute actions, no authority boundaries."
>
> "TuntasUMKM Agent: tool-calling via MCP, bounded business tools, Human-in-the-Loop gate, full audit trail, executes draft creation, clear authority boundaries."
>
> "Ini bukan AI yang bisa melakukan apa saja. Ini AI yang bisa melakukan hal yang tepat — dengan batas yang jelas."

---

### SLIDE 10 — CLOSING (7:15 - 7:45)

**[Visual: Closing slide — TUNTASUMKM]**

> "TuntasUMKM. AI Agent-assisted order management untuk UMKM."
>
> "Bounded authority. Human-in-the-Loop. Full audit trail."
>
> "Build Agent, Deliver Impact."
>
> "Terima kasih."

---

## RECORDING CHECKLIST

- [ ] Backend running di port 8765
- [ ] Frontend running di port 3000
- [ ] Browser fullscreen (F11)
- [ ] Zoom 100% (Ctrl+0)
- [ ] Resolution 1920×1080
- [ ] PPT file: `video-demo/TuntasUMKM-HackFest2026-v4.pptx`
- [ ] Script: `video-demo/speaker-script.md`
- [ ] No secrets visible di screen
- [ ] No .env files visible
- [ ] No API keys visible

---

## TIMING GUIDE

| Slide | Title | Duration | Cumulative |
|---|---|---|---|
| 0 | Title | 0:30 | 0:00 |
| 1 | The Problem | 0:45 | 0:30 |
| 2 | Architecture | 1:00 | 1:15 |
| 3 | Bounded Authority | 0:45 | 2:15 |
| 4 | Human-in-the-Loop | 0:45 | 3:00 |
| 5 | MCP Tools | 0:45 | 3:45 |
| 6 | Verified Demo Evidence | 0:45 | 4:30 |
| 7 | Audit Trail | 0:45 | 5:15 |
| 8 | Security & Safety | 0:45 | 6:00 |
| 9 | Why Different | 0:30 | 6:45 |
| 10 | Closing | 0:30 | 7:15 |

**Total: ~7:30 minutes**
