import streamlit as st
import pandas as pd
from DataAnalysis import loadData, create_bar_graph, create_line_graph, create_pie_chart

# User interface
def app():
    st.title("Programming Languages Usage Over Time")
    
    # Load data
    data = loadData()
    
    # Select graph type
    graph_type = st.selectbox("Select Graph Type:", ["Bar Graph", "Line Graph", "Pie Chart"])
    
    # Get inputs based on selected graph type
    if graph_type in ["Bar Graph", "Pie Chart"]:
        year_input = st.selectbox("Select Year:", [""] + sorted(data['Date'].dt.year.unique().astype(str)))
        month_input = st.selectbox("Select Month:", [""] + list(data['Date'].dt.strftime('%B').unique()))
    elif graph_type == "Line Graph":
        language_input = st.selectbox("Select Language:", [""] + list(data['Language'].unique()))
    
    # Create graph based on selected options
    if st.button("Generate Graph"):
        if graph_type in ["Bar Graph", "Pie Chart"]:
            if year_input != "" and month_input != "":
                full_date = pd.to_datetime(f"{year_input}-{month_input}-01")
                if graph_type == "Bar Graph":
                    create_bar_graph(full_date, data)
                else:
                    create_pie_chart(full_date, data)
        elif graph_type == "Line Graph":
            if language_input != "":
                create_line_graph(language_input, data)

# Run the application
if __name__ == '__main__':
    app()
