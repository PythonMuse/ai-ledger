"""The same fictional reconciliation, instrumented with OpenTelemetry.

PythonMuse Lab: "Your AI Workflow Is Running. Who Is Watching It?"
(technical appendix, Part 5). Code licensed under MIT; see LICENSE-CODE.

Prints one trace (four spans) and two counters to the terminal. Nothing is
sent anywhere: the console exporters only print. Demo only; all data is
fictional.

Requires:  python -m pip install opentelemetry-api opentelemetry-sdk
"""

from decimal import Decimal

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Same approved rule as bank_rec.py. Amounts are Decimal, not float, so that
# cents compare exactly (see the currency note in bank_rec.py).
MATCH_TOLERANCE = Decimal("1.00")

# Name the workflow, so its telemetry is labeled with something better than
# "unknown_service".
resource = Resource.create({"service.name": "bank-reconciliation-demo"})

# Traces: print each span to the terminal as soon as it ends.
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
tracer = trace_provider.get_tracer("bank_rec_lab")

# Metrics: the reader exports every 60 seconds, and once more at shutdown,
# so this short script prints its metrics when it finishes.
metric_reader = PeriodicExportingMetricReader(
    ConsoleMetricExporter(), export_interval_millis=60000
)
metric_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
meter = metric_provider.get_meter("bank_rec_lab")

processed_counter = meter.create_counter(
    "bankrec.transactions.processed", description="Transactions compared"
)
exception_counter = meter.create_counter(
    "bankrec.exceptions", description="Transactions outside the tolerance"
)

with tracer.start_as_current_span("bank_reconciliation") as main_span:
    main_span.set_attribute("accounting.match_tolerance", str(MATCH_TOLERANCE))

    with tracer.start_as_current_span("load_transactions"):
        transactions = [
            (Decimal("100.00"), Decimal("100.00")),
            (Decimal("250.00"), Decimal("250.00")),
            (Decimal("175.00"), Decimal("170.00")),
            (Decimal("400.00"), Decimal("400.00")),
            (Decimal("125.00"), Decimal("125.00")),
            (Decimal("60.00"), Decimal("60.75")),
        ]

    with tracer.start_as_current_span("compare_transactions"):
        exceptions = sum(
            abs(bank - ledger) > MATCH_TOLERANCE for bank, ledger in transactions
        )
        processed_counter.add(len(transactions))
        exception_counter.add(exceptions)
        main_span.set_attribute("accounting.exception_count", exceptions)

    with tracer.start_as_current_span("prepare_review"):
        review_status = "review_required" if exceptions else "ready_for_review"
        main_span.set_attribute("accounting.review_status", review_status)

trace_provider.shutdown()
metric_provider.shutdown()
