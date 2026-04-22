from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path


TREE_PATH = Path(__file__).resolve().parent.parent / "tree" / "reflection-tree.json"
AXIS_SIDES = {
    "axis1": ("internal", "external"),
    "axis2": ("contribution", "entitlement"),
    "axis3": ("self", "other"),
}

# One warm summary paragraph for each 2^3 dominant-signal combination.
SUMMARY_TEMPLATES = {
    "internal|contribution|self": (
        "You read the day as something you could still shape, but the frame "
        "stayed close to your own lane. That can be a useful form of discipline. "
        "It may also be worth noticing whether self-management became the whole "
        "story, leaving little room to see who else was being moved by the same day."
    ),
    "internal|contribution|other": (
        "You seem to leave the day seeing yourself as an active part of a larger "
        "effort. Your choices mattered, your effort had direction, and the frame "
        "was bigger than your own strain. The risk in this pattern is quiet "
        "overextension, because people who keep moving do not always notice how "
        "much they are carrying until later."
    ),
    "internal|entitlement|self": (
        "You experienced the day as something you had to navigate yourself while "
        "also feeling the lack of support around you. That can create a solitary "
        "kind of effort: active on the surface, privately tallying what should "
        "not have been yours to absorb. There may be something important in that tension."
    ),
    "internal|entitlement|other": (
        "You still saw places where you had agency, but your attention kept "
        "returning to what the system or other people should have supplied. "
        "That is not contradictory. Sometimes the clearest contributors are also "
        "the quickest to notice missing support, because they feel its cost across the team."
    ),
    "external|contribution|self": (
        "You were responding to a lot you did not control, yet you still measured "
        "the day by what you could put in. That can produce a gritty kind of "
        "steadiness. It may also leave little room to register how tiring it is "
        "to keep giving while feeling pushed around by the environment."
    ),
    "external|contribution|other": (
        "The day seems to have landed on you more than with you, and still your "
        "mind stayed connected to what others needed. That combination often "
        "belongs to people who keep carrying value through unstable conditions. "
        "It can be generous, though sometimes at the cost of feeling that your own leverage disappeared."
    ),
    "external|entitlement|self": (
        "The day reads as something that happened to you, with your attention "
        "pulled toward what was missing for you personally. That is a narrow and "
        "very human place to end up when resources feel thin. The value of seeing "
        "it clearly is not to correct it on the spot, only to notice the shape the day took."
    ),
    "external|entitlement|other": (
        "You noticed the day as shaped by outside forces and by gaps in what "
        "should have been available, but your frame still included other people "
        "in the system. That can create clear social perception: you are not just "
        "frustrated for yourself; you are reading strain across the group. "
        "Sometimes that is the beginning of a more accurate diagnosis, not just complaint."
    ),
}


def fresh_tallies() -> dict[str, dict[str, int]]:
    return {
        axis: {left: 0, right: 0}
        for axis, (left, right) in AXIS_SIDES.items()
    }


