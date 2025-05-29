import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "https://autoinsights-ai.streamlit.app/api"
# then call /analyze/, /history/, etc.


st.set_page_config(page_title="AutoInsights AI Dashboard", layout="wide")
st.title("AutoInsights AI - GenAI Data Insights Dashboard")

# --- Login Section ---
if "username" not in st.session_state:
    st.session_state["username"] = ""

with st.sidebar:
    st.subheader("🔒 Login")
    username = st.text_input("Enter your username:", st.session_state["username"])
    if username:
        st.session_state["username"] = username
        st.success(f"Logged in as: {username}")

# --- Upload & Analyze Section ---
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
user_query = st.text_input("Ask a business question (optional):", "")
df = None

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format.")

    if df is not None:
        st.write("### Data Preview")
        st.dataframe(df.head())
        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        if numeric_columns:
            selected_col = st.selectbox("Select a numeric column for Bar Chart", numeric_columns)
            if st.button("Show Bar Chart", disabled=not (df is not None and selected_col)):
                fig, ax = plt.subplots(figsize=(10, 6))
                df[selected_col].value_counts().plot(kind='bar', ax=ax)
                ax.set_title(f"Bar Chart of {selected_col}")
                st.pyplot(fig)
                st.write("**Summary Statistics:**")
                st.write(df[selected_col].describe())
        else:
            st.warning("No numeric columns found in the uploaded file.")

st.markdown("---")
st.info("Upload a CSV/Excel file, select a column, and click 'Show Bar Chart' to see the analysis.")

if st.button("Analyze & Show Bar Chart", disabled=not (df is not None and selected_col and username)):
    with st.spinner("Analyzing... please wait!"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}

        data = {"user_query": user_query}
        headers = {"X-User": st.session_state["username"]}
        response = requests.post(f"{API_URL}/analyze/", files=files, data=data, headers=headers)
        print("📡 Response Status:", response.status_code)
        print("📦 Raw Response:", response.text)

        if response.status_code == 200:
            try:
                result = response.json()
                print("✅ Parsed Result:", result)
            except requests.exceptions.JSONDecodeError:
                st.error("❌ API returned 200 OK but no valid JSON. Check API logs.")
                st.text("Raw Response:")
                st.text(response.text)
                result = None
        else:
            st.error(f"🚫 API Error {response.status_code}: {response.reason}")
            st.text("Raw Response:")
            st.text(response.text)
            result = None

            # Show latest analysis results
            st.subheader("AI-Generated Insights")
            st.write(result.get("genai_summary", "No summary found."))

            # if result.get("visualization_status") == "success" and result.get("chart_path"):
            #      chart_url = f"{API_URL}/download/{result['analysis_id']}/chart"
            #      st.image(chart_url, caption="Auto-Generated Chart")
            with st.spinner("Generating chart..."):
                fig, ax = plt.subplots(figsize=(10, 6))
                df[selected_col].value_counts().plot(kind='bar', ax=ax)
                ax.set_title(f"Bar Chart of {selected_col}")
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Count")
                st.pyplot(fig)

                st.write("**Summary Statistics:**")
                st.write(df[selected_col].describe())

            st.subheader("Exploratory Data Analysis (EDA)")
            st.json(result.get("eda_stats", {}))

            st.subheader("Downloads")
            st.markdown(
                f"[CSV]({API_URL}/download/{result['analysis_id']}/csv) &nbsp; | &nbsp; "
                f"[Excel]({API_URL}/download/{result['analysis_id']}/excel) &nbsp; | &nbsp; "
                f"[JSON Report]({API_URL}/download/{result['analysis_id']}/report) &nbsp; | &nbsp; "
                f"[PDF Report]({API_URL}/download/{result['analysis_id']}/pdf)"
            )
            if result.get("visualization_status") == "success":
                st.markdown(
                    f"[Chart (PNG)]({API_URL}/download/{result['analysis_id']}/chart)"
                )

            else:
                st.error("Error from API: " + response.text)

st.markdown("---")

# --- History Section with Search/Filter ---
st.header("🕑 Analysis History")

search_user = st.text_input("🔍 Filter by user (or leave empty for all):", value=st.session_state["username"])
with st.spinner("Fetching history..."):
    try:
        resp = requests.get(f"{API_URL}/history/")
        if resp.status_code == 200 and resp.text:
            history = resp.json()
            if history:
                history_df = pd.DataFrame(history)
                # Filter by user (case-insensitive substring match)
                if search_user:
                    filtered_df = history_df[history_df['user'].str.contains(search_user, case=False)]
                else:
                    filtered_df = history_df
                if not filtered_df.empty:
                    filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
                    st.dataframe(filtered_df[['analysis_id', 'original_file_name', 'timestamp', 'user']])
                    selected = st.selectbox(
                        "Select an analysis to view details/download:",
                        options=filtered_df["analysis_id"],
                        format_func=lambda x: f"ID {x} - {filtered_df[filtered_df['analysis_id'] == x]['original_file_name'].values[0]}"
                    )
                    if selected:
                        # Defensive get for details
                        detail_resp = requests.get(f"{API_URL}/history/{selected}")
                        if detail_resp.status_code == 200 and detail_resp.text:
                            details = detail_resp.json()
                            st.subheader("Previous AI Summary")
                            st.write(details.get("genai_summary", "No summary."))
                            st.subheader("Previous EDA")
                            st.json(details.get("eda_stats", {}))

                            if details.get("visualization_status") == "success":
                                chart_url = f"{API_URL}/download/{selected}/chart"
                                st.image(chart_url, caption="Chart for Analysis " + str(selected))

                            st.subheader("Downloads")
                            st.markdown(
                                f"[CSV]({API_URL}/download/{selected}/csv) &nbsp; | &nbsp; "
                                f"[Excel]({API_URL}/download/{selected}/excel) &nbsp; | &nbsp; "
                                f"[JSON Report]({API_URL}/download/{selected}/report) &nbsp; | &nbsp; "
                                f"[PDF Report]({API_URL}/download/{selected}/pdf)"
                            )
                            if details.get("visualization_status") == "success":
                                st.markdown(
                                    f"[Chart (PNG)]({API_URL}/download/{selected}/chart)"
                                )
                        elif detail_resp.status_code == 404:
                            st.warning("Analysis not found. Try uploading a new file and running Analyze Data.")
                        else:
                            st.error(f"API error: {detail_resp.status_code} {detail_resp.text}")
                else:
                    st.info("No analyses found for this user.")
            else:
                st.info("No analysis history yet. Run 'Analyze Data' to create one!")
        else:
            st.error(f"Could not fetch history from API. Status: {resp.status_code}")
    except Exception as e:
        st.error(f"Unexpected error fetching analysis history: {e}")
