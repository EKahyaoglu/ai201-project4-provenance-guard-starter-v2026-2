# Provenance Guard

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

## Attack Set Run

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

See [RUNNING.md](RUNNING.md) for setup and execution instructions.
