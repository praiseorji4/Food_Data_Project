import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt


@st.cache_data
def load_data():
    df = pd.read_csv("Project_data/Main.csv")
    df2 = pd.read_csv('Project_data/post_2010.csv')

    # Dropping unnamed columns from csvs
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df2.drop('Unnamed: 0', axis=1, inplace=True)
    return df, df2


st.set_page_config(
    page_title="Produce Price Trends App",
    page_icon="🥦",
    layout="wide",
)
# Title & Introduction
st.title("Produce Price Trends Analysis")
st.markdown("Explore and analyze price trends for various produce items across different countries and market types.")

# Sidebar Navigation
analysis_options = ["Data Preview", "Price Trends by Produce", "Comparison by Market Type", "Comparison by Country"]
choice = st.sidebar.selectbox("Choose Analysis Type", analysis_options)

df1, df2 = load_data()
# Data Exploration
if choice == "Data Preview":
    st.write(df1.sample(100))  # Display the first 100 rows

# Trends Analysis by Produce
elif choice == "Price Trends by Produce":
    produce_list = df2['produce'].unique().tolist()
    selected_produce = st.multiselect("Select Produce", produce_list, default=["Maize "])

    # Code to visualize price trends for the selected produce
    average_prices_comparison = df2[df2['produce'].isin(selected_produce)]
    average_prices_comparison = average_prices_comparison.groupby(['year', 'produce'])['price in Euro'].mean().reset_index()

    # Visualization
    num_of_columns = len(selected_produce)
    columns = st.columns(num_of_columns)
    for idx, produce in enumerate(selected_produce):
        with columns[idx]:
            plt.figure(figsize=(8, 6))
            subset = average_prices_comparison[average_prices_comparison['produce'] == produce]
            plt.plot(subset['year'], subset['price in Euro'], marker='o', label=produce)
            plt.xlabel('Date')
            plt.ylabel('Average Price')
            plt.title(f'Price Trend Over Time - {produce}')
            st.pyplot(plt)

# Comparison by Market Type
elif choice == "Comparison by Market Type":
    market_types = df2['market_type'].unique().tolist()
    produce_list = df2['produce'].unique().tolist()
    years = df1['year'].unique().tolist()

    selected_market_type = st.multiselect("Choose Market Type", market_types, default=market_types[0])
    selected_produce = st.selectbox("Select Produce", produce_list)

    # Code to visualize comparisons for the selected market type
    apc = df2[df2['market_type'].isin(selected_market_type)]
    apc = apc[apc['produce'] == selected_produce]
    apc = apc.groupby(['market_type', 'produce', 'year'])['price in Euro'].mean().reset_index()

    # Visualization
    num_of_columns = len(selected_market_type)
    columns = st.columns(num_of_columns)
    for idx, mt in enumerate(selected_market_type):
        with columns[idx]:
            plt.figure(figsize=(8, 6))
            subset = apc[apc['market_type'] == mt]
            plt.plot(subset['year'], subset['price in Euro'], marker='o', label=mt)
            plt.ylim(apc['price in Euro'].min(), apc['price in Euro'].max())
            plt.xlabel('Date')
            plt.ylabel('Average Price')
            plt.title(f'Price Trend Over Time for {selected_produce}- {mt}')
            st.pyplot(plt)

# Comparison by Country
elif choice == "Comparison by Country":
    produce_list = df2['produce'].unique().tolist()
    selected_produce = st.selectbox("Select Produce", produce_list)

    # Code to visualize comparisons for the selected countries
    apc = df2[df2['produce'] == selected_produce]
    countries = apc['country'].unique().tolist()
    selected_country = st.multiselect("Choose Country", countries)

    apc = apc[apc['country'].isin(countries)]
    apc = apc.groupby(['country', 'produce', 'year'])['price in Euro'].mean().reset_index()

    # Visualization
    num_of_columns = len(selected_country)
    columns = st.columns(num_of_columns)
    for idx, con in enumerate(selected_country):
        with columns[idx]:
            plt.figure(figsize=(8, 6))
            subset = apc[apc['country'] == con]
            plt.plot(subset['year'], subset['price in Euro'], marker='o', label=con)
            # plt.ylim(0, apc['price in Euro'].max())
            plt.xlabel('Date')
            plt.ylabel('Average Price')
            plt.title(f'Price Trend Over Time in {con}for {selected_produce}')
            st.pyplot(plt)

# st.title("African Food Market Data App")
#
# st.subheader("Your personal companion in analyzing food data")
#
# st.write("Basic Structure of our food data")
# df1, df2 = load_data()
# st.write(df1.sample(10))
# articles = df.article.unique()
# articles_selection = st.multiselect("Choose Product", [article for article in articles])
# articles_selected = df[df['article'].isin(articles_selection)]
# st.write(articles_selected.head())
# plotting

# line chart
# st.write("""### Sales over Time """)
# fig, ax = plt.subplots(figsize=(10,6))
# ax.plot(articles_selected['datetime']
#
