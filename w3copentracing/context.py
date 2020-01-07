import opentracing
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class SpanContext(opentracing.SpanContext):
    """W3C compatible SpanContext satisfies the opentracing.SpanContext contract.

    This object consists of:
    - trace_id of 16 bytes
    - span_id if 8 bytes
    - sampled flag as a boolean
    - dict of baggage key, value pairs
    """

    trace_id: bytes
    span_id: bytes
    sampled: bool = True
    baggage: Optional[Dict[str, str]] = None
