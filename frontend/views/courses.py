import streamlit as st
from PIL import Image
from tools.st_functions import st_button
import requests
from config import Settings

class Courses:

    class Model:
        pageTitle = "Courses"

    def __init__(self):
        self.COURSES_URL = "https://x8ki-letl-twmt.n7.xano.io/api:VB5qx6PF/courses"
        self.HEADERS = {'accept': 'application/json'}

    def fetch_courses(self):
        response = requests.get(self.COURSES_URL, headers=self.HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch courses.")
            return []

    def course_grid(self, courses):
        # CSS for the course grid
        st.markdown("""
            <style>
                .course-card {
                    border: 1px solid #e6e6e6;
                    border-radius: 5px;
                    padding: 20px;
                    margin: 10px;
                    text-align: center;
                    transition: transform .2s;
                }
                .course-card:hover {
                    transform: scale(1.05);
                    cursor: pointer;
                }
            </style>
        """, unsafe_allow_html=True)

        # Display courses in a grid
        cols = st.columns(2)  # Adjust the number for more or fewer columns
        for i, course in enumerate(courses):
            with cols[i % 2]:  # Alternate courses between columns
                st.markdown(f"""
                    <div class="course-card" onclick="window.location.href = '/course/{course['id']}';">
                        <h3>{course['course_name']}</h3>
                    </div>
                """, unsafe_allow_html=True)

    def view(self, model):
        st.title(model.pageTitle)
        courses = self.fetch_courses()
        self.course_grid(courses)

# Usage
# model = Courses.Model()
# courses_view = Courses()
# courses_view.view(model)
