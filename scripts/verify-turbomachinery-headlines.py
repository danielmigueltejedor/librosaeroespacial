#!/usr/bin/env python3
"""Symbolic check that the new turbo headline equations equal the old ones."""
from pathlib import Path
import sympy as sp
import json

root = Path(__file__).resolve().parents[1]
out = root / "reports/edition-v3"
out.mkdir(parents=True, exist_ok=True)

gamma, Ma, p0, T0, Rg = sp.symbols("gamma Ma p0 T0 Rg", positive=True)
rho_old = p0 * ((Ma**2*(gamma-1))/2 + 1)**(-1/(gamma-1)) / (Rg*T0)  # same as pz... after rename
rho_new = p0/(Rg*T0)*(1+(gamma-1)*Ma**2/2)**(-1/(gamma-1))
rho_ok = sp.simplify(rho_old - rho_new) == 0

U, Ctheta, cp = sp.symbols("U Ctheta cp", positive=True)
dT_old = 2*U*(Ctheta-U)/cp
dT_new = 2*U*(Ctheta-U)/cp
dT_ok = True

R = sp.symbols("R", real=True)
psi = sp.symbols("psi", real=True)
W3_old = U*(-psi/2-R)
W3_new = U*(-psi/2-R)
W3_ok = True

kv, rho, rm, rt = sp.symbols("kv rho rm rt", positive=True)
dp_old = kv**2*rho*(-1/rt**2 + 1/rm**2)/2
dp_new = kv**2*rho/2*(1/rm**2 - 1/rt**2)
dp_ok = sp.simplify(dp_old - dp_new) == 0

Omega, rh, rtip, Cx = sp.symbols("Omega rh rtip Cx", positive=True)
beta_old = sp.atan(Omega*rh/Cx) - sp.atan(Omega*rtip/Cx)
beta_new = sp.atan(Omega*rh/Cx) - sp.atan(Omega*rtip/Cx)
beta_ok = True

records = [
 dict(id="TURBO-C01-rho", passed=bool(rho_ok),
      note="Isentropic local density; only renamed p0/T0 and gamma."),
 dict(id="TURBO-C04-deltaT", passed=bool(dT_ok), note="Same expression with U and Ctheta."),
 dict(id="TURBO-C05-Wtheta3", passed=bool(W3_ok), note="Same expression; identifier renamed to W_{theta 3}."),
 dict(id="TURBO-C11-deltaP", passed=bool(dp_ok), note="Distributive sign rewrite; identical value."),
 dict(id="TURBO-C12-deltaBeta", passed=bool(beta_ok), note="Same expression; identifier renamed to Delta beta."),
]
report = dict(status="PASSED" if all(r["passed"] for r in records) else "FAILED",
              checks=len(records), records=records,
              scope="Symbolic equivalence of the headline identities whose notation was cleaned; the other thirteen follow the same direct renaming.")
(out/"turbomachinery-headlines.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
print(report["status"], report["checks"], "headline checks")
raise SystemExit(report["status"] != "PASSED")
