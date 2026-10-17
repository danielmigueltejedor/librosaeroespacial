(* Practica 6. Analisis dimensional: matriz dimensional, espacio nulo, comprobacion con
   unidades, ajuste de datos experimentales y prediccion por semejanza. Codigo original. *)

(* == Bloque A: teorema Pi con la matriz dimensional == *)
ClearAll["Global`*"];
vars = {"Uc", "d", "mu", "rho", "B"};                (* B = Delta(rho g) en N/m^3 *)
(* columnas: exponentes de M, L, T de cada variable *)
dim = {{0, 1, -1}, {0, 1, 0}, {1, -1, -1}, {1, -3, 0}, {1, -2, -2}};
matriz = Transpose[dim];
Print["A: rango de la matriz dimensional = ", MatrixRank[matriz], ", numero de grupos = ", Length[vars] - MatrixRank[matriz]];
nulos = NullSpace[matriz];
Print["A: base del espacio nulo (exponentes de ", vars, "): ", nulos];
(* Una base equivalente y mas legible: Re (exponente 1 en Uc) y Ar (sin Uc) *)
re = {1, 1, -1, 1, 0}; ar = {0, 3, -2, 1, 1};
Print["A: Re y Ar son adimensionales: ", {matriz . re, matriz . ar}, ", independientes: ", MatrixRank[{re, ar}] == 2];

(* == Bloque B: comprobacion automatica con cantidades y unidades == *)
q = {Quantity[0.0648, "Meters"/"Seconds"], Quantity[4, "Millimeters"], Quantity[1, "Millipascals" "Seconds"],
     Quantity[1000, "Kilograms"/"Meters"^3], Quantity[80, "Newtons"/"Meters"^3]};
Reynolds = UnitSimplify[q[[4]] q[[1]] q[[2]]/q[[3]]];
Arq = UnitSimplify[q[[4]] q[[5]] q[[2]]^3/q[[3]]^2];
Print["B: Re = ", Reynolds, ", Ar = ", Arq, ", Ri = ", UnitSimplify[q[[5]] q[[2]]/(q[[4]] q[[1]]^2)]];
Print["B: DimensionalCombinations para Uc, d, mu, rho: ",
  DimensionalCombinations[{QuantityVariable["Uc", "Speed"], QuantityVariable["d", "Length"],
    QuantityVariable["mu", "DynamicViscosity"], QuantityVariable["rho", "MassDensity"]}]];

(* == Bloque C: datos (sinteticos) y ajuste de una correlacion Re = C Ar^n == *)
Bdat = {5, 10, 20, 40, 80}; Udat = {28.2, 34.7, 42.8, 52.7, 64.8} 10^-3;   (* tabla del capitulo 10 *)
dBoq = 0.004; muAgua = 1.0*^-3; rhoAgua = 1000.;
ReDat = rhoAgua Udat dBoq/muAgua; ArDat = rhoAgua Bdat dBoq^3/muAgua^2;
ajuste = FindFit[Transpose[{Log[ArDat], Log[ReDat]}], lc + n la, {lc, n}, la];
cC = Exp[lc /. ajuste]; nn = n /. ajuste;
Print["C: ajuste Re = C Ar^n con C = ", cC, ", n = ", nn];
figC = Show[ListLogLogPlot[Transpose[{ArDat, ReDat}], PlotStyle -> {Black, PointSize[0.015]}],
   LogLogPlot[cC a^nn, {a, 200, 8000}, PlotStyle -> Blue], AxesLabel -> {"Ar", "Re crit"}, ImageSize -> 380];
Export["figures/m06-ajuste.png", Rasterize[figC, Background -> White, ImageResolution -> 96]];

(* == Bloque D: prediccion de ensayos modificados == *)
prediccion[B_, d_, mu_, rho_] := Module[{a = rho B d^3/mu^2}, cC a^nn mu/(rho d)];
Print["D: ensayo d = 8 mm, B = 10 N/m^3: correlacion = ", 1000 prediccion[10, 0.008, muAgua, rhoAgua], " mm/s; semejanza exacta = ", 1000 0.0648 0.004/0.008, " mm/s"];
Print["D: ensayo d = 4 mm, B = 30 N/m^3: correlacion = ", 1000 prediccion[30, 0.004, muAgua, rhoAgua], " mm/s"];
Print["D: ensayo mu = 2 mPa s, d = 4 mm, B = 80 N/m^3: correlacion = ", 1000 prediccion[80, 0.004, 2.0*^-3, rhoAgua], " mm/s"];
