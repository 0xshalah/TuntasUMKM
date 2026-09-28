import { useState } from "react";
import { AlertTriangle, ChevronDown } from "lucide-react";
import { GoldCard } from "@/components/ui/gold-card";
import { APPROVAL } from "@/constants/testIds";
import { orderTitle, orderTotal } from "../order-math";
import { AiInsightPanel } from "./AiInsightPanel";
import { DecisionActions } from "./DecisionActions";
import { OrderLines } from "./OrderLines";
import { RejectReasonForm } from "./RejectReasonForm";
import type { ActionFailure, Inventory, Order } from "../types";

type OrderDecisionCardProps = {
  order: Order;
  inventory: Inventory;
  failure: ActionFailure | null;
  onApprove: (id: string) => Promise<boolean>;
  onReject: (id: string, reason: string) => Promise<boolean>;
};

function FailureNotice({ failure }: { failure: ActionFailure }) {
  return (
    <p role="alert" data-testid={APPROVAL.failureAlert} className="mt-4 flex items-start gap-2 rounded-md bg-brand-peach/30 px-3 py-2 text-xs text-brand-navy">
      <AlertTriangle aria-hidden="true" className="mt-0.5 h-3.5 w-3.5 shrink-0 text-destructive" />
      <span><code className="font-mono font-semibold">{failure.code}</code> {failure.message}</span>
    </p>
  );
}

function DisclosureSection({ id, title, children, defaultOpen = false }: {
  id: string;
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="border-t border-brand-navy/10 pt-3">
      <button
        type="button"
        aria-expanded={open}
        aria-controls={`${id}-content`}
        data-testid={id}
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between text-xs font-semibold uppercase tracking-[0.1em] text-brand-navy/60 transition-colors hover:text-brand-navy focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue focus-visible:ring-offset-2"
      >
        {title}
        <ChevronDown aria-hidden="true" className={`h-3.5 w-3.5 transition-transform duration-200 motion-reduce:transition-none ${open ? "rotate-180" : ""}`} />
      </button>
      <div
        id={`${id}-content`}
        className={`grid transition-[grid-template-rows,opacity] duration-200 ease-out motion-reduce:transition-none ${open ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"}`}
      >
        <div className={`overflow-hidden ${open ? "mt-3" : ""}`}>
          {children}
        </div>
      </div>
    </div>
  );
}

export function OrderDecisionCard({ order, inventory, failure, onApprove, onReject }: OrderDecisionCardProps) {
  const [rejecting, setRejecting] = useState(false);
  const [busy, setBusy] = useState(false);
  const pending = order.status === "pending_approval";

  async function decide(run: () => Promise<boolean>) {
    setBusy(true);
    const ok = await run();
    setBusy(false);
    if (ok) setRejecting(false);
  }

  const actions = rejecting
    ? <RejectReasonForm busy={busy} onCancel={() => setRejecting(false)} onConfirm={(reason) => void decide(() => onReject(order.id, reason))} />
    : <DecisionActions busy={busy} order={order} inventory={inventory} onApprove={() => void decide(() => onApprove(order.id))} onReject={() => setRejecting(true)} />;

  return (
    <GoldCard
      testId={APPROVAL.decisionCard}
      heading={orderTitle(order, inventory)}
      reference={order.id}
      state={{ status: "success", approval: order.status }}
      actions={pending ? actions : undefined}
    >
      {/* Primary info: always visible */}
      <div className="space-y-2">
        {order.lines.map((line) => {
          const product = inventory[line.sku];
          return (
            <div key={line.sku} className="flex items-start justify-between gap-3 text-sm">
              <span>
                <span className="block font-medium">{product?.name ?? line.sku}</span>
                <span className="font-mono text-xs text-brand-navy/60">{line.quantity} × {product?.price ?? 0}</span>
              </span>
              <span className="font-mono text-sm tabular-nums">{formatRupiah((product?.price ?? 0) * line.quantity)}</span>
            </div>
          );
        })}
        <p className="flex items-baseline justify-between border-t border-dashed border-brand-navy/15 pt-2">
          <span className="text-xs font-semibold uppercase tracking-[0.12em] text-brand-navy/60">Total</span>
          <span data-testid={APPROVAL.orderTotal} className="font-display text-lg font-extrabold tabular-nums text-brand-navy">{formatRupiah(orderTotal(order, inventory))}</span>
        </p>
      </div>

      {/* Progressive disclosure: AI Insight */}
      {order.aiInsight && (
        <div className="mt-4">
          <DisclosureSection id="disclosure-ai" title="AI Insight">
            <AiInsightPanel insight={order.aiInsight} />
          </DisclosureSection>
        </div>
      )}

      {/* Progressive disclosure: Order Details */}
      <div className="mt-3">
        <DisclosureSection id="disclosure-details" title="Order Details">
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-brand-navy/60">Order ID</span>
              <span className="font-mono">{order.id}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-brand-navy/60">Channel</span>
              <span>{order.channel}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-brand-navy/60">Customer</span>
              <span>{order.customerAlias}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-brand-navy/60">Received</span>
              <span className="font-mono">{new Date(order.receivedAt).toLocaleString("id-ID")}</span>
            </div>
          </div>
        </DisclosureSection>
      </div>

      {/* Reject reason */}
      {order.rejectReason && (
        <p data-testid={APPROVAL.rejectReasonText} className="mt-4 text-xs text-brand-navy/70">
          Alasan: <span className="font-semibold text-destructive">{order.rejectReason}</span>
        </p>
      )}

      {/* Failure notice */}
      {failure && failure.context.order_id === order.id && <FailureNotice failure={failure} />}
    </GoldCard>
  );
}

function formatRupiah(value: number): string {
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", minimumFractionDigits: 0 }).format(value);
}
