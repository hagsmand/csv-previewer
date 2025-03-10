import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Upload CSV Files
st.sidebar.header("Upload Files")
uploaded_file = st.sidebar.file_uploader("Upload Primary CSV file", type=["csv"], key="primary_file")

# Add second file uploader
uploaded_file2 = st.sidebar.file_uploader("Upload Secondary CSV file (for comparison)", type=["csv"], key="secondary_file")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Show basic stats
    st.subheader("Dataset Preview")
    st.write(df.head())

    # Show row count and metadata
    st.subheader("📑 Dataset Information")
    
    # Display row count
    st.metric("Total Rows", df.shape[0])
    
    # Display column information in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Column Types")
        dtypes_df = pd.DataFrame(df.dtypes, columns=["Data Type"])
        dtypes_df.index.name = "Column"
        st.dataframe(dtypes_df.reset_index())
    
    with col2:
        st.subheader("Missing Values")
        missing_df = pd.DataFrame(df.isnull().sum(), columns=["Missing Values"])
        missing_df.index.name = "Column"
        missing_df["Percentage"] = (missing_df["Missing Values"] / len(df) * 100).round(2)
        missing_df["Percentage"] = missing_df["Percentage"].astype(str) + "%"
        st.dataframe(missing_df.reset_index())
    
    # Display summary statistics
    st.subheader("📊 Summary Statistics")
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    
    if numeric_columns:
        st.dataframe(df[numeric_columns].describe())
    else:
        st.warning("No numeric columns found for statistics.")
        
    # Add single column duplicate analysis
    st.subheader("🔍 Single Column Duplicate Analysis")
    selected_column = st.selectbox("Select column to analyze duplicates", df.columns)
    
    # Calculate duplicates
    duplicate_counts = df[selected_column].value_counts()
    duplicates = duplicate_counts[duplicate_counts > 1]
    
    if not duplicates.empty:
        st.write(f"Found {len(duplicates)} values that appear multiple times:")
        
        # Create a DataFrame showing duplicate values and their counts
        duplicate_df = pd.DataFrame({
            'Value': duplicates.index,
            'Count': duplicates.values
        })
        st.dataframe(duplicate_df)
        
        # Show total number of duplicate rows
        total_duplicates = sum(duplicates.values) - len(duplicates)
        st.metric("Total Duplicate Rows", total_duplicates)
    else:
        st.success("No duplicate values found in this column!")
    
    # File comparison section
    if uploaded_file2:
        st.subheader("📊 File Comparison")
        df2 = pd.read_csv(uploaded_file2)
        
        st.write(f"Secondary file: {uploaded_file2.name} ({df2.shape[0]} rows, {df2.shape[1]} columns)")
        
        # Get columns from both dataframes
        df1_columns = df.columns.tolist()
        df2_columns = df2.columns.tolist()
        
        # Select columns to compare
        col1, col2 = st.columns(2)
        compare_col1 = col1.selectbox("Select column from primary file", df1_columns)
        compare_col2 = col2.selectbox("Select column from secondary file", df2_columns)
        
        if st.button("Compare Files"):
            # Find duplicates
            st.subheader("Duplicate Analysis")
            
            # Values in both files
            common_values = set(df[compare_col1].dropna()) & set(df2[compare_col2].dropna())
            st.metric("Common Values", len(common_values))
            
            # Values only in first file
            only_in_first = set(df[compare_col1].dropna()) - set(df2[compare_col2].dropna())
            st.metric("Values only in primary file", len(only_in_first))
            
            # Values only in second file
            only_in_second = set(df2[compare_col2].dropna()) - set(df[compare_col1].dropna())
            st.metric("Values only in secondary file", len(only_in_second))
            
            # Show sample of values
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("Sample common values")
                st.write(list(common_values)[:10] if common_values else "None")
            
            with col2:
                st.write("Sample values only in primary")
                st.write(list(only_in_first)[:10] if only_in_first else "None")
            
            with col3:
                st.write("Sample values only in secondary")
                st.write(list(only_in_second)[:10] if only_in_second else "None")
else:
    st.info("Upload a CSV file to get started!")

