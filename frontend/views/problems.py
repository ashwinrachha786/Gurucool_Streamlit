import streamlit as st
import requests
from config import Settings
from tools.utilities import PINLEFT, PRECISION_TWO, draw_grid, load_html2
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, JsCode
import pandas as pd

settings = Settings()

class Problems:

    def __init__(_self):
        _self.DEFAULT_URL = settings.BACKEND_URLS["leetcode"]
        _self.LCDB_ALL_URL = "https://x8ki-letl-twmt.n7.xano.io/api:m3qoN9RM/lcdb"
        _self.LCDB_SINGLE_URL = _self.LCDB_ALL_URL + "/{lcdb_id}"
        _self.HEADERS = {'accept': 'application/json'}

    @st.cache_data()
    def fetch_all_problems(_self):
        response = requests.get(_self.LCDB_ALL_URL, headers=_self.HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch problems. Status code: {response.status_code}")
            return []

    @st.cache_data()
    def fetch_problem_details(_self, lcdb_id):
        response = requests.get(_self.LCDB_SINGLE_URL.format(lcdb_id=lcdb_id), headers=_self.HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch problem details for ID {lcdb_id}. Status code: {response.status_code}")
            return None

    def display_problems_table(_self, problems):
        # Create a dictionary to store checkbox states for each problem
        checkbox_states = {}
        selected_problem_id = None

        for problem in problems:
            checkbox_states[problem["id"]] = st.checkbox(f"ID: {problem['id']} - {problem['Title']}", key=f"checkbox_{problem['id']}")

            # If the checkbox for a problem is clicked, display its details
            if checkbox_states[problem["id"]]:
                selected_problem_id = problem["id"]
                problem_detail = _self.fetch_problem_details(selected_problem_id)
                #_self.display_problem_details(problem_detail)
                break  # Only display details for the first selected problem

        return selected_problem_id


    def display_problem_details(_self, problem_detail):
        st.title(problem_detail["Title"])
        #st.write("Problem Description:", problem_detail["Problem_Description"])
        st.write("Difficulty:", problem_detail["Difficulty"])
        st.write("Acceptance:", problem_detail["Acceptance"])
        # ... Display other details as needed

    def view(_self):
        problems = _self.fetch_all_problems()
        selected_problem_id = _self.display_problems_table(problems)

        if selected_problem_id:
            problem_detail = _self.fetch_problem_details(selected_problem_id)
            problem_description = problem_detail["Problem_Description"]
            load_html2(problem_description)
            _self.display_problem_details(problem_detail)
