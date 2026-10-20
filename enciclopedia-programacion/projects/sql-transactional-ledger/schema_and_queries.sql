PRAGMA foreign_keys = ON;

CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    parent_id INTEGER REFERENCES accounts(account_id),
    normal_side TEXT NOT NULL CHECK (normal_side IN ('DEBIT', 'CREDIT'))
);

CREATE TABLE journal_entries (
    entry_id INTEGER PRIMARY KEY,
    posted_at TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE postings (
    posting_id INTEGER PRIMARY KEY,
    entry_id INTEGER NOT NULL REFERENCES journal_entries(entry_id) ON DELETE CASCADE,
    account_id INTEGER NOT NULL REFERENCES accounts(account_id),
    signed_cents INTEGER NOT NULL CHECK (signed_cents != 0)
);

INSERT INTO accounts VALUES
    (1, '1000', 'Activos', NULL, 'DEBIT'),
    (2, '1100', 'Tesorería Bancaria', 1, 'DEBIT'),
    (3, '1200', 'Cuentas por Cobrar', 1, 'DEBIT'),
    (4, '4000', 'Ingresos de Ingeniería', NULL, 'CREDIT');

BEGIN TRANSACTION;
INSERT INTO journal_entries VALUES (101, '2026-10-01T09:00:00Z', 'Factura licencia software');
INSERT INTO postings VALUES (1, 101, 3, 250000), (2, 101, 4, -250000);

INSERT INTO journal_entries VALUES (102, '2026-10-05T14:30:00Z', 'Cobro parcial transferencia');
INSERT INTO postings VALUES (3, 102, 2, 150000), (4, 102, 3, -150000);
COMMIT;
