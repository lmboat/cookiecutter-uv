"""Tests for the per-project Claude Code files shipped with every generated project."""

from __future__ import annotations

import json


def test_claude_settings_is_valid_json(bake):
    project = bake()
    settings = json.loads(project.read_file(".claude/settings.json"))
    assert "Bash(uv *)" in settings["permissions"]["allow"]


def test_claude_md_renders_project_fields(bake):
    project = bake(project_name="my-project", project_description="Does a thing.")
    assert project.file_contains("CLAUDE.md", "# my-project")
    assert project.file_contains("CLAUDE.md", "Does a thing.")
    assert project.file_contains("CLAUDE.md", "make install")
    assert not project.file_contains("CLAUDE.md", "{{")


def test_claude_md_reflects_layout(bake):
    src_project = bake(layout="src", project_name="my-project")
    assert src_project.file_contains("CLAUDE.md", "src/my_project/")
    flat_project = bake(layout="flat", project_name="my-project")
    assert flat_project.file_contains("CLAUDE.md", "`my_project/`")
    assert not flat_project.file_contains("CLAUDE.md", "src/my_project/")


def test_gitignore_has_secret_and_data_blocks(bake):
    project = bake()
    for pattern in (
        "*.pem",
        "CLAUDE.local.md",
        ".claude/settings.local.json",
        "slurm-*.out",
        "data/**",
        "!data/**/.gitkeep",
    ):
        assert project.file_contains(".gitignore", pattern), pattern


def test_gitignore_keeps_data_gitkeep_tracked(bake):
    project = bake()
    project.git_init()
    for subdir in ("raw", "interim", "processed", "external", "metadata"):
        result = project.run(f"git check-ignore -q data/{subdir}/.gitkeep")
        assert result.returncode == 1, f"data/{subdir}/.gitkeep is ignored"
    result = project.run("git check-ignore -q data/raw/sample.csv")
    assert result.returncode == 0, "data/raw/sample.csv should be ignored"


def test_precommit_has_secret_hooks(bake):
    project = bake()
    assert project.is_valid_yaml(".pre-commit-config.yaml")
    for hook_id in ("detect-private-key", "check-added-large-files", "gitleaks"):
        assert project.file_contains(".pre-commit-config.yaml", hook_id), hook_id
