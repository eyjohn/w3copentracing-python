import unittest
from w3copentracing import SpanContext


class TestSpanContext(unittest.TestCase):
    def test_instantiate(self):
        SpanContext(b"01234567890abcdef", b"01234567", False)
        SpanContext(b"01234567890abcdef", b"01234567", False, {"key": "val"})
