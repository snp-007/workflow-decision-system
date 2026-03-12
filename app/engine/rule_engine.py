import operator


class RuleEngine:

    OPERATORS = {
        ">=": operator.ge,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        "<": operator.lt,
    }

    @staticmethod
    def evaluate(rule, data):

        for op_symbol, op_func in RuleEngine.OPERATORS.items():

            if op_symbol in rule:

                left, right = rule.split(op_symbol)

                left = left.strip()
                right = right.strip()

                left_value = data.get(left)

                # Handle invalid or missing input
                if left_value is None:
                    return False

                try:
                    left_value = float(left_value)
                    right_value = float(right)
                except Exception:
                    return False

                return op_func(left_value, right_value)

        return False