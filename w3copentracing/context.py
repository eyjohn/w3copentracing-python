import opentracing
import secrets
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

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(trace_id={self.trace_id.hex().upper()!r},'
                f' span_id={self.span_id.hex().upper()!r},'
                f' sampled={self.sampled!r},'
                f' baggage={self.baggage!r})')


def generate_span_id() -> bytes:
    return secrets.token_bytes(8)


def generate_trace_id() -> bytes:
    return secrets.token_bytes(16)
