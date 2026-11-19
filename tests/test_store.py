import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from main import Store, Api

class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=Store(Path(self.tmp.name)/'data'/'maiz_urbano.db')
    def tearDown(self):self.tmp.cleanup()
    def test_seed_and_sale_persist(self):
        item=self.store.bootstrap()['products'][0]
        result=self.store.sale([{'id':item['id'],'quantity':2}],'efectivo')
        self.assertEqual(result['total_cents'],item['price_cents']*2)
        new=Store(self.store.path)
        self.assertEqual(new.sales()[0]['total_cents'],result['total_cents'])
        self.assertEqual(len(new.sales()),1)
    def test_invalid_sale_rolls_back(self):
        with self.assertRaises(ValueError):self.store.sale([{'id':'des-cre-g','quantity':2},{'id':'missing','quantity':1}])
        self.assertFalse(self.store.sales())
    def test_stock_expiry_and_waste(self):
        item=self.store.inventory()[0]
        self.store.add_stock(item['id'],3,'2026-11-22')
        self.store.add_stock(item['id'],2,'2026-11-30')
        self.store.add_waste(item['id'],4,'Deteriorado')
        current=next(x for x in self.store.inventory() if x['id']==item['id'])
        self.assertAlmostEqual(current['quantity'],1)
        self.assertEqual(current['nearest_expiry'],'2026-11-30')
        with self.assertRaises(ValueError):self.store.add_waste(item['id'],3,'No permitido')
        self.assertAlmostEqual(next(x for x in self.store.inventory() if x['id']==item['id'])['quantity'],1)
    def test_report_snapshot_is_stable(self):
        week=date.today()-timedelta(days=date.today().weekday())
        a=self.store.generate_report(week.isoformat())
        self.store.sale([{'id':'tostielote','quantity':1}])
        b=self.store.generate_report(week.isoformat())
        self.assertEqual(a['snapshot']['sales_total_cents'],0)
        self.assertEqual(self.store.report(a['id'])['snapshot']['sales_total_cents'],0)
        self.assertEqual(b['snapshot']['sales_total_cents'],7000)
    def test_cash_close(self):
        self.store.cash_open(100)
        self.store.sale([{'id':'tostielote','quantity':1}])
        self.store.movement('expenses','Gas',20)
        self.store.cash_close(150)
        a=self.store.cash_status()['recent'][0]
        self.assertEqual(a['expected_cents'],15000)
        self.assertEqual(a['counted_cents'],15000)
    def test_api_result_errors(self):
        api=Api(self.store)
        self.assertFalse(api.call('sale',{'items':[{'id':'bad','quantity':1}]})['ok'])
        self.assertTrue(api.call('bootstrap')['ok'])

if __name__=='__main__':unittest.main()