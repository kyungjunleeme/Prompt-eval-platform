import argparse, os, pandas as pd, pathlib

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", required=False, help="Postgres DSN (optional for demo)")
    ap.add_argument("--s3", required=False, help="s3://bucket/prefix (optional for demo)")
    args = ap.parse_args()

    out = pathlib.Path("configs/eval/sample_testset.csv")
    if out.exists():
        print(f"Seed present: {out}")
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("id,input,expected,category,lang,reference_docs\n"
                       "ex001,\"반품 기간 알려줘\",\"30일\",policy,ko,\n", encoding="utf-8")
        print("Wrote sample testset.")
