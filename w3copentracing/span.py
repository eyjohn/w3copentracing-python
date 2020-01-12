import opentracing
from dataclasses import dataclass

from .context import SpanContext

@dataclass
class Span(opentracing.Span):
    """W3C compatible Span with deterministic modifiable SpanContext."""

    context: SpanContext
