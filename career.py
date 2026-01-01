import pandas as pd
import matplotlib.pyplot as plt


# Load Kaggle dataset
data = pd.read_csv("career.csv")

print("===================================")
print("   CAREER RECOMMENDATION SYSTEM")
print("===================================\n")

# First column = Career name
career_col = data.columns[0]

# Remaining columns = Skills
skill_cols = data.columns[1:]

print("Answer with 1 = Yes, 0 = No\n")

# Take user input for all skills
user_skills = {}
for skill in skill_cols:
    user_skills[skill] = int(input(f"Do you have skill in {skill}? (1/0): "))

scores = []

# Calculate matching score for each career
for _, row in data.iterrows():
    score = 0
    for skill in skill_cols:
        if user_skills[skill] == row[skill]:
            score += 1
    scores.append(score)

# Add score column
data["Score"] = scores

# Get top 3 career recommendations
top_careers = data.sort_values(by="Score", ascending=False).head(3)

print("\n===================================")
print("   TOP CAREER RECOMMENDATIONS")
print("===================================\n")
total_skills = len(skill_cols)

for i, row in top_careers.iterrows():
    percentage = (row['Score'] / total_skills) * 100
    print(
        f"Career: {row[career_col]}  |  Match: {percentage:.2f}%"
    )
    # Bar chart visualization
percentages = []
careers = []

for i, row in top_careers.iterrows():
    percent = (row['Score'] / total_skills) * 100
    percentages.append(percent)
    careers.append(row[career_col])

plt.figure(figsize=(8, 5))
plt.bar(careers, percentages)
plt.title("Top Career Match Percentage")
plt.ylabel("Match Percentage")
plt.xlabel("Career")
plt.ylim(0, 100)

plt.tight_layout()
plt.savefig("output.png")
plt.show()


print("\nThank you for using the system 👍")
