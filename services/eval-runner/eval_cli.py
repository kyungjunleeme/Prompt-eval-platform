import argparse, yaml, pandas as pd, json, time
from providers import PROVIDERS
from scorers import exact_score, rubric_score

def run_eval(cfg):
    testset_path = cfg["testset"]
    df = pd.read_parquet(testset_path) if testset_path.endswith(".parquet") else pd.read_csv(testset_path)
    results = []
    for _, row in df.iterrows():
        prompt_tpl = cfg["prompt"]["template"]
        prompt = prompt_tpl.replace("{{question}}", str(row["input"]))
        for m in cfg["models"]:
            p = PROVIDERS[m.split(":")[0]]
            r = p.generate(m, prompt, {"temperature":0})
            score = exact_score(r.output, row.get("expected",""))
            rub = rubric_score(r.output, row.get("expected",""))
            results.append({
                "id": row["id"], "model": m, "output": r.output,
                "score_exact": score, **rub,
                "latency_ms": r.latency_ms, "tokens_in": r.tokens_in,
                "tokens_out": r.tokens_out, "cost_usd": r.cost_usd
            })
    out = pd.DataFrame(results)
    out_path = cfg.get("output", "eval_results.parquet")
    out.to_parquet(out_path, index=False)
    print(f"Wrote {len(out)} rows to {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)
    run_eval(cfg)
