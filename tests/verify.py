"""Validate the working draft and execute competency questions from any directory."""
from pathlib import Path
from decimal import Decimal
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
E = Namespace("https://raw.githubusercontent.com/ITUAV/edso/main/ontology/edso.ttl#")
X = Namespace("https://example.org/edso/")
P = Namespace("http://www.w3.org/ns/prov#")
D = Namespace("http://purl.org/dc/terms/")
SH = Namespace("http://www.w3.org/ns/shacl#")
UNIT = URIRef("http://purl.org/linked-data/sdmx/2009/attribute#unitMeasure")

def read(path):
    return Graph().parse(ROOT / path, format="turtle")

schema = read("ontology/edso.ttl")
shapes = read("shapes/evidence.ttl")
data = read("examples/forecast.ttl") + read("examples/flexibility.ttl")

def check(graph):
    # Provide local class hierarchy. Keep domain/range inference off so it
    # cannot supply missing types and accidentally satisfy integrity checks.
    return validate(graph + schema, shacl_graph=shapes, inference="none",
                    meta_shacl=True, do_owl_imports=False)

def rows(graph, prefix):
    path, = (ROOT / "queries").glob(f"{prefix}-*.rq")
    return list(graph.query(path.read_text()))

def verify():
    valid, _, report = check(data)
    assert valid, report
    lineage = rows(data, "01")
    assert {tuple(row) for row in lineage} == {
        (X.tefScore, X.forecastV1, X.round1, X.siteA, X.loadA, X.allowA, X.policyA),
        (X.tefScore, X.forecastV1, X.round1, X.siteB, X.loadB, X.allowB, X.policyB),
    }
    match, = rows(data, "02")
    assert match.difference.toPython() == Decimal("0.4")
    account, = rows(data, "03")
    assert account.population == X.cohortAB and str(account.status) == "within stated ceiling"
    synthetic, = rows(data, "04")
    assert synthetic.source == X.historicalHoldout and synthetic.metric == X.meanGap
    assert {r.member for r in rows(data, "05")} == {X.tefScore, X.modelCard}
    discovery, = rows(data, "06")
    assert tuple(discovery) == (X.serviceA, X.loadA, X.feederProfileV1, X.policyA)
    print("Example conforms. Six competency queries returned their expected answers.")

    # Each fault must be detected at its intended focus node.
    cases = [
        (X.jobA, X.allowA, E.decisionOutcome, E.Deny),
        (X.jobA, X.allowA, D.subject, X.loadB),
        (X.jobA, X.allowA, P.generatedAtTime, Literal("2026-01-11T09:00:00Z", datatype=XSD.dateTime)),
        (X.round1, X.account1, E.accountScope, X.jobA),
        (X.account1, X.account1, E.delta, Literal(Decimal("1.0"))),
        (X.tefScore, X.tefScore, UNIT, None),
        (X.tef, X.tef, E.holdout, None),
        (X.review, X.review, E.evidenceFor, X.anotherRelease),
    ]
    for focus, subject, predicate, replacement in cases:
        altered = Graph() + data
        altered.remove((subject, predicate, None))
        if replacement is not None:
            altered.add((subject, predicate, replacement))
        if replacement == X.anotherRelease:
            altered.add((X.anotherRelease, RDF.type, E.FoundationModelRelease))
        valid, results, detail = check(altered)
        assert not valid and focus in results.objects(None, SH.focusNode), detail

    altered = Graph() + data
    altered.set((X.tef, E.scenario, X.changedScenario))
    assert not rows(altered, "02"), "Distinct scenarios must not be paired."
    altered = Graph() + data
    altered.set((X.account1, E.epsilonLimit, Literal(Decimal("1.0"))))
    assert str(rows(altered, "03")[0].status) == "above stated ceiling"
    print("Eight SHACL fault cases and two query counterexamples passed.")

if __name__ == "__main__":
    verify()
