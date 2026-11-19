"""Convert official toy CSV (raw-ID JSON columns) or full parquet into requests.
Never eval serialized cells. Full parquet requires pyarrow; column checks fail closed.
"""
import argparse,csv,json
from pathlib import Path

def convert(row, indexed=False):
    details_key='rec_result_details_with_idx' if indexed else 'rec_result_details'
    history_key='recent_clicked_note_idxs' if indexed else 'recent_clicked_note_ids'
    id_key='note_idx' if indexed else 'note_id'
    user_key='user_idx' if indexed else 'user_id'
    request_key='request_idx' if 'request_idx' in row else 'request_id'
    details=row[details_key]; history=row[history_key]
    if isinstance(details,str): details=json.loads(details)
    if isinstance(history,str): history=json.loads(history)
    if hasattr(details,'tolist'): details=details.tolist()
    if hasattr(history,'tolist'): history=history.tolist()
    if not isinstance(details,list) or not details: raise ValueError('empty or malformed details')
    candidates={}
    stamps=[]
    for d in details:
        item=str(d[id_key]); click=int(d['click'])
        if click not in (0,1): raise ValueError('unknown click label')
        # Multiple exposures in a request: explicitly aggregate click by max.
        candidates[item]={'id':item,'click':max(click,candidates.get(item,{}).get('click',0))}
        ts=float(d['request_timestamp'])
        stamps.append(ts/1000 if ts>100000000000 else ts)
    return {'request_id':str(row[request_key]),'user':str(row[user_key]),'timestamp':min(stamps),
            'history':[str(x) for x in history],'candidates':list(candidates.values())}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('input',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--indexed',action='store_true',help='For structured full-data note_idx fields; not numpy-string toy columns')
    args=p.parse_args()
    if args.input.resolve()==args.output.resolve(): raise ValueError('input and output must differ')
    if args.output.exists(): raise FileExistsError('choose a new output path')
    def records():
        if args.input.suffix=='.csv':
            with args.input.open(newline='') as f: yield from csv.DictReader(f)
        elif args.input.suffix=='.parquet':
            import pyarrow.parquet as pq
            for batch in pq.ParquetFile(args.input).iter_batches(batch_size=256): yield from batch.to_pylist()
        else: raise ValueError('supported inputs: .csv, .parquet')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    count=0; ids=set()
    with args.output.open('x') as out:
        for row in records():
            value=convert(row,args.indexed)
            if value['request_id'] in ids: raise ValueError('duplicate request ID')
            ids.add(value['request_id'])
            out.write(json.dumps(value,ensure_ascii=False)+'\n'); count+=1
    print(json.dumps({'requests':count,'output':str(args.output)}))
if __name__=='__main__': main()
