"""Dos autonomías originales hasta agotamiento de combustible accesible.
Comparación analítica local identificada con puntos de trim, no datos reales.
"""
from pathlib import Path
import csv,json,math,os
import numpy as np
from probe_jsbsim import setup
from run_jsbsim import get,write,LBM,LBF
from models import G
R=Path(__file__).resolve().parents[1]
def initialized(fuel_each,dt=.1):
    f=setup('B747',260,27000,dt)
    for i in range(5):f[f'propulsion/tank[{i}]/contents-lbs']=fuel_each if i<4 else 0
    f.run_ic();f.do_trim(0)
    return f
DT=float(os.environ.get("STUDIUM_ENDURANCE_DT", ".1"))
if not 0 < DT <= .2:raise ValueError("Invalid endurance time step")
fit=[]
for fuel in [2000,4000,6000,8000,10000]:
    f=initialized(fuel);fit.append(get(f))
x=np.array([(r['mass_kg']*G)**2 for r in fit]);y=np.array([r['drag_N'] for r in fit])
B,A=np.polyfit(x,y,1)
fit_error=float(np.max(abs((A+B*x)/y-1)))
write('b747-analytic-fit-trims.csv',fit)
out=[]
for fuel in [7000,9000]:
    dt=DT;f=initialized(fuel,dt);initial=get(f)
    V0=f['velocities/vtrue-fps'];h0=f['position/h-sl-ft'];th0=f['attitude/theta-rad']
    e0=f['fcs/elevator-cmd-norm'];t0=f['fcs/throttle-cmd-norm'];integ=0
    rows=[initial];reason='TIME_LIMIT'
    for j in range(round(20000/dt)):
        desired=th0+np.clip(.00008*(h0-f['position/h-sl-ft'])-.002*f['velocities/h-dot-fps'],-.06,.06)
        elevator=e0-1.8*(desired-f['attitude/theta-rad'])+1.3*f['velocities/q-rad_sec']
        ev=V0-f['velocities/vtrue-fps'];integ+=ev*dt
        throttle=float(np.clip(t0+.004*ev+.00002*integ,0,1))
        f['fcs/elevator-cmd-norm']=float(np.clip(elevator,-1,1))
        for i in range(4):f[f'fcs/throttle-cmd-norm[{i}]']=throttle
        f['fcs/aileron-cmd-norm']=float(np.clip(-f['attitude/phi-rad']-.3*f['velocities/p-rad_sec'],-.3,.3))
        f['fcs/rudder-cmd-norm']=float(np.clip(-.5*f['aero/beta-rad']+.1*f['velocities/r-rad_sec'],-.3,.3))
        assert f.run()
        if (j+1)%round(10/dt)==0:rows.append(get(f))
        if f['propulsion/total-fuel-lbs']<=.001:
            reason='USABLE_FUEL_EXHAUSTED';rows.append(get(f));break
    final=rows[-1];write(f'b747-endurance-{fuel*4}lbm.csv',rows)
    ct=initial['fuel_flow_kg_s']/initial['thrust_N']
    Wi=initial['mass_kg']*G;Wf=523816*LBM*G
    analytic=(math.atan(Wi*math.sqrt(B/A))-math.atan(Wf*math.sqrt(B/A)))/(G*ct*math.sqrt(A*B))
    duration=final['time_s']-initial['time_s']
    out.append(dict(initial_fuel_lbm=fuel*4,initial=initial,final=final,termination=reason,
      simulated_time_s=duration,constant_initial_flow_time_s=initial['fuel_kg']/initial['fuel_flow_kg_s'],
      equivalent_polar_time_s=analytic,relative_difference_equivalent=(duration/analytic-1),
      max_height_error_m=max(abs(r['h_m']-initial['h_m']) for r in rows),
      max_TAS_error_m_s=max(abs(r['TAS_m_s']-initial['TAS_m_s']) for r in rows)))
report=dict(dt_s=DT,cases=out,equivalent_drag_model=dict(A_N=float(A),B_per_N=float(B),max_relative_fit_error=fit_error,
       scope='D=A+B W² ajustado a cinco trimas del mismo modelo a CAS 260 kt y 27000 ft.'),
       scope='Simulación educativa hasta agotamiento de depósitos alimentadores. No es autonomía certificada ni ensayo.',
       convergence='Esta ejecución usa un solo paso; el estudio completo a 0.1/0.05/0.025 s se registra por separado en reports/edition-v2/endurance-convergence.json.')
(R/'reports/endurance-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
