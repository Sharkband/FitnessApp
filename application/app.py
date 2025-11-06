from flask import Flask, render_template, request, redirect, session
from database import (login, createMember , updatePersonalDetails, createNewHealthMetric, bookTrainingSession, editTrainingSession, 
assignedTrainingSessions, viewLastMetric, assignRoom, searchMember, getMetrics, getGoal, getTrainingSessions, getAllTrainingSession, 
getRooms, getMembers, getTrainers)

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        fullname, role, role_id, email = login(
            user=request.form["role"],
            email=request.form["email"]
        )
        if role:
            session["fullname"] = fullname
            session["role"] = role
            session["role_id"] = role_id
            session["email"] = email
            return redirect("/dashboard")
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "role" not in session:
        return redirect("/")
    
    metrics = []
    last_metric = []
    training_sessions = []
    goal = ""
    search_results = []
    search_query = ""
    rooms = []
    members = []
    trainers = []
    error = ""

    if session["role"] == "member":
        member_id = session["role_id"][0]
        metrics = getMetrics(member_id)
        last_metric = viewLastMetric(member_id)
        goal = getGoal(member_id)
        training_sessions = getTrainingSessions(member_id)

    elif session["role"] == "trainer":
        trainer_id = session["role_id"][0]
        training_sessions = assignedTrainingSessions(trainer_id)
        
        if request.method == "POST":
            search_query = request.form.get("query", "")
            if search_query:
                search_results = searchMember(search_query)

    elif session["role"] == "staff":          
        staff_id = session["role_id"][0]
        training_sessions = getAllTrainingSession()
        rooms = getRooms()
        members = getMembers()
        trainers = getTrainers()

        if request.method == "POST":
            action = request.form.get("action")

            if action == "assign_room":
                
                session_id = request.form.get("session_id")
                room_id = request.form.get("room_id")
                error = assignRoom(session_id, room_id, staff_id)
                print(error)

            elif action == "add_training":
                
                member_id = request.form.get("member_id")
                room_id = request.form.get("room_id")
                trainer_id = request.form.get("trainer_id")
                session_date = request.form.get("session_date")
                start_time = request.form.get("start_time")
                end_time = request.form.get("end_time")
                status = request.form.get("status")
                error = bookTrainingSession(member_id, room_id, trainer_id, staff_id, session_date, start_time, end_time, status)
                print(error)

            elif action == "edit_training":
                
                session_id =[]
                session_id = request.form.get("session_id")
                member_id = request.form.get("member_id")
                room_id = request.form.get("room_id")
                trainer_id = request.form.get("trainer_id")
                session_date = request.form.get("session_date")
                start_time = request.form.get("start_time")
                end_time = request.form.get("end_time")
                status = request.form.get("status")
                error = editTrainingSession(member_id, room_id, trainer_id, staff_id, session_date, start_time, end_time, status, session_id)
                print(error)
        
        
    

    return render_template("dashboard.html", fullname=session["fullname"][0], role=session["role"], metrics=metrics, 
                           last_metric=last_metric, goal=goal, training_sessions=training_sessions, search_results=search_results,
                           search_query=search_query, rooms=rooms, members=members, trainers=trainers, error=error)



@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    
    if request.method == "POST":
        try:
            createMember(
                name=request.form["name"],
                gender=request.form["gender"],
                email=request.form["email"],
                phone=request.form["phone"],
                fitness_goal=int(request.form["goal"])
            )
            return redirect("/")
        except Exception as e:
            print(e)
            return render_template("create_account.html", error="Missing Values")
        
    return render_template("create_account.html")


@app.route("/update-account", methods=["GET", "POST"])
def update_account():
    
    if request.method == "POST":
        try:
            updatePersonalDetails(
                name=request.form["name"],
                gender=request.form["gender"],
                email=request.form["email"],
                phone=request.form["phone"],
                fitness_goal=int(request.form["goal"])
            )
            return redirect("/dashboard")
        except Exception as e:
            print(e)
            return render_template("update_account.html", error="Missing Values")
        
    return render_template("update_account.html")

@app.route("/health-metric", methods=["GET", "POST"])
def health_metric():
    
    if request.method == "POST":
        try:
            print(session["role_id"])
            createNewHealthMetric(
                member_id=session["role_id"][0],
                date_recorded=request.form["date_recorded"],
                height=int(request.form["height"]),
                weight=int(request.form["weight"]),
                heart_rate=int(request.form["heart_rate"]),
                body_fat_percentage=int(request.form["body_fat_percentage"])
            )
            return redirect("/dashboard")
        except Exception as e:
            print(e)
            return render_template("health_metric.html", error="Missing Values")
        
    return render_template("health_metric.html")

if __name__ == "__main__":
    app.run(debug=True)