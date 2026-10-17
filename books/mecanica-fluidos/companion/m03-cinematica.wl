(* Practica 3. Cinematica de fluidos: funcion de corriente, aceleracion, vorticidad,
   lineas de corriente frente a trayectorias. Codigo original. *)

(* == Bloque A: de la funcion de corriente a la velocidad == *)
ClearAll["Global`*"];
K = 1;                                        (* 1/(m s) *)
psi = K (x^2 y + 2 x y^2);
vel = {D[psi, y], -D[psi, x]};
Print["A: velocidad = ", vel, ", divergencia = ", Simplify[Div[vel, {x, y}]]];

(* == Bloque B: gradiente de velocidad, aceleracion, vorticidad y fuerza == *)
gradV = Grad[vel, {x, y}];                     (* matriz d u_i / d x_j *)
acc = Simplify[gradV . vel];                   (* aceleracion convectiva (flujo estacionario) *)
vort = Curl[vel, {x, y}];                      (* escalar en 2D: dv/dx - du/dy *)
lamb = Simplify[Grad[(vel . vel)/2, {x, y}] - vort {vel[[2]], -vel[[1]]}];
Print["B: aceleracion = ", Factor[acc], ", vorticidad = ", vort];
Print["B: forma de Lamb igual a la convectiva: ", Simplify[lamb == acc]];
pt = {x -> 1, y -> 2}; {rho} = {1000};
Print["B: en (1,2): u = ", vel /. pt, ", a = ", acc /. pt, ", fuerza por unidad de volumen = ", rho acc /. pt, ", modulo = ", N[Norm[rho acc /. pt]]];
Print["B: laplaciano de u = ", Laplacian[#, {x, y}] & /@ vel, " ; -rot(omega) = ", {-D[vort, y], D[vort, x]}];

(* == Bloque C: visualizacion del campo y de las lineas psi = cte == *)
figC = Show[
   StreamPlot[vel, {x, -2, 2}, {y, -2, 3}, StreamColorFunction -> None, StreamStyle -> Gray, StreamPoints -> Coarse],
   ContourPlot[psi, {x, -2, 2}, {y, -2, 3}, Contours -> {-6, -3, -1, 1, 3, 6, 10}, ContourShading -> None, ContourStyle -> Blue],
   Graphics[{Red, PointSize[0.02], Point[{1, 2}], Arrow[{{1, 2}, {1, 2} + (acc /. pt)/150}]}],
   FrameLabel -> {"x (m)", "y (m)"}, ImageSize -> 360];
Export["figures/m03-corriente.png", Rasterize[figC, Background -> White, ImageResolution -> 72]];

(* == Bloque D: lineas de corriente frente a trayectorias en un flujo no estacionario == *)
u0 = 2; a = 0.5;                               (* u = u0, v = a t (capitulo 4) *)
tray = NDSolveValue[{X'[t] == u0, Y'[t] == a t, X[0] == 0, Y[0] == 0}, {X[t], Y[t]}, {t, 0, 4}];
Print["D: trayectoria en t = 4 s: ", tray /. t -> 4., ", analitica {u0 t, a t^2/2} = ", {u0 4, a 16/2}];
pendiente[t_] := a t/u0;                       (* las lineas de corriente en el instante t son rectas *)
Print["D: pendiente de las lineas de corriente en t = 2 s = ", pendiente[2], ", de la trayectoria en ese instante = ", (a t/u0) /. t -> 2];
figD = Show[ParametricPlot[tray, {t, 0, 4}, PlotStyle -> Blue],
   Plot[pendiente[4] xx, {xx, 0, 8}, PlotStyle -> {Dashed, Black}],
   AxesLabel -> {"x (m)", "y (m)"}, PlotRange -> {{0, 8}, {0, 8}}, AspectRatio -> 0.6, ImageSize -> 360];
Export["figures/m03-trayectoria.png", Rasterize[figD, Background -> White, ImageResolution -> 72]];
