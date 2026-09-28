import { useState } from "react";
import { AlertTriangle, Check, Loader2, X } from "lucide-react";
import { APPROVAL } from "@/constants/testIds";
import { formatRupiah } from "@/lib/format";
import type { Inventory, Order } from "../types";

const BASE =
  "inline-flex flex-1 items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-semibold transition-[background-color,transform,opacity] duration-150 ease-out " +
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue focus-visible:ring-offset-2 active:scale-[0.97] motion-reduce:active:scale-100 disabled:cursor-wait disabled:opacity-60";

type DecisionActionsProps = {
  busy: boolean;
  order: Order;
  inventory: Inventory;
  onApprove: () => void;
  onReject: () => void;
};

function ApprovalConfirmation({ order, inventory, busy, onConfirm, onCancel }: {
  order: Order;
  inventory: Inventory;
  busy: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  const firstLine = order.lines[0];
  const product = firstLine ? inventory[firstLine.sku] : undefined;
  const total = order.lines.reduce((sum, line) => {
    const p = inventory[line.sku];
    return sum + (p?.price ?? 0) * line.quantity;
  }, 0);

  return (
    <div data-testid="approval-confirmation" className="rounded-md border border-brand-blue/20 bg-brand-sky/30 p-4">
      <p className="flex items-center gap-2 text-sm font-semibold text-brand-navy">
        <AlertTriangle aria-hidden="true" className="h-4 w-4 text-brand-blue" />
        Approve {order.id}?
      </p>
      <dl className="mt-3 space-y-1.5 text-xs">
        <div className="flex justify-between gap-4">
          <dt className="text-brand-navy/60">Product</dt>
          <dd className="font-medium text-brand-navy">{product?.name ?? order.lines[0]?.sku}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-brand-navy/60">Quantity</dt>
          <dd className="font-medium text-brand-navy">{order.lines.reduce((s, l) => s + l.quantity, 0)} pcs</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-brand-navy/60">Total</dt>
          <dd className="font-mono font-semibold text-brand-navy">{formatRupiah(total)}</dd>
        </div>
      </dl>
      <div data-testid={APPROVAL.consequencesSection} className="mt-3 rounded-sm bg-white/60 p-3">
        <p className="text-[11px] font-semibold uppercase tracking-[0.1em] text-brand-navy/60">Consequences</p>
        <ul className="mt-1.5 space-y-1 text-xs text-brand-navy">
          <li className="flex items-center gap-1.5">
            <Check aria-hidden="true" className="h-3 w-3 text-brand-green" />
            Order will become approved
          </li>
          <li className="flex items-center gap-1.5">
            <Check aria-hidden="true" className="h-3 w-3 text-brand-green" />
            Stock will be deducted
          </li>
          <li className="flex items-center gap-1.5">
            <Check aria-hidden="true" className="h-3 w-3 text-brand-green" />
            Customer will be notified
          </li>
        </ul>
      </div>
      <div className="mt-4 flex gap-2">
        <button
          type="button"
          data-testid={APPROVAL.approveCancelButton}
          onClick={onCancel}
          disabled={busy}
          className={`${BASE} border border-brand-navy/15 text-brand-navy hover:bg-brand-mist`}
        >
          <X aria-hidden="true" className="h-4 w-4" />
          Cancel
        </button>
        <button
          type="button"
          data-testid={APPROVAL.approveConfirmButton}
          onClick={onConfirm}
          disabled={busy}
          className={`${BASE} bg-brand-green text-white hover:bg-brand-navy`}
        >
          {busy ? <Loader2 aria-hidden="true" className="h-4 w-4 animate-spin" /> : <Check aria-hidden="true" className="h-4 w-4" />}
          {busy ? "Processing…" : "Confirm Approval"}
        </button>
      </div>
    </div>
  );
}

export function DecisionActions({ busy, order, inventory, onApprove, onReject }: DecisionActionsProps) {
  const [confirming, setConfirming] = useState(false);

  if (confirming) {
    return (
      <ApprovalConfirmation
        order={order}
        inventory={inventory}
        busy={busy}
        onConfirm={() => { setConfirming(false); onApprove(); }}
        onCancel={() => setConfirming(false)}
      />
    );
  }

  return (
    <>
      <button
        type="button"
        data-testid={APPROVAL.approveButton}
        onClick={() => setConfirming(true)}
        disabled={busy}
        className={`${BASE} bg-brand-green text-white hover:bg-brand-navy`}
      >
        <Check aria-hidden="true" className="h-4 w-4" />
        Approve
      </button>
      <button
        type="button"
        data-testid={APPROVAL.rejectButton}
        onClick={onReject}
        disabled={busy}
        className={`${BASE} border border-brand-navy/15 text-brand-navy hover:bg-brand-mist`}
      >
        <X aria-hidden="true" className="h-4 w-4" />
        Reject
      </button>
    </>
  );
}
