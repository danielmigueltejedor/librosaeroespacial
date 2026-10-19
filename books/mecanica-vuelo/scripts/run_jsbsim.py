"""Experimentos docentes originales con JSBSim 1.3.3.
No ejecuta ni resuelve las condiciones de las prácticas evaluables.
"""
from pathlib import Path
import csv,json,hashlib,math
import jsbsim
from probe_jsbsim import setup
R=Path(__file__).resolve().parents[1]
OUT=R/'simulations/results'; OUT.mkdir(exist_ok=True)
FT=.3048; LBF=4.4482216152605; LBM=.45359237;KTS=.514444444444
def get(f):
    N=f.get_propulsion().get_num_engines()
    thrust=sum(f[f'propulsion/engine[{i}]/thrust-lbs'] for i in range(N))*LBF
    flow=sum(f[f'propulsion/engine[{i}]/fuel-flow-rate-pps'] for i in range(N))*LBM
    V=f['velocities/vtrue-fps']*FT
    return dict(time_s=f['simulation/sim-time-sec'],h_m=f['position/h-sl-ft']*FT,
      TAS_m_s=V,EAS_m_s=f['velocities/ve-kts']*KTS,CAS_m_s=f['velocities/vc-kts']*KTS,
      mass_kg=f['inertia/weight-lbs']*LBM,fuel_kg=f['propulsion/total-fuel-lbs']*LBM,
      drag_N=f['forces/fwx-aero-lbs']*LBF,lift_N=f['forces/fwz-aero-lbs']*LBF,
      thrust_N=thrust,thrust_power_W=thrust*V,fuel_flow_kg_s=flow,
      alpha_deg=f['aero/alpha-deg'],theta_rad=f['attitude/theta-rad'],
      udot_m_s2=f['accelerations/udot-ft_sec2']*FT,wdot_m_s2=f['accelerations/wdot-ft_sec2']*FT)
