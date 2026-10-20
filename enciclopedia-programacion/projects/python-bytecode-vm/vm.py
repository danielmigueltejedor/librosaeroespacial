"""Compilador de expresiones a bytecode y Máquina Virtual de pila determinista."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum, auto


class OpCode(Enum):
    LOAD_CONST = auto()
    LOAD_VAR = auto()
    STORE_VAR = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    RETURN_VALUE = auto()


@dataclass(frozen=True)
class Instruction:
    op: OpCode
    arg: int | float | str | None = None


class BytecodeCompiler(ast.NodeVisitor):
    """Compila un subconjunto seguro de AST aritmético y asignaciones a bytecode."""

    def __init__(self) -> None:
        self.code: list[Instruction] = []

    def compile_source(self, source: str) -> list[Instruction]:
        tree = ast.parse(source, mode="exec")
        for stmt in tree.body:
            if isinstance(stmt, ast.Assign):
                if len(stmt.targets) != 1 or not isinstance(stmt.targets[0], ast.Name):
                    raise ValueError("Solo se admiten asignaciones simples a variables")
                self.visit(stmt.value)
                self.code.append(Instruction(OpCode.STORE_VAR, stmt.targets[0].id))
            elif isinstance(stmt, ast.Expr):
                self.visit(stmt.value)
            else:
                raise TypeError(f"Sentencia no soportada: {type(stmt).__name__}")
        self.code.append(Instruction(OpCode.RETURN_VALUE))
        return list(self.code)

    def visit_Constant(self, node: ast.Constant) -> None:
        if not isinstance(node.value, (int, float)):
            raise TypeError("Solo se admiten constantes numéricas")
        self.code.append(Instruction(OpCode.LOAD_CONST, node.value))

    def visit_Name(self, node: ast.Name) -> None:
        self.code.append(Instruction(OpCode.LOAD_VAR, node.id))

    def visit_BinOp(self, node: ast.BinOp) -> None:
        self.visit(node.left)
        self.visit(node.right)
        if isinstance(node.op, ast.Add):
            self.code.append(Instruction(OpCode.ADD))
        elif isinstance(node.op, ast.Sub):
            self.code.append(Instruction(OpCode.SUB))
        elif isinstance(node.op, ast.Mult):
            self.code.append(Instruction(OpCode.MUL))
        elif isinstance(node.op, ast.Div):
            self.code.append(Instruction(OpCode.DIV))
        else:
            raise TypeError(f"Operador no soportado: {type(node.op).__name__}")


class StackVM:
    """Máquina virtual de evaluación basada en pila con entorno léxico simple."""

    def __init__(self) -> None:
        self.stack: list[float | int] = []
        self.env: dict[str, float | int] = {}

    def execute(self, instructions: list[Instruction], initial_env: dict[str, float | int] | None = None) -> float | int:
        self.stack.clear()
        self.env = dict(initial_env or {})
        for ins in instructions:
            if ins.op is OpCode.LOAD_CONST:
                assert isinstance(ins.arg, (int, float))
                self.stack.append(ins.arg)
            elif ins.op is OpCode.LOAD_VAR:
                assert isinstance(ins.arg, str)
                if ins.arg not in self.env:
                    raise NameError(f"Variable no definida: {ins.arg}")
                self.stack.append(self.env[ins.arg])
            elif ins.op is OpCode.STORE_VAR:
                assert isinstance(ins.arg, str)
                self.env[ins.arg] = self.stack.pop()
            elif ins.op is OpCode.ADD:
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a + b)
            elif ins.op is OpCode.SUB:
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a - b)
            elif ins.op is OpCode.MUL:
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a * b)
            elif ins.op is OpCode.DIV:
                b, a = self.stack.pop(), self.stack.pop()
                if b == 0:
                    raise ZeroDivisionError("División por cero en StackVM")
                self.stack.append(a / b)
            elif ins.op is OpCode.RETURN_VALUE:
                return self.stack[-1] if self.stack else 0
        return 0
