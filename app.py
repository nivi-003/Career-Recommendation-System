import streamlit as st
import pandas as pd
import plotly.express as px

st.cache_data.clear()
st.cache_resource.clear()


from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="Career Recommendation", layout="centered")

st.markdown("## 🚀 Career Recommendation System")
st.markdown("Choose your skills to discover the best-matched careers.")


# Load dataset
data = pd.read_csv("career.csv")

career_col = data.columns[0]
skill_cols = data.columns[1:]

st.subheader("Select Your Skills")

user_input = []
for skill in skill_cols:
    user_input.append(st.checkbox(skill))

user_df = pd.DataFrame([user_input], columns=skill_cols)

if st.button("🔍 Get Recommendation"):
    similarity = cosine_similarity(user_df, data[skill_cols])[0]
    data["Match %"] = similarity * 100

    top = data.sort_values("Match %", ascending=False).head(3)

    st.subheader("🎯 Top Career Matches")
    st.dataframe(top[[career_col, "Match %"]])

    # Advanced bar chart
    st.subheader("📊 Match Percentage Chart")

    fig = px.bar(
        top,
        x="Match %",
        y=career_col,
        orientation="h",
        color="Match %",
        color_continuous_scale="viridis",
        text=top["Match %"].round(2)
    )

    fig.update_layout(
        xaxis_title="Match Percentage",
        yaxis_title="Career",
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

