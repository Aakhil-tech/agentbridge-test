-- Run this in Supabase SQL Editor
ALTER TABLE logs
  ADD COLUMN IF NOT EXISTS risk_level TEXT DEFAULT 'low',
  ADD COLUMN IF NOT EXISTS compliance_tags JSONB DEFAULT '[]',
  ADD COLUMN IF NOT EXISTS compliance_violations JSONB DEFAULT '[]',
  ADD COLUMN IF NOT EXISTS reasoning TEXT,
  ADD COLUMN IF NOT EXISTS ai_reasoning TEXT,
  ADD COLUMN IF NOT EXISTS session_id TEXT,
  ADD COLUMN IF NOT EXISTS decision_id TEXT,
  ADD COLUMN IF NOT EXISTS ai_action_summary TEXT,
  ADD COLUMN IF NOT EXISTS ai_compliance_status TEXT,
  ADD COLUMN IF NOT EXISTS ai_risk_level TEXT,
  ADD COLUMN IF NOT EXISTS ai_category TEXT,
  ADD COLUMN IF NOT EXISTS ai_issue_detected BOOLEAN,
  ADD COLUMN IF NOT EXISTS ai_explanation TEXT,
  ADD COLUMN IF NOT EXISTS ai_recommended_action TEXT,
  ADD COLUMN IF NOT EXISTS ai_confidence_score FLOAT,
  ADD COLUMN IF NOT EXISTS ai_regulatory_refs JSONB DEFAULT '[]',
  ADD COLUMN IF NOT EXISTS ai_escalate_to_human BOOLEAN DEFAULT FALSE;
