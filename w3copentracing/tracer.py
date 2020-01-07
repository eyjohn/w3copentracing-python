import opentracing

from .context import SpanContext


class Tracer(opentracing.Tracer):
    """Partial implementation of a tracer with W3C compatible propagator.

    By default, this Tracer registers propagators for 
    :attr:`opentracing.Format.TEXT_MAP` and :attr:`opentracing.Format.HTTP_HEADERS`.
    The user should call :func:`register_propagator()` for each additional 
    inject/extract format.
    """

    def __init__(self, scope_manager=None):
        """Initialize a Tracer instance."""
        super(Tracer, self).__init__(scope_manager)

        self._propagators = {}
        self._register_required_propagators()

    def register_propagator(self, format, propagator):
        """Register a propagator with this Tracer.

        :param string format: a :class:`~opentracing.Format`
            identifier like :attr:`~opentracing.Format.TEXT_MAP`
        :param **Propagator** propagator: a **Propagator** instance to handle
            inject/extract calls involving `format`
        """
        self._propagators[format] = propagator

    def _register_required_propagators(self):
        from .text_propagator import TextPropagator
        self.register_propagator(opentracing.Format.TEXT_MAP, TextPropagator())
        self.register_propagator(
            opentracing.Format.HTTP_HEADERS, TextPropagator())

    def inject(self, span_context, format, carrier):
        if format in self._propagators:
            self._propagators[format].inject(span_context, carrier)
        else:
            raise opentracing.UnsupportedFormatException()

    def extract(self, format, carrier):
        if format in self._propagators:
            return self._propagators[format].extract(carrier)
        else:
            raise opentracing.UnsupportedFormatException()
