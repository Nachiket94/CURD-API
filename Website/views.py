from flask import Blueprint, render_template, request, flash
import duckdb

views = Blueprint('views', __name__)

db = duckdb.connect()
db.execute("CREATE TEMPORARY TABLE attributes AS SELECT * FROM read_csv_auto('user_attributes.csv')")
db.execute("CREATE TEMPORARY TABLE events AS SELECT * FROM read_csv_auto('user_events.csv')")

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
        login = attr.get('event_1')
        added_to_cart = attr.get('event_2')
        purchased_item = attr.get('event_3')
        time_stamp = attr.get('time_stamp')


    selected_queries = []
    query_select = ["SELECT * FROM attributes a WHERE"]
    parameters = []

    if attr.get('age')=='on':
        selected_queries.append(age_from)
        selected_queries.append(age_to)
        if age_from is not '' and age_to is not '':
            query_for_age = "(a.age BETWEEN ? AND ?) AND"
            query_select.append(query_for_age)
            parameters.append(age_from)
            parameters.append(age_to)
            # query_age = db.execute(query_for_age,(age_from,age_to)).fetchall()
    
    if attr.get('gender') == 'on':
        if gender_female == 'female':
            selected_queries.append(gender_female)
            query_for_female = "a.gender == 'Female' AND"
            query_select.append(query_for_female)
        if gender_male == 'male':
            selected_queries.append(gender_male)
            query_for_male = "a.gender == 'Male' AND"
            query_select.append(query_for_male)
    
    if attr.get('location') == 'on':
        selected_queries.append(input_location)
        query_for_location = "UPPER(a.location) == UPPER(?) AND"
        query_select.append(query_for_location)
        parameters.append(input_location)
    
    if attr.get('signup_date') == 'on':
        selected_queries.append(input_date)
        query_for_date = "(a.signup_date == ?) AND"
        parameters.append(input_date)
        query_select.append(query_for_date)

    if attr.get('sub_plan') == 'on':
        selected_queries.append(input_sub_plan)
        query_for_plan = "(UPPER(a.sub_plan) == UPPER(?)) AND"
        parameters.append(input_sub_plan)
        query_select.append(query_for_plan)

    if attr.get('device') == 'on':
        selected_queries.append(input_device)
        query_for_device = "(UPPER(a.device_type) == UPPER(?))"
        parameters.append(input_device)
        query_select.append(query_for_device)
        
    if attr.get('event_1') == 'on':
        selected_queries.append(login)
    if attr.get('event_2') == 'on':
        selected_queries.append(added_to_cart)
    if attr.get('event_3') == 'on':
        selected_queries.append(purchased_item)
    if attr.get('time_stamp') == 'on':
        selected_queries.append(time_stamp)
    print(selected_queries)

    query_selection = " ".join(query_select).rstrip("AND")
    print(query_selection, parameters)


    data = db.execute(query_selection, parameters).fetchall()
    # print(data)
    return render_template("table.html", data=data)

    # return render_template("table.html", data=data)