def load_tree(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Tree file must contain a JSON list of nodes.")
    return data


def build_node_map(nodes: list[dict]) -> dict[str, dict]:
    node_map: dict[str, dict] = {}
    for node in nodes:
        node_id = node["id"]
        if node_id in node_map:
            raise ValueError(f"Duplicate node id: {node_id}")
        node_map[node_id] = node
    return node_map


def build_child_map(nodes: list[dict]) -> dict[str, list[str]]:
    child_map: dict[str, list[str]] = {}
    for node in nodes:
        parent_id = node.get("parentId")
        if parent_id:
            child_map.setdefault(parent_id, []).append(node["id"])
    return child_map


def parse_routing(routing: str) -> list[tuple[list[str], str]]:
    routes: list[tuple[list[str], str]] = []
    if not routing:
        return routes
    for clause in routing.split(";"):
        clause = clause.strip()
        if not clause:
            continue
        if not clause.startswith("answer="):
            raise ValueError(f"Invalid routing clause: {clause}")
        answers_part, target = clause[len("answer="):].rsplit(":", 1)
        answers = [answer.strip() for answer in answers_part.split("|") if answer.strip()]
        if not answers or not target.strip():
            raise ValueError(f"Invalid routing clause: {clause}")
        routes.append((answers, target.strip()))
    return routes


def validate_tree(nodes: list[dict], node_map: dict[str, dict], child_map: dict[str, list[str]]) -> None:
    required_fields = {
        "id",
        "parentId",
        "type",
        "text",
        "options",
        "target",
        "signal",
        "routing",
    }
    counts = {
        "question": 0,
        "decision": 0,
        "reflection": 0,
        "bridge": 0,
        "summary": 0,
        "start": 0,
        "end": 0,
    }
    shared_entry_ids = {"A1_Q1", "A2_Q1", "A3_Q1", "SUMMARY"}

    for node in nodes:
        missing = required_fields - set(node.keys())
        if missing:
            raise ValueError(f"Node {node.get('id', '<unknown>')} is missing fields: {sorted(missing)}")

        node_type = node["type"]
        if node_type not in counts:
            raise ValueError(f"Unsupported node type: {node_type}")
        counts[node_type] += 1

        if node_type == "question":
            if not 3 <= len(node["options"]) <= 5:
                raise ValueError(f"Question node {node['id']} must have 3-5 options.")
        elif node["options"]:
            raise ValueError(f"Non-question node {node['id']} must have an empty options list.")

        if node_type == "decision":
            if not node["parentId"]:
                raise ValueError(f"Decision node {node['id']} must point to a parent question.")
            parent = node_map.get(node["parentId"])
            if not parent or parent["type"] != "question":
                raise ValueError(f"Decision node {node['id']} must follow a question node.")
            routed_answers = set()
            for answers, target in parse_routing(node["routing"]):
                for answer in answers:
                    routed_answers.add(answer)
                if target not in node_map:
                    raise ValueError(f"Decision node {node['id']} routes to missing node {target}.")
            option_set = set(parent["options"])
            if routed_answers != option_set:
                raise ValueError(
                    f"Decision node {node['id']} does not cover parent question options exactly."
                )
        else:
            if node["routing"]:
                raise ValueError(f"Only decision nodes may define routing. Found on {node['id']}.")

        if node_type == "bridge":
            if not node["target"]:
                raise ValueError(f"Bridge node {node['id']} must define a target.")
            if node["target"] not in node_map:
                raise ValueError(f"Bridge node {node['id']} targets missing node {node['target']}.")
        elif node["target"]:
            raise ValueError(f"Only bridge nodes may define a target. Found on {node['id']}.")

        if node["signal"]:
            axis, side = node["signal"].split(":")
            if axis not in AXIS_SIDES or side not in AXIS_SIDES[axis]:
                raise ValueError(f"Node {node['id']} has invalid signal {node['signal']}.")

    if len(nodes) < 25:
        raise ValueError("Tree must contain at least 25 nodes.")
    if counts["question"] < 8:
        raise ValueError("Tree must contain at least 8 question nodes.")
    if counts["decision"] < 4:
        raise ValueError("Tree must contain at least 4 decision nodes.")
    if counts["reflection"] < 4:
        raise ValueError("Tree must contain at least 4 reflection nodes.")
    if counts["bridge"] < 2:
        raise ValueError("Tree must contain at least 2 bridge nodes.")
    if counts["summary"] != 1 or counts["start"] != 1 or counts["end"] != 1:
        raise ValueError("Tree must contain exactly one start, one summary, and one end node.")

    for node in nodes:
        node_type = node["type"]
        node_id = node["id"]
        if node_type == "end":
            continue
        if node_type == "decision":
            continue
        if node_type == "bridge":
            continue
        children = child_map.get(node_id, [])
        if len(children) != 1 and node_id not in shared_entry_ids:
            raise ValueError(
                f"Node {node_id} should have exactly one child for linear progression; found {len(children)}."
            )
        if node_id in shared_entry_ids and len(children) != 1:
            raise ValueError(f"Shared entry node {node_id} must still have exactly one child.")


def dominant_signal(tallies: dict[str, dict[str, int]], axis: str) -> str:
    left, right = AXIS_SIDES[axis]
    left_count = tallies[axis][left]
    right_count = tallies[axis][right]
    if left_count >= right_count:
        return left
    return right


def summary_reflection(tallies: dict[str, dict[str, int]]) -> str:
    key = "|".join(
        dominant_signal(tallies, axis) for axis in ("axis1", "axis2", "axis3")
    )
    return SUMMARY_TEMPLATES[key]


def interpolate(text: str, state: dict[str, str], tallies: dict[str, dict[str, int]]) -> str:
    def replacer(match: re.Match[str]) -> str:
        token = match.group(1)
        if token.endswith(".answer"):
            node_id = token[:-len(".answer")]
            return state.get(node_id, "")
        if token.endswith(".dominant"):
            axis = token[:-len(".dominant")]
            return dominant_signal(tallies, axis)
        if token == "summary_reflection":
            return summary_reflection(tallies)
        return match.group(0)

    return re.sub(r"\{([^{}]+)\}", replacer, text)


def next_child(node_id: str, child_map: dict[str, list[str]]) -> str:
    children = child_map.get(node_id, [])
    if len(children) != 1:
        raise ValueError(f"Node {node_id} must have exactly one child, found {len(children)}.")
    return children[0]


def evaluate_decision(node: dict, state: dict[str, str]) -> str:
    parent_id = node["parentId"]
    selected_answer = state.get(parent_id, "")
    for answers, target in parse_routing(node["routing"]):
        if selected_answer in answers:
            return target
    raise ValueError(
        f"No routing rule matched decision {node['id']} for answer {selected_answer!r}."
    )


def increment_signal(signal: str, tallies: dict[str, dict[str, int]]) -> None:
    if not signal:
        return
    axis, side = signal.split(":")
    tallies[axis][side] += 1


def print_block(text: str) -> None:
    print()
    print(text)
    print()


def prompt_for_choice(options: list[str]) -> str:
    while True:
        raw = input("Choose an option number: ").strip()
        if raw.isdigit():
            index = int(raw)
            if 1 <= index <= len(options):
                return options[index - 1]
        print(f"Please enter a number from 1 to {len(options)}.")


def run(tree_nodes: list[dict]) -> None:
    node_map = build_node_map(tree_nodes)
    child_map = build_child_map(tree_nodes)
    validate_tree(tree_nodes, node_map, child_map)

    state: dict[str, str] = {}
    tallies = fresh_tallies()
    current_id = "START"

    while True:
        node = node_map[current_id]
        node_type = node["type"]
        rendered_text = interpolate(node["text"], state, tallies)

        if node_type == "start":
            print_block(rendered_text)
            current_id = next_child(current_id, child_map)
            continue

        if node_type == "question":
            print_block(rendered_text)
            for idx, option in enumerate(node["options"], start=1):
                print(f"{idx}. {option}")
            print()
            selected = prompt_for_choice(node["options"])
            state[current_id] = selected
            increment_signal(node["signal"], tallies)
            current_id = next_child(current_id, child_map)
            continue

        if node_type == "decision":
            current_id = evaluate_decision(node, state)
            continue

        if node_type == "reflection":
            print_block(rendered_text)
            input("Press Enter to continue...")
            current_id = next_child(current_id, child_map)
            continue

        if node_type == "bridge":
            print_block(rendered_text)
            current_id = node["target"]
            continue

        if node_type == "summary":
            print_block(rendered_text)
            input("Press Enter to continue...")
            current_id = next_child(current_id, child_map)
            continue

        if node_type == "end":
            print_block(rendered_text)
            return

        raise ValueError(f"Unsupported node type encountered: {node_type}")


def main() -> int:
    try:
        tree_nodes = load_tree(TREE_PATH)
        run(tree_nodes)
        return 0
    except FileNotFoundError:
        print(f"Tree file not found: {TREE_PATH}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - keeps CLI errors readable
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
