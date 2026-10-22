import unittest
from tool_schema_impact import run

def schema(props,required=()):return dict(type='object',properties=props,required=list(required),additionalProperties=False)
class DomainTests(unittest.TestCase):
 def test_narrowed_range_witness(self):
  r=run({'old':schema({'n':{'type':'integer','minimum':1,'maximum':10}},['n']),'new':schema({'n':{'type':'integer','maximum':5}},['n'])});self.assertEqual(r['status'],'breaking_witness');self.assertGreater(r['counterexample']['n'],5)
 def test_new_required_field(self):
  r=run({'old':schema({}),'new':schema({'x':{'type':'string'}},['x'])});self.assertEqual(r['counterexample'],{})
 def test_removed_enum_value(self):
  r=run({'old':schema({'x':{'type':'string','enum':['alpha','beta']}},['x']),'new':schema({'x':{'type':'string','enum':['alpha']}},['x'])});self.assertEqual(r['counterexample'],{'x':'beta'})
 def test_widened_schema_no_bounded_witness(self):self.assertEqual(run({'old':schema({'n':{'type':'integer','minimum':1}},['n']),'new':schema({'n':{'type':'number','minimum':0}},['n'])})['status'],'no_counterexample_in_finite_basis')
 def test_unsupported_pattern_rejected(self):
  with self.assertRaises(ValueError):run({'old':schema({'x':{'type':'string','pattern':'a'}}),'new':schema({})})

 def test_json_schema_numeric_enum_equivalence(self):
  from tool_schema_impact.core import check_scalar
  self.assertTrue(check_scalar(1.0,{'type':'number','enum':[1]}));self.assertFalse(check_scalar(True,{'type':'number','enum':[1]}))
 def test_open_objects_not_silently_assumed_closed(self):
  with self.assertRaises(ValueError):run({'old':{'type':'object','properties':{}},'new':schema({})})
