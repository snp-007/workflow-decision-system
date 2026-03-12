import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..schemas import WorkflowRequest
from ..models import WorkflowInstance
from ..engine.workflow_engine import WorkflowEngine

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/workflow/start")
def start_workflow(request: WorkflowRequest, db: Session = Depends(get_db)):

    existing = db.query(WorkflowInstance).filter(
        WorkflowInstance.request_id == request.request_id
    ).first()

    if existing:
        return {"status": existing.status}

    with open("app/config/workflows.json") as f:
        workflows = json.load(f)

    workflow_config = workflows[request.workflow_type]

    instance = WorkflowInstance(
        request_id=request.request_id,
        workflow_type=request.workflow_type,
        workflow_version=workflow_config["version"],
        status="processing",
        current_stage="started",
        input_data=request.data
    )

    db.add(instance)
    db.commit()
    db.refresh(instance)

    engine = WorkflowEngine(
        request.workflow_type,
        request.data,
        db,
        instance
    )

    decision, audit = engine.execute()

    instance.status = decision
    instance.current_stage = "completed"

    db.commit()

    return {
        "decision": decision,
        "audit": audit
    }


@router.post("/workflow/manual-review")
def manual_review(request_id: str, decision: str, db: Session = Depends(get_db)):

    instance = db.query(WorkflowInstance).filter(
        WorkflowInstance.request_id == request_id
    ).first()

    if not instance:
        return {"error": "workflow not found"}

    if instance.status != "manual_review_pending":
        return {"error": "workflow not awaiting manual review"}

    instance.status = decision
    instance.current_stage = "completed"

    db.commit()

    return {"status": decision}