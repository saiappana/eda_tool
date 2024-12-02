import streamlit as st
import pandas as pd

# Initialize session state variables if they don't exist
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'selected_rows' not in st.session_state:
    st.session_state.selected_rows = None
if 'selection_method' not in st.session_state:
    st.session_state.selection_method = "Select range"
if 'start_row' not in st.session_state:
    st.session_state.start_row = 0
if 'end_row' not in st.session_state:
    st.session_state.end_row = 99
if 'sample_size' not in st.session_state:
    st.session_state.sample_size = 100

# Callback functions to update session state
def update_start_row():
    st.session_state.selected_rows = st.session_state.uploaded_data.iloc[
        st.session_state.start_row:st.session_state.end_row + 1
    ]

def update_end_row():
    st.session_state.selected_rows = st.session_state.uploaded_data.iloc[
        st.session_state.start_row:st.session_state.end_row + 1
    ]

def update_sample_size():
    st.session_state.selected_rows = st.session_state.uploaded_data.sample(
        n=st.session_state.sample_size, 
        random_state=42
    )

def update_selection_method():
    # Reset selected rows when changing method
    if st.session_state.selection_method == "Select range":
        st.session_state.selected_rows = st.session_state.uploaded_data.iloc[
            st.session_state.start_row:st.session_state.end_row + 1
        ]
    elif st.session_state.selection_method == "Random sample":
        st.session_state.selected_rows = st.session_state.uploaded_data.sample(
            n=st.session_state.sample_size, 
            random_state=42
        )

st.title("Upload Your Dataset")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the data if it's a new file
    if st.session_state.uploaded_data is None:
        df = pd.read_csv(uploaded_file)
        st.session_state.uploaded_data = df
        st.session_state.selected_rows = df.iloc[st.session_state.start_row:st.session_state.end_row + 1]
    
    st.write("### Preview of uploaded data:")
    st.dataframe(st.session_state.uploaded_data.head())
    
    st.write("### Select rows for analysis:")
    
    # Allow multiple ways to select rows
    st.radio(
        "Choose how to select rows:",
        ["Select range", "Random sample"],
        key="selection_method",
        on_change=update_selection_method
    )
    
    if st.session_state.selection_method == "Select range":
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Start row (inclusive)",
                min_value=0,
                max_value=len(st.session_state.uploaded_data)-1,
                value=st.session_state.start_row,
                step=1,
                key="start_row",
                on_change=update_start_row
            )
        with col2:
            st.number_input(
                "End row (inclusive)",
                min_value=st.session_state.start_row,
                max_value=len(st.session_state.uploaded_data)-1,
                value=st.session_state.end_row,
                step=1,
                key="end_row",
                on_change=update_end_row
            )
        
    elif st.session_state.selection_method == "Random sample":
        st.number_input(
            "Enter number of rows to sample",
            min_value=1,
            max_value=len(st.session_state.uploaded_data),
            value=st.session_state.sample_size,
            step=1,
            key="sample_size",
            on_change=update_sample_size
        )
    
    # Show info about selected range
    if st.session_state.selected_rows is not None:
        st.write("### Selected data preview:")
        st.dataframe(st.session_state.selected_rows.head())
        st.write(f"Total selected rows: {len(st.session_state.selected_rows)}")
        
        if st.session_state.selection_method == "Select range":
            st.write(f"Selected rows {st.session_state.start_row} to {st.session_state.end_row} (inclusive)")