import pandas as pd
import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar, Radiobutton, Label, Button, StringVar

# Load the data from CSV into a DataFrame
data = pd.read_csv('symptoms.csv')

# Assuming 'Health Issue' is the target variable and other columns are features
X = data.drop('Health Issue', axis=1)
y = data['Health Issue']

# Create and train the model
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X, y)

# Function to handle predictions
def predict():
    try:
        # Retrieve values from the survey
        input_values = []
        for idx, symptom in enumerate(symptoms):
            value = 1 if symptom_vars[idx].get() == "Yes" else 0
            input_values.append(value)
        
        # Convert input values to DataFrame with the same columns as the training data
        input_df = pd.DataFrame([input_values], columns=symptoms)
        
        # Perform prediction
        prediction = model.predict(input_df)[0]
        
        # Display the prediction in a message box
        messagebox.showinfo("Prediction", f"The predicted health issue is: {prediction}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("Menopause and Menstrual Health Issues Predictor")
root.configure(bg='#CADBD7')  # Setting background color to a light pink

# Extra text at the top
extra_text = """Welcome to the Menopause and Menstrual Related Health Issue Predictor.
Please answer whether you have felt any of the symptoms recently to help identify a potential Health Issue."""
label_extra = Label(root, text=extra_text, bg='#CADBD7', fg='#333942', font=('Lucida Grande', 20, 'bold'), wraplength=600, justify="center")
label_extra.pack(padx=20, pady=20)

# Canvas with scrollbar for the survey
canvas = Canvas(root, bg='#F6F3F0', highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Frame to contain the survey items
survey_frame = tk.Frame(canvas, bg='#F6F3F0')  # Using the same background color

# Function to update scroll region for canvas
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Bind the frame and canvas to the event
survey_frame.bind("<Configure>", on_frame_configure)
canvas.create_window((0, 0), window=survey_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Labels for symptoms and Yes/No buttons
symptoms = list(X.columns)
symptom_vars = []

for idx, symptom in enumerate(symptoms):
    # Symptom label
    label = Label(survey_frame, text=symptom, width=50, anchor='w', bg='#F6F3F0', fg='#333942', font=('Lucida Grande', 14, 'bold'))
    label.grid(row=idx, column=0, padx=10, pady=5, columnspan=2)
    
    # Yes/No radio buttons
    var = StringVar(value="No")  # Default value is "No"
    symptom_vars.append(var)
    yes_button = Radiobutton(survey_frame, text="Yes", variable=var, value="Yes", bg='#F6F3F0', font=('Lucida Grande', 11))
    yes_button.grid(row=idx, column=2, padx=10)
    no_button = Radiobutton(survey_frame, text="No", variable=var, value="No", bg='#F6F3F0', font=('Lucida Grande', 11))
    no_button.grid(row=idx, column=3, padx=10)

# Predict button
predict_button = Button(survey_frame, text="Predict", command=predict, bg='#F6F3F0', fg='#333942', font=('Lucida Grande', 14, 'bold'))
predict_button.grid(row=len(symptoms), column=0, columnspan=4, pady=20, sticky='nsew')  # Place at the bottom, stretch across columns

root.mainloop()
