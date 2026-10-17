(* Practica 4. Bernoulli y volumenes de control: Venturi, vaciado de un deposito,
   presion sobre un cilindro y fuerza de un chorro. Codigo original. *)

(* == Bloque A: medidor Venturi y estudio parametrico == *)
ClearAll["Global`*"];
{rho, d1, d2} = {998., 0.100, 0.050};
area[d_] := Pi d^2/4;
caudal[dp_, beta_] := area[beta d1] Sqrt[2 dp/(rho (1 - beta^4))];
Print["A: Q para dp = 20 kPa y beta = 0.5: ", caudal[20000., 0.5], " m^3/s"];
dpNecesaria = dp /. Solve[caudal[dp, 0.5] == 0.020, dp][[1]];
Print["A: dp necesaria para Q = 20 l/s: ", dpNecesaria, " Pa"];
figA = Plot[Evaluate[Table[1000 caudal[dp, b], {b, {0.4, 0.5, 0.6, 0.7}}]], {dp, 0, 40000},
   PlotLegends -> {"d2/d1: 0.4", "0.5", "0.6", "0.7"}, AxesLabel -> {"dp (Pa)", "Q (l/s)"}, ImageSize -> 400];
Export["figures/m04-venturi.png", Rasterize[figA, Background -> White, ImageResolution -> 96]];

(* == Bloque B: vaciado de un deposito (Torricelli, DSolve y NDSolve) == *)
g = 9.81; At = 0.50; ao = 0.0010; h0 = 2.0;
sols = DSolve[{h'[t] == -(ao/At) Sqrt[2 g h[t]], h[0] == h0}, h[t], t];  (* dos ramas: hay que elegir *)
hAn[t_] := (Sqrt[h0] - (ao/At) Sqrt[g/2] t)^2;   (* rama fisica: el nivel baja desde h0 *)
tVac = (At/ao) Sqrt[2 h0/g];
Print["B: ramas de DSolve = ", Length[sols], ", residuo de la rama fisica = ", Simplify[hAn'[t] + (ao/At) Sqrt[2 g hAn[t]], 0 < t < tVac], ", tiempo de vaciado analitico = ", tVac, " s"];
Print["B: tiempo analitico hasta h = 1 mm = ", (At/ao) Sqrt[2/g] (Sqrt[h0] - Sqrt[0.001]), " s"];
num = NDSolve[{H'[t] == -(ao/At) Sqrt[2 g Max[H[t], 0]], H[0] == h0,
    WhenEvent[H[t] < 0.001, tEnd = t; "StopIntegration"]}, H, {t, 0, 2000}];
Print["B: tiempo hasta h = 1 mm con NDSolve = ", tEnd, " s"];

(* == Bloque C: coeficiente de presion sobre un cilindro y fuerzas == *)
cp[th_, G_] := 1 - (2 Sin[th] + G)^2;          (* G = Gamma/(2 pi R U) *)
drag[G_] := -Integrate[cp[th, G] Cos[th], {th, 0, 2 Pi}]/2;   (* coeficiente por unidad de longitud y de diametro *)
lift[G_] := -Integrate[cp[th, G] Sin[th], {th, 0, 2 Pi}]/2;
Print["C: Cd(G) = ", Simplify[drag[G]], ", Cl(G) = ", Simplify[lift[G]], " (Kutta-Joukowski: Cl = 2 pi G)"];
figC = Plot[{cp[th Degree, 0], cp[th Degree, 0.5]}, {th, 0, 360}, AxesLabel -> {"theta (grados)", "Cp"},
   PlotLegends -> {"sin circulacion", "G = 0.5"}, PlotStyle -> {Black, Blue}, ImageSize -> 400];
Export["figures/m04-cilindro.png", Rasterize[figC, Background -> White, ImageResolution -> 96]];

(* == Bloque D: fuerza de un chorro sobre un alabe (balance de cantidad de movimiento) == *)
V = 20.; Q = 0.005;
fuerza[beta_] := rho Q V (1 - Cos[beta]);
Print["D: fuerza para desvio de 90, 120 y 180 grados: ", fuerza /@ {90 Degree, 120 Degree, 180 Degree}, " N"];
