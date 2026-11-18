"""Tests of the MONDO matching rules on a tiny fixture.

Run:  python "Phase 4 - Entity Definition/src/tests/test_mondo_matching.py" -v
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from mondo_matching import MondoIndex, descendants, is_metastasis, normalize, strip_final_parentheses  # noqa: E402

T = lambda label, exact=(), other=(), dep=False: dict(label=label, exact=set(exact), other=set(other), deprecated=dep)  # noqa: E731
TERMS = {
    "MONDO:1": T("lung adenocarcinoma"),
    "MONDO:2": T("glioblastoma", exact=["glioblastoma multiforme"]),
    "MONDO:3": T("crohn disease", other=["crohn's-like disease"]),
    "MONDO:4": T("old term", dep=True),
    "MONDO:5": T("twin a", exact=["shared name"]),
    "MONDO:6": T("twin b", exact=["shared name"]),
    "MONDO:7": T("colorectal tumor"),
    "MONDO:8": T("myeloma"),
    "MONDO:90": T("non-human animal disease"),
    "MONDO:91": T("myeloma, non-human animal", exact=["myeloma"]),
}
TERMS["MONDO:91"]["parents"] = {"MONDO:90"}


class TestRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.idx = MondoIndex(TERMS)

    def test_normalize(self):
        self.assertEqual(normalize("Crohn's  disease-like, Tumour"), "crohn disease like tumor")

    def test_strip_parentheses(self):
        self.assertEqual(strip_final_parentheses("Lung adenocarcinoma (LUAD)"), "Lung adenocarcinoma")

    def test_label(self):
        self.assertEqual(self.idx.match("Lung adenocarcinoma")["mondoId"], "MONDO:1")

    def test_exact_synonym(self):
        self.assertEqual(self.idx.match("Glioblastoma Multiforme")["mondoId"], "MONDO:2")

    def test_without_parentheses(self):
        m = self.idx.match("Lung adenocarcinoma (LUAD)")
        self.assertEqual((m["status"], m["mondoId"], m["matchedOn"]), ("resolved", "MONDO:1", "without final parentheses"))

    def test_uk_spelling_normalized(self):
        self.assertEqual(self.idx.match("Colorectal tumour")["mondoId"], "MONDO:7")

    def test_related_only_not_resolved(self):
        m = self.idx.match("Crohn's-like disease")
        self.assertEqual((m["status"], m["mondoId"], m["candidates"]), ("related_only", "", "MONDO:3"))

    def test_ambiguous(self):
        self.assertEqual(self.idx.match("Shared name")["status"], "ambiguous")

    def test_obsolete_ignored(self):
        self.assertEqual(self.idx.match("Old term")["status"], "no_match")

    def test_abbreviation_alone_not_used(self):  # "(LUAD)" alone is never tried
        self.assertEqual(self.idx.match("LUAD")["status"], "no_match")

    def test_non_human_excluded(self):  # D24
        self.assertEqual(self.idx.match("Myeloma")["status"], "ambiguous")
        idx2 = MondoIndex(TERMS, skip=descendants(TERMS, "MONDO:90"))
        self.assertEqual(idx2.match("Myeloma")["mondoId"], "MONDO:8")

    def test_metastasis_flag(self):
        self.assertTrue(is_metastasis("Lung cancer brain metastasis"))


if __name__ == "__main__":
    unittest.main()
