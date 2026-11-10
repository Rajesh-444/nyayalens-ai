import unittest

from nyayalens.retriever import Document, TfidfRetriever
from nyayalens.triage import UrgencyTriage


DOCUMENTS = [
    Document("PAY", "Unpaid salary", "Keep payslips and request final wages.", "Test guide"),
    Document("CYB", "Account hacked", "Preserve screenshots and reset credentials.", "Test guide"),
]


class RetrieverTests(unittest.TestCase):
    def setUp(self):
        self.retriever = TfidfRetriever(DOCUMENTS)

    def test_ranks_relevant_document_first(self):
        results = self.retriever.search("salary payslips wages")
        self.assertEqual(results[0].document.id, "PAY")
        self.assertGreater(results[0].score, results[1].score)

    def test_empty_query_returns_stable_results(self):
        self.assertEqual([result.document.id for result in self.retriever.search("")], ["CYB", "PAY"])

    def test_result_has_auditable_citation(self):
        self.assertEqual(self.retriever.search("hacked")[0].citation, "[CYB] Account hacked - Test guide")

    def test_rejects_invalid_limit(self):
        with self.assertRaises(ValueError):
            self.retriever.search("salary", 0)


class TriageTests(unittest.TestCase):
    def test_urgent_signal_is_explainable(self):
        result = UrgencyTriage().classify("I received a threat of violence")
        self.assertEqual(result.label, "urgent")
        self.assertEqual(result.matched_signals, ("threat", "violence"))

    def test_default_is_standard(self):
        self.assertEqual(UrgencyTriage().classify("I want a copy of my invoice").label, "standard")


if __name__ == "__main__":
    unittest.main()

