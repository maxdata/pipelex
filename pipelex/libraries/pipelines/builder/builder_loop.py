import asyncio
import time
from typing import Annotated, Any, cast

import typer
from pydantic import ConfigDict, Field, ValidationError, field_validator

from pipelex import log, pretty_print
from pipelex.client.protocol import ImplicitMemory
from pipelex.core.bundles.pipelex_bundle_blueprint import PipeBlueprintUnion, PipelexBundleBlueprint
from pipelex.core.concepts.concept_blueprint import ConceptBlueprint
from pipelex.core.domains.domain_blueprint import DomainBlueprint
from pipelex.core.memory.working_memory import WorkingMemory
from pipelex.core.stuffs.stuff_content import ListContent, StructuredContent
from pipelex.exceptions import (
    ConceptDefinitionError,
    ConceptLoadingError,
    DomainLoadingError,
    PipeDefinitionError,
    PipelexError,
    PipeLoadingError,
    StaticValidationError,
)
from pipelex.hub import get_class_registry, get_library_manager, get_report_delegate
from pipelex.language.plx_factory import PlxFactory
from pipelex.libraries.pipelines.builder.builder import PipelexBundleSpec
from pipelex.libraries.pipelines.builder.concept.concept_spec import ConceptSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_batch_spec import PipeBatchSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_compose_spec import PipeComposeSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_condition_spec import PipeConditionSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_func_spec import PipeFuncSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_img_spec import PipeImgGenSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_llm_spec import PipeLLMSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_ocr_spec import PipeOcrSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_parallel_spec import PipeParallelSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_sequence_spec import PipeSequenceSpec
from pipelex.libraries.pipelines.builder.pipe.pipe_signature import PipeSignature
from pipelex.pipe_works.pipe_dry import dry_run_pipes
from pipelex.pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline
from pipelex.tools.misc.file_utils import ensure_directory_for_file_path, save_text_to_path
from pipelex.tools.typing.pydantic_utils import format_pydantic_validation_error


class BuilderLoop:
    async def build_and_fix(self, pipe_code: str, input_memory: ImplicitMemory | None = None) -> PipelexBundleSpec:
        pretty_print(f"Building and fixing with {pipe_code}")
        pipe_output = await execute_pipeline(
            pipe_code=pipe_code,
            input_memory=input_memory,
        )
        pretty_print(pipe_output, title="Pipe Output")

        pipelex_bundle_spec = pipe_output.working_memory.get_stuff_as(name="pipelex_bundle_spec", content_type=PipelexBundleSpec)
        pretty_print(pipelex_bundle_spec, title="Pipelex Bundle Spec")
        return pipelex_bundle_spec
