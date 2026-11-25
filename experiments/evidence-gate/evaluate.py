"""Deterministic metadata experiments. No energy controller or LLM is executed."""
from pathlib import Path
import importlib.util
import json
from rdflib import Graph, Literal, Namespace, RDF
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("edso_verify", ROOT.parents[1]/"tests/verify.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
E, X, P = v.E, v.X, v.P
def clone():
    return Graph() + v.data
def query(g, number):
    return v.rows(g, number)
def candidate(g):
    # Metadata gate for the one declared forecast request and target release.
    valid, _, _ = v.check(g)
    pairs = query(g, "02")
    lineage = query(g, "01")
    sites = {r.site for r in lineage if r.release == X.forecastV1}
    return valid and any(r.release == X.forecastV1 for r in pairs) and sites == {X.siteA, X.siteB}

def run():
    v.verify()
    results = {"snapshot": "0917407b3d343775fd955ba25ae1974d9073cdd7"}
    results["counts"] = {
        "ontology_triples":len(v.schema), "fixture_triples":len(v.data),
        "classes":len(set(v.schema.subjects(RDF.type, Namespace("http://www.w3.org/2002/07/owl#").Class)) & {s for s in v.schema.subjects() if str(s).startswith(str(E))}),
    }
    # One change per graph. All values deliberately differ from the baseline.
    mutations = [
        ("release", X.tef, E.evaluatedRelease, X.otherRelease),
        ("protocol", X.tef, E.protocol, X.otherProtocol),
        ("holdout", X.tef, E.holdout, X.otherHoldout),
        ("scenario", X.tef, E.scenario, X.otherScenario),
        ("baseline", X.tef, E.baseline, X.otherBaseline),
        ("metric", X.tefScore, v.D.type, X.otherMetric),
        ("unit", X.tefScore, v.UNIT, Namespace("http://qudt.org/vocab/unit/").MegaW),
    ]
    comparisons=[]
    for name, subject, predicate, replacement in mutations:
        g=clone()
        g.set((subject,predicate,replacement))
        count=len(query(g,"02"))
        assert count==0, name
        comparisons.append({"changed":name,"matched_pairs":count})
    results["comparison"]={"baseline_pairs":len(query(v.data,"02")),"mutations":comparisons}
    ablations=[]
    for name, edge in [
        ("decision link",(X.jobA,E.decisionRecord,X.allowA)),
        ("update provenance",(X.updateA,P.wasGeneratedBy,X.jobA)),
        ("checkpoint provenance",(X.checkpoint1,P.wasGeneratedBy,X.round1)),
        ("release derivation",(X.forecastV1,P.wasDerivedFrom,X.checkpoint1)),
    ]:
        g=clone()
        g.remove(edge)
        valid,_,_=v.check(g)
        record={"removed":name,"shacl_conforms":bool(valid),"lineage_rows":len(query(g,"01")),
                "policy_impact_rows":len(query(g,"07")),"candidate":candidate(g)}
        assert record["candidate"] is False
        expected = {
            "decision link": (False, 1, 0),
            "update provenance": (False, 1, 0),
            "checkpoint provenance": (True, 0, 0),
            "release derivation": (False, 0, 0),
        }[name]
        assert (bool(valid), record["lineage_rows"], record["policy_impact_rows"]) == expected, name
        ablations.append(record)
    results["ablations"]=ablations
    cases=[("complete",None,None,None,True),
           ("different scenario",X.tef,E.scenario,X.scenario2,False),
           ("denied contribution",X.allowA,E.decisionOutcome,E.Deny,False),
           ("missing score unit",X.tefScore,v.UNIT,None,False),
           ("missing checkpoint provenance",X.checkpoint1,P.wasGeneratedBy,None,False)]
    gate=[]
    for name,s,p,o,expected in cases:
        g=clone()
        if s:
            g.remove((s,p,None))
            if o is not None:g.add((s,p,o))
        if name == "different scenario":
            g.add((X.scenario2, RDF.type, P.Entity))
        result=candidate(g)
        assert result==expected,name
        valid, _, _ = v.check(g)
        assert bool(valid) == (name in {"complete", "different scenario", "missing checkpoint provenance"}), name
        gate.append({"case":name,"shacl_conforms":bool(valid),"candidate":result})
    results["candidate_gate"]=gate
    (ROOT/"results.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))
if __name__=="__main__":
    run()
