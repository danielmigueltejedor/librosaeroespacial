"""Print every authored scalar operation, retaining algebra and intermediates.

Only reviewed repository expressions are accepted. No external program is run.
This checks arithmetic, not the physical model or teaching quality.
"""
from __future__ import annotations
import ast
import math
import sympy as sp

FUNCTIONS = {'sqrt': sp.sqrt, 'log': sp.log, 'exp': sp.exp, 'sin': sp.sin,
             'cos': sp.cos, 'tan': sp.tan, 'asin': sp.asin, 'acos': sp.acos,
             'atan': sp.atan, 'erfc': sp.erfc, 'pi': sp.pi, 'abs': sp.Abs}
NAMES = {'rho':r'\rho','mu':r'\mu','nu':r'\nu','Omega':r'\Omega','Om':r'\Omega',
         'omega':r'\omega','theta':r'\theta','phi':r'\varphi','beta':r'\beta',
         'Gamma':r'\Gamma','tau':r'\tau','zeta':r'\zeta','alpha':r'\alpha',
         'CL':r'C_L','CD':r'C_D','CLmax':r'C_{L,\max}','CD0':r'C_{D0}'}
NAMES.update(Tz=r'T_0',pz=r'p_0',gam=r'\gamma',Rg=r'R_g',etap=r'\eta_p',
             t99=r't_{99}',TperL=r'T\prime',PperL=r'P\prime')

def expression(raw, names=()):
    tree=ast.parse(raw,mode='eval')
    for node in ast.walk(tree):
        if not isinstance(node,(ast.Expression,ast.BinOp,ast.UnaryOp,ast.Call,ast.Name,
                               ast.Load,ast.Constant,ast.Add,ast.Sub,ast.Mult,ast.Div,
                               ast.Pow,ast.UAdd,ast.USub)):
            raise ValueError(f'Unsupported scalar operation: {raw}')
        if isinstance(node,ast.Call) and (not isinstance(node.func,ast.Name) or node.func.id not in FUNCTIONS):
            raise ValueError(f'Unsupported function: {raw}')
    identifiers={n.id for n in ast.walk(tree) if isinstance(n,ast.Name) and n.id not in FUNCTIONS}
    local=FUNCTIONS|{k:sp.Symbol(k) for k in identifiers|set(names)}
    return sp.sympify(raw,locals=local,evaluate=False)

def number(value, precision=7):
    value=float(value)
    if not math.isfinite(value):raise ValueError('Non-finite intermediate')
    if value==0:return '0'
    s=f'{value:.{precision}g}'
    if 'e' in s:
        a,b=s.split('e');return a+r'\times10^{'+str(int(b))+'}'
    return s

def symbol(name):
    if name in NAMES:return NAMES[name]
    # Keep a multi-letter scalar distinct from a product of letters.
    if len(name)>1 and name.isalpha():return r'\mathrm{'+name+'}'
    if '_' in name:
        a,b=name.split('_',1);return symbol(a)+'_{'+b.replace('_',r'\,')+'}'
    return name

def unit(raw):
    if raw in ('','1','dimensionless','adimensional'):return ''
    if raw in ('degree','deg'):return r'{}^{\circ}'
    if raw=='1/min':return r'\mathrm{min^{-1}}'
    raw=raw.replace('**','^')
    import re
    raw=re.sub(r'\^\(?(-?(?:\d+(?:\.\d*)?|\.\d+))\)?',r'^{\1}',raw)
    return r'\mathrm{'+raw.replace('*',r'\,')+'}'

def mathlines(tex):
    """Keep the complete displayed operation within the manuscript width."""
    return r'\[\fitmath{'+tex+r'}\]'

def prose_tex(raw):
    """Keep authored math, escape reserved plain-text script characters."""
    import re
    pieces=re.split(r'(\$[^$]*\$|\\\(.*?\\\)|\\\[.*?\\\])',raw,flags=re.S)
    for i in range(0,len(pieces),2):
        pieces[i]=re.sub(r'(?<!\\)_',r'\\_',pieces[i])
        pieces[i]=re.sub(r'(?<!\\)\^',r'\\textasciicircum{}',pieces[i])
        for char,tex in {'Σ':r'\Sigma','τ':r'\tau','σ':r'\sigma','θ':r'\theta',
                         'φ':r'\phi','Ω':r'\Omega','≈':r'\approx','×':r'\times',
                         '√':r'\sqrt{\vphantom{3}}'}.items():
            pieces[i]=pieces[i].replace(char,r'\ensuremath{'+tex+'}')
        pieces[i]=pieces[i].replace('²',r'\textsuperscript{2}').replace('³',r'\textsuperscript{3}')
    return ''.join(pieces)

