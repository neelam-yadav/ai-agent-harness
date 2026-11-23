import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# Minimal module stubs allow isolated validator tests when packages are not installed.
try:
    import openai, dotenv, requests, bs4
except ImportError:
    import types
    for module in ('openai','dotenv','requests','bs4'):
        if module not in sys.modules: sys.modules[module] = types.ModuleType(module)
    sys.modules['openai'].OpenAI = object
    sys.modules['dotenv'].load_dotenv = lambda *args, **kwargs: None
    sys.modules['bs4'].BeautifulSoup = object
from main import validate, fetch_page, model_json

class HarnessTests(unittest.TestCase):
    def test_accepts_sourced_price(self):
        page='Starter plan costs $10 per user each month.'
        result=validate('Example', {'plans':[{'name':'Starter','price':10,'currency':'USD','period':'monthly','billing':'monthly','evidence':'Starter plan costs $10 per user each month.'}]}, 'https://example.com/pricing', page)
        self.assertEqual(result['plans'][0]['price'],10)
    def test_rejects_fake_evidence(self):
        with self.assertRaises(ValueError):
            validate('Example',{'plans':[{'name':'Starter','price':10,'evidence':'Price is $10'}]},'https://example.com/pricing','Only contact sales shown here.')
    def test_rejects_non_https(self):
        with self.assertRaises(ValueError):
            fetch_page('http://example.com/pricing','example.com')
    def test_rejects_other_domains(self):
        with self.assertRaises(ValueError):
            fetch_page('https://not-example.com/pricing','example.com')
    def test_rejects_empty_plans(self):
        with self.assertRaises(ValueError):
            validate('Example',{'plans':[]},'https://example.com','text')

if __name__=='__main__': unittest.main()
