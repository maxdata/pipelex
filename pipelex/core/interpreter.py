from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union, cast

import toml
from pydantic import BaseModel, model_validator
from typing_extensions import Self

from pipelex.core.bundles.pipelex_bundle_blueprint import PipelexBundleBlueprint
from pipelex.core.concepts.concept_blueprint import ConceptBlueprint
from pipelex.core.exceptions import (
    PipelexConfigurationError,
    PipelexUnknownPipeError,
)
from pipelex.core.pipes.pipe_input_blueprint import InputRequirementBlueprint
from pipelex.pipe_controllers.batch.pipe_batch_blueprint import PipeBatchBlueprint
from pipelex.pipe_controllers.condition.pipe_condition_blueprint import (
    PipeConditionBlueprint,
)
from pipelex.pipe_controllers.parallel.pipe_parallel_blueprint import (
    PipeParallelBlueprint,
)
from pipelex.pipe_controllers.sequence.pipe_sequence_blueprint import (
    PipeSequenceBlueprint,
)
from pipelex.pipe_operators.func.pipe_func_blueprint import PipeFuncBlueprint
from pipelex.pipe_operators.img_gen.pipe_img_gen_blueprint import PipeImgGenBlueprint
from pipelex.pipe_operators.jinja2.pipe_jinja2_blueprint import PipeJinja2Blueprint
from pipelex.pipe_operators.llm.pipe_llm_blueprint import PipeLLMBlueprint
from pipelex.pipe_operators.ocr.pipe_ocr_blueprint import PipeOcrBlueprint
from pipelex.tools.misc.toml_utils import (
    clean_trailing_whitespace,
    validate_toml_content,
    validate_toml_file,
)


class PLXDecodeError(toml.TomlDecodeError):
    """Raised when PLX decoding fails."""

    pass


class PipelexInterpreter(BaseModel):
    """plx -> PipelexBundleBlueprint"""

    file_path: Optional[Path] = None
    file_content: Optional[str] = None

    @staticmethod
    def escape_plx_string(value: Optional[str]) -> str:
        """Escape a string for plx serialization."""
        if value is None:
            return ""
        # Escape backslashes first (must be done first)
        value = value.replace("\\", "\\\\")
        # Escape quotes
        value = value.replace('"', '\\"')
        # Replace actual newlines with escaped newlines
        value = value.replace("\n", "\\n")
        value = value.replace("\r", "\\r")
        value = value.replace("\t", "\\t")
        return value

    @model_validator(mode="after")
    def check_file_path_or_file_content(self) -> Self:
        """Need to check if there is at least one of file_path or file_content"""
        if self.file_path is None and self.file_content is None:
            raise PipelexConfigurationError("Either file_path or file_content must be provided")
        return self

    @model_validator(mode="after")
    def validate_file_path(self) -> Self:
        if self.file_path:
            validate_toml_file(path=str(self.file_path))
        if self.file_content:
            validate_toml_content(content=self.file_content, file_path=str(self.file_path))
        return self

    def _read_and_reformat(self) -> str:
        """Load PLX content from file_path or use file_content directly."""
        if self.file_path:
            with open(self.file_path, "r", encoding="utf-8") as file:
                file_content = file.read()

            # Clean trailing whitespace and write back if needed
            cleaned_content = clean_trailing_whitespace(file_content)
            if file_content != cleaned_content:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(cleaned_content)
                return cleaned_content
            return file_content
        elif self.file_content is None:
            raise PipelexConfigurationError("file_content must be provided if file_path is not provided")
        return self.file_content

    @staticmethod
    def is_pipelex_file(file_path: Path) -> bool:
        """Check if a file is a valid Pipelex PLX file.

        Args:
            file_path: Path to the file to check

        Returns:
            True if the file is a Pipelex file, False otherwise

        Criteria:
            - Has .plx extension
            - Starts with "domain =" (ignoring leading whitespace)
        """
        # Check if it has .toml extension
        if file_path.suffix != ".plx":
            return False

        # Check if file exists
        if not file_path.exists() or not file_path.is_file():
            return False

        try:
            # Read the first few lines to check for "domain ="
            with open(file_path, "r", encoding="utf-8") as f:
                # Read first 100 characters (should be enough to find domain)
                content = f.read(100)
                # Remove leading whitespace and check if it starts with "domain ="
                stripped_content = content.lstrip()
                return stripped_content.startswith("domain =")
        except Exception:
            # If we can't read the file, it's not a valid Pipelex file
            return False

    def _parse_plx_content(self, content: str) -> Dict[str, Any]:
        """Parse PLX content and return the dictionary."""
        try:
            return toml.loads(content)
        except toml.TomlDecodeError as exc:
            file_path_str = str(self.file_path) if self.file_path else "content"
            raise PLXDecodeError(f"PLX parsing error in '{file_path_str}': {exc}", exc.doc, exc.pos) from exc

    def make_pipelex_bundle_blueprint(self) -> PipelexBundleBlueprint:
        """Make a PipelexBundleBlueprint from the file_path or file_content"""
        file_content = self._read_and_reformat()
        plx_data = self._parse_plx_content(file_content)
        return PipelexBundleBlueprint.model_validate(plx_data)
