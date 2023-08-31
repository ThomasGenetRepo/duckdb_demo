import os
import duckdb
import pandas as pd
from dagster import asset, Definitions, SourceAsset
from dagster_duckdb import DuckDBResource

from sql_queries import (
    import_customers,
    import_orders,
    import_product,
    spending_by_customer,
    customer_segmentation,
    inventory_level,
    customer_lifetime_value,
    product_review,
    frequent_customer
)

@asset
def load_data(duckdb: DuckDBResource) -> None:
    with duckdb.get_connection() as conn:
        conn.execute(import_customers)
        conn.execute(import_orders)
        conn.execute(import_product)

@asset(deps=[load_data])
def clean_data(duckdb: DuckDBResource):
    return

@asset(deps=[clean_data])
def transform_data(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.execute(spending_by_customer)
        conn.execute(customer_segmentation)
        conn.execute(inventory_level)
        conn.execute(customer_lifetime_value)
        conn.execute(product_review)
        conn.execute(frequent_customer)
    return 

defs = Definitions(
    assets=[load_data, clean_data, transform_data],
    resources={
        "duckdb": DuckDBResource(
            database="/data/transformed/dwh.duckdb",
        )
    },
)