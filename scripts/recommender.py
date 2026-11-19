"""Request-level, train-only popularity and ItemCF; not a CTR model."""
import math
from collections import Counter,defaultdict

class Recommender:
    def __init__(self, requests):
        self.pop=Counter()
        histories=defaultdict(set)
        self.catalog=set()
        for r in requests:
            for x in r['candidates']:
                self.catalog.add(x['id'])
                if x['click'] == 1:
                    self.pop[x['id']]+=1
                    histories[r['user']].add(x['id'])
        users=Counter()
        co=defaultdict(Counter)
        for items in histories.values():
            for a in items:
                users[a]+=1
                for b in items:
                    if a!=b: co[a][b]+=1/math.log2(2+len(items))
        self.sim={a:{b:v/math.sqrt(users[a]*users[b]) for b,v in row.items()} for a,row in co.items()}

    def rank(self, history, candidates=None, method='itemcf', k=10, filter_seen=True):
        if k<=0: raise ValueError('k must be positive')
        if method not in ('popular','itemcf'): raise ValueError('unknown method')
        seen=set(history)
        pool=set(self.catalog if candidates is None else candidates)
        if filter_seen: pool-=seen
        def key(i):
            cf=sum(self.sim.get(h,{}).get(i,0) for h in seen) if method=='itemcf' else 0
            return (-cf,-self.pop[i],i)
        return sorted(pool,key=key)[:k]

def temporal_split(rows, fraction=.7):
    if len(rows)<2: raise ValueError('need at least two requests')
    rows=sorted(rows,key=lambda x:(x['timestamp'],x['request_id']))
    if len({x['request_id'] for x in rows}) != len(rows): raise ValueError('duplicate request ID')
    boundary=rows[min(len(rows)-1,max(1,int(len(rows)*fraction)))]['timestamp']
    train=[r for r in rows if r['timestamp']<boundary]
    test=[r for r in rows if r['timestamp']>=boundary]
    if not train or not test: raise ValueError('timestamps cannot produce nonempty chronological split')
    return train,test
