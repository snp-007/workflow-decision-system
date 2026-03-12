import json

from ..models import WorkflowHistory
from .rule_engine import RuleEngine
from ..audit.audit_logger import log_rule

from ..services.external_service import credit_bureau_check
from ..services.retry_service import retry_operation


def save_history(db, instance_id, stage, decision):
    """
    Save workflow stage execution history
    """

    history = WorkflowHistory(
        instance_id=instance_id,
        stage=stage,
        decision=str(decision)
    )

    db.add(history)
    db.commit()


class WorkflowEngine:

    def __init__(self, workflow_type, data, db, instance):
        """
        Initialize workflow execution
        """

        with open("app/config/workflows.json") as f:
            workflows = json.load(f)

        self.workflow = workflows[workflow_type]
        self.version = self.workflow["version"]

        self.data = data
        self.db = db
        self.instance = instance

        self.audit = []

    def execute(self):
        """
        Execute workflow steps sequentially
        """

        for step in self.workflow["steps"]:

            stage_name = step["name"]

            # Simulate external dependency
            if stage_name == "credit_check":

                retry_operation(
                    lambda: credit_bureau_check(self.data)
                )

            rule = step["rule"]

            result = RuleEngine.evaluate(rule, self.data)

            # Save workflow history
            save_history(
                self.db,
                self.instance.id,
                stage_name,
                result
            )

            # Save audit log
            self.audit.append(
                log_rule(
                    rule,
                    result,
                    self.data,
                    self.version
                )
            )

            # If rule fails → manual review
            if not result:
                return "manual_review_pending", self.audit

        # All steps passed
        return self.workflow["success"], self.audit