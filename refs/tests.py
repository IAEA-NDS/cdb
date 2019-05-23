from django.test import TestCase
from refs.models import get_source_from_doi

class RefFromDOITest(TestCase):

    maxDiff = 1000

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_ref_created(self):
        doi = '10.1007/s10751-015-1166-4'
        ref = get_source_from_doi(doi)
        self.assertEqual(str(ref), """None: V. A. Dzuba, V. V. Flambaum, Highly charged ions for atomic clocks and search for variation of the fine structure constant""")
        self.assertEqual(ref.html(), """BNone: V. A. Dzuba, V. V. Flambaum, "Highly charged ions for atomic clocks and search for variation of the fine structure constant", <em>Hyperfine Interactions</em> <b>236</b>, 79-86 (2015). <span class="noprint"> [<a href="http://dx.doi.org/10.1007/s10751-015-1166-4">link to article</a>]</span>""")
