import logging

logging.basicConfig(level=logging.INFO)


def bare_except_example(x):
    # This should be reported as: bare-except
    try:
        return 10 / x
    except:
        # Very bad: catches everything, no type
        print("Something went wrong!")  # also logging/printing only


def empty_handler_example(data):
    # This should be reported as: empty-handler
    try:
        value = data["key"]
        return int(value)
    except KeyError:
        # Completely empty handler (ignored error)
        pass


def swallowed_exception_example(filename):
    # This should be reported as: swallowed-exception
    try:
        with open(filename) as f:
            return f.read()
    except OSError as e:
        # Only logs, does not re-raise
        logging.error("Failed to read file %s: %s", filename, e)


def good_handler_example(a, b):
    # This one is "good" and should NOT be reported
    try:
        return a / b
    except ZeroDivisionError as e:
        logging.warning("Division by zero: %s", e)
        # Properly re-raises the exception
        raise


class SomeClass:
    def method_with_bare_except(self, text):
        # Another bare-except, to show the script also finds methods in classes
        try:
            return text.upper()
        except:
            print("Could not uppercase text")
