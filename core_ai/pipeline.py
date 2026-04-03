import os
from core_ai.dao import DAO
from core_ai.parser import parse_to_dao
from core_ai.anomaly import check_anomalies
from core_ai.compliance import map_compliance
from core_ai.groq_reasoning import generate_reasoning
from core_ai.ai_analyser import analyze
from typing import Any, Dict


def process(raw_log: Dict[str, Any]) -> DAO:
    dao = parse_to_dao(raw_log)
    dao = check_anomalies(dao)
    dao = map_compliance(dao)

    xai_key = os.environ.get("XAI_API_KEY", "")
    groq_key = os.environ.get("GROQ_API_KEY", "")

    if xai_key:
        # Full Grok deep analysis
        try:
            dao = analyze(dao, xai_key)
        except Exception as e:
            print(f"[ai_analyser] Grok failed, falling back to Groq: {e}")
            if groq_key and (not dao.reasoning or not dao.reasoning.strip()):
                dao.ai_reasoning = generate_reasoning(dao)
    elif groq_key and (not dao.reasoning or not dao.reasoning.strip()):
        # Fallback: Groq quick reasoning
        dao.ai_reasoning = generate_reasoning(dao)

    return dao
