import os

import pytest

from pipelex import log
from pipelex.client.protocol import StuffContentOrData
from pipelex.core.concepts.concept_blueprint import ConceptBlueprint
from pipelex.core.concepts.concept_factory import ConceptFactory
from pipelex.core.stuffs.structured_content import StructuredContent
from pipelex.core.stuffs.stuff import Stuff
from pipelex.core.stuffs.stuff_factory import StuffFactory
from pipelex.hub import get_concept_library
from pipelex.system.registries.class_registry_utils import ClassRegistryUtils
from tests.unit.core.stuffs.data import TestData


@pytest.fixture(scope="class")
def setup_test_concept():
    # Register the class in the class registry
    ClassRegistryUtils.register_classes_in_file(
        file_path=os.path.join(os.path.dirname(__file__), "test_stuff_factory_implicit_memory.py"),
        base_class=StructuredContent,
        is_include_imported=False,
    )

    # Create and register the test concept
    concept_library = get_concept_library()

    # Create the concept
    concept = ConceptFactory.make(
        concept_code="MyConcept",
        domain="test_domain",
        description="Test concept for unit tests",
        structure_class_name="MyConcept",
    )
    # Register it in the library
    concept_library.add_new_concept(concept=concept)

    # Create a concept that is not native.Text but initiable by str
    concept_not_native_text = ConceptFactory.make_from_blueprint(
        domain="test_domain",
        concept_code="MyConceptNotNativeText",
        blueprint=ConceptBlueprint(
            description="Test concept for unit tests",
        ),
    )
    concept_library.add_new_concept(concept=concept_not_native_text)

    yield concept

    # Cleanup after test
    concept_library.remove_concepts_by_codes(concept_codes=["MyConcept", "MyConceptNotNativeText"])


class TestStuffFactoryImplicitMemory:
    """Test Case 1: Direct content without 'concept' key.

    This covers cases where stuff_content_or_data is directly:
    - A string (1.1)
    - A list of strings (1.2)
    - A StuffContent object (1.3)
    - A list of StuffContent objects (1.4)
    """

    @pytest.mark.parametrize(
        ("test_name", "stuff_content_or_data", "stuff_name", "stuff_code", "expected_stuff"),
        TestData.CASE,
    )
    def test_case(
        self,
        test_name: str,
        stuff_content_or_data: StuffContentOrData,
        stuff_name: str,
        stuff_code: str,
        expected_stuff: Stuff,
    ):
        log.info(f"Test Case 1: Direct content without concept key. {test_name}")
        log.debug(f"setup_test_concept: {setup_test_concept}")
        result = StuffFactory.make_stuff_from_stuff_content_or_data(
            name=stuff_name,
            code=stuff_code,
            stuff_content_or_data=stuff_content_or_data,
        )
        assert result == expected_stuff


# class TestStuffFactoryImplicitMemoryEdgeCases:
#     """Test edge cases and error conditions."""

#     def test_empty_list_raises_error(self):
#         """Test that empty list raises appropriate error."""
#         with pytest.raises(Exception) as exc_info:
#             StuffFactory.make_stuff_from_stuff_content_using_search_domains(
#                 name="test_stuff",
#                 stuff_content_or_data=[],
#                 search_domains=["test_domain"],
#             )
#         assert "no items" in str(exc_info.value).lower()

#     def test_dict_without_concept_raises_error(self):
#         """Test that dict without concept key raises appropriate error."""
#         with pytest.raises(Exception) as exc_info:
#             StuffFactory.make_stuff_from_stuff_content_using_search_domains(
#                 name="test_stuff",
#                 stuff_content_or_data={"content": "some content"},
#                 search_domains=["test_domain"],
#             )
#         assert "concept" in str(exc_info.value).lower()

#     def test_dict_without_content_raises_error(self):
#         """Test that dict without content key raises appropriate error."""
#         with pytest.raises(Exception) as exc_info:
#             StuffFactory.make_stuff_from_stuff_content_using_search_domains(
#                 name="test_stuff",
#                 stuff_content_or_data={"concept": "Text"},
#                 search_domains=["test_domain"],
#             )
#         assert "content" in str(exc_info.value).lower()

#     def test_concept_not_found_raises_error(self, setup_test_concept):
#         """Test that non-existent concept raises appropriate error."""
#         with pytest.raises(Exception) as exc_info:
#             StuffFactory.make_stuff_from_stuff_content_using_search_domains(
#                 name="test_stuff",
#                 stuff_content_or_data={
#                     "concept": "NonExistentConcept",
#                     "content": {"some": "data"},
#                 },
#                 search_domains=["test_domain"],
#             )
#         # Should raise error about concept not found

#     def test_list_with_mixed_types_raises_error(self, setup_test_concept):
#         """Test that list with mixed StuffContent types raises error."""
#         # This should ideally raise an error or at least log a warning
#         # The current implementation might not catch this, but it should
#         with pytest.raises(Exception):
#             StuffFactory.make_stuff_from_stuff_content_using_search_domains(
#                 name="test_stuff",
#                 stuff_content_or_data=[
#                     MyConcept(arg1="arg1", arg2=1, arg3=MySubClass(arg4="arg4")),
#                     TextContent(text="different type"),  # Different type!
#                 ],
#                 search_domains=["test_domain"],
#             )
