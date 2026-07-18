# Minimum JavaScript for automation

<!-- source-ids: tau-javascript-introduction, aate-local-lab, aate-adversarial-control-loop -->

## Progress

- Module: 02 - Browser and JavaScript foundations
- Lesson: 3 of 4
- Depth: Foundation
- Estimated time: 3 hours
- Prerequisites:
  - [DOM and Web APIs](02-dom-and-web-apis.md)
  - No prior JavaScript is assumed
- Required artifact: `artifacts/module-02/javascript-exercise.js`
- Next lesson: Async, fetch, and errors

## Role outcome

Read and write the variables, values, arrays, functions, objects, conditions,
and loops used by the Foundation browser client.

## Source basis

| Type | Source | Exact assigned area | What it supports | Limitation |
|---|---|---|---|---|
| PRACTITIONER_PERSPECTIVE | [Test Automation University: Introduction to JavaScript](https://testautomationu.applitools.com/javascript-tutorial/) | 1.1, 1.2, 2.1, 2.2, 3.1, 3.2, 4.1, 5.1, 6.1 | Provides one ordered beginner path through the exact language subset | Third-party instructional course; MDN is used for platform and async behavior. |
| LAB_SPECIFIC | [Foundation static site](../../labs/foundation/static-site.md) | `lab/foundation-web/app.js` after assigned instruction | Shows the subset in the actual target | Deliberately small and vulnerable; results do not generalize to production systems. |
| COURSE_SYNTHESIS | [AATE control loop](../../methodology/adversarial-control-loop.md) | Evidence and controlled-variable steps | Frames telemetry transformation as preserved evidence | Course synthesis; no cited standard defines the exact fifteen-step sequence. |

## Mental model

| Construct | Purpose | Foundation example |
|---|---|---|
| `const` / `let` | bind a name to a value | element reference / changing status |
| Array | ordered collection | inventory records |
| Object | named fields | `{ name, stock }` |
| Function | reusable operation | search handler or predicate |
| Condition | choose a path | match or error branch |
| Loop / array method | process members | filter and render results |

## Required external instruction

### JavaScript assignment

**Direct link:** [Introduction to JavaScript](https://testautomationu.applitools.com/javascript-tutorial/)  
**Exact section, chapter, or unit:** 1.1 Variables; 1.2 Data Types; 2.1 Arrays Introduction; 2.2 Using Arrays; 3.1 Functions; 3.2 Anonymous and Arrow Functions; 4.1 Objects; 5.1 Conditionals; 6.1 Loops  
**Estimated time:** 2 hours  
**What to focus on:** predicting values and control flow before executing each example  
**What to skip:** chapters not listed; browser automation appears in the next module  
**Expected takeaway:** explain and modify a small transformation from an array of request records to a filtered evidence summary.

## Course bridge

JavaScript values have types; variables bind names to values; objects group
named properties; arrays order values; functions encapsulate behavior; and
conditions/loops select and repeat work. These concepts are enough to read the
Foundation app and Playwright workflow before asynchronous operations are added.

!!! note "Course synthesis"
    **COURSE_SYNTHESIS:** Automation code should transform evidence explicitly.
    Preserve the original events, compute a derived summary, and avoid changing
    both the workflow and analysis in the same experiment.

## Worked example

```javascript
const events = [
  { method: "GET", status: 200, path: "/" },
  { method: "GET", status: 200, path: "/inventory.json" },
  { method: "POST", status: 403, path: "/reserve" },
];

const failures = events.filter((event) => event.status >= 400);
for (const event of failures) {
  console.log(`${event.method} ${event.path} -> ${event.status}`);
}
```

`events` is an array of objects. The arrow function receives one object and
returns a Boolean. `filter` creates a new array without changing the original.
The `for...of` loop visits each failure; the template literal formats fields.
Expected console output is `POST /reserve -> 403`.

## Guided exercise

### Objective

Turn a small event population into a method/status summary without network work.

### Setup

Create `artifacts/module-02/javascript-exercise.js`. Use a browser console or
Node after the file is written. The input is synthetic.

### Exact actions or commands

1. Copy the worked-example array.
2. Write `summarize(events)` that returns an object keyed by `METHOD-status`.
3. Use a loop and a condition; do not discard the original array.
4. Add two events, including one `429`, and print the returned object.
5. Add a condition that prints `blocked baseline present` when any status is
   `403` or `429`.
6. Comment each binding with its value type and role.

### Expected output

For the original three events plus one `GET 429` and one `POST 200`, a valid
summary resembles:

```text
{ 'GET-200': 2, 'POST-403': 1, 'GET-429': 1, 'POST-200': 1 }
blocked baseline present
```

### Interpretation

The summary counts response classes; it does not explain why a block occurred
or whether another attempt completed the action. Those require context and
protected-action evidence.

### Common failure modes

- Using `const` as if the bound object were deeply immutable
- Comparing the string `"429"` to a number without noticing coercion
- Mutating the evidence array while summarizing it
- Counting a displayed UI message instead of a network/server event

### Cleanup

Keep the script as the required artifact. It creates no service or persistent
state.

## Why this matters offensively

Playwright programs and telemetry processors are JavaScript/TypeScript programs,
not magic recorder output. Reading control flow is necessary to know which
requests were caused, which assertion passed, and whether evidence was silently
filtered or mutated.

## Required artifact

`artifacts/module-02/javascript-exercise.js` containing the input, commented
`summarize` function, expected output, and two assertions you would add in a
test framework.

## Pass gate

1. Why can an object bound with `const` still have a property changed?
2. What does `Array.filter` return?
3. What value must the filter callback produce conceptually?
4. How is an object useful for the summary?
5. Why preserve the raw event array?

## Answer key

<details>
<summary>Check your reasoning</summary>

1. `const` prevents rebinding the variable; it does not recursively freeze the referenced object.
2. A new array containing members whose callback result is truthy.
3. A truthy/falsy decision for whether the current member belongs in the output.
4. Named keys map each method/status category to its count.
5. Derived logic can be checked or recomputed without losing original evidence.

</details>

## Next lesson

[Async, fetch, and errors](04-async-fetch-and-errors.md) explains why browser
network work completes later and how code waits for and handles it.
