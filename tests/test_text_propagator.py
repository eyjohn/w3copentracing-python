import unittest
from w3copentracing import SpanContext, TextPropagator
from opentracing.propagation import SpanContextCorruptedException


class TestTextPropagator(unittest.TestCase):

    basic_test_cases = [
        (
            # Simple span, sampled
            {"trace-parent": "00-01000000000000000000000000000000-0200000000000000-01"},
            SpanContext(b"\x01" + b"\x00" * 15, b"\x02" + b"\x00" * 7)
        ),
        (
            # Unsampled Span
            {"trace-parent": "00-01000000000000000000000000000000-0200000000000000-00"},
            SpanContext(b"\x01" + b"\x00" * 15, b"\x02" + b"\x00" * 7, False)

        ),
        (
            # Span with Baggage
            {"trace-parent": "00-01000000000000000000000000000000-0200000000000000-01",
             "trace-state": "key1=val1,key2=val2"},
            SpanContext(b"\x01" + b"\x00" * 15, b"\x02" + b"\x00" * 7,
                        baggage={"key1": "val1", "key2": "val2"})
        ),
        (
            # No Span
            {},
            None
        )
    ]

    def test_inject(self):
        propagator = TextPropagator()
        for expected_carrier, context in self.basic_test_cases:
            carrier = {}
            propagator.inject(context, carrier)
            self.assertEqual(carrier, expected_carrier)

    def test_extract(self):
        propagator = TextPropagator()
        for carrier, expected_context in self.basic_test_cases:
            span_context = propagator.extract(carrier)
            self.assertEqual(span_context, expected_context)

    def test_extract_fail(self):
        fail_cases = [
            # Bad Version
            {"trace-parent": "01-01000000000000000000000000000000-0200000000000000-00"},

            # Malformed
            {"trace-parent": "00-010000000000000000000000000000-0200000000000000-00"},
            {"trace-parent": "00-0100000000000000000000000000000200000000000000-00"},

            # Not Hex
            {"trace-parent": "00-010000000000000000000000000000ZZ-0200000000000000-00"},

            # Bad Flags
            {"trace-parent": "00-010000000000000000000000000000ZZ-0200000000000000-02"}
        ]

        propagator = TextPropagator()
        for carrier in fail_cases:
            with self.assertRaises(SpanContextCorruptedException):
                propagator.extract(carrier)
