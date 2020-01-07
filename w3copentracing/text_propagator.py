from opentracing import SpanContextCorruptedException

from .context import SpanContext


class InvalidSpanContextException(Exception):
    """InvalidSpanContextException is used  when the provided span context
    instance does is not a W3C span context."""
    pass


class TextPropagator(object):
    """A W3C Trace Context compatible Propagator for Format.TEXT_MAP."""

    def inject(self, span_context, carrier):
        if span_context is None:
            return

        if not isinstance(span_context, SpanContext):
            raise InvalidSpanContextException()

        carrier["trace-parent"] = ("00-" + span_context.trace_id.hex().upper() +
                                   "-" + span_context.span_id.hex().upper() +
                                   ("-01" if span_context.sampled else "-00"))

        if span_context.baggage is not None:
            carrier["trace-state"] = ",".join(k+"=" +
                                              v for (k, v) in span_context.baggage.items())

    def extract(self, carrier):
        trace_parent = carrier.get("trace-parent", None)
        if trace_parent is None:
            return None

        try:
            (version, trace_id, span_id, sampled) = trace_parent.split("-")

            trace_id = bytes.fromhex(trace_id)
            span_id = bytes.fromhex(span_id)

            if version != "00" or sampled not in ("00", "01") or len(trace_id) != 16 or len(span_id) != 8:
                raise SpanContextCorruptedException()

            sampled = (sampled == "01")

            baggage = None
            trace_state = carrier.get("trace-state", None)
            if trace_state is not None:
                baggage = dict((x.strip() for x in p.split("="))
                               for p in trace_state.split(","))

            return SpanContext(trace_id, span_id, sampled, baggage)

        except ValueError:
            raise SpanContextCorruptedException()
