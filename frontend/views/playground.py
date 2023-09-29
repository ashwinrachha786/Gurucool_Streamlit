import streamlit as st
import streamlit.components.v1 as components
from tools.utilities import load_html
react_component = """
    import React from "react";
    function MyComponent() {
        return(
            <div>
                <h1>Hello from React!</h1>
            </div>
        )
    }
"""

class Playground:
    class Model:
        pageTitle = "playground"

    def view(self, model):
        load_html()