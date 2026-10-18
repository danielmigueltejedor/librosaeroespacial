(* Original educational workshop. SI unless Quantity is used. *)
ClearAll["Global`*"];
gap = .004; visc = .08; grad = 100.; n = 40;
dy = gap/n; grid = Range[1, n - 1] dy;
mat = SparseArray[{Band[{1, 1}] -> -2., Band[{1, 2}] -> 1., Band[{2, 1}] -> 1.}, {n - 1, n - 1}];
profile = LinearSolve[mat, ConstantArray[-grad dy^2/visc, n - 1]];
exact = grad grid (gap - grid)/(2 visc);
err = Max[Abs[profile - exact]];
res = Max[Abs[mat.profile + grad dy^2/visc]];
If[err > 10^-10 || res > 10^-10, Exit[1]];
Print[ExportString[<|"max_error_m_s" -> err, "discrete_residual" -> res|>, "RawJSON"]];
