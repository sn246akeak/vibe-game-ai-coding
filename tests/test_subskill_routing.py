import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SubskillRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        from scripts.subskill_router import load_manifest

        self.manifest = load_manifest(ROOT / "references" / "subskills.json")

    def route(self, phase: int, **context: object) -> list[str]:
        from scripts.subskill_router import select_routes

        return [
            item["skill"]
            for item in select_routes(self.manifest, phase=phase, context=context)
        ]

    def test_godot_prd_uses_design_ui_and_engine_specialists(self) -> None:
        self.assertEqual(
            self.route(2, engine="godot"),
            ["game-design-theory", "game-ui-ux", "godot"],
        )

    def test_game_feel_waits_until_mechanics_are_verified(self) -> None:
        self.assertNotIn(
            "game-feel",
            self.route(4, engine="godot", mechanics_verified=False),
        )
        self.assertIn(
            "game-feel",
            self.route(4, engine="godot", mechanics_verified=True),
        )

    def test_threejs_ui_replaces_engine_neutral_ui_in_art_integration(self) -> None:
        routed = self.route(7, engine="threejs", runtime="web")
        self.assertIn("threejs-game-ui-designer", routed)
        self.assertNotIn("game-ui-ux", routed)

    def test_godot_web_export_does_not_use_the_html_source_test_loop(self) -> None:
        routed = self.route(3, engine="godot", runtime="web")
        self.assertIn("godot", routed)
        self.assertNotIn("develop-web-game", routed)

    def test_higgsfield_is_only_selected_as_an_art_provider(self) -> None:
        self.assertNotIn("higgsfield-game-generation", self.route(6))
        self.assertIn(
            "higgsfield-game-generation",
            self.route(6, art_provider="higgsfield"),
        )

    def test_rivet_multiplayer_is_only_selected_for_rivetkit(self) -> None:
        self.assertNotIn("multiplayer-game", self.route(2, multiplayer_backend="godot"))
        self.assertIn(
            "multiplayer-game",
            self.route(2, multiplayer_backend="rivetkit"),
        )


class DependencyInspectionTests(unittest.TestCase):
    def test_dependency_inspection_reads_the_actual_skill_directories(self) -> None:
        from scripts.subskill_router import inspect_dependencies

        manifest = {
            "dependencies": [
                {"name": "required-skill", "tier": "core"},
                {"name": "optional-skill", "tier": "optional"},
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            skills_root = Path(temp_dir)
            installed = skills_root / "required-skill"
            installed.mkdir()
            (installed / "SKILL.md").write_text(
                "---\nname: required-skill\ndescription: test\n---\n",
                encoding="utf-8",
            )

            result = inspect_dependencies(manifest, skills_root)

        by_name = {item["name"]: item for item in result}
        self.assertTrue(by_name["required-skill"]["installed"])
        self.assertFalse(by_name["optional-skill"]["installed"])


class ManifestTests(unittest.TestCase):
    def test_manifest_is_valid_json_and_names_are_unique(self) -> None:
        manifest_path = ROOT / "references" / "subskills.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        names = [item["name"] for item in manifest["dependencies"]]
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
