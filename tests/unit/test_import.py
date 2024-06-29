import importlib

import pytest

# import io_schema


@pytest.mark.parametrize(
    "module_name",
    [
        "ProductBase",
        "ProductSchema",
        "ProductResponse",
    ],
)
def test_import(module_name: str):
    io_schema = importlib.import_module("io_schema")
    assert hasattr(io_schema, module_name)
