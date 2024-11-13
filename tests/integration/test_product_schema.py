import io_schema
import io_schema.test
import pytest
from icecream import ic


@pytest.fixture
def product_line() -> io_schema.ProductLine:
    return io_schema.test.make_product_line()


@pytest.fixture
def options(
    product_line: io_schema.ProductLine,
) -> dict[str, dict[str, io_schema.ProductLineOption]]:
    return {kind: product_line.options[kind][0] for kind in product_line.options}


# TODO: Add tests
def test_product_line_schema(
    product_line: io_schema.ProductLine,
    options: dict[str, io_schema.ProductLineOption],
):
    product = io_schema.test.make_product(
        product_line,
        options,
    )
    ic(product)
    assert product.product_line == product_line
    assert product.options == options
