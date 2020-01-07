import unittest
from w3copentracing import Tracer, SpanContext
from opentracing import Format


class TestSpanContext(unittest.TestCase):

    valid_carrier = {
        "trace-parent": "00-01000000000000000000000000000000-0200000000000000-01"}
    valid_context = SpanContext(b"\x01" + b"\x00" * 15, b"\x02" + b"\x00" * 7)

    def test_inject(self):
        tracer = Tracer()
        for fmt in (Format.TEXT_MAP, Format.HTTP_HEADERS):
            carrier = {}
            tracer.inject(self.valid_context, fmt, carrier)
            self.assertEqual(carrier, self.valid_carrier)

    def test_extract(self):
        tracer = Tracer()
        for fmt in (Format.TEXT_MAP, Format.HTTP_HEADERS):
            context = tracer.extract(fmt, self.valid_carrier)
            self.assertEqual(context, self.valid_context)
