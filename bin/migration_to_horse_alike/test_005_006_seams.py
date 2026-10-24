import pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent
class OwnershipTests(unittest.TestCase):
 def test_templates_owned_only_by_005(self):
  for script in HERE.glob('[0-9][0-9][0-9]_*.py'):
   if script.name.startswith('005_'):continue
   if script.name.startswith(('006_','007_')):
    self.assertNotIn("src/templates/", script.read_text())
 def test_payload_templates_have_new_bindings(self):
  for p in (HERE/'payload/templates').glob('*.pynml'):
   if p.stem=='header':continue
   s=p.read_text()
   self.assertNotIn('${consist.',s)
   self.assertNotIn('${vehicle.',s)
   self.assertIn('model_variant',s) if p.stem!='capacity_switches' else None
if __name__=='__main__':unittest.main()
