domain = "pipe_design"
definition = "Build and process pipes."

[concept]
PipeSignature = "A pipe contract which says what the pipe does, not how it does it: code (the pipe code in snake_case), type, description, inputs, output."
PipeSpec = "A structured spec for a pipe (union)."
# Pipe controllers
PipeBatchSpec = "A structured spec for a pipe batch."
PipeConditionSpec = "A structured spec for a pipe condition."
PipeParallelSpec = "A structured spec for a pipe parallel."
PipeSequenceSpec = "A structured spec for a pipe sequence."
# Pipe operators
PipeFuncSpec = "A structured spec for a pipe func."
PipeImgGenSpec = "A structured spec for a pipe img gen."
PipeComposeSpec = "A structured spec for a pipe jinja2."
PipeLLMSpec = "A structured spec for a pipe llm."
PipeOcrSpec = "A structured spec for a pipe ocr."
PipeFailure = "Details of a single pipe failure during dry run."

[pipe]

# ────────────────────────────────────────────────────────────────────────────────
# CORE: signature → route to spec emitter
# ────────────────────────────────────────────────────────────────────────────────
[pipe.detail_pipe_spec]
type = "PipeCondition"
description = "Route by signature.type to the correct spec emitter."
inputs = { pipe_signature = "PipeSignature", concept_specs = "ConceptSpec" }
output = "Dynamic"
expression = "pipe_signature.type"

[pipe.detail_pipe_spec.pipe_map]
PipeSequence  = "detail_pipe_sequence"
PipeParallel  = "detail_pipe_parallel"
PipeCondition = "detail_pipe_condition"
PipeLLM       = "detail_pipe_llm"
PipeOcr       = "detail_pipe_ocr"
PipeImgGen    = "detail_pipe_img_gen"
PipeCompose    = "detail_pipe_jinja"
PipeFunc      = "detail_pipe_func"

# ────────────────────────────────────────────────────────────────────────────────
# EMITTERS — one per pipe type, all using the same minimal contract
# (Optionally, emitters could be extended later to read from concept_index.)
# ────────────────────────────────────────────────────────────────────────────────

[pipe.detail_pipe_sequence]
type = "PipeLLM"
description = "Build a PipeSequenceSpec from the signature (children referenced by code)."
inputs = { pipe_signature = "PipeSignature", concept_specs = "concept.ConceptSpec" }
output = "PipeSequenceSpec"
llm = "llm_to_engineer"
prompt_template = """
Return a PipeSequenceSpec for this signature.
The Pipe sequence NEEDS to have at least one step.
Orchestrate all the necessary steps to achieve the goal of the pipe.

@pipe_signature

{% if concept_specs %}
We have already defined the concepts you can use for inputs/outputs:
@concept_specs
And of course you still have the native concepts if required: Text, Image, PDF, Number, Page.
{% else %}
You can use the native concepts for inputs/outputs as required: Text, Image, PDF, Number, Page.
{% endif %}
"""

[pipe.detail_pipe_parallel]
type = "PipeLLM"
description = "Build a PipeParallelSpec from the signature."
inputs = { pipe_signature = "PipeSignature", concept_specs = "concept.ConceptSpec" }
output = "PipeParallelSpec"
llm = "llm_to_engineer"
prompt_template = """
Return a PipeParallelSpec for this signature.

@pipe_signature

{% if concept_specs %}
We have already defined the concepts you can use for inputs/outputs:
@concept_specs
And of course you still have the native concepts if required: Text, Image, PDF, Number, Page.
{% else %}
You can use the native concepts for inputs/outputs as required: Text, Image, PDF, Number, Page.
{% endif %}
"""

[pipe.detail_pipe_condition]
type = "PipeLLM"
description = "Build a PipeConditionSpec from the signature (provide expression/pipe_map consistent with children)."
inputs = { pipe_signature = "PipeSignature", concept_specs = "concept.ConceptSpec" }
output = "PipeConditionSpec"
llm = "llm_to_engineer"
prompt_template = """
Return a PipeConditionSpec for this signature.

@pipe_signature

{% if concept_specs %}
We have already defined the concepts you can use for inputs/outputs:
@concept_specs
And of course you still have the native concepts if required: Text, Image, PDF, Number, Page.
{% else %}
You can use the native concepts for inputs/outputs as required: Text, Image, PDF, Number, Page.
{% endif %}
"""

