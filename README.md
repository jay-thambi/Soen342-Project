## Section II

### Team Members:
- Alexander Kepekci, 40113003
- Sanjay Thambithurai, 40184405

---

## Setup and Installation

### Prerequisites
- Python 3.x

### Installation Steps

1. **Create and activate a virtual environment:**
   ```bash
   From Soen342-Project directory:
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\\Scripts\\activate     # For Windows
   $env:FLASK_APP = "project.app"
   flask run

2. **Seed database**
   From Soen342-Project directory:
   python -m project.seed
### Visit the app at http://127.0.0.1:5000/ in your browser.

#### Formal Specification 1:
“Offerings are unique. In other words, multiple offerings on the same day and time slot must be offered at a different location.”

```
context Offering
inv UniqueOffering:
    Offering.allInstances()->forAll(firstOffering, secondOffering |
        firstOffering <> secondOffering implies
        (firstOffering.start_time <> secondOffering.start_time or
         firstOffering.end_time <> secondOffering.end_time or
         firstOffering.date <> secondOffering.date or
         firstOffering.location_id <> secondOffering.location_id)
    )
```
#### Formal Specification 2:
“Any client who is underage must necessarily be accompanied by an adult who acts as their guardian.”
```
context Booking
inv UnderageClient:
    -- Ensure that only adult clients (age >= 18) can make a booking
    self.client.age >= 18
```
#### Formal Specification 3:
“The city associated with an offering must be one the city’s that the instructor has indicated in their availabilities.”

```
context Offering
inv InstructorCity:
    let offeringCity : City = self.location.city in
        Instructor.allInstances()->exists(instructor |
            instructor.id = self.instructor_id and
            instructor.available_cities->includes(offeringCity)
        )

```
#### Formal Specification 4:
“A client does not have multiple bookings on the same day and time slot.” (for simplicity we consider only identical day and time slots, even though in reality a booking on Monday 3pm – 4pm and another also on Monday 3:30pm – 4:30pm should not be acceptable.)
```
context Booking
inv NoMultipleBookings:
    Booking.allInstances()->forAll(firstBooking, secondBooking |
        firstBooking <> secondBooking implies
        (firstBooking.client_id <> secondBooking.client_id or
         firstBooking.start_time <> secondBooking.start_time or
         firstBooking.end_time <> secondBooking.end_time or
         firstBooking.date <> secondBooking.date)
    )
```
