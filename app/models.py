from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from .database import Base


class WorkflowInstance(Base):

    __tablename__ = "workflow_instances"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True)
    workflow_type = Column(String)
    workflow_version = Column(String)

    status = Column(String)
    current_stage = Column(String)

    input_data = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)


class WorkflowHistory(Base):

    __tablename__ = "workflow_history"

    id = Column(Integer, primary_key=True)

    instance_id = Column(Integer)
    stage = Column(String)
    decision = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)