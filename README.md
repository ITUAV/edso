# Energy Data Space Ontology (EDSO)

**Public working draft · 0.1.0-draft · MIT.** EDSO describes how an energy dataset contributed to a specific model release and how that release was evaluated. An operator can follow a policy version forward to affected releases. A testing and experimentation facility (TEF) can follow a reported score back to the protocol, holdout and training inputs. Both can exchange metadata while keeping the operational records at source.

**Start with the [forecasting example](examples/forecast.ttl).** Two fictional operators run local training jobs under different agreements. Their updates produce a checkpoint used for a feeder-demand forecast model. An AI gym and a TEF evaluate that release. Their reported mean absolute errors are 4.2 kW and 4.6 kW. The comparison query returns a 0.4 kW difference because both records identify the same holdout, scenario, protocol, baseline, metric and unit. Change any of those references and the pair drops out. Matching metadata enables a comparison. Independent replication and statistical uncertainty still require experimental evidence.

## What you can use

| Artifact | Purpose |
|---|---|
| [OWL vocabulary in Turtle](ontology/edso.ttl) | Definitions for local contributions, use decisions, privacy accounts, model releases, evaluation runs and evidence bundles |
| [SHACL evidence profile](shapes/evidence.ttl) | Required fields, types, numeric bounds and cross-record integrity rules for this working draft |
| [Forecasting graph](examples/forecast.ttl) and [flexibility fragment](examples/flexibility.ttl) | End-to-end example and a separate illustration of direct SAREF reuse for EV flexibility |
| [Design and seed review](docs/design.md) | Prior art, term-level decisions, scope and reasons for the extensions |
| [Adoption and evaluation](docs/adoption.md) | Source-to-RDF mapping, independent pilot design and criteria for a research claim |

## Questions the graph answers

| Question | Query | Expected answer in the fictional example |
|---|---|---|
| Which training inputs and decisions contributed to this TEF score? | [Score lineage](queries/01-score-lineage.rq) | Two sites, two versioned data resources, two decisions and their respective policies |
| Which gym and TEF scores have matching evaluation conditions? | [Matched evaluations](queries/02-matched-evaluations.rq) | One pair. TEF minus gym MAE is +0.4 kW |
| What privacy bound was reported, for which population, adjacency and scope? | [Privacy scope](queries/03-privacy-scope.rq) | One illustrative round, household-level protection, ε = 1.2 at δ = 0.000001, stated ceiling 2.0 |
| Which synthetic holdout has a source and a measured fidelity result? | [Synthetic holdout](queries/04-synthetic-holdout.rq) | One holdout, its historical source and a 0.3 kW absolute mean gap |
| Who assembled which evidence for a deployment context? | [Review evidence](queries/05-review-evidence.rq) | One advisory-use bundle with two members, attributed to the example lab |
| Where is an input described and which profile and policy does it cite? | [Discovery](queries/06-discover-inputs.rq) | One catalogue service, feeder profile and policy version |
| If an operator reviews an earlier policy, which releases and scores reference it through training? | [Policy impact](queries/07-policy-impact.rq) | One release and both scores are candidates for review. The result makes no decision about revocation or retraining. |

## Run the checks

With Python 3.12, from the repository root:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python tests/verify.py
```

The runner loads the local schema and both example graphs, checks the shapes, executes all seven SPARQL queries, and exercises eleven deliberately changed cases. Use these queries against the asserted example data without an inference service. To review another policy, replace the example IRI in the last query's `VALUES` clause.

## Identifiers, scope and contributions

The draft prefix is `https://raw.githubusercontent.com/ITUAV/edso/main/ontology/edso.ttl#`. It resolves to the ontology on the default branch. Cite a Git commit for a fixed revision. A stable community namespace and migration map are decisions for a tagged release.

This independently maintained draft is designed for use in EnergAI-Share. Consortium adoption and field validation are open. The repository licence covers its original contributions. External vocabularies retain their own terms. To propose a term, give a question, a minimal non-sensitive graph, the expected answer, and the closest existing vocabulary term. A failing example is particularly helpful.
