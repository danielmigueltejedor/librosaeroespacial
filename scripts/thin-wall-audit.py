"""Independent line-integration/network route for the eight C06 geometries.

N-mm convention. Unknown edge shear-flow constants and two longitudinal stress
gradients satisfy nodal equilibrium, zero cell twist and prescribed resultants.
The model omits local plate bending and junction effects, as does the book.
"""
import numpy as np
def solve(spec):
    nodes={k:np.array(v,dtype=float) for k,v in spec['nodes'].items()}
    edges=[];direct=spec.get('direct_stress_walls',True)
    pieces=[]
    for w in spec['walls']:
        p=nodes[w['from']];delta=nodes[w['to']]-p;L=np.linalg.norm(delta);t=w['t']
        edges.append((w,p,delta/L,L))
        if direct:pieces.append((t*L,p+delta/2))
    for b in spec.get('booms',[]):pieces.append((b['area'],nodes[b['at']]))
    area=sum(a for a,p in pieces);centre=sum(a*p for a,p in pieces)/area
    moment=np.zeros((2,2))
    if direct:
        for w,p,tan,L in edges:
            q=p-centre
            moment+=w['t']*(L*np.outer(q,q)+L**2/2*(np.outer(q,tan)+np.outer(tan,q))+L**3/3*np.outer(tan,tan))
    for b in spec.get('booms',[]):
        q=nodes[b['at']]-centre;moment+=b['area']*np.outer(q,q)
    count=len(edges);width=count+2
    start=[];end=[];integrals=[]
    for i,(w,p,tan,L) in enumerate(edges):
        q=p-centre;t=w['t'] if direct else 0
        s=np.zeros(width);s[i]=1;start.append(s)
        e=s.copy();e[-2]=-t*(q[1]*L+tan[1]*L**2/2);e[-1]=-t*(q[0]*L+tan[0]*L**2/2);end.append(e)
        z=s*L;z[-2]=-t*(q[1]*L**2/2+tan[1]*L**3/6);z[-1]=-t*(q[0]*L**2/2+tan[0]*L**3/6);integrals.append(z)
    matrix=[]
    for name in list(nodes)[:-1]:
        row=np.zeros(width)
        for i,(w,p,tan,L) in enumerate(edges):
            if w['from']==name:row+=start[i]
            if w['to']==name:row-=end[i]
        boom=sum(b['area'] for b in spec.get('booms',[]) if b['at']==name);q=nodes[name]-centre
        row[-2]+=boom*q[1];row[-1]+=boom*q[0];matrix.append(row)
    for cell in spec.get('cells',[]):
        row=np.zeros(width)
        for a,b in zip(cell,cell[1:]+cell[:1]):
            for i,(w,p,tan,L) in enumerate(edges):
                if (w['from'],w['to'])==(a,b):row+=integrals[i]/w['t']
                elif (w['from'],w['to'])==(b,a):row-=integrals[i]/w['t']
        matrix.append(row)
    forces=np.array([sum(v*tan[j] for v,(w,p,tan,L) in zip(integrals,edges)) for j in [0,1]])
    matrix.extend(forces);matrix=np.array(matrix)
    assert matrix.shape==(width,width),matrix.shape
    def solution(Fz,Fy):
        rhs=np.zeros(width);rhs[-2:]=[Fz,Fy];return np.linalg.solve(matrix,rhs)
    torque=sum(v*(p[0]*tan[1]-p[1]*tan[0]) for v,(w,p,tan,L) in zip(integrals,edges))
    zc=float(torque@solution(0,1));yc=-float(torque@solution(1,0))
    coeff=solution(spec['shear']['Vz'],spec['shear']['Vy']);maximum=0
    for i,(w,p,tan,L) in enumerate(edges):
        q=p-centre;t=w['t'] if direct else 0
        A,B=coeff[-2:];linear=-t*(A*q[1]+B*q[0]);quadratic=-t*(A*tan[1]+B*tan[0])/2
        points=[0,L]
        if abs(quadratic)>1e-20:
            st=-linear/(2*quadratic)
            if 0<st<L:points.append(st)
        maximum=max(maximum,max(abs(coeff[i]+linear*s+quadratic*s*s)/w['t'] for s in points))
    return dict(A=area,z_G=float(centre[0]),y_G=float(centre[1]),I_y=float(moment[0,0]),I_z=float(moment[1,1]),I_yz=float(moment[0,1]),z_C=zc,y_C=yc,tau_max=maximum)
