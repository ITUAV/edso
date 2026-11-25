# Evidence-gate experiments

These deterministic metadata experiments accompany the [EDSO paper draft](../../paper/). They reuse the repository's ontology, shapes, examples, queries, and `tests/verify.py` rather than copying them into another directory.

From the repository root, with Python 3.12:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r experiments/evidence-gate/requirements.txt
python experiments/evidence-gate/evaluate.py
```

On Windows, activate with `.venv\Scripts\activate`. The script resolves all inputs relative to its own location and can be invoked from another working directory. It overwrites `results.json` next to the script.

## What is checked

The original verification suite runs first: seven competency queries, 15 SHACL fault cases, two query counterexamples, and a Python-float serialization round trip. The additional experiments then evaluate:

- Seven independent changes to release, protocol, holdout, scenario, baseline, metric, and unit; each removes the matched score pair.
- Four single-edge provenance ablations; removing checkpoint provenance still passes the current profile but eliminates lineage and policy-impact answers.
- Five candidate-selection cases combining profile conformance, a matching evaluation pair, and the independently declared expected site set.

The fixed request concerns `forecastV1` and the expected sites `siteA` and `siteB`. The alternative scenario is explicitly typed so that the case tests a different valid context. Each mutation starts from a fresh graph. Assertions verify the recorded outcomes.

## Version and limits

`results.json` was produced using the ontology at commit `0917407b3d343775fd955ba25ae1974d9073cdd7`; its `snapshot` field identifies this reference baseline. The runner reads the current checkout and asserts the expected baseline behavior. It does not automatically retrieve the old commit or guarantee unchanged ontology inputs. Reproduce this paper on its published branch revision; if core inputs change, inspect the differences and revise the baseline, manuscript, and results together.

No model, LLM, controller, or external API is executed. The gate is a fixed metadata example, not a production authorization or deployment procedure. Site coverage cannot detect every missing contribution at an already represented site. The paper explains the need for stronger manifests and independent application evaluation.
