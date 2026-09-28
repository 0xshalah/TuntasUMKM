"""
TuntasUMKM MCP Server - P0 Proof of Concept

Exposes read-only tools: search_catalog, check_inventory
Queries the EXISTING TuntasUMKM SQLite database.
Uses stdio transport via FastMCP.
"""

import json
import sqlite3
from pathlib import Path

from fastmcp import FastMCP

# Resolve path to existing TuntasUMKM database
DB_PATH = Path(__file__).parent / "tuntas.db"

mcp = FastMCP("tuntasumkm")


@mcp.tool()
def search_catalog(query: str) -> str:
    """Search the TuntasUMKM product catalog by name, SKU, or keyword.

    Args:
        query: Search query (product name, SKU, or keyword)

    Returns:
        JSON string with matching products (sku, name, price, stock)
    """
    query = query.strip()
    if not query:
        return json.dumps({"error": "Empty query"})

    # Query the EXISTING TuntasUMKM SQLite database
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        # Case-insensitive search on name and sku
        cur = conn.execute(
            "SELECT sku, name, price, stock FROM inventory WHERE LOWER(name) LIKE ? OR LOWER(sku) LIKE ? ORDER BY sku",
            (f"%{query.lower()}%", f"%{query.lower()}%"),
        )
        rows = cur.fetchall()
        conn.close()

        products = [
            {"sku": row["sku"], "name": row["name"], "price": int(row["price"]), "stock": int(row["stock"])}
            for row in rows
        ]

        return json.dumps({"products": products, "count": len(products)})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def check_inventory(sku: str) -> str:
    """Check current inventory/stock for a specific product by SKU.

    Args:
        sku: Product SKU (e.g., "BTK-KRS-01")

    Returns:
        JSON string with product details (sku, name, price, stock)
    """
    sku = sku.strip()
    if not sku:
        return json.dumps({"error": "Empty SKU"})

    # Query the EXISTING TuntasUMKM SQLite database
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(
            "SELECT sku, name, price, stock FROM inventory WHERE sku = ?",
            (sku,),
        )
        row = cur.fetchone()
        conn.close()

        if row is None:
            return json.dumps({"error": f"Product with SKU '{sku}' not found"})

        product = {
            "sku": row["sku"],
            "name": row["name"],
            "price": int(row["price"]),
            "stock": int(row["stock"]),
        }

        return json.dumps({"product": product})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def calculate_order_total(sku: str, quantity: int) -> str:
    """Calculate the total price for a proposed order.

    Args:
        sku: Product SKU (e.g., "BTK-KRS-01")
        quantity: Number of units to order

    Returns:
        JSON string with order total details (sku, name, unit_price, quantity, subtotal)
    """
    sku = sku.strip()
    if not sku:
        return json.dumps({"error": "Empty SKU"})
    if quantity <= 0:
        return json.dumps({"error": "Quantity must be positive"})

    # Query the EXISTING TuntasUMKM SQLite database
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(
            "SELECT sku, name, price FROM inventory WHERE sku = ?",
            (sku,),
        )
        row = cur.fetchone()
        conn.close()

        if row is None:
            return json.dumps({"error": f"Product with SKU '{sku}' not found"})

        unit_price = int(row["price"])
        subtotal = unit_price * quantity

        result = {
            "sku": row["sku"],
            "name": row["name"],
            "unit_price": unit_price,
            "quantity": quantity,
            "subtotal": subtotal,
        }

        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def create_order_draft(sku: str, quantity: int) -> str:
    """Create a pending order draft that requires human approval.

    Args:
        sku: Product SKU (e.g., "BTK-KRS-01")
        quantity: Number of units to order

    Returns:
        JSON string with order draft details (order_id, sku, product_name,
        quantity, unit_price, subtotal, status)
    """
    sku = sku.strip()
    if not sku:
        return json.dumps({"error": "Empty SKU"})
    if quantity <= 0:
        return json.dumps({"error": "Quantity must be positive"})

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        # Look up product from existing inventory database
        cur = conn.execute(
            "SELECT sku, name, price, stock FROM inventory WHERE sku = ?",
            (sku,),
        )
        row = cur.fetchone()
        if row is None:
            return json.dumps({"error": f"Product with SKU '{sku}' not found"})

        product_name = row["name"]
        unit_price = int(row["price"])
        subtotal = unit_price * quantity

        # Generate unique order ID
        import uuid
        from datetime import datetime, timezone
        order_id = f"ORD-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        # Prepare order data
        lines_json = json.dumps([{"sku": sku, "quantity": quantity}])
        messages_json = json.dumps([
            {
                "id": f"{order_id}-m0",
                "sender": "bot",
                "text": f"Draft pesanan dibuat oleh agent MCP. Menunggu persetujuan pemilik toko.",
                "at": datetime.now(timezone.utc).isoformat(),
                "draftedBy": "agent:mcp"
            }
        ])

        # INSERT order draft (status = pending_approval)
        conn.execute(
            """INSERT INTO orders(id, customer_alias, channel, lines_json,
               status, reject_reason, total_price, received_at, messages_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                order_id,
                "Agent MCP (sintetis)",
                "MCP Agent",
                lines_json,
                "pending_approval",
                None,
                subtotal,
                datetime.now(timezone.utc).isoformat(),
                messages_json,
            ),
        )

        # INSERT audit log (actor = agent)
        audit_id = f"{order_id}-create-{uuid.uuid4().hex[:6]}"
        conn.execute(
            """INSERT INTO audit_logs(id, order_id, actor, action, before_state,
               after_state, note, at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                audit_id,
                order_id,
                "agent",
                "create_draft",
                "",
                "pending_approval",
                "Draft created by MCP agent tool",
                datetime.now(timezone.utc).isoformat(),
            ),
        )

        conn.commit()

        result = {
            "order_id": order_id,
            "sku": sku,
            "product_name": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": subtotal,
            "status": "pending_approval",
        }

        return json.dumps({"result": result})
    except Exception as e:
        conn.rollback()
        return json.dumps({"error": str(e)})
    finally:
        conn.close()


if __name__ == "__main__":
    mcp.run()
