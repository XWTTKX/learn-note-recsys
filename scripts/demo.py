import argparse,json
from pathlib import Path
from recommender import Recommender,temporal_split
from metrics import metrics

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--data',type=Path,default=Path(__file__).resolve().parents[1]/'data/sample/requests.jsonl')
    p.add_argument('--test',type=Path,help='Explicit held-out split; --data then contains training requests')
    p.add_argument('--k',type=int,default=5)
    args=p.parse_args()
    rows=[json.loads(line) for line in args.data.read_text().splitlines() if line.strip()]
    if args.test:
        train=rows
        test=[json.loads(line) for line in args.test.read_text().splitlines() if line.strip()]
        if not train or not test: raise ValueError('empty split')
        if set(r['request_id'] for r in train)&set(r['request_id'] for r in test): raise ValueError('request overlap')
    else: train,test=temporal_split(rows)
    model=Recommender(train)
    for protocol in ('full-train-catalog','logged-candidates'):
        for method in ('popular','itemcf'):
            values=[]; empty=0; oov=0; positive=0
            for r in test:
                relevant={x['id'] for x in r['candidates'] if x['click']==1}
                # No seen filter for logged reranking: evaluate exactly the logged candidate pool.
                if protocol=='full-train-catalog': relevant-=set(r['history'])
                positive+=len(relevant);oov+=len(relevant-model.catalog)
                candidates=[x['id'] for x in r['candidates']] if protocol=='logged-candidates' else None
                ranking=model.rank(r['history'],candidates,method,args.k,filter_seen=protocol=='full-train-catalog')
                value=metrics(ranking,relevant,args.k)
                if value is None: empty+=1
                else: values.append(value)
            print(json.dumps({'input':args.data.name,'train_requests':len(train),'test_requests':len(test),
                'protocol':protocol,'method':method,'k':args.k,'catalog':len(model.catalog),
                'excluded_no_positive':empty,'positive_oov_rate':oov/positive if positive else None,
                'metrics':{k:sum(v[k] for v in values)/len(values) for k in values[0]} if values else {}},ensure_ascii=False))
if __name__=='__main__': main()
