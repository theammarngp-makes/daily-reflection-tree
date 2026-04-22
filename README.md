# Daily Reflection Tree

This project is a deterministic end-of-day reflection tool. It walks an employee through a fixed decision tree, records their answers, tallies three psychological axes, and ends with a personalized summary without making any runtime AI or LLM calls.

## Repo Structure

```text
.
├── agent
│   └── agent.py
├── transcripts
│   ├── persona-1-transcript.md
│   └── persona-2-transcript.md
├── tree
│   ├── reflection-tree.json
│   └── tree-diagram.md
├── README.md
└── write-up.md
```

## How To Run

```bash
cd agent
python agent.py
```

## How To Read The Tree File

The tree lives in `tree/reflection-tree.json` as a flat list of nodes.

- `id`: unique node identifier.
- `parentId`: previous node in the linear part of the flow, or `null` for shared entry nodes.
- `type`: one of `start`, `question`, `decision`, `reflection`, `bridge`, `summary`, or `end`.
- `text`: what the employee sees. It supports interpolation like `{A1_Q2_INT.answer}` and `{axis1.dominant}`.
- `options`: fixed answer choices for question nodes. Non-question nodes use an empty array.
- `target`: bridge destination. Other node types leave this empty.
- `signal`: tally marker such as `axis1:internal` or `axis3:other`.
- `routing`: decision-node routing rules in `answer=...:NODE_ID` form.

The Python agent loads this JSON at runtime, validates it, and executes the conversation directly from the data file.

## The Three Axes

### Axis 1: Locus of Control

This axis asks whether the day is remembered through agency or through outside force. It is not judging either path; it is surfacing where the employee located control.

### Axis 2: Orientation

This axis contrasts contribution with attention to what was missing, overdue, or not returned. The goal is to make giving and receiving visible without shaming either stance.

### Axis 3: Radius of Concern

This axis asks whether the story of the day stayed centered on the self or widened to teammates, customers, and the larger system. It treats the width of the frame as a lens, not a virtue score.

## Determinism Note

AI was used to assist in building this assignment, but the shipped product is deterministic. The runtime behavior comes entirely from the authored JSON tree plus standard Python control flow, with no model calls involved.
