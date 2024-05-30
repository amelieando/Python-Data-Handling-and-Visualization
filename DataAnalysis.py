import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go

# disable the warning for Streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to load the data from CSV
def loadData():
    data = pd.read_csv("/Users/amelieando/Desktop/Popularity of Programming Languages from 2004 to 2023.csv")
    
    # Convert date assuming it's the first day of the month
    data['Date'] = pd.to_datetime(data['Date'] + ' 01', format="%B %Y %d")
    
    # formating the data for easier plotting
    data = data.melt(id_vars=['Date'], var_name='Language', value_name='Popularity')
    return data

# User interface app for streamlit
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
        
        if st.button("Generate Graph"):
            if year_input != "" and month_input != "":
                if graph_type == "Bar Graph":
                    create_bar_graph(year_input, month_input, data)
                else:
                    create_pie_chart(year_input, month_input, data)
    elif graph_type == "Line Graph":
        language_input = st.selectbox("Select Language:", [""] + list(data['Language'].unique()))
        
        if st.button("Generate Graph"):
            if language_input != "":
                create_line_graph(language_input, data)

# Function to create a bar graph for a specific month
def create_bar_graph(year_input, month_input, data):
    target_date = pd.to_datetime(f"{year_input}-{month_input}-01")
    subset_data = data[data['Date'] == target_date]
    
    fig, ax = plt.subplots(figsize=(16, 9))
    sns.barplot(data=subset_data, x='Language', y='Popularity', hue='Language', ax=ax)
    ax.set_title(f"Popularity of Programming Languages in {target_date.strftime('%B %Y')}")
    ax.set_xlabel('Language')
    ax.set_ylabel('Popularity (%)')
    ax.tick_params(axis='x', rotation=45)
    
    # Display the plot using st.pyplot()
    st.pyplot(fig)

# Function to create a line graph for a specific language
def create_line_graph(language_input, data):
    subset_data = data[data['Language'] == language_input]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=subset_data, x='Date', y='Popularity', hue='Language', ax=ax)
    ax.set_title(f"Trend of {language_input} Over Time")
    ax.set_xlabel('Date')
    ax.set_ylabel('Popularity (%)')
    ax.tick_params(axis='x', rotation=45)
    
    # Display the plot using st.pyplot()
    st.pyplot(fig)

# Function to create a pie chart for a specific month
def create_pie_chart(year_input, month_input, data):
    target_date = pd.to_datetime(f"{year_input}-{month_input}-01")
    subset_data = data[data['Date'] == target_date]
    
    # Create a Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=subset_data['Language'], values=subset_data['Popularity'], hole=0.3)])
    fig.update_layout(title=f"Distribution of Programming Languages in {target_date.strftime('%B %Y')}",
                      margin=dict(l=20, r=20, t=50, b=20))  # Adjust margin for better layout
    
    # Display the plot using st.plotly_chart()
    st.plotly_chart(fig)

# Run the application
if __name__ == '__main__':
    app()
