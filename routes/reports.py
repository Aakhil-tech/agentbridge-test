from fastapi import APIRouter, HTTPException
from database import supabase
from core_ai.dao import DAO
from core_ai.report_generator import generate_report
import json
import ast

router = APIRouter()

def _parse_inputs(data):
    if not data:
        return {}
    if isinstance(data, dict):
        return data
    try:
        # Handle stringified python dicts stored in DB
        return ast.literal_eval(data)
    except:
        try:
            return json.loads(data)
        except:
            return {"raw_input": str(data)}

@router.get("/report")
async def get_report(api_key: str, session_id: str = None):
    if not api_key:
        raise HTTPException(status_code=400, detail="api_key required")

    query = supabase.table("logs").select("*").eq("api_key", api_key)
    if session_id:
        query = query.eq("session_id", session_id)
    
    res = query.order("created_at", desc=True).execute()
    logs = res.data

    if not logs:
        return {"message": "No data yet for this api_key"}

    daos = []
    for l in logs:
        dao = DAO(
            decision_id=l.get("decision_id") or "",
            session_id=l.get("session_id") or "",
            timestamp=str(l.get("created_at", "")),
            agent_name=l.get("agent_name") or "",
            action_type=l.get("action") or "unknown",
            risk_level=l.get("risk_level") or "low",
            flag_reason=l.get("flag_reason"),
            reasoning=l.get("reasoning"),
            compliance_tags=l.get("compliance_tags") or [],
            compliance_violations=l.get("compliance_violations") or [],
            input=_parse_inputs(l.get("inputs")),
            output=_parse_inputs(l.get("output")),
        )

        # Load AI fields
        dao.ai_action_summary = l.get("ai_action_summary")
        dao.ai_compliance_status = l.get("ai_compliance_status")
        dao.ai_risk_level = l.get("ai_risk_level")
        dao.ai_category = l.get("ai_category")
        dao.ai_issue_detected = l.get("ai_issue_detected")
        dao.ai_explanation = l.get("ai_explanation")
        dao.ai_recommended_action = l.get("ai_recommended_action")
        dao.ai_confidence_score = l.get("ai_confidence_score")
        dao.ai_regulatory_refs = l.get("ai_regulatory_refs") or []
        dao.ai_escalate_to_human = l.get("ai_escalate_to_human", False)

        daos.append(dao)

    sid = session_id or (logs[0].get("session_id") or "all")
    return generate_report(sid, daos)