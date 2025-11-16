import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Titanic Analysis", page_icon="🚢", layout="wide")
st.title("🚢 Titanic Dataset Analysis")

uploaded_file = st.file_uploader("Upload your Titanic file", type=['csv', 'xls', 'xlsx'])

if uploaded_file:
    # Read file based on extension
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.header("📊 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Passengers", len(df))
    col2.metric("Survived", int(df['Survived'].sum()) if 'Survived' in df.columns else 0)
    col3.metric("Did Not Survive", int(len(df) - df['Survived'].sum()) if 'Survived' in df.columns else 0)
    col4.metric("Features", len(df.columns))
    
    with st.expander("View Raw Data"):
        st.dataframe(df)
    
    with st.expander("ℹ️ Data Information"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Data Types")
            st.write(df.dtypes)
        with col2:
            st.subheader("Missing Values")
            st.write(df.isnull().sum())
    
    st.header("📈 Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["Survival", "Demographics", "Class Analysis"])
    
    with tab1:
        if 'Survived' in df.columns:
            col1, col2 = st.columns(2)
            with col1:
                survival_counts = df['Survived'].value_counts()
                fig = px.pie(values=survival_counts.values, 
                            names=['Did Not Survive', 'Survived'],
                            title='Survival Rate',
                            color_discrete_sequence=['#FF6B6B', '#4ECDC4'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'Sex' in df.columns:
                    survival_gender = df.groupby(['Sex', 'Survived']).size().unstack()
                    fig = px.bar(survival_gender, 
                                title='Survival by Gender', 
                                barmode='group',
                                color_discrete_sequence=['#FF6B6B', '#4ECDC4'])
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            if 'Age' in df.columns:
                fig = px.histogram(df, x='Age', title='Age Distribution', nbins=30,
                                 color_discrete_sequence=['#95E1D3'])
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            if 'Sex' in df.columns:
                gender_counts = df['Sex'].value_counts()
                fig = px.bar(x=gender_counts.index, y=gender_counts.values, 
                           title='Gender Distribution',
                           color_discrete_sequence=['#F38181'])
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            if 'Pclass' in df.columns and 'Survived' in df.columns:
                class_survival = df.groupby('Pclass')['Survived'].mean() * 100
                fig = px.bar(x=class_survival.index, y=class_survival.values, 
                           title='Survival Rate by Class (%)',
                           labels={'x': 'Passenger Class', 'y': 'Survival Rate (%)'},
                           color_discrete_sequence=['#AA96DA'])
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            if 'Fare' in df.columns:
                fig = px.box(df, y='Fare', title='Fare Distribution',
                           color_discrete_sequence=['#FCBAD3'])
                st.plotly_chart(fig, use_container_width=True)
    
    if 'Age' in df.columns and 'Survived' in df.columns:
        st.subheader("Age vs Survival")
        fig = px.histogram(df, x='Age', color='Survived',
                         title='Age Distribution by Survival Status',
                         labels={'Survived': 'Status'},
                         barmode='overlay',
                         nbins=30,
                         color_discrete_map={0: '#FF6B6B', 1: '#4ECDC4'})
        fig.update_traces(opacity=0.7)
        st.plotly_chart(fig, use_container_width=True)
    
    st.header("📉 Statistical Summary")
    st.dataframe(df.describe())
else:
    st.info("👆 Please upload a CSV or Excel file to begin")
    st.markdown("""
    ### Supported file formats:
    - CSV (.csv)
    - Excel (.xls, .xlsx)
    """)