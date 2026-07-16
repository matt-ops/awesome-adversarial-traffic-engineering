# Python telemetry as evidence

<!-- source-ids: python-standard-library, pytest-documentation, aate-local-lab -->

> **Progress**
>
> Module: 09 - Tooling and secure code review
>
> Lesson: 1 of 4
>
> Depth: Foundation
>
> Estimated time: 3 hours
>
> Prerequisites: Modules 00-08
>
> Artifact: `artifacts/module-09/telemetry-summary.json`
>
> Next: Async and bounded concurrency

## Role outcome

Turn line-oriented request evidence into typed, reproducible counts while keeping
observation, label, inference, and limitation separate.

## Prerequisites

- [Experimental method](../00-method/03-experimental-method.md)
- Ability to identify a request, response, session, and population label

## Source basis

| Label | Source | Assigned area | Why it is used |
|---|---|---|---|
| OFFICIAL_DOCUMENTATION | [Python tutorial: data structures](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) | dictionaries and looping techniques | Grounds record access and aggregation |
| OFFICIAL_DOCUMENTATION | [Python `json`](https://docs.python.org/3/library/json.html) and [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) | decoding and counts | Grounds the fixture pipeline |
| OFFICIAL_DOCUMENTATION | [pytest assertions](https://docs.pytest.org/en/stable/how-to/assert.html) | assertion introspection | Grounds regression evidence |
| LAB_SPECIFIC | [Python tooling lab](../../labs/applied/python-tooling.md) | telemetry command and expected shape | Supplies the tested local exercise |

## Mental model

```text
JSONL bytes -> decode one object -> validate shape -> derive transparent fields
            -> aggregate counts -> serialize artifact -> assert invariants

observation: population="headed"     label: is_abuse=true
calculation: headed_count=4            inference: why that happened
```

JSON Lines stores one JSON value per line. That makes partial failures locatable:
the loader can name the bad line instead of losing an entire array. A Python
`dict` represents each object, a `list` preserves fixture order, and `Counter`
records frequencies. Type hints document expected shapes; they do not validate
untrusted runtime data.

## Required external instruction

### Required Python assignment

**Direct link:** [Python dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries), [`json`](https://docs.python.org/3/library/json.html), and [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)

**Exact assignment:** read Dictionaries; Looping Techniques; `json.loads`; `json.dumps`; `JSONDecodeError`; `Counter` object, `elements`, and `most_common`

**Estimated time:** 65 minutes

**Focus on:** missing keys, iteration order versus evidentiary order, decode errors, deterministic serialization, and count semantics

**Skip:** encoder subclassing, command-line pretty printing, arithmetic on counters, and unrelated container types

**Expected takeaway:** explain every transformation from a JSONL line to a count and identify where validation must occur.

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

### Actions

1. For the first fixture line, identify raw keys, teaching labels, and absent fields.
2. Trace `load_jsonl()` from text line through `json.loads()` and shape validation.
3. Trace `summarize()` through both counters and the returned limitations.
4. Execute `python -m lab.tooling.client telemetry` from the repository root.
5. Execute `python -m unittest lab.tests.test_tooling -v`.
6. Add one local-only count to your artifact, such as missing population labels;
   describe whether it is an observation or inference before editing course code.

### Expected output

The command prints a JSON object with `records`, `populations`, `labels`, and
`limitations`. The test suite reports three passing tooling tests.

### Interpretation

A correct artifact lets another reviewer recompute each number and states what
the fixture cannot establish. A polished chart without a traceable denominator
is weaker evidence than a small reproducible table.

### Common failure modes

- Treating a missing key as `False` without documenting the choice
- Counting events when the claim is about unique sessions
- Mutating or discarding raw records before preserving them
- Converting a teaching label into an identity claim

### Cleanup

Keep the generated artifact; no process or service needs cleanup.

## Why this matters offensively

Control-evasion work depends on comparing populations, actions, failures, and
residual anomalies. Transparent analysis lets the operator defend an impact
claim and lets the control owner reproduce or reject it.

## Required artifact

`artifacts/module-09/telemetry-summary.json` plus a short data dictionary naming
each raw field, derived field, label, denominator, and limitation.

## Pass gate

1. Why is JSONL useful for request evidence?
2. What is the difference between an observation and a label?
3. What does a Python type hint guarantee at runtime?
4. When is event count the wrong denominator?
5. What makes a derived metric reproducible?
6. Why must limitations travel with the summary?

## Answer key

<details><summary>Check your reasoning</summary>

1. Each record is independently decodable and a malformed line can be located.
2. An observation came from evidence; a label is an assigned category that may be wrong or synthetic.
3. Nothing by itself; runtime validation or tests must check external values.
4. When the claim concerns sessions, identities, workflows, users, or another unit.
5. Preserved inputs, explicit transformation, stable denominator, versioned code, and tests.
6. Otherwise readers may generalize a small synthetic count beyond its evidence.

</details>

## Next lesson

Continue to [Async and bounded concurrency](02-async-and-bounded-concurrency.md).