[pipe.detail_pipe_llm]
type = "PipeLLM"
description = "Build a PipeLLMSpec from the signature."
inputs = { pipe_signature = "PipeSignature", concept_specs = "concept.ConceptSpec" }
output = "PipeLLMSpec"
llm = "llm_to_engineer"
prompt_template = """
Return a PipeLLMSpec for this signature.

THe prompt is the field "prompt_template" in the PipeLLMSpec.
@pipe_signature

{% if concept_specs %}
We have already defined the concepts you can use for inputs/outputs:
@concept_specs
And of course you still have the native concepts if required: Text, Image, PDF, Number, Page.
{% else %}
You can use the native concepts for inputs/outputs as required: Text, Image, PDF, Number, Page.
{% endif %}
"""

[pipe.detail_pipe_ocr]
type = "PipeLLM"
description = "Build a PipeOcrSpec from the signature."
inputs = { pipe_signature = "PipeSignature", concept_specs = "concept.ConceptSpec" }
output = "PipeOcrSpec"
prompt_template = """
Return a PipeOcrSpec for this signature.

VERY IMPORTANT: THE INPUT OF THE PIPEOCR MUST BE either an image or a pdf or a concept which refines one of them.
@pipe_signature

{% if concept_specs %}
We have already defined the concepts you can use for inputs/outputs:
@concept_specs
And of course you still have the native concepts if required: Text, Image, PDF, Number, Page.
{% else %}
You can use the native concepts for inputs/outputs as required: Text, Image, PDF, Number, Page.
{% endif %}
"""

[pipe.detail_pipe_img_gen]
type = "PipeLLM"
description = "Build a PipeImgGenSpec from the signature."
inputs = { pipe_signature = "PipeSignature", concept_specs = "concept.ConceptSpec" }
output = "PipeImgGenSpec"
prompt_template = """
Return a PipeImgGenSpec for this signature.

The inputs for the image has to be a single input named "prompt" with a concept that is Text or refines Text.
The output concept should be a concept in PascalCase that refines Image.
For example:
```
inputs = { prompt: ImgGenPrompt }
```
if ImgGenPrompt is a text concept.

The prompt will need to be be generated by a pipe with the necessary elements.

@pipe_signature

{% if concept_specs %}
We have already defined the concepts you can use for inputs/outputs:
@concept_specs
And of course you still have the native concepts if required: Text, Image, PDF, Number, Page.
{% else %}
You can use the native concepts for inputs/outputs as required: Text, Image, PDF, Number, Page.
{% endif %}
"""

[pipe.detail_pipe_jinja]
type = "PipeLLM"
description = "Build a PipeComposeSpec from the signature."
inputs = { pipe_signature = "PipeSignature", concept_specs = "concept.ConceptSpec" }
output = "PipeComposeSpec"
prompt_template = """
Return a PipeComposeSpec for this signature.

@pipe_signature

{% if concept_specs %}
We have already defined the concepts you can use for inputs/outputs:
@concept_specs
And of course you still have the native concepts if required: Text, Image, PDF, Number, Page.
{% else %}
You can use the native concepts for inputs/outputs as required: Text, Image, PDF, Number, Page.
{% endif %}
"""

[pipe.detail_pipe_func]
type = "PipeLLM"
description = "Build a PipeFuncSpec from the signature."
inputs = { pipe_signature = "PipeSignature", concept_specs = "concept.ConceptSpec" }
output = "PipeFuncSpec"
llm = "llm_to_engineer"
prompt_template = """
Return a PipeFuncSpec for this signature.

@pipe_signature

{% if concept_specs %}
We have already defined the concepts you can use for inputs/outputs:
@concept_specs
And of course you still have the native concepts if required: Text, Image, PDF, Number, Page.
{% else %}
You can use the native concepts for inputs/outputs as required: Text, Image, PDF, Number, Page.
{% endif %}
"""

