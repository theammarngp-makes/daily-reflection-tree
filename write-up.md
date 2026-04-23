# Write-up: Design Rationale — Daily Reflection Tree

## 1. Objective

The goal of this project was to design a deterministic reflection system that guides an employee through structured thinking at the end of the day.

Unlike LLM-based systems, this tool:
- Does not generate responses dynamically  
- Does not rely on interpretation or ambiguity  
- Produces consistent outputs for identical inputs

The intelligence is embedded in the tree structure itself, not in runtime computation.

---

## 2. Design Philosophy

The system is built around one core idea:

> Reflection improves when ambiguity is removed but meaning is preserved.

To achieve this, I focused on:
- Fixed, human-realistic options (not robotic choices)
- Branching that reflects psychological direction, not judgment
- A tone that feels like a thoughtful colleague, not a system

---

## 3. The Three Axes

The tree is structured across three psychological dimensions:

### Axis 1: Locus (Control — Internal vs External)

Inspired by:
- Julian Rotter (Locus of Control)
- Carol Dweck (Growth Mindset)

Design intent:
- Surface whether the user sees themselves as actor or reactor
- Avoid blame — instead highlight small moments of choice

Branching logic:
- Internal answers → reinforce agency
- External answers → gently surface awareness of attention patterns

---

### Axis 2: Orientation (Contribution vs Entitlement)

Inspired by:
- Psychological Entitlement theory
- Organizational Citizenship Behavior

Design intent:
- Shift thinking from “What did I get?” → “What did I give?”
- Make entitlement visible without shaming

Branching logic:
- Contribution → highlight quiet value
- Entitlement → normalize gaps but expand perspective

---

### Axis 3: Radius (Self vs Others)

Inspired by:
- Maslow (Self-Transcendence)
- Perspective-taking research

Design intent:
- Expand awareness from self → team → system
- Show that meaning increases with broader context

Branching logic:
- Self-focused → frame as protection, not flaw
- Other-focused → connect effort to impact

---

## 4. Tree Structure Decisions

### Determinism

Every node follows:
- Fixed options
- Explicit routing rules
- No randomness

This ensures:
- Repeatability
- Auditability
- Predictability

---

### Signals & State

Each axis uses signals:
- axis1:internal / external
- axis2:contribution / entitlement
- axis3:self / other

These signals:
- Accumulate during traversal
- Determine dominant orientation
- Drive the final summary

---

### Reflection Design

Reflections are:
- Short
- Non-judgmental
- Observational

They do NOT:
- Give advice
- Moralize
- Over-explain

Instead, they:
> Hold up a mirror to the user’s own answers.

---

## 5. Trade-offs

### 1. Depth vs Simplicity
- Deeper trees → more insight but more friction
- I chose moderate depth (25+ nodes) for balance

### 2. Precision vs Natural Language
- Too precise → robotic
- Too natural → ambiguous

I balanced this by:
- Using natural phrasing
- Keeping options clearly distinct

### 3. Coverage vs Cognitive Load
- More questions = better signal
- But too many = fatigue

Solution:
- 2 questions per axis
- 1 reflection per branch

---

## 6. What I Would Improve

Given more time, I would:

1. Add deeper branching inside each axis  
2. Create more dynamic summary templates  
3. Introduce weighted signals instead of simple counts  
4. Add multiple tone variations (strict, reflective, coaching)  
5. Build a better frontend UI for smoother interaction  

---

## 7. Conclusion

This system demonstrates:

- Ability to convert psychology → structure
- Ability to design deterministic decision systems
- Understanding of user cognition and behavior

The final product is not just a tree —  
it is a guided thinking system encoded as data.

---
