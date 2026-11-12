# Provenance Guard

## Build Summary

- **System extended:** Provenance Guard, a local Flask service that scores
  writing with a GPT-2 signal and a stylometry signal.
- **New failure handling:** detector failures receive bounded retries. A
  temporary failure can recover, while a permanent failure returns `503` after
  three total attempts and is logged as rejected.
- **New observability:** every `/submit` request writes a structured
  `request_completed` audit record with timestamp, input summary, output
  summary, HTTP status, and duration in milliseconds.
- **Shape:** B, hardening an existing system against detector outages, malformed
  input, and rate limits.
- **Out of scope:** this remains a single-process local service. It does not
  provide distributed retry coordination, persistent rate-limit storage, or
  authorship certainty.

## What This Does

1. `POST /submit` checks that the JSON body contains non-empty string values
   for `text` and `creator_id`, and rejects invalid input before scoring.
2. `detector.model_signal` measures how predictable the text is to the local
   GPT-2 model.
3. `stylometry.style_signal` measures the text's sentence-length spread,
   vocabulary variety, and punctuation density.
4. `scoring.combine_signals` combines the two 0 to 1 signals.
5. `scoring.score_to_label` maps the combined score to a reader-facing label.
6. `audit.log_decision` writes the decision and both signal scores to
   `logs/audit.jsonl`.
7. The route returns the content ID, both signal scores, confidence, guess, and
   label.

An appeal sent to `POST /appeal` verifies the content ID, records the
reasoning, and appends an `under_review` entry without changing the original
decision.

## Rate Limiting

`POST /submit` allows 10 requests per creator per minute and 200 per creator
per day. This leaves room for a writer to submit their own work while limiting
scripts that send many variations to map the thresholds.

Run the flood check with:

```text
python run_attacks.py --flood 15
```

The limiter returns `429` after the per-minute limit is reached. Rate-limited
requests and invalid submissions are recorded in the audit log as rejected
events.

If the local detector cannot load or score a submission, `/submit` returns
`503` with `error: "detector_unavailable"` instead of a server error. The
failed submission is also recorded as a rejected audit event, so a client can
retry after a short delay. Before giving up, the service makes two bounded
retries with a 250 ms delay. Successful responses include `detector_attempts`,
and permanent failures include the same count in the response and audit log.
Set `AI201_DETECTOR_RETRIES` or `AI201_DETECTOR_RETRY_DELAY` to adjust this
policy.

## Attack Run - Before

I ran all 56 rows from the supplied attack set on 2026-11-04. The detailed
report is in `results/attack_run_2026-11-04_2106.md`.

| Family | Attacks | Held | Broke |
|---|---:|---:|---:|
| evasion | 10 | 7 | 3 |
| false_positive | 8 | 6 | 2 |
| prompt_injection | 6 | 6 | 0 |
| malformed | 20 | 13 | 7 |
| flood_same_creator | 12 | 2 | 10 |
| **Total** | **56** | **34** | **22** |

I marked an evasion as broke when the detector called the AI text human, and
a false positive as broke when genuine human text was called AI. Malformed
requests were held when safely rejected and broke when accepted as junk or
caused a server error. The flood rows that returned `201` were marked broke;
the two rows that returned `429` were held.

The worst writer-facing outcome was `FP07`. It was genuine human writing with
a deliberately repeated phrase, but the service returned `ai` with a combined
score of `0.7000`. `FP05` was another false positive, with technical
documentation returned as `ai` at `0.6727`.

Selected audit entries from the run, including rejected requests:

