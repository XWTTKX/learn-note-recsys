import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from recommender import Recommender,temporal_split
from import_qilin import convert
class RecTest(unittest.TestCase):
    def test_no_future_popularity(self):
        rows=[{'request_id':str(t),'timestamp':t,'user':'u','history':[],
               'candidates':[{'id':'early' if t<7 else 'future','click':1}]} for t in range(10)]
        train,test=temporal_split(rows)
        self.assertLess(max(r['timestamp'] for r in train),min(r['timestamp'] for r in test))
        model=Recommender(train)
        self.assertNotIn('future',model.catalog)
        self.assertEqual(model.rank(['early']),[])
        self.assertEqual(model.rank([]),['early'])
    def test_duplicate_and_milliseconds(self):
        row={'request_id':'r','user_id':'u','recent_clicked_note_ids':'[]',
          'rec_result_details':'[{"note_id":"a","click":0,"request_timestamp":1732709057254},{"note_id":"a","click":1,"request_timestamp":1732709057254}]'}
        r=convert(row)
        self.assertEqual(r['candidates'],[{'id':'a','click':1}])
        self.assertAlmostEqual(r['timestamp'],1732709057.254)
