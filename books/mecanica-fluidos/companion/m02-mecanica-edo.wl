(* Practica 2. Mecanica clasica y ecuaciones diferenciales: proyectil con resistencia,
   pendulo no lineal y vehiculo a potencia constante. Codigo original. *)

(* == Bloque A: proyectil sin resistencia (DSolve) == *)
ClearAll["Global`*"];
g = 9.81; v0 = 30.; th = 40 Degree;
solA = DSolve[{x''[t] == 0, y''[t] == -g, x[0] == 0, y[0] == 0,
    x'[0] == v0 Cos[th], y'[0] == v0 Sin[th]}, {x[t], y[t]}, t] // First;
tFlight = t /. Last[Solve[(y[t] /. solA) == 0, t]];
Print["A: x(t), y(t) = ", {x[t], y[t]} /. solA];
Print["A: tiempo de vuelo = ", tFlight, " s, alcance = ", (x[t] /. solA) /. t -> tFlight, " m, formula v0^2 sin(2 th)/g = ", v0^2 Sin[2 th]/g];

(* == Bloque B: proyectil con resistencia cuadratica (NDSolve y WhenEvent) == *)
{m, diam, rho, cd} = {0.057, 0.067, 1.2, 0.55};   (* pelota de tenis *)
kq = rho cd Pi diam^2/4/2;                       (* k = rho Cd A / 2, en kg/m *)
eqs = {X''[t] == -(kq/m) Sqrt[X'[t]^2 + Y'[t]^2] X'[t],
       Y''[t] == -g - (kq/m) Sqrt[X'[t]^2 + Y'[t]^2] Y'[t],
       X[0] == 0, Y[0] == 0, X'[0] == v0 Cos[th], Y'[0] == v0 Sin[th],
       WhenEvent[Y[t] < 0, tImpact = t; "StopIntegration"]};
solB = NDSolve[eqs, {X, Y}, {t, 0, 10}] // First;
Print["B: k = ", kq, " kg/m, tiempo de vuelo = ", tImpact, " s, alcance con resistencia = ", X[tImpact] /. solB, " m"];
figB = Show[ParametricPlot[{x[t], y[t]} /. solA, {t, 0, tFlight}, PlotStyle -> {Dashed, Black}],
   ParametricPlot[{X[t], Y[t]} /. solB, {t, 0, tImpact}, PlotStyle -> Blue],
   AxesLabel -> {"x (m)", "y (m)"}, PlotRange -> All, AspectRatio -> 0.45, ImageSize -> 420];
Export["figures/m02-proyectil.png", Rasterize[figB, Background -> White, ImageResolution -> 96]];
(* Verificacion: la energia mecanica debe disminuir monotonamente con resistencia *)
energia[t_] := (1/2) m (X'[t]^2 + Y'[t]^2) + m g Y[t] /. solB;
Print["B: energia inicial y final (J) = ", {energia[0], energia[tImpact]}, ", trabajo disipado = ", energia[0] - energia[tImpact]];

(* == Bloque C: pendulo lineal y no lineal; periodo frente a amplitud == *)
L = 1.0; w0 = Sqrt[g/L];
lin = DSolveValue[{q''[t] + w0^2 q[t] == 0, q[0] == q0, q'[0] == 0}, q[t], t];
Print["C: solucion lineal = ", lin, ", periodo lineal = ", 2 Pi/w0, " s"];
periodo[amp_?NumericQ] := Module[{qq, tc = {}},
   NDSolve[{qq''[t] + w0^2 Sin[qq[t]] == 0, qq[0] == amp, qq'[0] == 0,
      WhenEvent[qq[t] == 0, AppendTo[tc, t]]}, qq, {t, 0, 20}, MaxStepSize -> 0.005];
   2 (tc[[2]] - tc[[1]])];                       (* dos pasos por cero consecutivos = medio periodo *)
periodoExacto[amp_] := 4 EllipticK[Sin[amp/2]^2]/w0;
Print["C: periodo a 90 grados: NDSolve = ", periodo[N[Pi/2]], " s, integral eliptica = ", N[periodoExacto[Pi/2]], " s"];
Print["C: periodo a 10 grados: NDSolve = ", periodo[N[10 Degree]], " s, lineal = ", 2 Pi/w0, " s"];
figC = Plot[{periodoExacto[a Degree], 2 Pi/w0}, {a, 1, 170}, PlotStyle -> {Blue, {Dashed, Black}},
   AxesLabel -> {"amplitud (grados)", "T (s)"}, PlotRange -> {0, 6}, ImageSize -> 400,
   Epilog -> {Red, PointSize[0.015], Point[{#, periodo[N[# Degree]]} & /@ {30, 60, 90, 120, 150}]}];
Export["figures/m02-periodo.png", Rasterize[figC, Background -> White, ImageResolution -> 96]];
(* Conservacion de la energia como comprobacion del integrador *)
solC = NDSolve[{p''[t] + w0^2 Sin[p[t]] == 0, p[0] == Pi/2, p'[0] == 0}, p, {t, 0, 20}] // First;
en[t_] := (1/2) p'[t]^2 + w0^2 (1 - Cos[p[t]]) /. solC;
Print["C: deriva relativa maxima de la energia en 20 s = ", Max[Table[Abs[(en[t] - en[0])/en[0]], {t, 0, 20, 0.01}]]];

(* == Bloque D: vehiculo a potencia constante en una pendiente (capitulo 1) == *)
M = 85; P = 250; phi = ArcTan[0.04]; kd = 0.5 rho 0.35;
vmax = v /. FindRoot[P/v - M g Sin[phi] - kd v^2 == 0, {v, 5}];
solD = NDSolve[{M V'[t] == P/V[t] - M g Sin[phi] - kd V[t]^2, V[0] == 1,
    WhenEvent[V[t] > 0.95 vmax, t95 = t]}, V, {t, 0, 200}] // First;
Print["D: velocidad maxima = ", vmax, " m/s, tiempo hasta el 95 % partiendo de 1 m/s = ", t95, " s"];
