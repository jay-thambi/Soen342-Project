from flask import Flask, render_template, request, redirect, url_for
from models.models import db, Offering, Instructor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    offerings = Offering.query.all()
    return render_template('home.html', offerings=offerings)

@app.route('/create-offering', methods=['GET', 'POST'])
def create_offering():
    if request.method == 'POST':
        location = request.form['location']
        time_slot = request.form['time_slot']
        specialization = request.form['specialization']
        new_offering = Offering(location=location, time_slot=time_slot, specialization=specialization)
        db.session.add(new_offering)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_offering.html')

@app.route('/select-offering/<int:id>', methods=['GET', 'POST'])
def select_offering(id):
    offering = Offering.query.get(id)
    if request.method == 'POST':
        instructor_id = request.form['instructor_id']
        instructor = Instructor.query.get(instructor_id)
        offering.instructor_id = instructor.id
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('select_offering.html', offering=offering)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
