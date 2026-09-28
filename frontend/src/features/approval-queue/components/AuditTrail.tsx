import { Bot, User } from "lucide-react";
import { formatClock } from "@/lib/format";
import { APPROVAL } from "@/constants/testIds";
import type { AuditEntry } from "../types";

type ActorCategory = "AGENT" | "HUMAN";

const ACTOR_META: Record<ActorCategory, { label: string; icon: typeof Bot; badgeClass: string }> = {
  AGENT: { label: "Agent", icon: Bot, badgeClass: "bg-brand-sky text-brand-blue" },
  HUMAN: { label: "Human", icon: User, badgeClass: "bg-brand-mint text-brand-green" },
};

function categorizeActor(entry: AuditEntry): ActorCategory {
  return entry.actor === "human" ? "HUMAN" : "AGENT";
}

function actionLabel(action: string): string {
  const labels: Record<string, string> = {
    create_draft: "Created Draft",
    APPROVE_ORDER: "Approved Order",
    REJECT_ORDER: "Rejected Order",
    DEDUCT_STOCK: "Stock Deducted",
    NOTIFY_CUSTOMER: "Customer Notified",
    INBOUND_MESSAGE: "Inbound Message",
    AI_PARSE_MESSAGE: "AI Parsed Message",
  };
  return labels[action] ?? action;
}

function AuditRow({ entry }: { entry: AuditEntry }) {
  const category = categorizeActor(entry);
  const meta = ACTOR_META[category];
  const Icon = meta.icon;
  return (
    <li className="grid grid-cols-[auto_1fr_auto] items-start gap-3 py-2.5 text-xs">
      <time dateTime={entry.at} className="mt-0.5 font-mono tabular-nums text-brand-navy/50">{formatClock(entry.at)}</time>
      <span className="min-w-0">
        <span className="flex items-center gap-1.5">
          <span
            data-testid={`audit-actor-${category.toLowerCase()}`}
            className={`inline-flex items-center gap-1 rounded-sm px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-[0.08em] ${meta.badgeClass}`}
          >
            <Icon aria-hidden="true" className="h-3 w-3" />
            {meta.label}
          </span>
          <span className="font-semibold text-brand-navy">{actionLabel(entry.action)}</span>
        </span>
        <span className="mt-0.5 block font-mono text-[11px] text-brand-navy/50">
          {entry.orderId} · {entry.before} → {entry.after}
        </span>
      </span>
    </li>
  );
}

export function AuditTrail({ entries }: { entries: AuditEntry[] }) {
  return (
    <section data-testid={APPROVAL.audit} aria-labelledby="audit-heading" className="rounded-lg bg-white p-5 shadow-brand-rest">
      <h2 id="audit-heading" className="font-display text-base font-bold text-brand-navy">Audit Log</h2>
      {entries.length === 0 ? (
        <p className="mt-3 text-sm text-brand-navy/60">Belum ada keputusan di sesi ini. Setiap Approve/Reject tercatat di sini.</p>
      ) : (
        <ol aria-live="polite" className="mt-2 divide-y divide-brand-navy/5 lg:max-h-[220px] lg:overflow-y-auto">
          {entries.slice(0, 12).map((e) => <AuditRow key={e.id} entry={e} />)}
        </ol>
      )}
    </section>
  );
}
