import streamlit as st
import pandas as pd
import requests
import json
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode
#settings = Settings()

def load_css():
    with open("tools/style.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    st.markdown(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
        unsafe_allow_html=True)
    
def load_html():
    with open("./static/index.html") as f:
        html_content = f.read()
    st.components.v1.html(html_content, width=1100, height=1000)

def load_html2(problem_description):
    with open("./static/index2.html") as f:
        html_content = f.read()
        # Replace the placeholder with the actual problem description
        html_content = html_content.replace("#$#Example Code", problem_description)
    st.components.v1.html(html_content, width=1100, height=1000)

def get_problems_df():
    url = "https://x8ki-letl-twmt.n7.xano.io/api:m3qoN9RM/lcdb"
    response = requests.get(url)
    data = response.json()
    df = pd.read_json(data, orient = "records")
    print(df.head())



MAX_TABLE_HEIGHT = 500


def get_numeric_style_with_precision(precision: int) -> dict:
    return {"type": ["numericColumn", "customNumericFormat"], "precision": precision}


PRECISION_ZERO = get_numeric_style_with_precision(0)
PRECISION_ONE = get_numeric_style_with_precision(1)
PRECISION_TWO = get_numeric_style_with_precision(2)
PINLEFT = {"pinned": "left"}


def draw_grid(
        df,
        formatter: dict = None,
        selection="multiple",
        use_checkbox=False,
        fit_columns=False,
        theme="streamlit",
        max_height: int = MAX_TABLE_HEIGHT,
        wrap_text: bool = False,
        auto_height: bool = False,
        grid_options: dict = None,
        key=None,
        css: dict = None
):

    gb = GridOptionsBuilder()
    gb.configure_default_column(
        filterable=True,
        groupable=False,
        editable=False,
        wrapText=wrap_text,
        autoHeight=auto_height
    )

    if grid_options is not None:
        gb.configure_grid_options(**grid_options)

    for latin_name, (cyr_name, style_dict) in formatter.items():
        gb.configure_column(latin_name, header_name=cyr_name, **style_dict)

    gb.configure_selection(selection_mode=selection, use_checkbox=use_checkbox)

    return AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=fit_columns,
        height=min(max_height, (1 + len(df.index)) * 29),
        theme=theme,
        key=key,
        custom_css=css
    )


def highlight(color, condition):
    code = f"""
        function(params) {{
            color = "{color}";
            if ({condition}) {{
                return {{
                    'backgroundColor': color
                }}
            }}
        }};
    """
    return JsCode(code)