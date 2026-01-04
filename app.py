import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components


st.cache_data.clear()
st.cache_resource.clear()



from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config( 
    page_title="Career Recommendation",
    layout="centered"
)


st.markdown("""
<style>
/* Background with soft animated gradient */
.stApp {
    background: linear-gradient(135deg, #c8e6c9, #a5d6a7, #e8f5e9);
    background-size: 300% 300%;
    animation: bgMove 10s ease infinite;
}

@keyframes bgMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass card */
.block-container {
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    background: rgba(255, 255, 255, 0.35);
    border-radius: 20px;
    padding: 2.2rem;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 8px 32px rgba(31, 135, 64, 0.25);
}

/* Buttons - glass + glow */
.stButton>button {
    background: rgba(46, 125, 50, 0.75);
    color: white;
    border-radius: 14px;
    padding: 0.6em 1.4em;
    font-weight: bold;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 0 20px rgba(129,199,132,0.6);
}
.stButton>button:hover {
    background: rgba(27, 94, 32, 0.85);
    box-shadow: 0 0 30px rgba(129,199,132,1);
}

/* Checkbox text */
label {
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.progress-wrap {
    width: 100%;
    background: rgba(46,125,50,0.15);
    border-radius: 12px;
    overflow: hidden;
    margin: 12px 0 6px 0;
}

.progress-bar {
    height: 18px;
    width: 0%;
    background: linear-gradient(90deg, #81c784, #2e7d32);
    border-radius: 12px;
    animation: loadBar 1.2s ease-out forwards;
}

@keyframes loadBar {
    from { width: 0%; }
    to   { width: var(--target); }
}

.progress-label {
    font-size: 14px;
    font-weight: 600;
    color: #1b5e20;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Result glass card */
.result-card {
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    background: rgba(255, 255, 255, 0.4);
    border-radius: 20px;
    padding: 25px;
    margin-top: 25px;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 10px 35px rgba(31, 135, 64, 0.3);
    animation: fadeUp 0.8s ease-in-out;
}

/* Title */
.result-title {
    color: #1b5e20;
    font-size: 22px;
    font-weight: bold;
}

/* Percentage badge */
.match-badge {
    display: inline-block;
    background: linear-gradient(90deg, #43a047, #81c784);
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: bold;
    margin-top: 10px;
    box-shadow: 0 0 15px rgba(129,199,132,0.8);
}

/* Animation */
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<h1 style="
text-align:center;
color:#1b5e20;
text-shadow: 0 0 15px rgba(129,199,132,0.9);
">
🚀 Career Recommendation System
</h1>
<p style="text-align:center; color:#2e7d32; font-size:17px;">
Find your perfect career with smart recommendations
</p>
""", unsafe_allow_html=True)


st.markdown("""
<style>
@keyframes popGlow {
    0% {
        opacity: 0;
        transform: scale(0.85);
        text-shadow: 0 0 0 rgba(129,199,132,0);
    }
    60% {
        opacity: 1;
        transform: scale(1.05);
        text-shadow: 0 0 18px rgba(129,199,132,0.9);
    }
    100% {
        opacity: 1;
        transform: scale(1);
        text-shadow: 0 0 12px rgba(129,199,132,0.7);
    }
}

.hero-career {
    animation: popGlow 0.9s ease-out forwards;
}
</style>
""", unsafe_allow_html=True)








# Load dataset
data = pd.read_csv("career.csv")

career_col = data.columns[0]
skill_cols = data.columns[1:]

st.subheader("Select Your Skills")

user_input = []
for skill in skill_cols:
    user_input.append(st.checkbox(skill))

user_df = pd.DataFrame([user_input], columns=skill_cols)
if st.button("Get Recommendation"):
    
    similarity = cosine_similarity(user_df, data[skill_cols])[0]
    data["Match %"] = similarity * 100

    top = data.sort_values("Match %", ascending=False)

    icon_map = {
        "UI UX Designer": "🎨",
        "Software Developer": "💻",
        "Data Scientist": "📊",
        "Data Analyst": "📈",
        "Machine Learning Engineer": "🤖",
        "AI Engineer": "🚀",
        "Project Manager": "💼",
        "Technical Recruiter": "🧑‍💼",
        "Blockchain Developer": "⛓️",
        "DevOps Engineer": "⚙️"
    }

    top_career = top.iloc[0][career_col]
    match_percent = round(top.iloc[0]["Match %"], 2)
    career_icon = icon_map.get(top_career, "⭐")

    # ---------- RESULT CARD ----------
    import streamlit.components.v1 as components

    fit_label = (
        "Strong" if match_percent >= 70 else
        "Moderate" if match_percent >= 40 else
        "Average"
    )

    result_html = f"""
    <div class="result-card" style="line-height:1.6;">

        <div style="
            font-size:28px;
            font-weight:800;
            color:#1b5e20;
            margin-bottom:14px;
        ">
            🎯 Recommended Career
        </div>

        <h1 class="hero-career" style="
            font-size:34px;
            margin:10px 0 16px 0;
            font-weight:900;
            color:#1b5e20;
        ">
            {career_icon} {top_career}
        </h1>

        <div class="match-badge" style="margin-bottom:18px;">
            Match Score: {match_percent}%
        </div>

        <div class="progress-wrap" style="margin:18px 0 6px 0;">
            <div class="progress-bar" style="--target:{match_percent}%"></div>
        </div>

        <div class="progress-label" style="
            font-size:15px;
            font-weight:600;
            margin-bottom:18px;
        ">
            Career Fit Level: <b>{fit_label}</b>
        </div>

        <div style="
            margin-top:14px;
            color:#1b5e20;
            font-size:15.5px;
            line-height:1.8;
        ">
            ✅ Based on your selected skills<br>
            ✅ Strong career fit<br>
            ✅ High demand field
        </div>

    </div>
    """

    components.html(result_html, height=380)

    # ---------- BAR CHART ----------
    top_5 = top.head(5).copy()

    top_5["Career_Icon"] = top_5[career_col].apply(
        lambda x: f"{icon_map.get(x, '⭐')} {x}"
    )

    fig = px.bar(
        top_5,
        x="Match %",
        y="Career_Icon",
        orientation="h",
        text="Match %",
        color="Match %",
        color_continuous_scale=[
            [0.0, "#c8e6c9"],
            [0.5, "#66bb6a"],
            [1.0, "#1b5e20"]
        ],
        height=420
    )

    fig.update_layout(
        title=dict(
            text="✨ Top 5 Career Matches",
            x=0.5,
            xanchor="center",
            font=dict(
                size=26,
                color="#1b5e20",
                family="Poppins, Arial Black"
            )
        ),
        yaxis=dict(
            autorange="reversed",
            title="",
            tickfont=dict(
                size=18,
                color="#2e7d32",
                family="Poppins, Arial"
            )
        ),
        xaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        bargap=0.35,
        transition=dict(duration=900, easing="cubic-in-out"),
        margin=dict(l=50, r=40, t=90, b=40)
    )

    st.plotly_chart(fig, use_container_width=True, key="career_bar_chart")
