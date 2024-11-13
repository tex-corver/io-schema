import random
from collections import defaultdict

import utils
from io_schema import image as image_schemas, product as product_schemas


def make_image(**kwargs) -> image_schemas.Image:
    id = kwargs.get("id", utils.generate_random_string())
    path = kwargs.get("path", utils.generate_random_string())
    order = kwargs.get("order", random.randint(0, 100))
    return image_schemas.Image(
        id=id,
        path=path,
        order=order,
    )


def make_product_line_option(**kwargs) -> product_schemas.ProductLineOption:
    id = kwargs.get("id", utils.generate_random_string())
    name = kwargs.get("name", utils.generate_random_string())
    kind = kwargs.get("kind", utils.generate_random_string())
    description = kwargs.get("description", utils.generate_random_string())
    price = kwargs.get("price", random.randint(1, 100000))
    images = kwargs.get("images", [make_image() for _ in range(random.randint(0, 10))])
    return product_schemas.ProductLineOption(
        id=id,
        name=name,
        kind=kind,
        description=description,
        price=price,
        images=images,
    )


def make_product_line(**kwargs) -> product_schemas.ProductLine:
    id = kwargs.get("id", utils.generate_random_string())
    name = kwargs.get("name", utils.generate_random_string())
    description = kwargs.get("description", utils.generate_random_string())
    price = kwargs.get("price", random.randint(1, 100000))
    images = kwargs.get("images", [make_image() for _ in range(random.randint(0, 10))])
    options = [make_product_line_option() for _ in range(random.randint(2, 10))]
    options[-1].kind = options[-2].kind
    grouped_options = defaultdict(list)
    for option in options:
        grouped_options[option.kind].append(option)
    return product_schemas.ProductLine(
        id=id,
        name=name,
        description=description,
        price=price,
        images=images,
        options=grouped_options,
    )


def make_product(
    product_line: product_schemas.ProductLine | None = None,
    options: dict[str, product_schemas.ProductLineOption] | None = None,
) -> product_schemas.Product:
    product_line: product_schemas.ProductLine = product_line or make_product_line()
    options: dict[str, product_schemas.ProductLineOption] = options or {
        kind: product_line.options[kind][0] for kind in product_line.options
    }
    return product_schemas.Product.from_product_line_and_options(
        product_line=product_line,
        options=options,
    )
