# Failure-handling run log

- System: Provenance Guard
- Shape: B
- Test method: Flask test client with detector stubs
- Trials: 3 per criterion
- Baseline: `DETECTOR_RETRIES=0`
- After: `DETECTOR_RETRIES=2`, `DETECTOR_RETRY_DELAY=0`

| Criterion | Before fix, trials 1-3 | After fix, trials 1-3 | Verdict |
|---|---|---|---|
| Temporary detector recovery | 503 after 1 attempt, 3/3 | 201 after 2 attempts, 3/3 | MET |
| Permanent detector failure | 503 after 1 attempt, 3/3 | 503 after 3 attempts, 3/3 | MET |
| Invalid input avoids detector work | 4xx, detector calls 0, 3/3 | 4xx, detector calls 0, 3/3 | MET |
| Rate-limit rejection is visible | 429 plus rejection log, 3/3 | 429 plus rejection log, 3/3 | MET |
| Structured timing data | No completion record, 3/3 | Complete record, 3/3 | MET |

## Diagnosis

- The retry criterion changed because the new retry loop converts a transient
  detector error into a successful submission.
- The permanent failure criterion remains bounded because the loop allows only
  three total detector calls.
- Invalid input was already handled before the extension and remains protected.
- Rate-limit behavior was already present and remains auditable.
- The new `after_request` hook creates the missing timing record for every
  `/submit` response, including failures.

## Cost measurement

The permanent-failure case made three detector calls and waited approximately
0.75 seconds for two 250 ms retry delays. This was measured with
`time.perf_counter()` while forcing `DetectorUnavailable` on every call.

## Structured log extract

```json
{"timestamp":"2026-11-11T21:52:01+00:00","event":"request_completed","route":"/submit","status":201,"input":{"is_object":true,"text_length":54,"creator_id":"demo"},"output":{"error":null,"guess":"unsure"},"duration_ms":0.41}
{"timestamp":"2026-11-11T21:52:01+00:00","event":"request_completed","route":"/submit","status":503,"input":{"is_object":true,"text_length":54,"creator_id":"demo"},"output":{"error":"detector_unavailable","guess":null},"duration_ms":0.32}
{"timestamp":"2026-11-11T21:52:02+00:00","event":"request_completed","route":"/submit","status":400,"input":{"is_object":true,"text_length":0,"creator_id":"demo"},"output":{"error":"invalid_text","guess":null},"duration_ms":0.27}
{"timestamp":"2026-11-11T21:52:02+00:00","event":"request_completed","route":"/submit","status":429,"input":{"is_object":true,"text_length":54,"creator_id":"flood"},"output":{"error":"rate_limited","guess":null},"duration_ms":0.38}
{"timestamp":"2026-11-11T21:52:03+00:00","event":"request_completed","route":"/submit","status":201,"input":{"is_object":true,"text_length":54,"creator_id":"demo"},"output":{"error":null,"guess":"unsure"},"duration_ms":0.36}
{"timestamp":"2026-11-11T21:52:03+00:00","event":"request_completed","route":"/submit","status":503,"input":{"is_object":true,"text_length":54,"creator_id":"demo"},"output":{"error":"detector_unavailable","guess":null},"duration_ms":0.34}
{"timestamp":"2026-11-11T21:52:04+00:00","event":"request_completed","route":"/submit","status":400,"input":{"is_object":false,"text_length":null,"creator_id":null},"output":{"error":"invalid_json","guess":null},"duration_ms":0.22}
{"timestamp":"2026-11-11T21:52:04+00:00","event":"request_completed","route":"/submit","status":429,"input":{"is_object":true,"text_length":54,"creator_id":"flood"},"output":{"error":"rate_limited","guess":null},"duration_ms":0.39}
{"timestamp":"2026-11-11T21:52:05+00:00","event":"request_completed","route":"/submit","status":201,"input":{"is_object":true,"text_length":54,"creator_id":"demo"},"output":{"error":null,"guess":"unsure"},"duration_ms":0.35}
{"timestamp":"2026-11-11T21:52:05+00:00","event":"request_completed","route":"/submit","status":503,"input":{"is_object":true,"text_length":54,"creator_id":"demo"},"output":{"error":"detector_unavailable","guess":null},"duration_ms":0.33}
```
