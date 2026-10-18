(* Original educational workshop. SI unless Quantity is used. *)
ClearAll["Global`*"];
gravity = 9.81; tank = .8; hole = .0004; cd = .62;
h0 = 2.; h1 = .5;
tf = 2 tank (Sqrt[h0] - Sqrt[h1])/(cd hole Sqrt[2 gravity]);
level = NDSolveValue[{h'[t] == -cd hole Sqrt[2 gravity h[t]]/tank, h[0] == h0}, h, {t, 0, tf}, AccuracyGoal -> 11, PrecisionGoal -> 10];
err = Abs[level[tf] - h1];
If[err > 10^-7, Exit[1]];
Print[ExportString[<|"time_s" -> tf, "terminal_level_m" -> level[tf], "error_m" -> err|>, "RawJSON"]];
