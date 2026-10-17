(* Practica 1. Fundamentos de Mathematica: la atmosfera estandar como hilo conductor.
   Mecanica de Fluidos (ULE 0710311), segunda edicion. Codigo original. Ejecutar con
   wolframscript -file m01-fundamentos.wl  (o copiar los bloques en un cuaderno). *)

(* == Bloque A: parametros y asignaciones == *)
ClearAll["Global`*"];
g0 = 9.80665;            (* m/s^2, gravedad estandar *)
R = 287.05287;           (* J/(kg K), constante del aire *)
T0 = 288.15; p0 = 101325.; (* K y Pa al nivel del mar *)
lapse = N[-6.5/1000];     (* K/m: -6,5 K por km en la troposfera *)
r1 = RandomReal[];       (* Set (=): se evalua una vez *)
r2 := RandomReal[];      (* SetDelayed (:=): se evalua en cada uso *)
Print["A: r1 dos veces = ", {r1, r1}, "  r2 dos veces distintas = ", Unequal[r2, r2]];

(* == Bloque B: funciones y calculo simbolico == *)
temp[z_] := T0 + lapse z;
pres[z_] := p0 (temp[z]/T0)^(-g0/(lapse R));
dens[z_] := pres[z]/(R temp[z]);
Print["B: p(11000) = ", pres[11000.], " Pa,  rho(11000) = ", dens[11000.], " kg/m^3"];
(* Comprobacion: la presion cumple la ecuacion de la hidrostatica (derivada de p mas rho g, nula) *)
hydro = Simplify[D[pres[z], z] + dens[z] g0, 0 < z < 11000];
Print["B: dp/dz + rho g simplificado = ", Chop[hydro]];

(* == Bloque C: resolver e integrar == *)
zHalf = z /. FindRoot[pres[z] == p0/2, {z, 5000}];
Print["C: altitud con la mitad de la presion = ", zHalf, " m"];
(* Masa de aire por metro cuadrado entre 0 y 11 km, integrando la densidad *)
mCol = NIntegrate[dens[z], {z, 0, 11000}];
Print["C: masa de la columna 0-11 km = ", mCol, " kg/m^2,  (p0 - p(11 km))/g0 = ", (p0 - pres[11000.])/g0];
(* Atmosfera isoterma: solucion simbolica con DSolve *)
iso = DSolveValue[{pp'[z] == -pp[z] g0/(R TT), pp[0] == p0}, pp[z], z];
Print["C: atmosfera isoterma p(z) = ", iso];

(* == Bloque D: graficos == *)
figD = Plot[{pres[z]/p0, dens[z]/dens[0], temp[z]/T0}, {z, 0, 11000},
  PlotLegends -> {"p/p0", "rho/rho0", "T/T0"}, AxesLabel -> {"z (m)", None},
  PlotStyle -> {Black, Blue, Red}, ImageSize -> 400];
Export["figures/m01-atmosfera.png", Rasterize[figD, Background -> White, ImageResolution -> 96]];
figP = ParametricPlot[{pres[z]/1000, z/1000}, {z, 0, 11000}, AspectRatio -> 0.8,
  AxesLabel -> {"p (kPa)", "z (km)"}, PlotStyle -> Blue, ImageSize -> 300];
Export["figures/m01-parametrico.png", Rasterize[figP, Background -> White, ImageResolution -> 96]];

(* == Bloque E: exploracion interactiva (ejecutar en un cuaderno) == *)
explorar = Manipulate[
  Plot[(1 + a z/T0)^(-g0/(a R)), {z, 0, 11000}, PlotRange -> {0, 1},
    AxesLabel -> {"z (m)", "p/p0"}],
  {{a, -0.0065, "gradiente (K/m)"}, -0.0098, -0.002}];
(* Verificacion sin interfaz: el cuerpo del Manipulate en un valor concreto del control *)
Print["E: p/p0 a 5 km con a = -0.0065: ", (1 + lapse 5000/T0)^(-g0/(lapse R)), " ; con a = -0.0098: ", (1 - 0.0098 5000/T0)^(-g0/(-0.0098 R))];
