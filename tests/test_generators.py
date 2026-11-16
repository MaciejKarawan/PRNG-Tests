import contextlib, io, importlib, unittest
import numpy as np
from prng_tests.generators.lcg import lcg
from prng_tests.generators.glcg import glcg
from prng_tests.generators.rc4 import rc4
from prng_tests.generators.xorshift import xorshift
class ProjectTests(unittest.TestCase):
    def test_imports_do_not_parse_args_or_generate(self):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            for name in ['lcg','glcg','rc4','rc4_multiple_keys','xorshift']:
                importlib.reload(importlib.import_module('prng_tests.generators.'+name))
        self.assertEqual(output.getvalue(), '')
    def test_lcg_known_sequence(self):
        np.testing.assert_array_equal(lcg(6,1,16,5,3), [1,8,11,10,5,12])
    def test_deterministic_generator_shapes(self):
        for call in [lambda: glcg(8,np.array([1,2]),16,np.array([3,5])), lambda: rc4('101',8,32), lambda: xorshift(8,123)]:
            np.testing.assert_array_equal(call(),call())
            self.assertEqual(len(call()),8)
if __name__ == '__main__':unittest.main()
