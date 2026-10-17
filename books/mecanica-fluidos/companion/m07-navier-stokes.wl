(* Practica 7. Navier-Stokes y metodos numericos: arranque de un flujo de Couette y primer
   problema de Stokes. Solucion analitica, NDSolve por el metodo de lineas y sensibilidad.
   Codigo original. *)

(* == Bloque A: arranque de Couette; ecuacion, condiciones y solucion en serie == *)
ClearAll["Global`*"];
nu = 1.0*^-6; h = 0.010; U = 0.10;          (* agua, holgura de 10 mm, placa inferior a 0,1 m/s *)
(* u_t = nu u_yy,  u(0,t) = U (placa movil), u(h,t) = 0 (placa fija), u(y,0) = 0 *)
serie[y_, t_, nmax_: 40] := U (1 - y/h) - (2 U/Pi) Sum[If[n^2 Pi^2 nu t/h^2 < 700, Exp[-n^2 Pi^2 nu t/h^2], 0] Sin[n Pi y/h]/n, {n, 1, nmax}];
Print["A: tiempo viscoso h^2/nu = ", h^2/nu, " s"];
serieSim[y_, t_] := U (1 - y/h) - (2 U/Pi) Sum[Exp[-n^2 Pi^2 nu t/h^2] Sin[n Pi y/h]/n, {n, 1, 20}];
Print["A: comprobacion de la serie (20 terminos): residuo de la EDP en (h/3, 10 s) = ",
  (D[serieSim[y, t], t] - nu D[serieSim[y, t], {y, 2}]) /. {y -> h/3, t -> 10.}];

(* == Bloque B: solucion numerica con NDSolve (metodo de lineas) == *)
resolver[pts_] := NDSolveValue[{D[u[y, t], t] == nu D[u[y, t], {y, 2}], u[0, t] == U, u[h, t] == 0,
     u[y, 0] == If[y == 0, U, 0]}, u, {y, 0, h}, {t, 0, 200},
   Method -> {"MethodOfLines", "SpatialDiscretization" -> {"TensorProductGrid", "MinPoints" -> pts, "MaxPoints" -> pts}}];
sol = resolver[101];
errores = Table[Abs[sol[yy, tt] - serie[yy, tt]], {tt, {5., 20., 60.}}, {yy, h/10, 9 h/10, h/10}];
Print["B: error maximo frente a la serie en t = 5, 20, 60 s: ", Max /@ errores, " m/s"];
figB = Plot[Evaluate[Table[sol[y, tt], {tt, {2, 10, 30, 60, 200}}]], {y, 0, h},
   PlotLegends -> {"t = 2 s", "10 s", "30 s", "60 s", "200 s"}, AxesLabel -> {"y (m)", "u (m/s)"}, ImageSize -> 400];
Export["figures/m07-arranque.png", Rasterize[figB, Background -> White, ImageResolution -> 96]];

(* == Bloque C: establecimiento del esfuerzo en la placa fija == *)
tauFija[t_?NumericQ] := -(10^-3) Derivative[1, 0][sol][h, t];      (* mu = 1e-3 Pa s *)
tauEst = 10^-3 U/h;
razonSerie[t_?NumericQ] := 1 + 2 Sum[(-1)^n If[n^2 Pi^2 nu t/h^2 < 700, Exp[-n^2 Pi^2 nu t/h^2], 0], {n, 1, 40}];
Print["C: tau/tau_est en t = 10, 30, 60 s, NDSolve: ", Table[tauFija[tt]/tauEst, {tt, {10., 30., 60.}}], " ; serie: ", Table[razonSerie[tt], {tt, {10., 30., 60.}}]];
t99 = t /. FindRoot[tauFija[t] == 0.99 tauEst, {t, 60}];
t99an = t /. FindRoot[razonSerie[t] == 0.99, {t, 40, 70}, Method -> "Brent"];
Print["C: t para el 99 % del esfuerzo: NDSolve = ", t99, " s, serie = ", t99an, " s = ", t99an nu/h^2, " h^2/nu"];
(* Un error del 0,1 % en el esfuerzo desplaza el instante del 99 % en mas de un segundo: cerca de una
   asintota, un tiempo de cruce es una magnitud mal condicionada. *)

(* == Bloque D: sensibilidad a la malla y al parametro nu == *)
Print["D: u(h/2, 20 s) con 11, 21, 51 y 101 puntos: ", Table[resolver[n][h/2, 20.], {n, {11, 21, 51, 101}}], " ; serie: ", serie[h/2, 20.]];
Print["D: u(h/2, 20 s) con nu x 0.5, 1, 2: ", Table[Block[{nu = f 1.0*^-6}, resolver[51][h/2, 20.]], {f, {0.5, 1, 2}}]];

(* == Bloque E: primer problema de Stokes (placa en un fluido semi-infinito) == *)
stokes[y_, t_] := U Erfc[y/(2 Sqrt[nu t])];
solS = NDSolveValue[{D[w[y, t], t] == nu D[w[y, t], {y, 2}], w[0, t] == U, w[0.05, t] == 0, w[y, 0] == If[y == 0, U, 0]},
   w, {y, 0, 0.05}, {t, 0, 100}];
Print["E: espesor 1 % (y donde u = 0.01 U) en t = 100 s: ", y /. FindRoot[stokes[y, 100.] == 0.01 U, {y, 0.02}], " m; 3.64 sqrt(nu t) = ", 3.64 Sqrt[nu 100.]];
Print["E: error maximo NDSolve frente a erfc en t = 100 s: ", Max[Table[Abs[solS[yy, 100.] - stokes[yy, 100.]], {yy, 0, 0.03, 0.001}]], " m/s"];
