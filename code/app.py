from flask import Flask, render_template, request, redirect, url_for, flash
from models.models import db, Instructor, Offering
from catalogs.Users import register_client, register_instructor, get_user_by_email
from catalogs.Offerings import create_offering, get_all_offerings, update_offering, delete_offering

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for flashing messages
db.init_app(app)

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Create Offering Route (Admin Only)
@app.route('/create_offering', methods=['GET', 'POST'])
def create_offering_route():
    if request.method == 'POST':
        location = request.form['location']
        time_slot = request.form['time_slot']
        specialization = request.form['specialization']
        instructor_id = request.form.get('instructor_id')

        new_offering = create_offering(location, time_slot, specialization, instructor_id)
        db.session.add(new_offering)
        db.session.commit()

        flash("Offering created successfully!", "success")
        return redirect(url_for('view_offerings'))

    return render_template('create_offering.html')

# View All Offerings Route
@app.route('/view_offerings')
def view_offerings():
    offerings = get_all_offerings()
    return render_template('view_offerings.html', offerings=offerings)

# Select Offering Route (Instructor Only)
@app.route('/select_offering', methods=['GET', 'POST'])
def select_offering():
    instructor_id = request.args.get('instructor_id')
    instructor = Instructor.query.get(instructor_id)
    offerings = Offering.query.filter_by(instructor_id=None).all()

    if request.method == 'POST':
        offering_id = request.form['offering_id']
        offering = Offering.query.get(offering_id)

        if offering and not offering.instructor:
            offering.instructor_id = instructor.id
            db.session.commit()
            flash("Offering selected successfully!", "success")
            return redirect(url_for('instructor_portal', instructor_id=instructor.id))

    return render_template('select_offering.html', offerings=offerings, instructor=instructor)

# Instructor Portal Route
@app.route('/instructor_portal')
def instructor_portal():
    instructor_id = request.args.get('instructor_id')
    instructor = Instructor.query.get(instructor_id)
    return render_template('instructor_portal.html', instructor=instructor)

# Update Offering Route (Admin Only)
@app.route('/update_offering/<int:id>', methods=['GET', 'POST'])
def update_offering_route(id):
    offering = Offering.query.get(id)
    if request.method == 'POST':
        location = request.form['location']
        time_slot = request.form['time_slot']
        specialization = request.form['specialization']
        instructor_id = request.form.get('instructor_id')

        updated_offering = update_offering(offering.id, location, time_slot, specialization, instructor_id)
        flash("Offering updated successfully!", "success")
        return redirect(url_for('view_offerings'))

    return render_template('update_offering.html', offering=offering)

# Delete Offering Confirmation Route
@app.route('/delete_offering/<int:id>', methods=['POST'])
def delete_offering_route(id):
    if delete_offering(id):
        flash("Offering deleted successfully!", "success")
    else:
        flash("Offering not found.", "error")
    return redirect(url_for('view_offerings'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']  # Get password from the form
        role = request.form['role']

        if role == 'client':
            register_client(name, email, password)  # Include password
        elif role == 'instructor':
            phone_number = request.form['phone_number']
            specialization = request.form['specialization']
            available_cities = request.form['available_cities']
            register_instructor(name, phone_number, specialization, available_cities, email, password)
        elif role == 'admin':
            register_admin(name, email, password)
        else:
            flash("Invalid role selected.", "error")
            return redirect(url_for('register'))

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)

        if user and user.password == password:
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials.", "error")

    return render_template('login.html')

# Error Handling Route
@app.route('/error')
def error():
    error_title = request.args.get('error_title', 'Error')
    error_message = request.args.get('error_message', 'An unexpected error occurred.')
    return render_template('error.html', error_title=error_title, error_message=error_message)

# Run the App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don’t exist
    app.run(debug=True)
