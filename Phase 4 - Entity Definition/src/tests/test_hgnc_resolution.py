"""Tests of the HGNC resolution on a tiny HGNC-like fixture (one case per status).

Run:  python "Phase 4 - Entity Definition/src/tests/test_hgnc_resolution.py" -v
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import is_valid_hgnc_id, normalize_symbol, split_pipe  # noqa: E402
from hgnc_resolution import HGNCResolver, apply_policy  # noqa: E402

FIXTURE = [
    dict(hgnc_id="HGNC:1", symbol="AAA1", name="gene a", status="Approved", prev_symbol="OLD1", alias_symbol=""),
    dict(hgnc_id="HGNC:2", symbol="BBB2", name="gene b", status="Approved", prev_symbol="", alias_symbol='"XX1|AAA1"'),
    dict(hgnc_id="HGNC:3", symbol="C1orf9", name="gene c", status="Approved", prev_symbol="", alias_symbol="SHARED"),
    dict(hgnc_id="HGNC:4", symbol="DDD4", name="gene d", status="Approved", prev_symbol="SHARED", alias_symbol=""),
    dict(hgnc_id="HGNC:5", symbol="EEE5", name="gene e", status="Approved", prev_symbol="", alias_symbol=""),
    dict(hgnc_id="HGNC:6", symbol="eee5", name="gene e bis", status="Approved", prev_symbol="", alias_symbol=""),
    dict(hgnc_id="BAD7", symbol="FFF7", name="bad id", status="Approved", prev_symbol="", alias_symbol=""),
]


class TestNormalization(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize_symbol("  c1orf9 "), "C1ORF9")
        self.assertEqual(normalize_symbol(None), "")

    def test_split_pipe(self):
        self.assertEqual(split_pipe('"A|B"'), ["A", "B"])
        self.assertEqual(split_pipe(""), [])

    def test_hgnc_id_format(self):
        self.assertTrue(is_valid_hgnc_id("HGNC:11998"))
        self.assertFalse(is_valid_hgnc_id("11998"))


class TestResolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = HGNCResolver(FIXTURE)

    def test_resolved_case_insensitive(self):
        out = self.r.resolve(" c1orf9")
        self.assertEqual((out["status"], out["hgnc_id"], out["approved_symbol"]), ("resolved", "HGNC:3", "C1orf9"))

    def test_resolved_with_warning(self):
        out = self.r.resolve("AAA1")  # approved for HGNC:1, alias of HGNC:2
        self.assertEqual(out["status"], "resolved")
        self.assertEqual(out["hgnc_id"], "HGNC:1")
        self.assertIn("HGNC:2", out["warning"])

    def test_non_approved_match(self):
        out = self.r.resolve("SHARED")
        self.assertEqual(out["status"], "non_approved_match")
        self.assertEqual(out["candidates"], "HGNC:3|HGNC:4")
        self.assertEqual(out["hgnc_id"], "")

    def test_ambiguous(self):
        out = self.r.resolve("EEE5")  # two approved entries differ only in case
        self.assertEqual(out["status"], "ambiguous")
        self.assertEqual(out["candidates"], "HGNC:5|HGNC:6")

    def test_not_found(self):
        self.assertEqual(self.r.resolve("ZZZ9")["status"], "not_found")

    def test_invalid(self):
        self.assertEqual(self.r.resolve("  ")["status"], "invalid")
        self.assertEqual(self.r.resolve("AB CD")["status"], "invalid")

    def test_malformed_hgnc_id_skipped(self):
        self.assertEqual(self.r.bad_ids, ["BAD7"])
        self.assertEqual(self.r.resolve("FFF7")["status"], "not_found")


class TestPolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = HGNCResolver(FIXTURE + [dict(hgnc_id="HGNC:8", symbol="GGG8", name="gene g", status="Approved",
                                              prev_symbol="UNIQ", alias_symbol="")])

    def test_unique_alias_resolved(self):  # D20
        out = apply_policy(self.r.resolve("uniq"), self.r.by_id)
        self.assertEqual((out["status"], out["hgnc_id"], out["resolution_method"], out["in_kg"]),
                         ("resolved", "HGNC:8", "prev_or_alias", "yes"))

    def test_multi_candidate_alias_not_resolved(self):  # D20
        out = apply_policy(self.r.resolve("SHARED"), self.r.by_id)
        self.assertEqual((out["status"], out["in_kg"]), ("non_approved_match", "no"))

    def test_only_resolved_in_kg(self):  # D21
        self.assertEqual(apply_policy(self.r.resolve("ZZZ9"), self.r.by_id)["in_kg"], "no")
        self.assertEqual(apply_policy(self.r.resolve("AAA1"), self.r.by_id)["resolution_method"], "approved_symbol")


if __name__ == "__main__":
    unittest.main()
