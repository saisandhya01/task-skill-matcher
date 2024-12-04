from flask import Flask, render_template, request, jsonify
import json
import spacy

app = Flask(__name__)

app = Flask(__name__)

# Load employee data from employee.json
with open('employee.json', 'r') as file:
    employees_data = json.load(file)

nlp = spacy.load("en_core_web_sm")

# Predefined skill list for matching (for simplicity)
skills_list = ["C++", "PHP", "Ruby", "SQL", "Git", "JavaScript", "CSS", "HTML", "Python", "Java", "Springboot", "Machine Learning", "Pytorch", "Swift", "Docker"]

@app.route('/', methods=['GET', 'POST'])
def home():
    employees = []
    skills = []
    prompt = ""
    if request.method == 'POST':
        prompt = request.form['prompt']
        
        # Extract skills from the prompt using NLP
        doc = nlp(prompt)
        extracted_skills = set()

        for token in doc:
            if token.text.capitalize() in skills_list:
                extracted_skills.add(token.text.capitalize())

        # Calculate match score for each employee
        employee_scores = []
        for employee in employees_data:
            employee_skills = set(employee['skills'].keys())
            matched_skills = extracted_skills & employee_skills  # Intersection of extracted and employee skills
            match_score = sum([employee['skills'][skill] for skill in matched_skills])  # Sum of the skill levels
            # Append match_score to each employee dictionary
            employee_with_score = employee.copy()
            employee_with_score['match_score'] = match_score
            employee_scores.append((employee_with_score, match_score))

        # Sort employees by match score (highest first)
        employee_scores.sort(key=lambda x: x[1], reverse=True)

        # Only take the top 5 employees (or fewer if there are less than 5)
        employees = [employee for employee, _ in employee_scores[:5]]
        skills = extracted_skills

    return render_template('home.html', prompt=prompt, employees=employees, skills=skills)



@app.route('/employee/<int:emp_id>')
def employee_detail(emp_id):
    # Find the employee by ID
    employee = next((emp for emp in employees_data if emp['emp_id'] == emp_id), None)
    if employee:
        return render_template('employee_detail.html', employee=employee)
    else:
        return "Employee not found", 404

if __name__ == '__main__':
    app.run(debug=True)
