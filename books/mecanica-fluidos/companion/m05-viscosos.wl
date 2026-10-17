(* Practica 5. Flujos viscosos: Couette-Poiseuille entre placas y cilindros giratorios,
   par, potencia y comprobacion de la disipacion. Codigo original. *)

(* == Bloque A: Couette con gradiente de presion (DSolve con condiciones de contorno) == *)
ClearAll["Global`*"];
perfil = DSolveValue[{mu u''[y] == -G, u[0] == 0, u[h] == U}, u[y], y];
Print["A: u(y) = ", Simplify[perfil]];
q = Integrate[perfil, {y, 0, h}];
tauPared = mu D[perfil, y] /. y -> 0;
Print["A: caudal por unidad de anchura = ", Simplify[q], ", esfuerzo en y = 0: ", Simplify[tauPared]];
Print["A: gradiente que anula el esfuerzo en la placa fija: G = ", G /. Solve[tauPared == 0, G][[1]]];
adim = Simplify[perfil/U /. {y -> eta h, G -> 2 mu U P/h^2}];
Print["A: perfil adimensional u/U = ", adim];
figA = Plot[Evaluate[Table[adim, {P, {-2, -1, 0, 1, 2}}]], {eta, 0, 1}, PlotLegends -> {"P=-2", "P=-1", "P=0", "P=1", "P=2"},
   AxesLabel -> {"y/h", "u/U"}, ImageSize -> 400];
Export["figures/m05-couette.png", Rasterize[figA, Background -> White, ImageResolution -> 96]];
(* En un cuaderno: Manipulate[Plot[adim, {eta, 0, 1}, PlotRange -> {-0.5, 1.6}], {P, -3, 3}] *)

(* == Bloque B: cilindros coaxiales, solucion simbolica de Navier-Stokes azimutal == *)
ec = v''[r] + v'[r]/r - v[r]/r^2 == 0;
vSol = DSolveValue[{ec, v[R1] == W1 R1, v[R2] == W2 R2}, v[r], r];
Print["B: u_theta(r) = ", Simplify[vSol]];
tau[r_] = mu r D[vSol/r, r];
par = Simplify[-2 Pi R1^2 tau[R1]];             (* par del motor sobre el cilindro interior, por unidad de longitud *)
Print["B: par por unidad de longitud = ", par];
Print["B: limite fluido ilimitado (R2 -> oo, cilindro exterior en reposo): ", Limit[par /. W2 -> 0, R2 -> Infinity]];
(* Comprobacion energetica: disipacion integrada = potencia neta de los cilindros *)
phi[r_] = tau[r]^2/mu;
disip = Simplify[Integrate[phi[r] 2 Pi r, {r, R1, R2}, Assumptions -> 0 < R1 < R2]];
Print["B: disipacion - (W1 - W2) par = ", Simplify[disip - (W1 - W2) par]];

(* == Bloque C: ejemplo numerico (eje en glicerina, capitulo 14) y comprobacion numerica == *)
datos = {mu -> 1.41, W1 -> 300., R1 -> 0.010, W2 -> 0};
potIlim = 4 Pi mu W1^2 R1^2 /. datos;
Print["C: potencia por unidad de longitud en fluido ilimitado = ", potIlim, " W/m"];
Print["C: con carcasa a R2 = 15 mm: ", W1 par /. datos /. R2 -> 0.015, " W/m"];
(* Verificacion numerica independiente: resolver el problema de contorno con NDSolve *)
num = NDSolveValue[{v''[r] + v'[r]/r - v[r]/r^2 == 0, v[0.010] == 3., v[0.015] == 0}, v, {r, 0.010, 0.015}];
an = vSol /. {R1 -> 0.010, R2 -> 0.015, W1 -> 300., W2 -> 0};
Print["C: error maximo NDSolve frente a la solucion exacta = ", Max[Table[Abs[num[rr] - (an /. r -> rr)], {rr, 0.010, 0.015, 0.0001}]], " m/s"];
figC = Plot[Evaluate[{If[rr <= 0.015, an /. r -> rr, Undefined], 3. 0.010/rr}], {rr, 0.010, 0.030}, PlotStyle -> {Blue, {Dashed, Red}},
   AxesLabel -> {"r (m)", "u_theta (m/s)"}, PlotLegends -> {"carcasa en 15 mm", "fluido ilimitado"}, ImageSize -> 400];
Export["figures/m05-cilindros.png", Rasterize[figC, Background -> White, ImageResolution -> 96]];
