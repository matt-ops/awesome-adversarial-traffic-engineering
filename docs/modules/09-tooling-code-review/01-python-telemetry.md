# Python telemetry as evidence

<!-- source-ids: python-standard-library, pytest-documentation, aate-local-lab -->

## Progress

- Module: 09 - Tooling and secure code review
- Lesson: 1 of 4
- Depth: Foundation
- Estimated time: 3 hours
- Prerequisites:
  - [Experimental method](../00-method/03-experimental-method.md)
  - Ability to identify a request, response, session, and population label
- Next lesson: Async and bounded concurrency

## Role outcome

Turn line-oriented request evidence into typed, reproducible counts while keeping
observation, label, inference, and limitation separate.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Python documentation](https://docs.python.org/3/) | Tutorial: Dictionaries and Looping Techniques; `json.loads`; `collections.Counter` objects and `most_common` | Grounds record access, JSON decoding, and deterministic aggregation | Lessons link to the exact subsection used; not all Python documentation is assigned. |
| OFFICIAL_DOCUMENTATION | [pytest assertions](https://docs.pytest.org/en/stable/how-to/assert.html) | How to write and report assertions | Grounds regression evidence for the fixture summary | Only the features used by the code-review exercises are assigned. |
| LAB_SPECIFIC | [Python tooling lab](../../labs/applied/python-tooling.md) | telemetry command and expected shape | Supplies the tested local exercise | Deliberately small and vulnerable; results do not generalize to production systems. |

## Mental model

```text
JSONL bytes -> decode one object -> validate shape -> derive transparent fields
            -> aggregate counts -> serialize output -> assert invariants

observation: population="headed"     label: is_abuse=true
calculation: headed_count=4            inference: why that happened
```

JSON Lines stores one JSON value per line. That makes partial failures locatable:
the loader can name the bad line instead of losing an entire array. A Python
`dict` represents each object, a `list` preserves fixture order, and `Counter`
records frequencies. Type hints document expected shapes; they do not validate
untrusted runtime data.

## Required external instruction

### Dictionary assignment

**Direct link:** [Python dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)  
**Exact section, chapter, or unit:** Dictionaries and Looping Techniques  
**Estimated time:** 20 minutes  
**What to focus on:** missing keys, membership checks, item iteration, and iteration order versus evidentiary order  
**What to skip:** unrelated container types and advanced comprehensions  
**Expected takeaway:** explain how one decoded record is accessed and where a missing or mistyped field must be rejected.

### JSON assignment

**Direct link:** [Python `json`](https://docs.python.org/3/library/json.html)  
**Exact section, chapter, or unit:** `json.loads`, `json.dumps`, and `JSONDecodeError`  
**Estimated time:** 25 minutes  
**What to focus on:** decode errors, Python-to-JSON type conversion, and deterministic serialization options  
**What to skip:** encoder subclassing and command-line pretty printing  
**Expected takeaway:** trace a JSONL line through decoding, validation, and serialized output.

### Counter assignment

**Direct link:** [Python `Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)  
**Exact section, chapter, or unit:** Counter objects, `elements`, and `most_common`  
**Estimated time:** 20 minutes  
**What to focus on:** missing-count behavior, update semantics, and deterministic presentation of counts  
**What to skip:** counter arithmetic and unrelated collection types  
**Expected takeaway:** explain how validated labels become counts without confusing a count with identity or causation.

## Course bridge

The course fixture contains synthetic observations and an `is_abuse` teaching
label. Neither a population string nor a model decision proves a person, tool,
or intent. Preserve raw evidence, derive new fields explicitly, and attach
limitations to every summary.

!!! note "Lab-specific behavior"
    The bundled command counts a fixed local fixture. Its output is deterministic
    because it performs no remote lookup, clock-based bucketing, or random sampling.

## Worked example

Given three records—two `headed`, one `manual`; one abuse label—the summary is:

```json
{
  "records": 3,
  "populations": {"headed": 2, "manual": 1},
  "labels": {"abuse": 1, "benign": 2}
}
```

That supports “two fixture rows have the `headed` population label.” It does not
support “two real browsers were operated by the same adversary.” Identity and
causation require evidence the fixture does not contain.

## Guided exercise

### Objective

Trace, run, test, and extend one transparent telemetry transformation.

### Setup

Open `lab/tooling/client.py`, `lab/analysis/analyze.py`, and
`lab/fixtures/requests.jsonl`. No service or Docker container is required.

### Exact actions or commands

1. For the first fixture line, identify raw keys, teaching labels, and absent fields.
2. Trace `load_jsonl()` from text line through `json.loads()` and shape validation.
3. Trace `summarize()` through both counters and the returned limitations.
4. From the repository root, execute `python -m lab.tooling.client telemetry`.
5. From that same repository root, execute
   `python -m unittest lab.tests.test_tooling -v`.
6. Add one local-only count to the output, such as missing population labels;
   describe whether it is an observation or inference before editing course code.

### Expected output

The command prints a JSON object with `records`, `populations`, `labels`, and
`limitations`. The test suite reports three passing tooling tests.

### Interpretation

A correct result lets another reviewer recompute each number and states what
the fixture cannot establish. A polished chart without a traceable denominator
is weaker evidence than a small reproducible table.

### Common failure modes

- Treating a missing key as `False` without documenting the choice
- Counting events when the claim is about unique sessions
- Mutating or discarding raw records before preserving them
- Converting a teaching label into an identity claim

### Cleanup

No process or service needs cleanup. Keep or delete the generated output.

## Why this matters offensively

Control-evasion work depends on comparing populations, actions, failures, and
residual anomalies. Transparent analysis lets the operator defend an impact
claim and lets the control owner reproduce or reject it.

## Check your understanding

1. The exercise stores one JSON object per line in JSONL. How does that format help a reviewer locate and handle a malformed request record?
2. A telemetry row contains an observed HTTP status and a synthetic label named `blocked`. What is the difference between the observation and the label?
3. A Python function annotates an input as `RequestEvent`. What does that type hint guarantee when untrusted JSON reaches the program at runtime?
4. A summary claims a percentage of blocked sessions but divides by event count. Why is the denominator wrong for that claim?
5. Which preserved inputs, transformation details, denominator, code version, and tests make the derived summary reproducible?

## Answer key

<details>
<summary>Show answers</summary>

- **1. Each line is independently decodable, so a parser can identify the exact bad record and continue or fail with a precise location.** One malformed line does not make record boundaries ambiguous.

- **2. The HTTP status came directly from captured evidence, while `blocked` is an assigned interpretation that may be synthetic or mistaken.** The data model should preserve which fields were observed and which were inferred.

- **3. The type hint provides static guidance but performs no runtime validation by itself.** Code must still parse and validate external fields before treating the object as a trustworthy RequestEvent.

- **4. The claim concerns sessions, so the calculation must group or count sessions rather than individual events.** Multiple events from one session would otherwise give that session extra weight.

- **5. Preserve the input records, define the exact transformation and stable denominator, record the code version, and test known cases.** Limitations should travel with the summary so reviewers do not generalize beyond the sample.

</details>

## Next lesson

Continue to [Async and bounded concurrency](02-async-and-bounded-concurrency.md).