```json
{"combined_score":0.3063,"content_id":"86779e1e-46a8-4038-a652-52238d752e81","creator_id":"attacker_EV01","guess":"human","label":"High-confidence human: this text is probably written by a person.","model_score":0.1635,"status":"decided","style_score":0.4491,"timestamp":"2026-11-05T02:06:05+00:00"}
{"combined_score":0.3056,"content_id":"ab04ce3a-a0bd-4746-9d52-93e37c2ffad5","creator_id":"attacker_EV05","guess":"human","label":"High-confidence human: this text is probably written by a person.","model_score":0.3212,"status":"decided","style_score":0.29,"timestamp":"2026-11-05T02:06:06+00:00"}
{"combined_score":0.3191,"content_id":"86dce6bf-2dfc-4755-b340-55d5f82bde2f","creator_id":"attacker_EV08","guess":"human","label":"High-confidence human: this text is probably written by a person.","model_score":0.2452,"status":"decided","style_score":0.3929,"timestamp":"2026-11-05T02:06:06+00:00"}
{"combined_score":0.6727,"content_id":"f13ea1b4-1ea9-47c0-adbf-383002f353df","creator_id":"attacker_FP05","guess":"ai","label":"High-confidence AI: this text is probably AI-generated.","model_score":0.8005,"status":"decided","style_score":0.545,"timestamp":"2026-11-05T02:06:07+00:00"}
{"combined_score":0.7,"content_id":"86c24de5-7c8a-4b61-9f9d-b82afc4b5d1e","creator_id":"attacker_FP07","guess":"ai","label":"High-confidence AI: this text is probably AI-generated.","model_score":0.8816,"status":"decided","style_score":0.5184,"timestamp":"2026-11-05T02:06:08+00:00"}
{"combined_score":0.9985,"content_id":"371248b1-5261-4b82-a718-c603500f644f","creator_id":"attacker_MF06","guess":"ai","label":"High-confidence AI: this text is probably AI-generated.","model_score":0.9969,"status":"decided","style_score":1.0,"timestamp":"2026-11-05T02:06:10+00:00"}
{"combined_score":0.9532,"content_id":"ec39e299-c6fd-4e0e-af54-a401b53dcd44","creator_id":"attacker_MF07","guess":"ai","label":"High-confidence AI: this text is probably AI-generated.","model_score":0.9064,"status":"decided","style_score":1.0,"timestamp":"2026-11-05T02:06:10+00:00"}
{"combined_score":0.8621,"content_id":"55045301-44cc-49e3-a9cf-98eccf8e6b1e","creator_id":"attacker_MF08","guess":"ai","label":"High-confidence AI: this text is probably AI-generated.","model_score":0.9876,"status":"decided","style_score":0.7367,"timestamp":"2026-11-05T02:06:10+00:00"}
{"creator_id":"attacker_RQ12","event":"rejected","reason":"invalid_text","status":"rejected","timestamp":"2026-11-05T02:06:10+00:00"}
{"creator_id":"attacker_flood","event":"rejected","limit":"10 per 1 minute","reason":"rate_limited","status":"rejected","timestamp":"2026-11-05T02:06:11+00:00"}
```

## Run Log and Verdicts

I replaced the placeholders in `scenarios.py` and ran
`python run_eval.py --label before`. The evaluator produced
`results/run_2026-11-04_2110_before.md`. Each trial was unchanged, and all
three trials were identical.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing called AI | At most 1 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. All three labels reachable | 3 of 3 | 2/3 | 2/3 | 2/3 | MISSED |
| 3. Malformed input returns 400, not 500 | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |
| 4. Every valid decision has complete fields | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Identical input gives repeatable scores | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

The table and JSON below were produced by `run_eval.py::write_report`; the
scenario inputs are defined in `scenarios.py::SCENARIOS`.

### Criterion 1 output

```json
[
  {"status":201,"guess":"unsure","confidence":0.4407,"model_score":0.5221,"style_score":0.3594},
  {"status":201,"guess":"unsure","confidence":0.3694,"model_score":0.4807,"style_score":0.258},
  {"status":201,"guess":"human","confidence":0.2631,"model_score":0.2492,"style_score":0.2771},
  {"status":201,"guess":"human","confidence":0.2616,"model_score":0.2138,"style_score":0.3095},
  {"status":201,"guess":"human","confidence":0.2589,"model_score":0.1883,"style_score":0.3295},
  {"status":201,"guess":"human","confidence":0.2516,"model_score":0.1958,"style_score":0.3075},
  {"status":201,"guess":"unsure","confidence":0.4173,"model_score":0.3267,"style_score":0.508},
  {"status":201,"guess":"unsure","confidence":0.3779,"model_score":0.4952,"style_score":0.2606},
  {"status":201,"guess":"human","confidence":0.2463,"model_score":0.138,"style_score":0.3546},
  {"status":201,"guess":"unsure","confidence":0.3601,"model_score":0.3674,"style_score":0.3528}
]
```

### Criterion 2 output

```json
[
  {"status":201,"guess":"unsure","confidence":0.5221,"model_score":0.7384,"style_score":0.3058},
  {"status":201,"guess":"unsure","confidence":0.4528,"model_score":0.3821,"style_score":0.5235},
  {"status":201,"guess":"human","confidence":0.2512,"model_score":0.2271,"style_score":0.2754}
]
```

### Criterion 3 output

