-- Minimal meta schema
CREATE TABLE IF NOT EXISTS prompts (
  id TEXT NOT NULL,
  version INT NOT NULL,
  owner TEXT NOT NULL,
  description TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (id, version)
);

CREATE TABLE IF NOT EXISTS testsets (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,         -- golden, preference, adversarial, rag_faithfulness
  uri  TEXT NOT NULL,         -- s3://... or file://...
  schema JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS runs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  prompt_id TEXT NOT NULL,
  prompt_version INT NOT NULL,
  testset_id TEXT NOT NULL,
  provider TEXT NOT NULL,
  model TEXT NOT NULL,
  params JSONB,
  started_at TIMESTAMPTZ DEFAULT now(),
  finished_at TIMESTAMPTZ,
  status TEXT DEFAULT 'running'
);

CREATE TABLE IF NOT EXISTS results (
  run_id UUID REFERENCES runs(id),
  example_id TEXT,
  output TEXT,
  score_json JSONB,
  tokens_in INT,
  tokens_out INT,
  latency_ms INT,
  cost_usd NUMERIC(12,6),
  PRIMARY KEY (run_id, example_id)
);
