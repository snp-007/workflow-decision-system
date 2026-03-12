def log_rule(rule, result, data, version):

    return {
        "workflow_version": version,
        "rule": rule,
        "result": "PASS" if result else "FAIL",
        "data": data
    }