def scalar_tex(raw, values=None):
    """Print the original operation tree without SymPy constructor evaluation."""
    expression(raw, values or ())  # Same restricted grammar as evaluation.
    tree=ast.parse(raw,mode='eval').body
    def emit(node):
        if isinstance(node,ast.Constant):return number(node.value,10)
        if isinstance(node,ast.Name):
            if node.id=='pi':return r'\pi'
            return '('+number(values[node.id],10)+')' if values is not None else symbol(node.id)
        if isinstance(node,ast.UnaryOp):
            value=emit(node.operand)
            if isinstance(node.operand,ast.BinOp):value=r'\left('+value+r'\right)'
            return ('-' if isinstance(node.op,ast.USub) else '+')+value
        if isinstance(node,ast.BinOp):
            a,b=emit(node.left),emit(node.right)
            if isinstance(node.op,ast.Div):return r'\frac{'+a+'}{'+b+'}'
            if isinstance(node.op,ast.Pow):
                if isinstance(node.left,(ast.BinOp,ast.UnaryOp)):a=r'\left('+a+r'\right)'
                return '{'+a+'}^{'+b+'}'
            if isinstance(node.op,ast.Mult):
                if isinstance(node.left,ast.BinOp) and isinstance(node.left.op,(ast.Add,ast.Sub)):a=r'\left('+a+r'\right)'
                if isinstance(node.right,ast.BinOp) and isinstance(node.right.op,(ast.Add,ast.Sub)):b=r'\left('+b+r'\right)'
                return a+r'\cdot '+b
            if isinstance(node.op,ast.Sub):
                if isinstance(node.right,ast.BinOp) and isinstance(node.right.op,(ast.Add,ast.Sub)):b=r'\left('+b+r'\right)'
                return a+'-'+b
            return a+'+'+b
        if isinstance(node,ast.Call):
            args=[emit(x) for x in node.args];name=node.func.id
            if name=='sqrt':return r'\sqrt{'+args[0]+'}'
            if name=='abs':return r'\left|'+args[0]+r'\right|'
            if name=='log' and len(args)==2:return r'\frac{\ln\left('+args[0]+r'\right)}{\ln\left('+args[1]+r'\right)}'
            if name=='erfc':return r'\operatorname{erfc}\left('+args[0]+r'\right)'
            fn={'log':'ln','asin':'arcsin','acos':'arccos','atan':'arctan'}.get(name,name)
            return '\\'+fn+r'\left('+args[0]+r'\right)'
        raise ValueError('Unsupported TeX scalar node')
    return emit(tree)

def numeric_steps(rows, values=None):
    """One reason, symbolic expression, substitution and computed value per row."""
    env=dict(values or {})
    out=[r'\begin{enumerate}'];records=[]
    for i,row in enumerate(rows,1):
        target=row.get('target',f'y_{i}')
        if not row.get('expression'):
            if not row.get('equation'):raise ValueError('A step needs an equation or calculation')
            out.append(r'\item '+prose_tex(row.get('why',row.get('text',''))))
            out.append(mathlines(row['equation']))
            records.append(dict(index=i,target=target,equation=row['equation'],scope='authored algebra; not numeric replay'))
            continue
        ex=expression(row['expression'], env)
        unknown={str(s) for s in ex.free_symbols}-set(env)
        if unknown:raise ValueError(f'{target}: undefined inputs {unknown}')
        numeric=ex.xreplace({s:sp.Float(str(env[str(s)]),17) for s in ex.free_symbols})
        result=float(numeric.evalf(30))
        substitution=scalar_tex(row['expression'],env)
        expected=row.get('expected')
        # Expected values in historic exports are rounded, with variable
        # precision. Preserve the discrepancy for review rather than printing
        # a stale stored literal as if it were a computation.
        mismatch=expected is not None and not math.isclose(result,float(expected),rel_tol=5e-4,abs_tol=1e-8)
        out.append(r'\item '+prose_tex(row.get('why',row.get('text','Cálculo de la magnitud indicada.'))))
        names={s:symbol(str(s)) for s in ex.free_symbols}
        if ex.free_symbols:out.append(mathlines(symbol(target)+'='+scalar_tex(row['expression'])))
        out.append(mathlines(symbol(target)+'='+substitution+r'\approx '+number(result)+r'\,'+unit(row.get('unit',''))))
        records.append(dict(index=i,target=target,expression=row['expression'],value=result,
                            unit=row.get('unit',''),historic_expected=expected,historic_mismatch=mismatch))
        env[target]=result
    out.append(r'\end{enumerate}')
    return '\n\n'.join(out),records
