(* Original educational workshop. SI unless Quantity is used. *)
ClearAll["Global`*"];
field = {a x, -a y, 0}; coords = {x, y, z};
dv = Div[field, coords]; rot = Curl[field, coords];
acc = Simplify[Table[Sum[field[[j]] D[field[[i]], coords[[j]]], {j, 3}], {i, 3}]];
If[dv =!= 0 || rot =!= {0, 0, 0} || acc =!= {a^2 x, a^2 y, 0}, Exit[1]];
Print[ExportString[<|"divergence" -> dv, "curl" -> rot,
 "acceleration_m_s2" -> N[acc /. {a -> .6, x -> .3, y -> .2}]|>, "RawJSON"]];
