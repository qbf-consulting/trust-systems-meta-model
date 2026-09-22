---
owner: maintainers
last_reviewed: 2026-09-22
applicable_version: 0.24.0
tier: 1
title: Composite Authority Lifecycle Pressure Test
permalink: /model/composite-authority-lifecycle-pressure-test.html
parent: Model
grand_parent: Documentation
---

# Composite Authority Lifecycle Pressure Test

## Purpose

This informative pressure test asks whether existing TSMM lifecycle semantics can
handle authority whose exercise depends on current group membership and a
composition rule such as 2-of-3, without introducing cryptosystem-specific core
states.

## Disposition

The pressure test does **not** require a new top-level lifecycle state.

A membership change or an exercise-rule/threshold change is instead treated as a
material change to the authority/evidence conditions under which a previous
current-authority conclusion was produced. Prior composition evidence therefore
cannot silently authorize a new act after such a change.

For current authorization:

- material membership change -> `reassessment_required`;
- material exercise-rule change -> `reassessment_required`;
- unknown impact -> `indeterminate`;
- explicitly non-material metadata/documentation change may preserve `current`
  when the governing evaluator records that judgment.

For historical verification, an act that was valid under the authority state
applicable at time T remains historically verifiable; later membership or rule
changes alter current consequences rather than rewriting history.

## Authority boundary

TSMM owns this semantic distinction between current authority evidence and
historical validity. It does not define threshold cryptography or portable wire
fields. TIS determines the portable serialization and TGA may exercise the
resulting composition as implementation evidence.

## Executable evidence

`validation/pressure_tests/composite-authority-lifecycle.json` and
`scripts/test_composite_authority_lifecycle.py` provide positive, negative and
unknown-impact cases. They are pressure-test evidence against the v0.24.0
candidate semantics, not a new normative release surface.
