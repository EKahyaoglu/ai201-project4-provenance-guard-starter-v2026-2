# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 21:11
- Marked BROKE: **21**
- Marked HELD: **35**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 201 | `376feb41-410f-46a3-b8db-5abe98c6d4a6` | human | 0.306  | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 201 | `1663d054-b8c2-4ade-b8bd-240f478e7081` | unsure | 0.424  | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 201 | `f9146aee-94f7-47fd-885e-3d0c804069e2` | unsure | 0.497  | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 201 | `a28d44d5-73ea-4ac7-9530-65256f4243b6` | unsure | 0.525  | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 201 | `72aed82b-999e-4fcc-991c-a67671da0143` | human | 0.306  | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 201 | `ec5b00e6-85c6-4f1e-b5b0-d1facfe2592f` | unsure | 0.415  | HELD |
| EV07 | evasion | signal two: padding with punctuation | 201 | `44fc54a1-aed1-4449-be27-97412f658cf5` | unsure | 0.585  | HELD |
| EV08 | evasion | signal one: text below the token window | 201 | `3ab87e49-42c2-4430-9983-cfbb5b7a0053` | human | 0.319  | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 201 | `7e350a6c-7e48-434a-b11d-67ad114bfe75` | unsure | 0.513  | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 201 | `953f8ded-d158-4f28-a2b7-48efb114d66d` | ai | 0.840  | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 201 | `192c37ae-5bf2-4f73-a853-13210ff3c629` | unsure | 0.506  | HELD |
| FP02 | false_positive | human writing in a formal register | 201 | `dfd1e79d-cca0-43be-8e80-d2f0e49ff528` | unsure | 0.607  | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 201 | `2472b13d-fb03-4139-8262-c8a3dbdad49f` | unsure | 0.618  | HELD |
| FP04 | false_positive | a student essay written to a rubric | 201 | `5e20d902-3e75-4697-839d-63b314d2a353` | unsure | 0.596  | HELD |
| FP05 | false_positive | technical documentation written by a person | 201 | `6a398a24-9f98-4edc-8a34-5f5d4432a405` | ai | 0.673  | BROKE |
| FP06 | false_positive | a person imitating a formal template | 201 | `a4d83057-39b8-491e-8758-d904f89a250d` | unsure | 0.622  | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 201 | `6171213a-8baf-4dc4-aa16-725d55b11865` | ai | 0.700  | BROKE |
| FP08 | false_positive | very short genuine human submission | 201 | `f0c14c57-fa1b-41cd-84ee-242e9126f00d` | human | 0.331  | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 201 | `5cc311f4-84ac-4165-b7ec-b72ff0f8e3c5` | unsure | 0.375  | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 201 | `ee72792e-1437-4a4a-8fbe-35eba2982a74` | human | 0.243  | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 201 | `29f31714-20fe-4eab-b61d-0d4b56a375d8` | unsure | 0.480  | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 201 | `120bc138-70fd-4dc9-b0dd-23503905ef33` | unsure | 0.421  | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 201 | `5d991d69-2c7b-494a-84d6-419d9bbce9a9` | unsure | 0.467  | HELD |
| PI06 | prompt_injection | instruction plus real human text | 201 | `a0b3abb6-5708-4079-a16d-e711a8c5c40b` | unsure | 0.479  | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | —  | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | —  | HELD |
| MF03 | malformed | text is control characters | 201 | `17af74c6-0da9-4314-b507-d94e4ad5f8da` | human | 0.300  | BROKE |
| MF04 | malformed | text is only punctuation | 201 | `7e2b354d-de63-49ce-b031-f28c2aabb14f` | unsure | 0.456  | BROKE |
| MF05 | malformed | text is a very long single word | 201 | `87927ef7-4e78-40b5-bbfa-c64189312db7` | ai | 0.799  | BROKE |
| MF06 | malformed | text is emoji only | 201 | `3ef24301-a323-4326-9ce7-01bdd6793e13` | ai | 0.999  | BROKE |
| MF07 | malformed | text is right-to-left script | 201 | `8e36c48e-597d-4450-91f9-e34c62dde2c5` | ai | 0.953  | BROKE |
| MF08 | malformed | text is 60,000 characters | 201 | `80cf386c-3995-476d-ae52-4587f07962fc` | ai | 0.862  | BROKE |
| RQ01 | malformed | no text field at all | 400 | `—` | — | —  | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | —  | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | —  | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | —  | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | —  | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | —  | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | —  | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | —  | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | —  | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | —  | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | —  | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | —  | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 201 | `0309be5f-7759-4907-809a-707a3768368c` | human | 0.314  | BROKE |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 201 | `e86e405d-f226-45f9-a916-604ff26e3085` | human | 0.314  | BROKE |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 201 | `b5bc89c5-4c3a-4b03-b389-85323f6875f4` | human | 0.314  | BROKE |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 201 | `0da0fa55-b705-41fb-af7f-d974981f66fb` | human | 0.314  | BROKE |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 201 | `1160e854-9009-40c1-9038-ff1dd3b11e98` | human | 0.314  | BROKE |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 201 | `95dd6d67-a084-4fbd-9b99-adfe93fc9573` | human | 0.314  | BROKE |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 201 | `b0dbd530-d621-43cd-93ae-c3db9ab873ca` | human | 0.314  | BROKE |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 201 | `2ae47ba5-c071-4265-a2c3-e160ff43bc8b` | human | 0.314  | BROKE |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 201 | `078858f4-0f2e-42a6-b847-2a8ea151513a` | human | 0.314  | BROKE |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 201 | `7a40ea21-5220-4949-af46-3e7a20bc036f` | human | 0.314  | BROKE |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | —  | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | —  | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 201,
  "content_id": "376feb41-410f-46a3-b8db-5abe98c6d4a6",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3063,
  "model_score": 0.1635,
  "style_score": 0.4491,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 201,
  "content_id": "1663d054-b8c2-4ade-b8bd-240f478e7081",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4237,
  "model_score": 0.5943,
  "style_score": 0.253,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 201,
  "content_id": "f9146aee-94f7-47fd-885e-3d0c804069e2",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4969,
  "model_score": 0.6662,
  "style_score": 0.3275,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 201,
  "content_id": "a28d44d5-73ea-4ac7-9530-65256f4243b6",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5252,
  "model_score": 0.6114,
  "style_score": 0.4389,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 201,
  "content_id": "72aed82b-999e-4fcc-991c-a67671da0143",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3056,
  "model_score": 0.3212,
  "style_score": 0.29,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 201,
  "content_id": "ec5b00e6-85c6-4f1e-b5b0-d1facfe2592f",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4146,
  "model_score": 0.5727,
  "style_score": 0.2566,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 201,
  "content_id": "44fc54a1-aed1-4449-be27-97412f658cf5",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5845,
  "model_score": 0.5862,
  "style_score": 0.5828,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 201,
  "content_id": "3ab87e49-42c2-4430-9983-cfbb5b7a0053",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3191,
  "model_score": 0.2452,
  "style_score": 0.3929,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 201,
  "content_id": "7e350a6c-7e48-434a-b11d-67ad114bfe75",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5127,
  "model_score": 0.7042,
  "style_score": 0.3212,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 201,
  "content_id": "953f8ded-d158-4f28-a2b7-48efb114d66d",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8399,
  "model_score": 0.9792,
  "style_score": 0.7006,
  "label": "High-confidence AI: this text is probably AI-generated.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 201,
  "content_id": "192c37ae-5bf2-4f73-a853-13210ff3c629",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5061,
  "model_score": 0.6175,
  "style_score": 0.3948,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 201,
  "content_id": "dfd1e79d-cca0-43be-8e80-d2f0e49ff528",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6068,
  "model_score": 0.7387,
  "style_score": 0.4748,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 201,
  "content_id": "2472b13d-fb03-4139-8262-c8a3dbdad49f",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6179,
  "model_score": 0.8051,
  "style_score": 0.4307,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 201,
  "content_id": "5e20d902-3e75-4697-839d-63b314d2a353",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5955,
  "model_score": 0.8329,
  "style_score": 0.358,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 201,
  "content_id": "6a398a24-9f98-4edc-8a34-5f5d4432a405",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6727,
  "model_score": 0.8005,
  "style_score": 0.545,
  "label": "High-confidence AI: this text is probably AI-generated.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 201,
  "content_id": "a4d83057-39b8-491e-8758-d904f89a250d",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6216,
  "model_score": 0.8814,
  "style_score": 0.3618,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 201,
  "content_id": "6171213a-8baf-4dc4-aa16-725d55b11865",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7,
  "model_score": 0.8816,
  "style_score": 0.5184,
  "label": "High-confidence AI: this text is probably AI-generated.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 201,
  "content_id": "f0c14c57-fa1b-41cd-84ee-242e9126f00d",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3312,
  "model_score": 0.3223,
  "style_score": 0.3401,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 201,
  "content_id": "5cc311f4-84ac-4165-b7ec-b72ff0f8e3c5",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3754,
  "model_score": 0.4625,
  "style_score": 0.2882,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 201,
  "content_id": "ee72792e-1437-4a4a-8fbe-35eba2982a74",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2434,
  "model_score": 0.2044,
  "style_score": 0.2824,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 201,
  "content_id": "29f31714-20fe-4eab-b61d-0d4b56a375d8",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4801,
  "model_score": 0.5943,
  "style_score": 0.3658,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 201,
  "content_id": "120bc138-70fd-4dc9-b0dd-23503905ef33",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4209,
  "model_score": 0.4998,
  "style_score": 0.3419,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 201,
  "content_id": "5d991d69-2c7b-494a-84d6-419d9bbce9a9",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4672,
  "model_score": 0.6401,
  "style_score": 0.2943,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 201,
  "content_id": "a0b3abb6-5708-4079-a16d-e711a8c5c40b",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4788,
  "model_score": 0.5583,
  "style_score": 0.3993,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 201,
  "content_id": "17af74c6-0da9-4314-b507-d94e4ad5f8da",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.3,
  "model_score": 0.0,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 201,
  "content_id": "7e2b354d-de63-49ce-b031-f28c2aabb14f",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4556,
  "model_score": 0.0112,
  "style_score": 0.9,
  "label": "Unsure: the available signals are not strong enough to determine authorship.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 201,
  "content_id": "87927ef7-4e78-40b5-bbfa-c64189312db7",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.7988,
  "model_score": 0.9976,
  "style_score": 0.6,
  "label": "High-confidence AI: this text is probably AI-generated.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 201,
  "content_id": "3ef24301-a323-4326-9ce7-01bdd6793e13",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9985,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "High-confidence AI: this text is probably AI-generated.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 201,
  "content_id": "8e36c48e-597d-4450-91f9-e34c62dde2c5",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "High-confidence AI: this text is probably AI-generated.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 201,
  "content_id": "80cf386c-3995-476d-ae52-4587f07962fc",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8621,
  "model_score": 0.9876,
  "style_score": 0.7367,
  "label": "High-confidence AI: this text is probably AI-generated.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 201,
  "content_id": "0309be5f-7759-4907-809a-707a3768368c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 201,
  "content_id": "e86e405d-f226-45f9-a916-604ff26e3085",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 201,
  "content_id": "b5bc89c5-4c3a-4b03-b389-85323f6875f4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 201,
  "content_id": "0da0fa55-b705-41fb-af7f-d974981f66fb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 201,
  "content_id": "1160e854-9009-40c1-9038-ff1dd3b11e98",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 201,
  "content_id": "95dd6d67-a084-4fbd-9b99-adfe93fc9573",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 201,
  "content_id": "b0dbd530-d621-43cd-93ae-c3db9ab873ca",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 201,
  "content_id": "2ae47ba5-c071-4265-a2c3-e160ff43bc8b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 201,
  "content_id": "078858f4-0f2e-42a6-b847-2a8ea151513a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 201,
  "content_id": "7a40ea21-5220-4949-af46-3e7a20bc036f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
  "label": "High-confidence human: this text is probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
