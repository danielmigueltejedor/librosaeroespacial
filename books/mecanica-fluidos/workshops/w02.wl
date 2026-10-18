(* Original educational workshop. SI unless Quantity is used. *)
ClearAll["Global`*"];
mass = 24.; drag = 0.8; initial = 8.; final = 6.;
vel = NDSolveValue[{v'[t] == -drag v[t]^2/mass, v[0] == initial}, v, {t, 0, final}, AccuracyGoal -> 11, PrecisionGoal -> 10, MaxStepFraction -> 1/200];
exact[t_] := initial/(1 + drag initial t/mass);
err = Max[Table[Abs[vel[t] - exact[t]], {t, 0, final, final/100}]];
If[err > 10^-7, Exit[1]];
Print[ExportString[<|"velocity_m_s" -> vel[final], "max_error_m_s" -> err|>, "RawJSON"]];
