import unittest

from skills.view_obj import CapabilityBreakdown


class TestCapabilityBreakdown(unittest.TestCase):

    def test_happy_path(self):
        cb = CapabilityBreakdown(distribution=[1, 4, 16, 8, 3])

        self.assertEqual(32, cb.sum)
        self.assertEqual('3.25', cb.avg['val'])
        self.assertEqual(19.8, cb.avg['rel_val'])