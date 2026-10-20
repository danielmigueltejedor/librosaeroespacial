#!/usr/bin/env python3
"""Verifica integridad contable de partida doble, CTE recursivas y funciones ventana en SQLite 3.54."""
from __future__ import annotations

import sqlite3
from pathlib import Path


def run_verification() -> dict[str, object]:
    sql_path = Path(__file__).with_name("schema_and_queries.sql")
    conn = sqlite3.connect(":memory:")
    conn.executescript(sql_path.read_text(encoding="utf-8"))

    # 1. Invariante de suma cero por asiento (partida doble)
    unbalanced = conn.execute(
        "SELECT entry_id, SUM(signed_cents) FROM postings GROUP BY entry_id HAVING SUM(signed_cents) != 0"
    ).fetchall()
    assert unbalanced == [], f"Asientos descuadrados: {unbalanced}"

    # 2. CTE recursiva para jerarquía de cuentas y agregación por árbol
    hierarchy = conn.execute(
        """
        WITH RECURSIVE tree(account_id, root_code, depth) AS (
            SELECT account_id, code, 0 FROM accounts WHERE parent_id IS NULL
            UNION ALL
            SELECT a.account_id, t.root_code, t.depth + 1
            FROM accounts a JOIN tree t ON a.parent_id = t.account_id
        )
        SELECT t.root_code, SUM(p.signed_cents)
        FROM tree t JOIN postings p ON p.account_id = t.account_id
        GROUP BY t.root_code
        ORDER BY t.root_code
        """
    ).fetchall()
    assert hierarchy == [("1000", 250000), ("4000", -250000)], hierarchy

    # 3. Función ventana (Window Function) para saldo acumulado de Cuentas por Cobrar
    running = conn.execute(
        """
        SELECT j.entry_id, p.signed_cents,
               SUM(p.signed_cents) OVER (
                   PARTITION BY p.account_id
                   ORDER BY j.posted_at, j.entry_id
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
               ) AS running_balance
        FROM postings p
        JOIN journal_entries j ON j.entry_id = p.entry_id
        WHERE p.account_id = 3
        ORDER BY j.entry_id
        """
    ).fetchall()
    assert running == [(101, 250000, 250000), (102, -150000, 100000)], running
    conn.close()
    return {"status": "verified", "sqlite_version": sqlite3.sqlite_version, "running_balance_final_cents": 100000}


if __name__ == "__main__":
    print(run_verification())
