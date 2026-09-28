---
owner: maintainers
last_reviewed: 2026-09-28
applicable_version: 0.26.0
tier: 0
title: Documentation
permalink: /documentation/
nav_order: 2
has_children: true
---


# Trust Systems Meta Model Documentation

TSMM is a portable reference model for designing, comparing, implementing, and assuring trust systems. The documentation is organized around implementer tasks rather than release history. TSMM also serves as the semantic foundation and coordination point for the Trust Systems Modelling Stack (TSMS), without acquiring authority over TIS portable contracts or TGA implementation artifacts.

## Start with the stack

- [Trust Systems Modelling Stack (TSMS)](tsms.md) — architecture, authority boundaries, candidate compatibility baseline, and consumption paths.

## Start by task

| Task | Primary docs | Machine-readable artifacts |
| --- | --- | --- |
| Understand the model | [Core model](core-model.md), [Entity model](model/tsmm-entities.md), [Relationship model](model/tsmm-relationships.md) | `schemas/tsmm.schema.json` |
| Model a system | [Model, Bind, Validate, Compare](getting-started/model-bind-validate-compare.md), [TSMM Graph Model](model/tsmm-graph-model.md) | `model/graph/tsmm.graph.json` |
| Trace decision resolution | [Decision Resolution Semantics](decision-resolution-semantics.md) | `model/decision-resolution-semantics.json`, `schemas/decision-resolution-semantics.schema.json` |
| Govern runtime effects | [Runtime Governance Envelope](model/runtime-governance-envelope.md), [Decision Receipt](model/decision-receipt.md) | `schemas/tsmm-runtime-governance.schema.json`, `schemas/tsmm-decision-receipt.schema.json` |
| Govern agent discovery | [Discovery Governance](model/discovery-governance.md), [Agent Discovery Pattern](patterns/agent-discovery-pattern.md) | `schemas/tsmm-discovery-governance.schema.json` |
| Negotiate capabilities | [Capability Negotiation](model/capability-negotiation.md), [Capability Negotiation Pattern](patterns/capability-negotiation-pattern.md) | `schemas/tsmm-capability-negotiation.schema.json` |
| Track task evidence | [Task Evidence Lifecycle](model/task-evidence-lifecycle.md), [Task Evidence Pattern](patterns/task-evidence-pattern.md) | `schemas/tsmm-task-evidence-lifecycle.schema.json` |
| Bind ecosystems | [Bindings overview](bindings/index.md), [Binding contract](bindings/binding-contract.md) | `bindings/*/*.json` |
| Validate conformance | [Validation and testability](conformance/validation-and-testability.md) | `validation/test_vectors/` |

## Agent interaction release surfaces

- [Discovery Governance Model](model/discovery-governance.md)
- [Capability Negotiation Model](model/capability-negotiation.md)
- [Task Evidence Lifecycle Model](model/task-evidence-lifecycle.md)
- [Governed A2A-Class Discovery Walkthrough](examples/a2a-governed-discovery-walkthrough.md)
- [A2A Binding](bindings/a2a-binding.md)
- [A2A Crosswalk](crosswalks/a2a-crosswalk.md)
- [GTR GRID/DIA Binding](bindings/gtr-binding.md)
- [GTR GRID/DIA Crosswalk](crosswalks/gtr-grid-dia-crosswalk.md)

## Conformance profiles

- [TSMM Minimal Profile](conformance/tsmm-profile-minimal.md)
- [TSMM Operational Profile](conformance/tsmm-profile-operational.md)
- [TSMM Assured Profile](conformance/tsmm-profile-assured.md)
- [TSMM Agentic Conformance Profile](conformance/tsmm-profile-agentic.md)
- [Runtime Governance Test Profile](conformance/runtime-governance-test-profile.md)

## Reference patterns

- [Trust Registry Pattern](patterns/trust-registry-pattern.md)
- [Delegated Agent Pattern](patterns/delegated-agent-pattern.md)
- [Credential Verification Pattern](patterns/credential-verification-pattern.md)
- [Assurance Evidence Pattern](patterns/assurance-evidence-pattern.md)
- [Multi-Agent Coordination Pattern](patterns/multi-agent-coordination-pattern.md)
- [Agent Discovery Pattern](patterns/agent-discovery-pattern.md)
- [Capability Negotiation Pattern](patterns/capability-negotiation-pattern.md)
- [Task Evidence Pattern](patterns/task-evidence-pattern.md)

## Operational docs

- [Freshness audit](freshness-audit.md)
- [Documentation governance](documentation-governance.md)
- [GitHub Pages deployment](pages-deployment.md)
- [Roadmap](roadmap.md)
- [Glossary](glossary.md)
- [Release v0.23.0](../releases/v0.23.0.md)

## Cross-repo executable artifact alignment

- [Trust Infrastructure Schemas alignment](cross-repo/trust-infrastructure-schemas-alignment.md)
- [TIS crosswalk](crosswalks/trust-infrastructure-schemas-crosswalk.md)
- [TIS binding](bindings/tis-binding.md)
- [TIS executable artifact walkthrough](examples/tis-executable-artifact-walkthrough.md)

## Publication coverage

- [Complete documentation site map](site-map.md)
- [GitHub Pages deployment contract](pages-deployment.md)