```json
[
  {"status":400,"guess":null,"confidence":null,"model_score":null,"style_score":null,"label":null,"sent":"(empty text)"},
  {"status":400,"guess":null,"confidence":null,"model_score":null,"style_score":null,"label":null,"sent":"{\"creator_id\": \"eval_bad_missing\"}"},
  {"status":400,"guess":null,"confidence":null,"model_score":null,"style_score":null,"label":null,"sent":"{\"text\": null, \"creator_id\": \"eval_bad_null\"}"},
  {"status":null,"error":"JSONDecodeError: Expecting value: line 1 column 1 (char 0)","sent":"x"},
  {"status":400,"guess":null,"confidence":null,"model_score":null,"style_score":null,"label":null,"sent":"{\"text\": [\"not\", \"text\"], \"creator_id\": \"eval_bad_list\"}"}
]
```

### Criterion 4 output

```json
[
  {"status":201,"guess":"human","confidence":0.1914,"model_score":0.0679,"style_score":0.3148,"label":"High-confidence human: this text is probably written by a person."},
  {"status":201,"guess":"human","confidence":0.2511,"model_score":0.1647,"style_score":0.3375,"label":"High-confidence human: this text is probably written by a person."},
  {"status":201,"guess":"unsure","confidence":0.3598,"model_score":0.1708,"style_score":0.5488,"label":"Unsure: the available signals are not strong enough to determine authorship."},
  {"status":201,"guess":"human","confidence":0.3379,"model_score":0.3904,"style_score":0.2855,"label":"High-confidence human: this text is probably written by a person."},
  {"status":201,"guess":"human","confidence":0.2742,"model_score":0.2856,"style_score":0.2627,"label":"High-confidence human: this text is probably written by a person."}
]
```

### Criterion 5 output

```json
[
  {"status":201,"guess":"human","confidence":0.2314,"model_score":0.0698,"style_score":0.3929},
  {"status":201,"guess":"unsure","confidence":0.5051,"model_score":0.5419,"style_score":0.4683},
  {"status":201,"guess":"human","confidence":0.2771,"model_score":0.2042,"style_score":0.35},
  {"status":201,"guess":"human","confidence":0.3194,"model_score":0.323,"style_score":0.3157},
  {"status":201,"guess":"unsure","confidence":0.4602,"model_score":0.3345,"style_score":0.586}
]
```

### Diagnoses

Criterion 2 missed at the label mapping stage. The first two inputs scored
`0.5221` and `0.4528`, so they correctly mapped to `unsure`; the third scored
`0.2512`, so it mapped to `human`. None reached the `0.65` AI threshold. The
combining rule averaged the signals down, so the criterion's input selection
did not cover the upper score range.

Criterion 3 missed at the route and signal-one boundary. The route checks only
that text is a non-empty string, so the single character `"x"` passed input
validation. Signal one then raised `ValueError: Text is too short to score`,
and Flask returned an HTML error page instead of JSON. The other four malformed
bodies were safely rejected with `400`.

The broken attack outcomes have the following stage and mechanism:

- `EV01`: signal two, where typos increase measured word variety and lower the
  apparent AI score.
- `EV05`: signal two and the combining rule, where heavy editing makes both
  signals look more human and the average crosses the human threshold.
- `EV08`: signal one, where text below the model token window is not a reliable
  authorship measurement and was classified human.
- `FP05` and `FP07`: signal one, where predictable formal or repeated human
  writing produced high model scores and the average crossed the AI threshold.
- `MF02`: route validation, which accepted one character, followed by signal
  one, which raised an unhandled short-text error.
- `MF03`: route validation accepted control characters, then signal one
  produced a zero score, so junk was treated as human.
- `MF04`: route validation accepted punctuation-only text, and the two signals
  produced an unsure decision instead of rejecting junk.
- `MF05`, `MF06`, `MF07`, and `MF08`: route validation accepted malformed,
  emoji, right-to-left, and oversized-but-allowed content; signal one and
  signal two then produced ordinary classification scores for inputs that
  should have been rejected as unusable.
- `FL01_01` through `FL01_10`: the rate-limit stage intentionally allows the
  first ten requests in the minute, so those flood requests reached scoring.
  `FL01_11` and `FL01_12` were held with `429`.

## The Improvement

I made one change: `/submit` now rejects text with fewer than 20 non-whitespace
characters before either signal runs. The change is in `app.py::submit`, and
the rejection is logged as `text_too_short`. I chose input validation because
`MF02` passed the old non-empty check and then signal one raised
`ValueError: Text is too short to score`.

### Attack Run - After

I reran all 56 attacks with `python run_attacks.py --set attack_set --label
after`. The full report is
`results/attack_run_2026-11-04_2111_after.md`.

| Family | Before broke | After broke | Change |
|---|---:|---:|---:|
| evasion | 3 | 3 | 0 |
| false_positive | 2 | 2 | 0 |
| prompt_injection | 0 | 0 | 0 |
| malformed | 7 | 6 | -1 |
| flood_same_creator | 10 | 10 | 0 |
| **Total** | **22** | **21** | **-1** |

