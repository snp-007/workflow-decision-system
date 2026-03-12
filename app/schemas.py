from pydantic import BaseModel
from typing import Dict


class WorkflowRequest(BaseModel):

    workflow_type: str
    request_id: str
    data: Dict