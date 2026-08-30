#!/usr/bin/env python3
"""web-crawl-attestation-oracle -- a deterministic attestation-integrity decider for the `web-crawl` knowledge domain.

An **oracle** *deterministically decides* the truth of a case. This one decides, for a `web-crawl` knowledge
capsule, whether it is a well-formed, provenance-carrying attestation. VALID iff: domain=='web-crawl', a non-empty
`kind`, a non-empty `content`, a `provenance`, and a valid `content_hash` (hex). Empirical structure+provenance
integrity (fast-default ceremony) -- not a deep formal proof.
"""
import json, os, re, sys
_HEX = re.compile(r"^[0-9a-f]{8,}$")
def decide(c):
    if c.get("domain") != "web-crawl": return "INVALID"
    if not c.get("kind"): return "INVALID"
    if not c.get("content"): return "INVALID"
    if not c.get("provenance"): return "INVALID"
    if not _HEX.match(str(c.get("content_hash") or "")): return "INVALID"
    return "VALID"
def _run_probes(path):
    probes=[json.loads(l) for l in open(path,encoding="utf-8") if l.strip()]
    if not (any(p.get("expected_verdict")=="VALID" for p in probes) and any(p.get("expected_verdict")=="INVALID" for p in probes)):
        print("DEGENERATE corpus -- FAIL"); return 1
    tp=fp=fn=0
    for p in probes:
        v=decide(p); e=p.get("expected_verdict")
        if e=="VALID" and v=="VALID": tp+=1
        elif e=="VALID" and v=="INVALID": fn+=1
        elif e=="INVALID" and v=="VALID": fp+=1
    recall=tp/(tp+fn) if (tp+fn) else 0.0
    ok=(recall==1.0 and fp==0)
    print("web-crawl attestation oracle: probes=%d | recall=%.3f | false_positives=%d | verdict=%s"%(len(probes),recall,fp,"PASS" if ok else "FAIL"))
    return 0 if ok else 1
if __name__=="__main__":
    base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(_run_probes(sys.argv[1] if len(sys.argv)>1 else os.path.join(base,"probes","probes.jsonl")))
