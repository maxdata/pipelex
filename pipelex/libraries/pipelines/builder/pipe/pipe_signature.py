from typing import Any

from pydantic import Field, field_validator

from pipelex.core.pipes.exceptions import PipeBlueprintError
from pipelex.core.pipes.pipe_blueprint import AllowedPipeCategories, AllowedPipeTypes, PipeBlueprint
from pipelex.core.pipes.pipe_input_blueprint import InputRequirementBlueprint
from pipelex.core.stuffs.stuff_content import StructuredContent
from pipelex.libraries.pipelines.builder.concept.concept_spec import ConceptSpec
from pipelex.libraries.pipelines.builder.pipe.inputs_spec import InputRequirementSpec
from pipelex.tools.misc.string_utils import is_snake_case


class PipeSignature(StructuredContent):
    code: str = Field(description="Pipe code. Must be snake_case.")
    type: AllowedPipeTypes = Field(description="Pipe type.")
    category: AllowedPipeCategories = Field(description="Pipe category.")
    description: str = Field(description="What the pipe does")
    inputs: dict[str, str] = Field(description="Pipe inputs: key is the concept code in snake_case, value is the ConceptCode in PascalCase.")
    result: str = Field(description="The name of the result of the pipe. Must be snake_case. It could be referenced as input in a following pipe.")
    output: str = Field(description="ConceptCode in PascalCase")
    # important_features: dict[str, Any] | None = Field(
    #     default=None,
    #     description="Important features specific to this pipe type "
    #     "(e.g., referenced pipe codes for controllers, specific configuration for operators)",
    # )


class PipeSpec(StructuredContent):
    """Spec defining a pipe: an executable component with a clear contract defined by its inputs and output.
    There are two categories of pipes: controllers and operators.
    Controllers are used to control the flow of the pipeline, and operators are used to perform specific tasks.
    """

    type: Any = Field(description=f"Pipe type. It is defined with type `Any` but validated at runtime and it must be one of: {AllowedPipeTypes}")
    category: Any = Field(
        description=f"Pipe category. It is defined with type `Any` but validated at runtime and it must be one of: {AllowedPipeCategories}"
    )
    definition: str | None = Field(description="Natural language description of what the pipe does.")
    inputs: dict[str, str | InputRequirementSpec] | None = Field(
        description=(
            "Input concept specifications. The keys are input names in snake_case. "
            "Each value is aither the ConceptCode in PascalCase or an InputRequirementSpec with additional constraints"
        ),
    )
    output: str = Field(description="Output concept code in PascalCase format!! Very important")

    @field_validator("type", mode="after")
    @staticmethod
    def validate_pipe_type(value: Any) -> Any:
        if value not in AllowedPipeTypes.value_list():
            msg = f"Invalid pipe type '{value}'. Must be one of: {AllowedPipeTypes.value_list()}"
            raise PipeBlueprintError(msg)
        return value

    @field_validator("output", mode="before")
    @staticmethod
    def validate_concept_string_or_code(output: str) -> str:
        ConceptSpec.validate_concept_string_or_code(concept_string_or_code=output)
        return output

    @classmethod
    def validate_pipe_code_syntax(cls, pipe_code: str) -> str:
        if not is_snake_case(pipe_code):
            msg = f"Invalid pipe code syntax '{pipe_code}'. Must be in snake_case."
            raise PipeBlueprintError(msg)
        return pipe_code

    def to_blueprint(self) -> PipeBlueprint:
        converted_inputs: dict[str, str | InputRequirementBlueprint] | None = None
        if self.inputs is not None:
            converted_inputs = {}
            for input_name, input_spec in self.inputs.items():
                if isinstance(input_spec, InputRequirementSpec):
                    converted_inputs[input_name] = input_spec.to_blueprint()
                else:
                    converted_inputs[input_name] = InputRequirementBlueprint(concept=input_spec)

        return PipeBlueprint(
            definition=self.definition,
            inputs=converted_inputs,
            output=self.output,
            type=self.type,
            category=self.category,
        )
