import duckdb
import streamlit as st
import pandas as pd

dwh = duckdb.connect("/data/transformed/dwh.duckdb", read_only=True)

def get_tables():
    tables = dwh.execute("SHOW TABLES;").df()
    return tables.name.to_list()

with st.sidebar.container():
    st.title("Available Tables")
with st.sidebar.container():
    available_tables = st.selectbox(
        'List of Avaible Tables in the Data Warehouse',
        get_tables(),
    )
    st.write('Showing table "', available_tables, '"')
    selected_df = dwh.query(f"SELECT * FROM {available_tables}").df()
    selected_df_schema = pd.DataFrame(selected_df.dtypes, columns=['Data Type'])
    selected_df_schema.index.name = "Field Name"
    schema, preview = st.tabs(["Shema", "Preview"])
    with schema:
        st.dataframe(selected_df_schema)
    with preview:
        st.dataframe(selected_df.head(20))

query = st.text_input('Query the Data Warehouse', placeholder='Ex: select * from raw_orders')
if query != '':
    try:
        tmp_df = dwh.query(query).df()
        st.dataframe(tmp_df)
    except RuntimeError as e:
        error_message = str(e)
        if "Catalog Error" in error_message:
            st.write("A Catalog Error occurred:")
        elif "Syntax Error" in error_message:
            st.write("A Syntax Error occurred:")
        elif "Constraint Error" in error_message:
            st.write("A Constraint Error occurred:")
        else:
            st.write("A different DuckDBError occurred:")
    except Exception as e:
        st.write("An unexpected error occurred:", e)
else:
    st.write("")