def write(name,rows):
    with (OUT/name).open('w',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def model():
    # Auditar ambas masas y ambas altitudes con las mismas CAS solicitadas.
    grid=[];failures=[]
    for fuel in [300,425]:
      for h in [5000,9000]:
       for vc in range(115,216,10):
        try:
            f=setup('t6texan2',vc,h)
            for i in range(2): f[f'propulsion/tank[{i}]/contents-lbs']=fuel
            f.run_ic();f.do_trim(0)
            row=get(f);row.update(tank_each_lbm=fuel,requested_h_ft=h,requested_CAS_kts=vc)
            # Potencia disponible: motor estabilizado a gas máximo, sin avanzar avión.
            f['fcs/throttle-cmd-norm']=1
            # Update FCS and cached propulsion inputs while the airframe is held.
            # GetSteadyState alone reuses the inputs from the last executive run.
            held={k:f[k] for k in ['velocities/vtrue-fps','position/h-sl-ft','simulation/sim-time-sec']}
            f.suspend_integration()
            try:
                assert f.run()
                f.get_propulsion().get_steady_state()
            finally:f.resume_integration()
            assert abs(f['fcs/throttle-pos-norm']-1)<1e-12
            assert all(abs(f[k]-v)<1e-10 for k,v in held.items())
            Tmax=f['propulsion/engine/thrust-lbs']*LBF
            row['max_throttle_position']=f['fcs/throttle-pos-norm'];row['max_engine_n1']=f['propulsion/engine/n1'];row['held_airframe']=True
            row['max_thrust_N']=Tmax;row['max_thrust_power_W']=Tmax*row['TAS_m_s']
            row['excess_power_approx_m_s']=(Tmax-row['drag_N'])*row['TAS_m_s']/(row['mass_kg']*9.80665)
            row['sin_gamma_approx']=(Tmax-row['drag_N'])/(row['mass_kg']*9.80665)
            grid.append(row)
        except Exception as e: failures.append(dict(fuel=fuel,h=h,vc=vc,error=str(e)))
    write('t6-trim-grid.csv',grid)
    # Solución libre 60s alrededor del trim: no se impone un piloto automático.
    convergence=[]
    for dt in [.10,.05,.025]:
        f=setup('t6texan2',155,5000,dt);rows=[]
        for j in range(round(60/dt)+1):
            if j%round(1/dt)==0: rows.append(get(f))
            if j<round(60/dt):f.run()
        write(f't6-free-dt-{dt}.csv',rows)
        convergence.append(dict(dt=dt,**rows[-1]))
    # B747: integración continua con control docente explícito de altura/TAS.
    f=setup('B747',260,27000,.05)
    refV=f['velocities/vtrue-fps']; refH=f['position/h-sl-ft'];theta0=f['attitude/theta-rad']
    elevator0=f['fcs/elevator-cmd-norm'];throttle0=f['fcs/throttle-cmd-norm']
    rows=[]; speedint=0
    for j in range(36001):
        if j%200==0: rows.append(get(f))
        eh=refH-f['position/h-sl-ft']; climb=f['velocities/h-dot-fps']
        desired=theta0+max(-.06,min(.06,.00008*eh-.002*climb))
        elevator=elevator0-1.8*(desired-f['attitude/theta-rad'])+1.3*f['velocities/q-rad_sec']
        ev=refV-f['velocities/vtrue-fps']; speedint+=ev*.05
        throttle=max(0,min(1,throttle0+.004*ev+.00002*speedint))
        f['fcs/elevator-cmd-norm']=max(-1,min(1,elevator))
        for i in range(4): f[f'fcs/throttle-cmd-norm[{i}]']=throttle
        # Amortiguación lateral didáctica; la simetría inicial deja residuos terrestres.
        f['fcs/aileron-cmd-norm']=max(-.3,min(.3,-1.0*f['attitude/phi-rad']-.3*f['velocities/p-rad_sec']))
        f['fcs/rudder-cmd-norm']=max(-.3,min(.3,-.5*f['aero/beta-rad']+.1*f['velocities/r-rad_sec']))
        if j<36000: f.run()
    write('b747-cruise-1800s.csv',rows)
    first,last=rows[0],rows[-1]
    effective_ct=first['fuel_flow_kg_s']/first['thrust_N']
    summary=dict(version=jsbsim.__version__,commit='66f7fafc07fe13e7ede9db20873030fed2881713',
      t6_grid_rows=len(grid),trim_failures=failures,convergence=convergence,
      b747=dict(initial=first,final=last,altitude_max_error_m=max(abs(x['h_m']-first['h_m']) for x in rows),
      TAS_max_error_m_s=max(abs(x['TAS_m_s']-first['TAS_m_s']) for x in rows),
      initial_effective_cT_kg_Ns=effective_ct,
      frozen_initial_flow_burn_kg=first['fuel_flow_kg_s']*1800,
      simulated_burn_kg=first['fuel_kg']-last['fuel_kg']),
      caveats=['Modelos upstream educativos ALPHA/BETA, sin validación experimental.',
        'La rejilla de trim usa CAS solicitada y registra EAS y TAS resultantes.',
        'T6: surrogate de empuje turbine_engine+direct, no potencia al eje de PT6.',
        'Estimaciones de ascenso usan L≈W y equilibrio horizontal; no son trim de ascenso.',
        'B747 usa control proporcional/integral docente; no es un piloto automático certificado.',
        'Convergencia T6 se limita a la trayectoria libre de 60 s.'])
    summary['model_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'simulations/jsbsim-upstream/aircraft/t6texan2/t6texan2.xml',R/'simulations/jsbsim-upstream/aircraft/B747/B747.xml',R/'simulations/jsbsim-upstream/engine/PT6A-68.xml',R/'simulations/jsbsim-upstream/engine/GE-CF6-80C2-B1F.xml']}
    (R/'reports/jsbsim-results.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=='__main__':model()
