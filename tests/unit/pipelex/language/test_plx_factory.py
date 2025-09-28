from pathlib import Path
from typing import Type

import pytest

from pipelex import log, pretty_print
from pipelex.core.bundles.pipelex_bundle_blueprint import PipelexBundleBlueprint
from pipelex.language.plx_factory import PlxFactory

from tests.unit.pipelex.core.test_data import InterpreterTestCases


class TestPlxFactory:

    @pytest.mark.parametrize("test_name,expected_plx_content,blueprint", InterpreterTestCases.VALID_TEST_CASES)
    def test_make_plx_content(self, test_name: str, expected_plx_content: str, blueprint: PipelexBundleBlueprint):
        """Test making blueprint from various valid PLX content."""
        plx_content = PlxFactory.make_plx_content(blueprint=blueprint)
        pretty_print(plx_content, title=f"Plx content {test_name}")
        pretty_print(expected_plx_content, title=f"Expected PLX content {test_name}")
        assert plx_content == expected_plx_content

