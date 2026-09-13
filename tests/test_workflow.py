import argparse
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from scripts.workflow import apply_action, current, initial_state, check_state
from scripts.subskill_router import load_manifest, select_routes, resolve_routes, tree_digest

ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        (self.project / "spec.md").write_text("Approved rules", encoding="utf-8")
        (self.project / "checks.md").write_text("Observed validation evidence", encoding="utf-8")
        self.state = initial_state("v0.1", "Godot 4.4")

    def act(self, command="transition", **values):
        args = dict(command=command, module=current(self.state)["id"], evidence=[], decision="", note="")
        args.update(values)
        self.state = apply_action(self.state, argparse.Namespace(**args), self.project)

    def ready(self):
        self.act(to="designing")
        self.act(to="ready_to_build", evidence=["spec.md"], decision="User approved this contract")

    def review(self):
        self.ready()
        self.act(to="implementing")
        self.act(to="verifying")
        self.act("verify", evidence=["checks.md"])
        self.act(to="needs_user_review")

    def test_no_skipping_gate_and_no_self_acceptance(self):
        before = copy.deepcopy(self.state)
        with self.assertRaises(ValueError):
            self.act(to="accepted", decision="ok")
        self.assertEqual(before, self.state)
        self.review()
        with self.assertRaises(ValueError):
            self.act(to="accepted")
        self.act(to="accepted", decision="User accepted charter")
        self.assertEqual(current(self.state)["id"], "phase-1")

    def test_changed_source_requires_new_review(self):
        self.ready()
        (self.project / "spec.md").write_text("Changed rules", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "input changed"):
            self.act(to="implementing")
        self.act("revise", note="User changed source")
        self.assertFalse(current(self.state)["inputs"])

    def test_missing_evidence_and_changed_evidence_block_acceptance(self):
        self.ready()
        self.act(to="implementing")
        self.act(to="verifying")
        with self.assertRaises(ValueError):
            self.act(to="needs_user_review")
        self.act(to="needs_user_review", evidence=["checks.md"])
        (self.project / "checks.md").write_text("Checks now fail", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.act(to="accepted", decision="User approved earlier evidence")

    def test_fixed_version_module_is_inserted_before_art_and_requires_scope_decision(self):
        args = dict(id="cards", name="Card system", phase=4, source=["spec.md"], depends_on=["phase-3"])
        with self.assertRaises(ValueError):
            self.act("add", **args)
        self.act("add", **args, decision="Cards included in v0.1")
        ids = [m["id"] for m in self.state["modules"]]
        self.assertLess(ids.index("cards"), ids.index("phase-6"))

    def test_full_version_cycle_with_module_and_deferral(self):
        self.act("add", id="cards", name="Cards", phase=4, source=[], depends_on=["phase-3"], decision="In scope")
        completed = []
        while current(self.state):
            module_id = current(self.state)["id"]
            if module_id == "phase-8":
                self.act("defer", decision="User deferred audio for this prototype")
            else:
                self.review()
                self.act(to="accepted", decision="Simulated user accepted this gate")
            completed.append(module_id)
            self.state = json.loads(json.dumps(self.state))
        self.assertEqual(completed[-1], "phase-9")
        self.assertIn("cards", completed)
        check_state(self.state)

    def test_cli_init_resume_and_legacy_preservation(self):
        command = [sys.executable, str(ROOT / "scripts/workflow.py"), "--project", str(self.project)]
        init = subprocess.run(command + ["init", "--version", "v0.1", "--engine", "godot"], capture_output=True)
        self.assertEqual(init.returncode, 0, init.stdout)
        again = subprocess.run(command + ["init", "--version", "v0.2", "--engine", "godot"], capture_output=True)
        self.assertEqual(again.returncode, 2)
        self.assertEqual(subprocess.run(command + ["validate"], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(command + ["export"], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(command + ["export"], capture_output=True).returncode, 2)

    def test_dependency_order_can_put_data_before_gameplay(self):
        self.act("add", id="card-data", name="Data", phase=5, source=[], depends_on=["phase-3"], decision="Include data")
        self.act("add", id="cards", name="Cards", phase=4, source=[], depends_on=["card-data"], decision="Include cards")
        ids = [m["id"] for m in self.state["modules"]]
        self.assertLess(ids.index("card-data"), ids.index("cards"))
        self.assertLess(ids.index("cards"), ids.index("phase-6"))

    def test_scope_addition_does_not_interrupt_active_work(self):
        while current(self.state)["id"] != "phase-6":
            self.review()
            self.act(to="accepted", decision="Simulated acceptance")
        self.ready()
        self.act("add", id="revision", name="Revision", phase=4, source=[], depends_on=["phase-3"], decision="Add revision")
        self.assertEqual(current(self.state)["id"], "phase-6")
        with self.assertRaises(ValueError):
            self.act("context", key="engine", value="web", decision="Change engine")

    def test_delegation_contract_is_current_bounded_and_cleared_on_review(self):
        contract = {"module": "phase-0", "delegate": "demo", "objective": "Review",
                    "input_source": ["spec.md"], "allowed_scope": ["spec"],
                    "forbidden": ["code"], "required_output": ["report"], "return_gate": "review"}
        path = self.project / "contract.json"
        path.write_text(json.dumps(contract), encoding="utf-8")
        self.ready()
        with patch("scripts.subskill_router.resolve_routes", return_value=[{"skill": "demo", "status": "modified"}]):
            with self.assertRaises(ValueError):
                self.act("delegate", contract="contract.json", skills_root=str(self.project))
        with patch("scripts.subskill_router.resolve_routes", return_value=[{"skill": "demo", "status": "verified"}]):
            self.act("delegate", contract="contract.json", skills_root=str(self.project))
        self.assertEqual(current(self.state)["delegation"], contract)
        self.act(to="implementing")
        self.act(to="verifying")
        self.act(to="needs_user_review", evidence=["checks.md"])
        self.assertIsNone(current(self.state)["delegation"])

    def test_legacy_status_and_writer_lock_are_preserved(self):
        directory = self.project / "docs/ai-coding-workflow"
        directory.mkdir(parents=True)
        status = directory / "STATUS.md"
        status.write_text("Human project log", encoding="utf-8")
        cmd = [sys.executable, str(ROOT / "scripts/workflow.py"), "--project", str(self.project),
               "init", "--version", "v1", "--engine", "godot"]
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)
        self.assertEqual(status.read_text(encoding="utf-8"), "Human project log")
        self.assertFalse((directory / "workflow.json").exists())
        lock = directory / ".workflow.lock"
        lock.write_text("other writer", encoding="utf-8")
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)
        self.assertTrue(lock.exists())

    def test_cli_complete_version_resumes_between_processes(self):
        command = [sys.executable, str(ROOT / "scripts/workflow.py"), "--project", str(self.project)]
        def run(*args):
            result = subprocess.run(command + list(args), capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        run("init", "--version", "v1", "--engine", "godot")
        for phase in (0, 1, 2, 3, 6, 7, 8, 9):
            identifier = f"phase-{phase}"
            run("transition", identifier, "--to", "designing")
            run("transition", identifier, "--to", "ready_to_build", "--evidence", "spec.md", "--decision", "Simulated design approval")
            run("transition", identifier, "--to", "implementing")
            run("transition", identifier, "--to", "verifying")
            run("transition", identifier, "--to", "needs_user_review", "--evidence", "checks.md")
            run("transition", identifier, "--to", "accepted", "--decision", "Simulated user acceptance")
        run("validate")
        run("export")
        state = json.loads((self.project / "docs/ai-coding-workflow/workflow.json").read_text(encoding="utf-8"))
        self.assertIsNone(current(state))

    def test_deferred_sample_does_not_allow_batch_implementation(self):
        while current(self.state)["id"] != "phase-6":
            self.review()
            self.act(to="accepted", decision="Simulated acceptance")
        self.act("defer", decision="User defers the visual pass")
        self.ready()
        with self.assertRaisesRegex(ValueError, "dependencies must be accepted"):
            self.act(to="implementing")
        self.act("defer", decision="User also defers batch integration")
        self.assertEqual(current(self.state)["id"], "phase-8")

    def test_revision_preserves_earlier_evidence_in_history(self):
        self.review()
        evidence = copy.deepcopy(current(self.state)["evidence"])
        self.act("revise", note="User requested changes")
        self.assertFalse(current(self.state)["evidence"])
        self.assertEqual(self.state["history"][-2]["details"]["evidence"], evidence)


class ResolverTests(unittest.TestCase):
    def test_aliases_and_phase8_feedback_gate(self):
        manifest = load_manifest(ROOT / "references/subskills.json")
        for engine in ("Godot 4.4", "godot4", "Godot Engine"):
            self.assertIn("godot", [r["skill"] for r in select_routes(manifest, 2, {"engine": engine})])
        self.assertNotIn("game-feel", [r["skill"] for r in select_routes(manifest, 8, {})])

    def test_only_current_route_is_required_and_hash_change_is_visible(self):
        source = {"repo": "test/test", "path": "demo", "ref": "a" * 40}
        manifest = {"dependencies": [{"name": "demo", "source": source}],
                    "routes": [{"phase": 2, "skill": "demo"}]}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            lock = {"dependencies": {"demo": {"source": source, "sha256": tree_digest({"SKILL.md": b"original"})}}}
            self.assertEqual(resolve_routes(manifest, 2, {}, root, lock)[0]["status"], "missing")
            (root / "demo").mkdir()
            (root / "demo/SKILL.md").write_bytes(b"original")
            self.assertEqual(resolve_routes(manifest, 2, {}, root, lock)[0]["status"], "verified")
            (root / "demo/SKILL.md").write_bytes(b"changed")
            self.assertEqual(resolve_routes(manifest, 2, {}, root, lock)[0]["status"], "modified")
            self.assertEqual(resolve_routes(manifest, 1, {}, root, lock), [])


if __name__ == "__main__":
    unittest.main()
