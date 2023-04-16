# SafeTracker

Who said location sharing would affect privacy? Not on our watch! We are developing a solution in which the location of any object is retrieved, however, only in controlled locations.

## How it works

Multiple beacons are distributed in an area and are also registered in the location service with its signal strength, location and a brief description about its location.

The phones of the users record every signal they receive for a certain beacon UUID and stored in a queue along with its timestamp, the signal strengths and beacon IDs are then sent periodically for the location service which computes the most likely position of the phone and returns it to the user.


## Components

This project is divided into a location service and the frontend. In a more realistic environment there would be an intermedian Backend which would glue the other 2 components.

### Location Service

The location service was developed in ``Python`` using ``FastApi`` for handling requests and ``PyMongo`` to persistently store information in a ``MongoDB``.

The triangulation and signal handling is in the file ``safe_tracker_app/src/services/location_service``.

### Frontend

The frontend was developed in flutter because one of the requirements was to access the Bluethooth, and for that, an application would be better than a web page.