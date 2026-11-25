# EDSO IEEE conference paper draft

**EDSO: Connecting Energy Data Governance to AI Evaluation Evidence**

Mohammed Al-Rawi, Instituto de Telecomunicações, Aveiro, Portugal.

[Read the PDF](EDSO_IEEE.pdf) · [Edit the LaTeX](EDSO_IEEE.tex) · [Run the experiments](../experiments/evidence-gate/)

This five-page working draft describes EDSO and investigates task-specific evidence checks for energy AI applications. It uses public material and synthetic metadata examples. The agentic applications are proposed uses, not field deployments. This is an unpublished draft, not an accepted IEEE publication.

## Build

With a standard TeX Live or MiKTeX installation, from this directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error EDSO_IEEE.tex
pdflatex -interaction=nonstopmode -halt-on-error EDSO_IEEE.tex
```

Alternatively, upload this directory to Overleaf and select `EDSO_IEEE.tex` as the main document. The supplied `evidence_path.pdf` must remain beside the source. References are embedded; BibTeX is not needed. `IEEEtran.cls` is the unmodified official CTAN class and retains its own license. The optional `figures/draw_evidence_path.py` script regenerates the illustration using Matplotlib; it is not needed to compile the manuscript.

## Reproducibility and scope

The evaluated ontology snapshot is commit `0917407b3d343775fd955ba25ae1974d9073cdd7`. The experiment reads the repository's existing ontology, shapes, examples, queries, and verification code directly; there is no duplicate `public_edso/` directory. The manuscript and its recorded results describe that fixed snapshot. Future ontology changes should be evaluated explicitly before updating the paper's claims.

The experiments demonstrate context matching and a gap between the existing shape profile and a task's required provenance. They do not establish energy savings, legal compliance, metadata authenticity, or successful autonomous control.

## Contributing

Contributions are welcome through issues and pull requests: independent metadata exports, competing-profile comparisons, application experiments, vocabulary mappings, and failing cases are especially useful. A next experiment should compare an agent using ordinary catalog descriptions against one using structured evidence checks, measuring unsupported recommendations, missed dependencies, correct abstention, and review effort. Authorship should reflect agreed substantive contributions.

Before submission, select a venue, apply its formatting and review requirements, and archive the exact evaluated revision.
