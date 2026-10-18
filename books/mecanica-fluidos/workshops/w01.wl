(* Original educational workshop. SI unless Quantity is used. *)
ClearAll["Global`*"];
q = UnitConvert[Quantity[60, "Milliliters"/"Minutes"], "Meters"^3/"Seconds"];
r = UnitConvert[Quantity[1, "Millimeters"], "Meters"];
mu = Quantity[0.012, "Pascals"*"Seconds"];
len = Quantity[0.8, "Meters"];
dp = UnitConvert[8 mu len q/(Pi r^4), "Pascals"];
value = QuantityMagnitude[dp];
If[Abs[value - 24446.1992589151] > 10^-7, Exit[1]];
Print[ExportString[<|"dp_Pa" -> value|>, "RawJSON"]];