The improvement helped: `MF02` changed from `500` and BROKE to `400` and
HELD. Every other attack produced the same classification as before.

### Criteria Run - After

I reran `python run_eval.py --label after`; the output is in
`results/run_2026-11-04_2111_after.md`. All three trials again matched.

| Criterion | Before | After | Verdict after |
|---|---:|---:|---|
| 1. My own writing called AI | 0/10 | 0/10 | MET |
| 2. All three labels reachable | 2/3 | 2/3 | MISSED |
| 3. Malformed input returns 400, not 500 | 4/5 | 5/5 | MET |
| 4. Every valid decision has complete fields | 5/5 | 5/5 | MET |
| 5. Identical input gives repeatable scores | 5/5 | 5/5 | MET |

The change fixed the malformed-input criterion. It did not improve label
coverage because that miss is caused by the label threshold and scenario
inputs, not by short text reaching the detector.

## What's Still Broken

The remaining broken attacks are `EV01`, `EV05`, `EV08`, `FP05`, `FP07`,
`MF03`, `MF04`, `MF05`, `MF06`, `MF07`, `MF08`, and `FL01_01` through
`FL01_10`.

- `EV01`, `EV05`, and `EV08` still exploit signal one or signal two with typos,
  editing, or a short token-window input. I would add adversarial validation
  and calibrate both signals on edited AI text, but I stopped because that
  would be a second change and would need a new measured baseline.
- `FP05` and `FP07` still accuse genuine technical or repetitive writing. I
  would widen the unsure band or lower the AI threshold after measuring the
  false-positive tradeoff. I stopped to avoid changing the scoring policy
  without a separate before-and-after experiment.
- `MF03` through `MF08` still allow control characters, punctuation, unusual
  scripts, or very large inputs to reach scoring. I would add content-quality
  validation for printable text, token limits, and script-aware handling. I
  stopped after fixing the diagnosed crash so the effect of one change stayed
  measurable.
- `FL01_01` through `FL01_10` are expected to pass because the configured
  policy allows ten requests per creator per minute. I would lower the burst
  limit or add a short-term window if abuse mattered more than writer
  convenience. I stopped because changing the limit would be a separate
  rate-limit experiment.

The remaining missed criterion is label coverage. I would add a calibrated
high-score fixture or revise the target only if the criterion were measuring
the intended reachable range. I stopped because the current run honestly shows
that the supplied three inputs reached only human and unsure.

In production I would prefer fewer wrong accusations over catching every
possible AI submission, because a false accusation harms a real writer's
review and trust. The cost is that some AI text would remain in the unsure or
human bands, so I would pair the detector with human review rather than treat
the label as proof.

## Failure-Handling Run Log

The dedicated evidence file is
`results/failure_handling_run.md`.

The extension was tested separately from the earlier classifier run. Each row
has three trials. The baseline uses the same service with
`DETECTOR_RETRIES=0`; the after run uses the default two retries.

| Criterion | Before fix, trials 1-3 | After fix, trials 1-3 | Verdict after | Diagnosis |
|---|---|---|---|---|
| 1. Temporary recovery | 503 after 1 attempt, 3/3 | 201 after 2 attempts, 3/3 | MET | Retry loop recovers a transient detector outage. |
| 2. Permanent failure | 503 after 1 attempt, 3/3 | 503 after 3 attempts, 3/3 | MET | Retry loop is bounded and rejection is logged. |
| 3. Invalid input | 400, detector calls 0, 3/3 | 400, detector calls 0, 3/3 | MET | Validation already ran before the extension. |
| 4. Rate-limit visibility | 429 and rejection log, 3/3 | 429 and rejection log, 3/3 | MET | Existing limiter and rejection handler meet the target. |
| 5. Structured timing | No request record, 3/3 | Complete record, 3/3 | MET | `after_request` now records input, output, status, and duration. |

The baseline and after values were measured with Flask's test client and
detector stubs, so the model download was not part of this comparison. The
three trials for each criterion used fresh temporary audit logs.

### Structured log extract

Each line below is one measured `/submit` completion record. The input is
summarized rather than storing the submitted writing in this timing event.

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

### Cost measurement

One failure-handling run costs **three detector attempts and about 0.75 seconds
of retry delay** in the permanent-failure case. I measured this by setting
`AI201_DETECTOR_RETRIES=2`, `AI201_DETECTOR_RETRY_DELAY=0.25`, forcing the
detector to raise `DetectorUnavailable`, and timing the three calls with
`time.perf_counter()`. A successful first attempt costs no retry delay; a
successful second attempt costs one delay.

