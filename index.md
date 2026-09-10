---
layout: default
title: Trust Systems Meta-Model
nav_order: 1
permalink: /
---

# Trust Systems Meta-Model (TSMM)

A portable semantic reference model for designing, comparing, implementing, and assuring trust systems.

**Current release:** v0.24.0 — Candidate Specification  
**Author and maintainer:** Sankarshan Mukhopadhyay, QBF Consulting LLP — `sankarshan@qbfconsulting.digital`  
**Project stewardship:** QBF Consulting LLP  
**Canonical repository:** https://github.com/qbf-consulting/trust-systems-meta-model

[View the v0.24.0 release notes](releases/v0.24.0.md) · [Citation metadata](CITATION.cff) · [Stewardship](docs/stewardship.md)

## Start here

If you are new to TSMM, start with the [documentation home](docs/), then use the [Getting Started](docs/getting-started/) path to model a system, bind it to external technologies, validate the artifacts, and compare trust architectures.

## What TSMM models

TSMM provides explicit semantics for trust-system entities, relationships, authority, delegation, evidence, assurance, lifecycle, governance, and decision effects. It is intended to make trust architecture reviewable rather than implicit.

The model is deliberately protocol-neutral. Bindings and crosswalks connect TSMM semantics to external specifications without transferring semantic authority from those specifications into TSMM or vice versa.

## TSMM and the Trust Systems Modelling Stack

TSMM is the semantic foundation of the **Trust Systems Modelling Stack (TSMS)**:

- **TSMM** owns canonical semantics and semantic projections.
- **TIS** owns portable machine-readable contracts and validation for its artifacts.
- **TGA** owns executable governance compositions and implementation patterns in its own repository.

The current candidate baseline is **TSMM v0.24.0 / TIS v0.15.0 / TGA v0.12.1**. Common or related stewardship does not collapse these repository authority boundaries.

## Status and conformance

TSMM is a **Candidate Specification**, not a certification programme. Conformance profiles, validation evidence, and compatibility declarations establish repository-defined technical claims; they do not by themselves establish legal recognition, production assurance, or independent certification.

See [repository status](docs/repository-status.md), [candidate readiness](docs/candidate-readiness.md), and [conformance](docs/conformance/) for the current evidence posture.

## Historical continuity

The repository moved from Sankarshan Mukhopadhyay's personal GitHub namespace to QBF Consulting LLP stewardship. Historical release artifacts, receipts, commit SHAs, and identifiers that record the earlier namespace remain historical evidence and are not silently rewritten. Current project publication and citation surfaces use the QBF namespace.
