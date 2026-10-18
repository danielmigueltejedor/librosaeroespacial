(* Original educational workshop. SI unless Quantity is used. *)
ClearAll["Global`*"];
gap = .01; visc = 10^-5; rate = visc Pi^2/gap^2;
sizes = {20, 40, 80};
rates = Table[4 visc Sin[Pi/(2 n)]^2/(gap/n)^2, {n, sizes}];
errors = N[Abs[rates - rate], 16];
ratios = Most[errors]/Rest[errors];
If[Min[ratios] < 3.98 || Max[ratios] > 4.02, Exit[1]];
Print[ExportString[<|"errors_s_inverse" -> errors, "ratios" -> ratios|>, "RawJSON"]];