## What's Left

The retry extension does not make the detector accurate or distributed. A
production version would add persistent rate-limit storage, request
correlation IDs, and a queue for slow model work. I stopped after the bounded
retry and structured timing changes because they address the selected failure
path without changing the classifier's scoring policy.

## Signals and Scoring

### Model signal

`detector.model_signal` measures language-model predictability through
perplexity. Lower perplexity produces a higher AI-likelihood score because
generated text often uses likely, conventional continuations.

It cannot establish authorship. Plain human writing, second-language writing,
and edited AI writing can also be predictable. Topic, length, and the choice of
GPT-2 model also affect the score.

### Style signal

`stylometry.style_signal` measures sentence-length variation, type-token ratio,
and punctuation density. Generated prose can have even sentence lengths,
repeated vocabulary, and restrained punctuation.

It cannot understand meaning or context. Reformatting, adding typos, inserting
quotations, or changing punctuation can change the score without changing the
ideas or authorship.

### Combining rule

The service uses an equal weighted average:

`0.5 * model_score + 0.5 * style_score`

The result is clamped to 0.0 through 1.0 and rounded to four decimal places.
When the signals disagree, the average moves toward the unsure range. For
example, 0.90 and 0.10 produce 0.50.

The rule lives in `scoring.py::combine_signals`.

## Label Variants

| Exact label text | Score range |
|---|---:|
| `High-confidence human: this text is probably written by a person.` | 0.00 through 0.35 |
| `Unsure: the available signals are not strong enough to determine authorship.` | Above 0.35 through below 0.65 |
| `High-confidence AI: this text is probably AI-generated.` | 0.65 through 1.00 |

The unsure label states the limitation of the signals without accusing the
writer. The short machine-readable guesses are `human`, `unsure`, and `ai`.

## Sample Run

### Submission request

```text
POST /submit
Content-Type: application/json

{"text":"I wrote this short example to test the review path. The wording is plain and the sentences are intentionally different in length.","creator_id":"sample-writer"}
```

### Submission response

```json
{
  "content_id": "d3c2d386-57e4-43b6-8124-3a8c87fd25cd",
  "guess": "unsure",
  "confidence": 0.445,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "model_score": 0.5781,
  "style_score": 0.3119
}
```

### Appeal request

```text
POST /appeal
Content-Type: application/json

{"content_id":"d3c2d386-57e4-43b6-8124-3a8c87fd25cd","reasoning":"I wrote this passage myself and would like a human review."}
```

### Appeal response

```json
{
  "content_id": "d3c2d386-57e4-43b6-8124-3a8c87fd25cd",
  "status": "under_review",
  "message": "Appeal recorded; this content is under review."
}
```

### Log entries

These are the corresponding lines in `logs/audit.jsonl`:

```json
{"timestamp":"2026-10-29T01:31:50+00:00","content_id":"d3c2d386-57e4-43b6-8124-3a8c87fd25cd","creator_id":"sample-writer","guess":"unsure","model_score":0.5781,"style_score":0.3119,"combined_score":0.445,"label":"Unsure: the available signals are not strong enough to determine authorship.","status":"decided"}
{"timestamp":"2026-10-29T01:39:48+00:00","content_id":"d3c2d386-57e4-43b6-8124-3a8c87fd25cd","creator_id":"sample-writer","event":"appeal","status":"under_review","reasoning":"I wrote this passage myself and would like a human review."}
```

## How I Used AI

### Moment 1

- What I asked: Review the scoring and label code against the required response
  fields and score ranges.
- What I got: A check that the combined score, guess, label, and signal scores
  were returned consistently.
- What I changed: Kept the equal weighting, documented the clamping and
  rounding rule, and documented the exact label text and ranges.

### Moment 2

- What I asked: Check the sample submission and appeal evidence for consistency
  with the Flask routes and audit functions.
- What I got: A finding that the sample needed both signal scores and a
  separate appeal entry with `under_review` status.
- What I changed: Replaced placeholders with a complete request, response, and
  two matching JSONL log entries.

### Moment 3

- What I asked: Help compare the attack and evaluation runs and identify one
  measurable improvement without changing multiple stages at once.
- What I got: A recommendation to validate minimum text length before calling
  the detector because the single-character attack reached signal one and
  caused a server error.
- What I changed: Added the 20-character input check, reran both suites, and
  documented that it fixed the malformed-input miss while leaving the other
  classifications unchanged.

See [RUNNING.md](RUNNING.md) for setup and execution instructions.
