import sys

if __name__ == "__main__":
    if "--sandbox" in sys.argv:
        from execution.execute_sandbox import execute_sandbox
        execute_sandbox()