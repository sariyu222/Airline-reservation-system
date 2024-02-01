import datetime
from bson import ObjectId
from flask import Flask, request, render_template, session, redirect
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017')
my_db = myclient['AirlineReservation']
customer_col = my_db['customer']
Airport_col = my_db['Airport']
Airplane_col = my_db['Airplane']
flight_schedules_col = my_db['Flight_Schedules']
booking_col = my_db['booking']
payment_col = my_db["payment"]
ticket_col = my_db["ticket"]
app = Flask(__name__)
app.secret_key = "airline"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin_login1", methods=['post'])
def admin_login1():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == 'admin' and password == 'admin':
        session['role'] = 'admin'
        return render_template("admin.html")
    else:
        return render_template("Mmsg.html", message="Invalid Login Details")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/customer_Reg")
def customer_Reg():
    return render_template("customer_Reg.html")


@app.route("/customer_Reg1", methods=['post'])
def customer_Reg1():
    Customer_name = request.form.get("Customer_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    age = request.form.get("age")
    gender = request.form.get("gender")
    address = request.form.get("address")
    query = {"$or": [{"email": email}, {"phone": phone}]}
    count = customer_col.count_documents(query)
    if count > 0:
        return render_template("Mmsg.html", message="User Already Exits", color="text-danger")
    else:
        query2 = {"Customer_name": Customer_name, "email": email, "phone": phone, "password": password, "age": age,
                  "gender": gender, "address": address}
        customer_col.insert_one(query2)
        return render_template("Mmsg.html", message="Register Added Successfully", color="text-success")

@app.route("/customer_login")
def customer_login():
    return render_template("customer_login.html")


@app.route("/customer_login1", methods=['post'])
def customer_login1():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {"email": email, "password": password}
    count = customer_col.count_documents(query)
    if count > 0:
        customer = customer_col.find_one(query)
        session['customer_id'] = str(customer['_id'])
        session['role'] = 'customer'
        return redirect("/customerhome")
    else:
        return render_template("Mmsg.html", message="Invalid Login", color="text-danger")


@app.route("/customerhome")
def customerhome():
    customer = customer_col.find_one({'_id': ObjectId(session['customer_id'])})
    return render_template("customerhome.html", customer=customer)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


@app.route("/AddAirport1", methods=['post'])
def AddAirport1():
    airport_name = request.form.get("airport_name")
    perameter = request.form.get("perameter")
    no_of_air_strips = request.form.get("no_of_air_strips")
    airport_description = request.form.get("airport_description")
    address = request.form.get("address")
    query = {"airport_name": airport_name}
    count = Airport_col.count_documents(query)
    if count > 0:
        return render_template("amsg.html", message="Duplicate Value Enter", color="text-danger")
    query2 = {"airport_name": airport_name, "perameter": perameter, "no_of_air_strips": no_of_air_strips,
              "airport_description": airport_description, "address": address}
    Airport_col.insert_one(query2)
    return redirect("/ViewAirport")


@app.route("/ViewAirport")
def ViewAirport():
    Airports = Airport_col.find()
    Airports = list(Airports)
    return render_template("ViewAirport.html", Airports=Airports)


@app.route("/AddAirplane")
def AddAirplane():
    return render_template("AddAirplane.html")


@app.route("/AddAirplane1", methods=['post'])
def AddAirplane1():
    company_name = request.form.get("company_name")
    airplane_name = request.form.get("airplane_name")
    no_of_seats_in_first_class = request.form.get("no_of_seats_in_first_class")
    no_of_seats_in_business_class = request.form.get("no_of_seats_in_business_class")
    no_of_seats_in_economy_class = request.form.get("no_of_seats_in_economy_class")
    airplane_description = request.form.get("airplane_description")
    query2 = {"company_name": company_name, "airplane_name": airplane_name,
              "no_of_seats_in_first_class": no_of_seats_in_first_class,
              "no_of_seats_in_business_class": no_of_seats_in_business_class,
              "no_of_seats_in_economy_class": no_of_seats_in_economy_class,
              "airplane_description": airplane_description}
    Airplane_col.insert_one(query2)
    return redirect("/ViewAirplane")


@app.route("/ViewAirplane")
def ViewAirplane():
    Airplanes = Airplane_col.find()
    Airplanes = list(Airplanes)
    return render_template("ViewAirplane.html", Airplanes=Airplanes)


@app.route("/Addflight_schedules")
def Addflight_schedules():
    Airports = Airport_col.find()
    Airplanes = Airplane_col.find()
    Airports = list(Airports)
    return render_template("Addflight_schedules.html", Airports=Airports, Airplanes=Airplanes)


@app.route("/Addflight_schedules1", methods=["post"])
def Addflight_schedules1():
    Airplane_id = request.form.get("Airplane_id")
    date = request.form.get("date")
    From_airport_id = request.form.get("From_airport_id")
    to_airport_id = request.form.get("to_airport_id")
    journey_of_departure_time = request.form.get("journey_of_departure_time")
    journey_of_arrived_time = request.form.get("journey_of_arrived_time")
    price_of_seats_in_first_class = request.form.get("price_of_seats_in_first_class")
    price_of_seats_in_business_class = request.form.get("price_of_seats_in_business_class")
    price_of_seats_in_economy_class = request.form.get("price_of_seats_in_economy_class")
    journey_of_departure_time = journey_of_departure_time.replace('T', ' ')
    journey_of_arrived_time = journey_of_arrived_time.replace('T', ' ')
    journey_of_departure_time = datetime.datetime.strptime(journey_of_departure_time, "%Y-%m-%d %H:%M")
    journey_of_arrived_time = datetime.datetime.strptime(journey_of_arrived_time, "%Y-%m-%d %H:%M")
    query = {"$or": [
        {"journey_of_departure_time": {"$gte": journey_of_departure_time, "$lte": journey_of_arrived_time},
         "journey_of_arrived_time": {"$gte": journey_of_departure_time, "$gte": journey_of_arrived_time}},
        {"journey_of_departure_time": {"$lte": journey_of_departure_time, "$lte": journey_of_arrived_time},
         "journey_of_arrived_time": {"$gte": journey_of_departure_time, "$lte": journey_of_arrived_time}},
        {"journey_of_departure_time": {"$lte": journey_of_departure_time, "$lte": journey_of_arrived_time},
         "journey_of_arrived_time": {"$gte": journey_of_departure_time, "$gte": journey_of_arrived_time}},
        {"journey_of_departure_time": {"$gte": journey_of_departure_time, "$lte": journey_of_arrived_time},
         "journey_of_arrived_time": {"$gte": journey_of_departure_time, "$lte": journey_of_arrived_time}}
    ]}
    count = flight_schedules_col.count_documents(query)
    if count > 0:
        return render_template("amsg.html", message="Time Conflict Occurred", color='text-danger')
    query = {"Airplane_id": ObjectId(Airplane_id), "From_airport_id": ObjectId(From_airport_id),
             "to_airport_id": ObjectId(to_airport_id), "date": date,
             "journey_of_departure_time": journey_of_departure_time, "journey_of_arrived_time": journey_of_arrived_time,
             "price_of_seats_in_first_class": price_of_seats_in_first_class,
             "price_of_seats_in_business_class": price_of_seats_in_business_class,
             "price_of_seats_in_economy_class": price_of_seats_in_economy_class}
    flight_schedules_col.insert_one(query)
    return redirect("/Viewflight_schedules")


@app.route("/Viewflight_schedules")
def Viewflight_schedules():
    Airports = Airport_col.find()
    Airplanes = Airplane_col.find()
    Airports = list(Airports)
    flight_schedules = flight_schedules_col.find()
    flight_schedules = list(flight_schedules)
    flight_schedules.reverse()

    return render_template("Viewflight_schedules.html", flight_schedules=flight_schedules,
                           getAirportbyAirportid=getAirportbyAirportid, getAirportbyAirportid2=getAirportbyAirportid2,
                           getAirplanebyAirplanrid=getAirplanebyAirplanrid, Airports=Airports, Airplanes=Airplanes)


def getAirportbyAirportid(Airport_id):
    fromAirport = Airport_col.find_one({"_id": ObjectId(Airport_id)})
    return fromAirport


def getAirportbyAirportid2(Airport_id):
    ToAirport = Airport_col.find_one({"_id": ObjectId(Airport_id)})
    return ToAirport


def getAirplanebyAirplanrid(Airplane_id):
    Airplane = Airplane_col.find_one({"_id": ObjectId(Airplane_id)})
    return Airplane


@app.route("/User_view_flight_schedules")
def User_view_flight_schedules():
    fromAirports = Airport_col.find()
    ToAirports = Airport_col.find()
    return render_template("User_view_flight_schedules.html", fromAirports=fromAirports, ToAirports=ToAirports)


@app.route("/User_view_flight_schedules1")
def User_view_flight_schedules1():
    from_airport_name = request.args.get("from_airport_name")
    To_airport_name = request.args.get("To_airport_name")
    date = request.args.get("date")
    query1 = {"airport_name": from_airport_name}
    from_airport = Airport_col.find_one(query1)
    if from_airport == None:
        return render_template("Umsg.html", message=" '" + from_airport_name + "' Not  Found ", color="text-primary")
    from_airport_id = from_airport['_id']
    query2 = {"airport_name": To_airport_name}
    To_airport = Airport_col.find_one(query2)
    if To_airport == None:
        return render_template("Umsg.html", message=" '" + To_airport_name + "' Not  Found", color="text-primary")
    To_airport_id = To_airport['_id']
    query3 = {"From_airport_id": ObjectId(from_airport_id), "to_airport_id": ObjectId(To_airport_id), "date": date}
    flight_schedules = flight_schedules_col.find(query3)
    flight_schedules = list(flight_schedules)
    if len(flight_schedules) == 0:
        return render_template("Umsg.html", message="No Schedules On This Date", color="text-primary")
    return render_template("Customer_view_flight_schedules.html", flight_schedules=flight_schedules,
                           getAirportbyAirportid=getAirportbyAirportid, getAirportbyAirportid2=getAirportbyAirportid2,
                           getAirplanebyAirplanrid=getAirplanebyAirplanrid)


@app.route("/Booknow")
def Booknow():
    flight_schedule_id = request.args.get("flight_schedule_id")
    query = {"_id": ObjectId(flight_schedule_id)}
    flight_schedule = flight_schedules_col.find_one(query)
    query2 = {"_id": flight_schedule['Airplane_id']}
    Airplane = Airplane_col.find_one(query2)
    return render_template("Booknow.html", is_seat_booked=is_seat_booked, flight_schedule_id=flight_schedule_id,
                           flight_schedule=flight_schedule, Airplane=Airplane, int=int,
                           getAirportbyAirportid=getAirportbyAirportid, getAirportbyAirportid2=getAirportbyAirportid2)


@app.route("/Book_Ticket", methods=['post'])
def Book_Ticket():
    flight_schedule_id = request.form.get("flight_schedule_id")
    query = {"_id": ObjectId(flight_schedule_id)}
    flight_schedule = flight_schedules_col.find_one(query)
    query2 = {"_id": flight_schedule['Airplane_id']}
    Airplane = Airplane_col.find_one(query2)
    first_class_selected_seats = []
    for i in range(1, int(Airplane['no_of_seats_in_first_class']) + 1):
        seat_number = request.form.get("F_seat_number" + str(i))
        if seat_number is not None:
            first_class_selected_seats.append(i)
    Business_class_selected_seats = []
    for i in range(1, int(Airplane['no_of_seats_in_business_class']) + 1):
        seat_number = request.form.get("B_seat_number" + str(i))
        if seat_number is not None:
            Business_class_selected_seats.append(i)
    Economy_class_selected_seats = []
    for i in range(1, int(Airplane['no_of_seats_in_economy_class']) + 1):
        seat_number = request.form.get("E_seat_number" + str(i))
        if seat_number is not None:
            Economy_class_selected_seats.append(i)
    status = "payment_pending"
    booked_date = datetime.datetime.now()
    customer_id = session["customer_id"]
    Total_amount = int(flight_schedule["price_of_seats_in_economy_class"]) * len(Economy_class_selected_seats) + int(
        flight_schedule["price_of_seats_in_business_class"]) * len(Business_class_selected_seats) + int(
        flight_schedule["price_of_seats_in_first_class"]) * len(first_class_selected_seats)
    query = {"customer_id": ObjectId(customer_id), "flight_schedule_id": ObjectId(flight_schedule_id), "status": status,
             "booked_date": booked_date, "first_class_booked": first_class_selected_seats,
             "business_class_booked": Business_class_selected_seats,
             "economy_class_booked": Economy_class_selected_seats, "Total_amount": Total_amount}
    result = booking_col.insert_one(query)
    booking_id = result.inserted_id
    query = {"_id": booking_id}
    booking = booking_col.find_one(query)
    return render_template("Book_Ticket.html", len=len, first_class_selected_seats=first_class_selected_seats,
                           Business_class_selected_seats=Business_class_selected_seats,
                           Economy_class_selected_seats=Economy_class_selected_seats, booking=booking,
                           Total_amount=Total_amount, flight_schedule=flight_schedule, Airplane=Airplane,
                           getAirportbyAirportid=getAirportbyAirportid, getAirportbyAirportid2=getAirportbyAirportid2)


@app.route("/Book_Ticket1", methods=["post"])
def Book_Ticket1():
    Total_amount = request.form.get("Total_amount")
    booking_id = request.form.get("booking_id")
    query = {"_id": ObjectId(booking_id)}
    booking = booking_col.find_one(query)
    flight_schedule = booking["flight_schedule_id"]
    query = {"_id": ObjectId(flight_schedule)}
    flight_schedule = flight_schedules_col.find_one(query)
    card_number = request.form.get("card_number")
    card_name = request.form.get("card_name")
    expiry_date = request.form.get("expiry_date")
    card_cvv = request.form.get("card_cvv")
    status = "Amount Paid"
    query = {"booking_id": ObjectId(booking_id), "status": status, "Total_amount": Total_amount,
             "card_number": card_number, "card_name": card_name, "expiry_date": expiry_date, "card_cvv": card_cvv}
    payment_col.insert_one(query)
    query2 = {"_id": ObjectId(booking_id)}
    query3 = {"$set": {"status": "booked"}}
    booking_col.update_one(query2, query3)
    status = "Confirmed"
    date = flight_schedule['date']
    from_airport = flight_schedule["From_airport_id"]
    To_airport = flight_schedule["to_airport_id"]
    Departure_time = flight_schedule["journey_of_departure_time"]
    Arrived_time = flight_schedule["journey_of_arrived_time"]
    query = {"_id": flight_schedule["Airplane_id"]}
    Airplane = Airplane_col.find_one(query)
    airplane_name = Airplane["airplane_name"]
    for Economy_booked in booking["economy_class_booked"]:
        passenger_name = request.form.get('E' + str(Economy_booked) + 'name')
        passenger_age = request.form.get('E' + str(Economy_booked) + 'age')
        query = {"booking_id": ObjectId(booking_id), "passenger_name": passenger_name, "passenger_age": passenger_age,
                 "seat_number": Economy_booked, "status": status, "date": date, "from_airport": ObjectId(from_airport),
                 "To_airport": To_airport, "Departure_time": Departure_time, "Arrived_time": Arrived_time,
                 "airplane_name": airplane_name, "E": "Economy_booked"}
        ticket_col.insert_one(query)
    for business_booked in booking["business_class_booked"]:
        passenger_name = request.form.get('B' + str(business_booked) + 'name')
        passenger_age = request.form.get('B' + str(business_booked) + 'age')
        query = {"booking_id": ObjectId(booking_id), "passenger_name": passenger_name, "passenger_age": passenger_age,
                 "seat_number": business_booked, "status": status, "date": date,
                 "from_airport": ObjectId(from_airport), "To_airport": To_airport, "Departure_time": Departure_time,
                 "Arrived_time": Arrived_time, "airplane_name": airplane_name, "B": "business_booked"}
        ticket_col.insert_one(query)
    for first_booked in booking["first_class_booked"]:
        passenger_name = request.form.get('F' + str(first_booked) + 'name')
        passenger_age = request.form.get('F' + str(first_booked) + 'age')
        query = {"booking_id": ObjectId(booking_id), "passenger_name": passenger_name, "passenger_age": passenger_age,
                 "seat_number": first_booked, "status": status, "date": date, "from_airport": ObjectId(from_airport),
                 "To_airport": To_airport, "Departure_time": Departure_time, "Arrived_time": Arrived_time,
                 "airplane_name": airplane_name, "F": "first_booked"}
        ticket_col.insert_one(query)
    return render_template("Umsg.html", message="Flight Booked Successfully", color="text-primary")


@app.route("/ViewBooking")
def ViewBooking():
    customer_id = session["customer_id"]
    query = {"customer_id": ObjectId(customer_id), "status": "booked"}
    bookings = booking_col.find(query)
    bookings = list(bookings)
    if len(bookings) == 0:
        return render_template("Umsg.html", message="Bookings Not Available", color="text-primary")
    return render_template("ViewBooking.html", len=len,int=int, customernamebycustomerId=customernamebycustomerId,
                           bookings=bookings, getflight_schedulebybooking=getflight_schedulebybooking,
                           getAirportbyAirportid=getAirportbyAirportid, getAirportbyAirportid2=getAirportbyAirportid2,
                           getTicketbybooking=getTicketbybooking, getAirplanebyAirplanrid=getAirplanebyAirplanrid,get_first_class_pass_details=get_first_class_pass_details,get_economy_class_pass_details=get_economy_class_pass_details,get_business_class_pass_details=get_business_class_pass_details)


def getflight_schedulebybooking(flight_schedule_id):
    flight_schedule = flight_schedules_col.find_one({"_id": ObjectId(flight_schedule_id)})
    return flight_schedule


def getTicketbybooking(booking_id):
    query = {"booking_id": ObjectId(booking_id)}
    ticket = ticket_col.find_one(query)
    return ticket


def is_seat_booked(flight_schedule_id, class_type, i):
    query = {"flight_schedule_id": flight_schedule_id, "status": "booked", class_type: i}
    count = booking_col.count_documents(query)
    if count > 0:
        return True
    else:
        return False


@app.route("/Viewpayment")
def Viewpayment():
    booking_id = request.args.get("booking_id")
    query = {"booking_id": ObjectId(booking_id)}
    payment = payment_col.find_one(query)
    return render_template("Viewpayment.html", payment=payment)


@app.route("/Viewticket")
def Viewticket():
    booking_id = request.args.get("booking_id")
    query = {"booking_id": ObjectId(booking_id)}
    tickets = ticket_col.find(query)
    return render_template("Viewticket.html", tickets=tickets,int=int,
                           getflight_schedulebybooking2=getflight_schedulebybooking2,
                           getAirportbyAirportid=getAirportbyAirportid, getAirportbyAirportid2=getAirportbyAirportid2)


def getflight_schedulebybooking2(booking_id):
    query = {"_id": ObjectId(booking_id)}
    print(booking_id)
    booking = booking_col.find_one(query)
    flight_schedule = booking["flight_schedule_id"]
    query = {"_id": ObjectId(flight_schedule)}
    flight_schedule = flight_schedules_col.find_one(query)
    return flight_schedule


def customernamebycustomerId(customer_id):
    customer = customer_col.find_one({"_id": ObjectId(customer_id)})
    return customer


@app.route("/AdminViewBooking")
def AdminViewBooking():
    flight_schedule_id = request.args.get("flight_schedule_id")
    query = {"flight_schedule_id": ObjectId(flight_schedule_id), "status": "booked"}
    bookings = booking_col.find(query)
    bookings = list(bookings)
    if len(bookings) == 0:
        return render_template("amsg.html", message=" Bookings  Not Available", color="text-primary")
    return render_template("AdminViewBooking.html", customernamebycustomerId=customernamebycustomerId,
                           bookings=bookings, getflight_schedulebybooking=getflight_schedulebybooking,int=int,
                           getAirportbyAirportid=getAirportbyAirportid, getAirportbyAirportid2=getAirportbyAirportid2,
                           getTicketbybooking=getTicketbybooking, getAirplanebyAirplanrid=getAirplanebyAirplanrid,get_first_class_pass_details=get_first_class_pass_details,get_economy_class_pass_details=get_economy_class_pass_details,get_business_class_pass_details=get_business_class_pass_details)


@app.route("/Cancelled_Booking")
def Cancelled_Booking():
    customer_id = session["customer_id"]
    query = {"customer_id": ObjectId(customer_id), "status": "Booking Cancelled"}
    bookings = booking_col.find(query)
    bookings = list(bookings)
    if len(bookings) == 0:
        return render_template("Umsg.html", message="No Cancelled Bookings", color="text-danger")
    return render_template("Cancelled_Booking.html", len=len, customernamebycustomerId=customernamebycustomerId,
                           bookings=bookings, getflight_schedulebybooking=getflight_schedulebybooking,
                           getAirportbyAirportid=getAirportbyAirportid, getAirportbyAirportid2=getAirportbyAirportid2,
                           getTicketbybooking=getTicketbybooking, getAirplanebyAirplanrid=getAirplanebyAirplanrid,get_first_class_pass_details=get_first_class_pass_details,get_economy_class_pass_details=get_economy_class_pass_details,get_business_class_pass_details=get_business_class_pass_details,int=int)


@app.route("/CancelBooking")
def CancelBooking():
    booking_id = request.args.get("booking_id")
    query = {"_id": ObjectId(booking_id)}
    query1 = {"$set": {"status": "Booking Cancelled"}}
    booking_col.update_one(query, query1)
    return render_template("Umsg.html", message="Booking Cancelled", color="text-danger")


@app.route("/ViewCancelled_Booking")
def ViewCancelled_Booking():
    query = {"status": "Booking Cancelled"}
    bookings = booking_col.find(query)
    bookings = list(bookings)
    if len(bookings) == 0:
        return render_template("amsg.html", message=" No Cancelled Bookings", color="text-primary")
    return render_template("ViewCancelled_Booking.html", len=len, bookings=bookings,
                           getflight_schedulebybooking=getflight_schedulebybooking,
                           getAirportbyAirportid=getAirportbyAirportid, getAirportbyAirportid2=getAirportbyAirportid2,
                           getTicketbybooking=getTicketbybooking, getAirplanebyAirplanrid=getAirplanebyAirplanrid,
                           customernamebycustomerId=customernamebycustomerId,get_first_class_pass_details=get_first_class_pass_details,get_economy_class_pass_details=get_economy_class_pass_details,get_business_class_pass_details=get_business_class_pass_details,int=int)


def get_first_class_pass_details(booking_id,seat_number):
    ticket = ticket_col.find_one({"booking_id": ObjectId(booking_id),"F":"first_booked","seat_number": seat_number})
    return ticket



def get_economy_class_pass_details(booking_id,seat_number):
    ticket2 = ticket_col.find_one({"booking_id": ObjectId(booking_id),"seat_number": seat_number,"E": "Economy_booked"})
    return ticket2

def get_business_class_pass_details(booking_id,seat_number):
    ticket3 = ticket_col.find_one({"booking_id": ObjectId(booking_id),"seat_number": seat_number,"B": "business_booked"})
    return ticket3


app.run(debug=True)
