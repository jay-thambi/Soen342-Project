from code.models.models import db, Client, Instructor, Admin

# --- Client Management Functions ---

def register_client(name, email, password):
    """Registers a new client."""
    new_client = Client(name=name, email=email, password=password)
    db.session.add(new_client)
    db.session.commit()
    return new_client

def get_client_by_id(client_id):
    """Retrieves a client by their ID."""
    return Client.query.get(client_id)

def get_all_clients():
    """Retrieves all clients."""
    return Client.query.all()

def delete_client(client_id):
    """Deletes a client by their ID."""
    client = Client.query.get(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()

# --- Instructor Management Functions ---

def register_instructor(name, phone_number, specialization, available_cities, email, password):
    """Registers a new instructor."""
    new_instructor = Instructor(name=name, phone_number=phone_number,
                                specialization=specialization, available_cities=available_cities,
                                email=email, password=password)
    db.session.add(new_instructor)
    db.session.commit()
    return new_instructor

def get_instructor_by_id(instructor_id):
    """Retrieves an instructor by their ID."""
    return Instructor.query.get(instructor_id)

def get_all_instructors():
    """Retrieves all instructors."""
    return Instructor.query.all()

def delete_instructor(instructor_id):
    """Deletes an instructor by their ID."""
    instructor = Instructor.query.get(instructor_id)
    if instructor:
        db.session.delete(instructor)
        db.session.commit()

# --- Administrator Management Functions ---

def register_admin(name, email, password):
    """Registers a new administrator."""
    new_admin = Admin(name=name, email=email, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin

def get_admin_by_id(admin_id):
    """Retrieves an administrator by their ID."""
    return Admin.query.get(admin_id)

def get_all_admins():
    """Retrieves all administrators."""
    return Admin.query.all()

def delete_admin(admin_id):
    """Deletes an administrator by their ID."""
    admin = Admin.query.get(admin_id)
    if admin:
        db.session.delete(admin)
        db.session.commit()

# --- General User Functions ---

def get_user_by_email(email):
    """Retrieves a user by their email (across all roles)."""
    user = Client.query.filter_by(email=email).first()
    if not user:
        user = Instructor.query.filter_by(email=email).first()
    if not user:
        user = Admin.query.filter_by(email=email).first()
    return user

def authenticate_user(email, password):
    """Authenticates a user by checking their email and password."""
    user = get_user_by_email(email)
    if user and user.password == password:
        return user
    return None
