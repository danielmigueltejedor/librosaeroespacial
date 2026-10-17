from pathlib import Path
import math,json
from scipy.integrate import quad
from scipy.optimize import brentq,minimize_scalar
from pint import UnitRegistry
from physics import *
from problem_bank import bank
ROOT=Path(__file__).resolve().parents[1];u=UnitRegistry();rows=[]
for p in bank():
 d={g['symbol']:g['value'] for g in p['given']};x=p['value'];k=p['key'];v=list(d.values())
 if k=='P01':y=101325*math.exp(quad(lambda h:-G0/(R*(288.15-.0065*h)),0,6000)[0])
 elif k=='P02':y=isa(6000)['p']/(R*isa(6000)['T'])
 elif k=='P03':y=isa(16000)['p']
 elif k=='P04':y=quad(lambda z:(6356766/(6356766+z))**2,0,14000)[0]
 elif k=='P05':y=brentq(lambda h:isa(h)['rho']-.90,0,11000)
 elif k=='P06':y=d['V']/math.sqrt(1.4*R*d['T'])
 elif k=='P07':y=math.degrees(math.atan(1/math.sqrt(d['Ma']**2-1)))
 elif k=='P08':y=d['Re']*(d['mu']/d['rho'])/d['V']
 elif k=='P09':y=(d['rho1']*d['V1']*d['A1'])/(d['V2']*d['A2'])
 elif k=='P10':y=math.sqrt(2*(d['V1']**2/2+d['dp']/d['rho']))
 elif k=='P11':y=math.sqrt(d['qc']/(.5*d['rho']))
 elif k=='P12':y=brentq(lambda m:(1+.2*m*m)**3.5-d['pt']/d['p'],0,.999999)
 elif k=='P13':y=d['rhoair']*d['Vol']-d['rhogas']*d['Vol']-d['ms']
 elif k=='P14':y=2*quad(lambda t:d['cr']*(1-(1-d['lam'])*t/(d['b']/2)),0,d['b']/2)[0]
 elif k=='P15':y=quad(lambda t:(d['cr']*(1-(1-d['lam'])*t))**2,0,1)[0]/quad(lambda t:d['cr']*(1-(1-d['lam'])*t),0,1)[0]
 elif k=='P16':
  cl=brentq(lambda cl:cl-d['a0']*(.1-cl/(math.pi*d['ei']*d['AR'])),0,1);y=cl/.1
 elif k=='P17':y=1/(math.pi*d['AR']*(1/(math.pi*d['ei']*d['AR'])+d['kp']))
 elif k=='P18':y=d['W']/(.5*d['rho']*d['V']**2*d['S'])
 elif k=='P19':
  q=.5*d['rho']*d['V']**2;cl=d['W']/(q*d['S']);y=q*d['S']*(d['CD0']+d['K']*cl*cl)
 elif k in ['P20','P21']:
  n=0 if k=='P20' else 1;y=minimize_scalar(lambda z:drag(z,d['rho'],d['W'],d['S'],d['CD0'],d['K'])*z**n,bounds=(20,200),method='bounded',options={'xatol':1e-9}).x
 elif k=='P22':y=-minimize_scalar(lambda cl:-cl/(d['CD0']+d['K']*cl*cl),bounds=(.01,2),method='bounded').fun
 elif k=='P23':y=d['V']*math.sin(math.asin((d['T']-d['D'])/d['W']))
 elif k=='P24':y=d['height']/math.tan(math.atan(1/d['LD']))
 elif k=='P25':
  n=1/math.cos(d['phi']);y=d['V']**2/(d['g']*math.sqrt(n*n-1))
 elif k=='P26':y=-(d['hcg']-d['hn'])
 elif k=='P27':y=math.degrees(math.atan(d['cross']/math.sqrt(d['V']**2-d['cross']**2)))
 elif k=='P28':y=brentq(lambda z:z*z/d['r']-d['mu']/d['r']**2,1,20000)
 elif k=='P29':y=quad(lambda m:-d['Isp']*G0/m,d['ratio'],1)[0]
 elif k=='P30':y=d['dp']*d['Q']+(1/d['eta']-1)*d['dp']*d['Q']
 err=abs(x-y)/max(abs(x),1);assert err<1e-7,(k,x,y,err)
 env={g['symbol']:g['value']*u(g['unit']) for g in p['given']}
 env.update(pi=math.pi,sqrt=lambda q:q**.5,exp=lambda q:math.exp(q.to('').magnitude)*u(''),log=lambda q:math.log(q.to('').magnitude)*u(''),asin=lambda q:math.asin(q.to('').magnitude)*u(''),tan=lambda q:math.tan(q.to('').magnitude)*u(''))
 z=eval(p['expression'],{'__builtins__':{}},env)
 if not hasattr(z,'dimensionality'):z=z*u('')
 dimok=z.dimensionality==u(p['unit']).dimensionality;assert dimok,k
 rows.append({'key':k,'calculation':'REPRODUCIDO','second_route':'VERIFICADO','scope':'Ruta matemática o balance alternativo bajo el mismo modelo; no certificación del modelo físico','value':x,'alternative_value':y,'relative_difference':err,'dimensional_check':'VERIFICADO','dimensions':str(z.dimensionality),'units':p['unit']})
(ROOT/'reports/bank-crosschecks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(len(rows),'rutas alternativas y dimensiones comprobadas')
