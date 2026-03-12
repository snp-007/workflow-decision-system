from app.engine.workflow_engine import WorkflowEngine


class DummyDB:
    def add(self, x): pass
    def commit(self): pass


class DummyInstance:
    id = 1


def test_happy_path():

    data = {
        "credit_score": 720,
        "income": 50000
    }

    engine = WorkflowEngine(
        "loan_approval",
        data,
        DummyDB(),
        DummyInstance()
    )

    decision, _ = engine.execute()

    assert decision == "approved"


def test_manual_review():

    data = {
        "credit_score": 500,
        "income": 50000
    }

    engine = WorkflowEngine(
        "loan_approval",
        data,
        DummyDB(),
        DummyInstance()
    )

    decision, _ = engine.execute()

    assert decision == "manual_review_pending"


def test_invalid_input():

    data = {
        "credit_score": None,
        "income": 50000
    }

    engine = WorkflowEngine(
        "loan_approval",
        data,
        DummyDB(),
        DummyInstance()
    )

    decision, _ = engine.execute()

    assert decision == "manual_review_pending"


def test_rule_change():

    data = {
        "credit_score": 680,
        "income": 50000
    }

    engine = WorkflowEngine(
        "loan_approval",
        data,
        DummyDB(),
        DummyInstance()
    )

    decision, _ = engine.execute()

    assert decision in ["approved", "manual_review_pending"]

def test_duplicate_request():

    data = {
        "credit_score": 720,
        "income": 50000
    }

    db = DummyDB()
    instance = DummyInstance()

    engine = WorkflowEngine(
        "loan_approval",
        data,
        db,
        instance
    )

    # first execution
    decision1, _ = engine.execute()

    # simulate duplicate execution
    decision2, _ = engine.execute()

    # decisions should match
    assert decision1 == decision2