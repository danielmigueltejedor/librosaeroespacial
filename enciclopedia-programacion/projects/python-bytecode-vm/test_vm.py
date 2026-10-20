from __future__ import annotations

import pytest
from vm import BytecodeCompiler, OpCode, StackVM


def test_compile_and_execute_arithmetic_program() -> None:
    program = "base = 12 * 3\nbonus = (base - 6) / 5\nbase + bonus"
    compiler = BytecodeCompiler()
    bytecode = compiler.compile_source(program)
    assert bytecode[-1].op is OpCode.RETURN_VALUE
    vm = StackVM()
    result = vm.execute(bytecode)
    assert result == 42.0
    assert vm.env["base"] == 36
    assert vm.env["bonus"] == 6.0


def test_division_by_zero_raises_clean_exception() -> None:
    compiler = BytecodeCompiler()
    bytecode = compiler.compile_source("10 / (5 - 5)")
    vm = StackVM()
    with pytest.raises(ZeroDivisionError):
        vm.execute(bytecode)


def test_compiler_reuse_discards_previous_program() -> None:
    compiler = BytecodeCompiler()
    compiler.compile_source("100")
    assert StackVM().execute(compiler.compile_source("2 + 3")) == 5


@pytest.mark.parametrize("source", ["f(1)", "[1, 2]", "True", "x.y", "not 1", "1 ** 2"])
def test_unsupported_syntax_is_rejected_instead_of_partially_evaluated(source) -> None:
    with pytest.raises(TypeError):
        BytecodeCompiler().compile_source(source)


def test_unary_signs_and_undefined_variables() -> None:
    compiler = BytecodeCompiler()
    assert StackVM().execute(compiler.compile_source("-2 * (3 + +4)")) == -14
    with pytest.raises(NameError):
        StackVM().execute(compiler.compile_source("missing + 1"))
