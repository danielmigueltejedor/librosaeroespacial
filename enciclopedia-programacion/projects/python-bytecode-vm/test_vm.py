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
