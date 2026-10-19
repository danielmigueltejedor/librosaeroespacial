"""Ejecuta realmente el par XML original sin copiarlo al modelo externo."""
import jsbsim,json
from pathlib import Path
from run_jsbsim import get,write
R=Path(__file__).resolve().parents[1]
f=jsbsim.FGFDMExec(str(R/'simulations/jsbsim-upstream'));f.set_debug_level(0)
assert f.load_script(str(R/'simulations/t6-original-run.xml'),.05,str(R/'simulations/t6-original-ic.xml'))
f['propulsion/set-running']=-1
f['gear/gear-cmd-norm']=0;f['gear/gear-pos-norm']=0
assert f.run_ic()
f.do_trim(0)
initial=get(f);rows=[initial]
for i in range(1200):
    assert f.run()
    if (i+1)%20==0:rows.append(get(f))
write('t6-xml-executed.csv',rows)
(R/'reports/xml-run.json').write_text(json.dumps(dict(executed=True,steps=1200,dt=.05,initial=initial,final=rows[-1]),indent=2))
print('XML ejecutado:',len(rows),'filas')
