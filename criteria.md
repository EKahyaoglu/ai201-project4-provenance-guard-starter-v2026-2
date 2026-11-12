# Acceptance criteria: failure handling

These criteria were written before measuring the retry and structured-logging
extension. They test the bad paths rather than only the normal classifier.

## 1. Temporary detector recovery

When the detector fails once and succeeds on the next call, all three trials
must return HTTP 201, use exactly two attempts, and write a decided audit entry.

Why this target: a short-lived model failure should not make a valid submission
fail when a bounded retry can recover it.

## 2. Permanent detector failure

When every detector call fails, all three trials must return HTTP 503 after
exactly three total attempts, and each trial must write one rejected audit
record with `reason: "detector_unavailable"`.

Why this target: retries must have a hard limit so an unavailable model cannot
hold a request open forever or turn into an unexplained 500.

## 3. Invalid input avoids expensive work

For missing, empty, non-string, and oversized text, all three trials must
return a 4xx response and invoke neither detector signal.

Why this target: malformed input should be rejected before model work is spent.

## 4. Rate-limit rejection is visible

Across three flood trials of 15 requests from one creator, at least one request
per trial must return HTTP 429 and the audit log must contain a matching
`rate_limited` rejection.

Why this target: rate limiting only helps if rejected abuse is both blocked and
diagnosable.

## 5. Every submission has structured timing data

Across three trials containing one valid request and one rejected request,
every `/submit` request must create a `request_completed` record containing
`timestamp`, `input`, `output`, `status`, and non-negative `duration_ms`.

Why this target: failure handling needs measurable evidence of what arrived,
what the client received, and how long the service took.
