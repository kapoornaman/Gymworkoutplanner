from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("megaGymDataset.csv")

@app.route('/')
def index():
    levels = ["Beginner", "Intermediate", "Expert"]
    bodyparts = df["BodyPart"].unique()
    return render_template('index.html', levels=levels, bodyparts=bodyparts)

@app.route('/generate_workout', methods=['POST'])
def generate_workout():
    data = request.form
    level = data.get('level')
    muscle_to_train = data.get('muscle_to_train')
    no_of_exercises = int(data.get('no_of_exercises'))
    
    # Filter exercises by muscle group
    exercises = df[df["BodyPart"] == muscle_to_train]
    
    # Filter exercises by level
    if level == "Beginner":
        exercises = exercises[exercises["Level"] == "Beginner"]
    elif level == "Intermediate":
        exercises = exercises[exercises["Level"].isin(["Beginner", "Intermediate"])]
    elif level == "Expert":
        exercises = exercises[exercises["Level"].isin(["Beginner", "Intermediate", "Expert"])]
    
    # Sort exercises by rating
    sorted_exercises = exercises.sort_values(by='Rating', ascending=False)
    
    # Select top exercises based on user input
    top_exercises = sorted_exercises.head(no_of_exercises)
    
    # Convert top exercises DataFrame to list of dictionaries with ExerciseName and Rating
    top_exercises_dict = top_exercises[['Title', 'Rating']].to_dict(orient='records')
    
    return render_template('workout_plan.html', exercises=top_exercises_dict)

if __name__ == '__main__':
    app.run(debug=True)
