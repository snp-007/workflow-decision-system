# Architecture Document

## Configurable Workflow Decision Platform

---

# 1. Introduction

This document describes the architecture of the **Configurable Workflow Decision Platform**, a system designed to process configurable business workflows while maintaining resilience, auditability, and adaptability to changing requirements.

The platform evaluates incoming requests against configurable rules, executes workflow stages, maintains state, records audit trails, and handles dependency failures with retries.

The architecture is designed to emphasize:

* modular design
* configurability
* explainability
* fault tolerance
* extensibility

---

# 2. System Overview

The system processes workflow requests through a configurable decision engine.

A request passes through multiple stages:

1. Request intake
2. Workflow configuration loading
3. Rule evaluation
4. External dependency simulation
5. Workflow decision generation
6. State persistence
7. Audit logging

The workflow definitions are externalized in configuration files, allowing rule changes without modifying application code.

---

# 3. High-Level Architecture

```
Client Request
      ↓
REST API (FastAPI)
      ↓
Workflow Engine
      ↓
Rule Engine
      ↓
External Dependency (Simulated)
      ↓
Database (State + History)
      ↓
Audit Logs
```

---

# 4. Core Components

## 4.1 API Layer

The API layer is implemented using FastAPI and exposes REST endpoints for interacting with the workflow platform.

Responsibilities:

* accept incoming workflow requests
* validate request schema
* enforce idempotency
* trigger workflow execution
* return workflow decisions

Example endpoint:

```
POST /workflow/start
```

---

## 4.2 Workflow Engine

The Workflow Engine orchestrates workflow execution.

Responsibilities:

* load workflow definitions from configuration
* execute workflow steps sequentially
* call rule evaluation
* interact with external dependencies
* track workflow execution state
* generate audit logs

The engine acts as the **central orchestrator of the platform**.

---

## 4.3 Rule Engine

The Rule Engine evaluates rule expressions defined in workflow configuration.

Example rule:

```
credit_score >= 650
```

The rule engine supports comparison operators such as:

* `>`
* `<`
* `>=`
* `<=`
* `==`
* `!=`

Invalid inputs are safely handled by treating them as rule failures.

---

## 4.4 Workflow Configuration

Workflows are defined using configuration files located in:

```
app/config/workflows.json
```

Example workflow configuration:

```json
{
  "loan_approval": {
    "version": "1.0",
    "steps": [
      {
        "name": "credit_check",
        "rule": "credit_score >= 650"
      },
      {
        "name": "income_check",
        "rule": "income >= 30000"
      }
    ],
    "success": "approved",
    "fail": "manual_review_pending"
  }
}
```

Benefits:

* rules can be changed without code modification
* new workflows can be added easily
* business logic is decoupled from application code

---

## 4.5 External Dependency Simulation

The system simulates an external service such as a **credit bureau API**.

The simulated dependency introduces:

* random failures
* network latency

This allows testing of:

* retry logic
* failure handling
* dependency resilience

---

## 4.6 Retry Mechanism

External dependency failures are handled using a retry strategy.

Retry behavior:

* up to 3 retry attempts
* small delay between retries

This improves reliability when external services are temporarily unavailable.

---

## 4.7 Database Layer

The system uses SQLite for persistence.

Two main tables are used.

### Workflow Instances

Stores current workflow state.

Fields include:

* request_id
* workflow_type
* workflow_version
* workflow status
* input data
* creation timestamp

---

### Workflow History

Stores the full workflow execution history.

Fields include:

* workflow stage
* decision
* timestamp

This table provides **complete execution traceability**.

---

## 4.8 Audit Logging

Audit logs capture the reasoning behind every workflow decision.

Each rule evaluation generates an audit entry containing:

* rule evaluated
* rule result
* workflow version
* input data

Example audit entry:

```json
{
  "rule": "credit_score >= 650",
  "result": "PASS",
  "workflow_version": "1.0"
}
```

Audit logs provide transparency and explainability.

---

# 5. Data Flow

The following steps describe the workflow processing lifecycle.

### Step 1 — Request Intake

A client submits a workflow request through the REST API.

Example:

```
POST /workflow/start
```

---

### Step 2 — Idempotency Check

The system checks whether a request with the same `request_id` has already been processed.

If a duplicate request exists:

* the stored decision is returned
* the workflow is not executed again

---

### Step 3 — Workflow Configuration Loading

The system loads the appropriate workflow definition from the configuration file.

---

### Step 4 — External Dependency Call

The workflow engine calls simulated external dependencies when required.

Failures may trigger retry logic.

---

### Step 5 — Rule Evaluation

The rule engine evaluates configured rules against the request data.

Each rule produces a PASS or FAIL result.

---

### Step 6 — Decision Determination

If all rules pass:

```
approved
```

If a rule fails:

```
manual_review_pending
```

---

### Step 7 — State Persistence

Workflow results and state are saved to the database.

---

### Step 8 — Audit Logging

Rule evaluations and results are recorded for explainability.

---

### Step 9 — Response

The API returns:

* workflow decision
* audit trace

---

# 6. Failure Handling

The system supports multiple failure scenarios.

### Invalid Input

Invalid input values are treated as rule failures instead of causing system crashes.

---

### External Dependency Failure

External service failures trigger retry attempts.

If retries fail, the workflow may transition to manual review.

---

### Duplicate Requests

Duplicate workflow requests are handled via idempotency checks.

---

### Manual Review

If automated rules cannot determine a decision, the workflow transitions to:

```
manual_review_pending
```

This allows human intervention.

---

# 7. Scaling Considerations

The current implementation runs as a single-node prototype.

However, the architecture supports future scaling.

Possible scaling improvements include:

### Stateless API Instances

Multiple API servers can run behind a load balancer.

---

### Asynchronous Workflow Processing

Workflow execution could be offloaded to worker nodes.

---

### Message Queue Integration

Workflows could be distributed using message brokers.

Examples:

* Redis
* RabbitMQ
* Kafka

---

### Rule Caching

Workflow configurations could be cached in memory to reduce disk reads.

---

### Database Scaling

For high throughput systems:

* read replicas
* database sharding
* distributed SQL databases

---

# 8. Trade-offs

Several trade-offs were made in the design.

### Simplicity vs Feature Richness

A lightweight rule engine was implemented rather than integrating a complex rule framework.

This keeps the system easy to understand and maintain.

---

### Configuration Files vs Database Rules

Rules are stored in configuration files rather than the database.

This simplifies the prototype but limits runtime rule updates.

---

### SQLite vs Production Databases

SQLite was chosen for simplicity and ease of setup.

Production systems would likely use PostgreSQL or another scalable database.

---

### Synchronous Execution

Workflow execution is currently synchronous.

Asynchronous processing would improve scalability for large workloads.

---

# 9. Assumptions

Several assumptions were made during development.

* Workflow rules are simple comparison expressions.
* Input requests follow a predefined schema.
* External dependencies are simulated rather than real services.
* Workflow execution volume is moderate for the prototype environment.
* Configuration changes are applied by updating the configuration file.

---

# 10. Conclusion

The Configurable Workflow Decision Platform demonstrates a resilient architecture for processing configurable business workflows.

The system provides:

* configurable rule-driven workflows
* reliable workflow orchestration
* auditability and explainable decisions
* failure handling and retry mechanisms
* idempotent request processing

The modular architecture allows the platform to evolve into a scalable workflow orchestration system capable of supporting complex enterprise workflows.
