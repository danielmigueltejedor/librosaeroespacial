from pathlib import Path
import json, jsbsim
R=Path(__file__).resolve().parents[1]
root=R/'simulations/jsbsim-upstream'
def setup(model,vc=150,h=5000,dt=.05):
    f=jsbsim.FGFDMExec(str(root)); f.set_debug_level(0); f.set_dt(dt)
    assert f.load_model(model)
    f['ic/lat-gc-deg']=42.6;f['ic/long-gc-deg']=-5.6
    f['ic/h-sl-ft']=h;f['ic/gamma-deg']=0;f['ic/vc-kts']=vc
    if model=='B747':
        for i in range(5): f[f'propulsion/tank[{i}]/contents-lbs']=9000 if i<4 else 0
    f['propulsion/set-running']=-1
    f['gear/gear-cmd-norm']=0;f['gear/gear-pos-norm']=0
    f.run_ic();f.do_trim(0)
    return f
if __name__=='__main__':
    out=[]
    for model,vc,h in [('t6texan2',155,5000),('B747',260,27000)]:
        try:
            f=setup(model,vc,h)
            props=['velocities/vtrue-fps','velocities/ve-kts','velocities/vc-kts','aero/qbar-psf','forces/fwx-aero-lbs','forces/fwz-aero-lbs','propulsion/engine/thrust-lbs','propulsion/engine/fuel-flow-rate-pps','inertia/weight-lbs','aero/alpha-deg','fcs/throttle-cmd-norm','accelerations/udot-ft_sec2','accelerations/wdot-ft_sec2']
            out.append(dict(model=model,values={p:f[p] for p in props},catalog=[p for p in f.get_property_catalog() if 'fuel' in p or 'thrust' in p]))
        except Exception as e: out.append(dict(model=model,error=str(e)))
    (R/'reports/jsbsim-probe.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
