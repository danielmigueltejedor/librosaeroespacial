"""Comprobaciones simbólicas de las ampliaciones de derivación."""
from pathlib import Path
import json
import sympy as s
R=Path(__file__).resolve().parents[1];out=[]
def check(name,expr,scope):
    residual=s.simplify(s.trigsimp(expr))
    out.append(dict(name=name,residual=str(residual),passed=residual==0,scope=scope,expert_review='PENDING'))
z=s.symbols('z',real=True)
check('Primitiva de alcance: rama alta',s.diff(s.sin(z)-s.Rational(2,3)*s.sin(z)**3,z)-s.cos(z)*s.cos(2*z),'Empuje constante, polar y densidad fijas.')
check('Primitiva de alcance: rama baja',s.diff(s.cos(z)-s.Rational(2,3)*s.cos(z)**3,z)-s.sin(z)*s.cos(2*z),'Mismas hipótesis y rama baja.')
a,ae,ma,me,cm0,CL,CL0=s.symbols('a ae ma me cm0 CL CL0',real=True)
det=a*me-ae*ma
alpha=(me*(CL-CL0)+ae*cm0)/det;de=(-a*cm0-ma*(CL-CL0))/det
check('Trim lineal: sustentación',CL0+a*alpha+ae*de-CL,'Determinante distinto de cero.')
check('Trim lineal: momento',cm0+ma*alpha+me*de,'Modelo lineal declarado.')
A,C,T,z=s.symbols('A C T z',positive=True)
W=T/(2*s.sqrt(A*C))*s.sin(2*z);vh=s.sqrt(T/A)*s.cos(z);vl=s.sqrt(T/A)*s.sin(z)
check('Empuje constante: velocidad alta',A*vh**2+C*W**2/vh**2-T,'Rama angular interior y V>0.')
check('Empuje constante: velocidad baja',A*vl**2+C*W**2/vl**2-T,'Rama angular interior y V>0.')
cl,c0,k=s.symbols('CL c0 k',positive=True);cd=c0+k*cl**2
ld=s.diff(s.log(cd)-s.Rational(3,4)*s.log(cl**2+cd**2),cl)
expected=cl*(4*k*cl**2-2*k*cd**2-3*cd)/(2*cd*(cl**2+cd**2))
check('Descenso exacto: condición diferencial',ld-expected,'Condición necesaria; falta recortar dominio y comprobar mínimo.')
q0,q1,q2,q3,p,q,r=s.symbols('q0 q1 q2 q3 p q r',real=True)
Q=s.Matrix([q0,q1,q2,q3]);rate=s.Matrix([-q1*p-q2*q-q3*r,q0*p+q2*r-q3*q,q0*q+q3*p-q1*r,q0*r+q1*q-q2*p])/2
check('Cuaternión: conservación de norma',2*Q.dot(rate),'Hamilton, escalar primero, rotación activa cuerpo a NED.')
(R/'reports/additional-symbolic-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('Comprobaciones adicionales:',len(out),'correctas:',sum(r['passed'] for r in out))
assert all(r['passed'] for r in out)
