(* Original educational workshop. SI unless Quantity is used. *)
ClearAll["Global`*"];
speeds = {1., 2., 4., 5.};
forces = {0.12, 0.30, 0.84, 1.20};
design = Transpose[{speeds, speeds^2}];
coef = LeastSquares[design, forces];
res = Norm[design.coef - forces];
If[Max[Abs[coef - {.09, .03}]] > 10^-10 || res > 10^-10, Exit[1]];
Print[ExportString[<|"a_kg_s" -> coef[[1]], "b_kg_m" -> coef[[2]], "residual_N" -> res|>, "RawJSON"]];
