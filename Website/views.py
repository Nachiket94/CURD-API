from flask import Blueprint, render_template, request, flash
import duckdb

views = Blueprint('views', __name__)

db = duckdb.connect()

# value = request.form('checkbox') 
# print(value)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/query_output', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        attr = request.form
        age_from = attr.get('age_from')
        age_to = attr.get('age_to')
        gender_male = attr.get('male')
        gender_female = attr.get('female')
        input_location = attr.get('input_location')
        input_date = attr.get('input_date')
        input_sub_plan = attr.get('input_sub_plan')
        input_device = attr.get('input_device')
    




    selected_queries = []
    if attr.get('age')=='on':
        selected_queries.append(age_from)
        selected_queries.append(age_to)
    if attr.get('gender') == 'on':
        if gender_female == 'female':
            selected_queries.append(gender_female)
        if gender_male == 'male':
            selected_queries.append(gender_male)
    if attr.get('location') == 'on':
        selected_queries.append(input_location)
    if attr.get('signup_date') == 'on':
        selected_queries.append(input_date)
    if attr.get('sub_plan') == 'on':
        selected_queries.append(input_sub_plan)
    if attr.get('device') == 'on':
        selected_queries.append(input_device)
    print(selected_queries)

    data = db.sql(""" SELECT a.*, e.*
            FROM read_csv_auto('user_attributes.csv') a
            JOIN read_csv_auto('user_events.csv') e
            USING (user_ID)
            ORDER BY user_ID
            ;""").fetchall()
    return render_template("table.html", data=data)

    # return render_template("table.html", data=data)
