import argparse
import re
from dataclasses import dataclass


@dataclass
class Operation:
    key: str
    operator: str
    value: int
    next_workflow: str  # workflow name or accept / reject


@dataclass
class Workflow:
    label: str
    operations: list[Operation]
    catch_all: str


@dataclass
class Part:
    x: str
    m: str
    a: str
    s: str


def parse_operations(ops: str) -> list[Operation]:
    operation_re = re.compile(r"([xmas])(<|>)(\d+):([a-zAR]+)")
    operations = []
    for op in ops.split(","):
        if m := operation_re.match(op):
            operations.append(
                Operation(m.group(1), m.group(2), int(m.group(3)), m.group(4))
            )
    return operations


def parse_file(file):
    workflow_re = re.compile(r"([a-z]+){((?:[xmas](?:<|>)\d+:[a-zAR]+,)+)([a-zA-Z]+)}")

    workflows = {}
    while line := file.pop(0):
        if m := workflow_re.match(line):
            label = m.group(1)
            operations = parse_operations(m.group(2))
            catch_all = m.group(3)
            print(label, operations, catch_all)
            workflows[label] = Workflow(label, operations, catch_all)

    xmas_re = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")
    parts = []
    while line := file.pop(0):
        if m := xmas_re.match(line):
            parts.append(
                {
                    "x": int(m.group(1)),
                    "m": int(m.group(2)),
                    "a": int(m.group(3)),
                    "s": int(m.group(4)),
                }
            )
        else:
            raise ValueError(f"Encountered invalid part: {line}")

    return workflows, parts


def process_part(workflows, part) -> bool:
    workflow = workflows["in"]
    while True:
        for o in workflow.operations:
            if (o.operator == ">" and part[o.key] > o.value) or (
                o.operator == "<" and part[o.key] < o.value
            ):
                next_workflow = o.next_workflow
                break
        else:
            next_workflow = workflow.catch_all

        if next_workflow == "A":
            return True
        if next_workflow == "R":
            return False

        workflow = workflows[next_workflow]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="test.txt")
    args = parser.parse_args()

    filename = args.filename

    with open(filename) as f:
        file = f.read().splitlines() + [""]
        workflows, parts = parse_file(file)

    print(workflows)
    print(parts)

    accepted_parts = [part for part in parts if process_part(workflows, part)]
    print(sum([v for part in accepted_parts for v in part.values()]))
