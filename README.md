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
