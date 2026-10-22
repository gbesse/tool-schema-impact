import itertools,math
from .common import integer,number
TYPES={'string','integer','number','boolean','null'}
def check_scalar(v,s):
    kind=s['type'];ok={'string':isinstance(v,str),'integer':isinstance(v,int) and not isinstance(v,bool),'number':isinstance(v,(int,float)) and not isinstance(v,bool),'boolean':isinstance(v,bool),'null':v is None}[kind]
    if not ok:return False
    if 'enum' in s and not any((type(v)==type(x) or isinstance(v,(int,float)) and not isinstance(v,bool) and isinstance(x,(int,float)) and not isinstance(x,bool)) and v==x for x in s['enum']):return False
    if kind in ('number','integer') and not s.get('minimum',-math.inf)<=v<=s.get('maximum',math.inf):return False
    if kind=='string' and not s.get('minLength',0)<=len(v)<=s.get('maxLength',10000):return False
    return True
def validate_schema(s):
    if set(s)-{'type','properties','required','additionalProperties'} or s.get('type')!='object' or not isinstance(s.get('properties'),dict):raise ValueError('unsupported_schema')
    if s.get('additionalProperties') is not False:raise ValueError('additional_properties_subset')
    if not set(s.get('required',[]))<=set(s['properties']):raise ValueError('required')
    for p in s['properties'].values():
        if set(p)-{'type','enum','minimum','maximum','minLength','maxLength'} or p.get('type') not in TYPES:raise ValueError('unsupported_property')
        if 'enum' in p:
            if not isinstance(p['enum'],list) or len(p['enum'])>20 or any(isinstance(v,(dict,list)) for v in p['enum']):raise ValueError('enum')
        for key in ('minimum','maximum'):
            if key in p:number(p[key],-10**12,10**12)
        for key in ('minLength','maxLength'):
            if key in p:integer(p[key],0,10000)
        if p.get('minimum',-math.inf)>p.get('maximum',math.inf) or p.get('minLength',0)>p.get('maxLength',10000):raise ValueError('bounds')
def accepts(obj,s):return set(obj)<=set(s['properties']) and set(s.get('required',[]))<=set(obj) and all(check_scalar(v,s['properties'][k]) for k,v in obj.items())
def run(data):
    old=data['old'];new=data['new'];validate_schema(old);validate_schema(new);keys=sorted(set(old['properties'])|set(new['properties']))
    if len(keys)>8:raise ValueError('size')
    missing=object();options=[]
    for key in keys:
        schemas=[s['properties'][key] for s in (old,new) if key in s['properties']];values=[None,False,True,0,1,-1,'','x']
        for s in schemas:
            values+=s.get('enum',[])
            for k in ('minimum','maximum'):
                if k in s:values += [s[k]-1,s[k],s[k]+1]
            for k in ('minLength','maxLength'):
                if k in s:values += ['x'*n for n in (max(0,s[k]-1),s[k],min(10001,s[k]+1))]
        unique=[]
        for v in values:
            if not any(type(v)==type(x) and v==x for x in unique):unique.append(v)
        options.append([missing]+[v for v in unique if key in old['properties'] and check_scalar(v,old['properties'][key])])
    states=math.prod(len(o) for o in options)
    if states>100000:raise ValueError('candidate_limit')
    tested=0
    for selection in itertools.product(*options):
        obj={k:v for k,v in zip(keys,selection) if v is not missing}
        if not accepts(obj,old):continue
        tested+=1
        if not accepts(obj,new):return {'counterexample':obj,'old_accepts':True,'new_accepts':False,'tested':tested,'status':'breaking_witness'}
    return {'counterexample':None,'tested':tested,'status':'no_counterexample_in_finite_basis','scope':'flat closed objects; finite enum/type/boundary basis, not general JSON Schema inclusion proof'}
