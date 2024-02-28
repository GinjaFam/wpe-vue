
from geoalchemy2 import Geometry, WKTElement
import random
from flask import current_app
from utilities.models_db import db, Mock


def generate_random_hrus():

    def create_random_polygon():
        x, y = random.uniform(5, 35), random.uniform(-10, 10)
        return WKTElement(f'POLYGON(({x} {y}, {x+1} {y}, {x+1} {y+1}, {x} {y+1}, {x} {y}))', srid=4326)

    with current_app.app_context():
        for i in range(500):
            new_hru = Mock(
                watershed_id=random.randint(1, 10),
                zone_id=random.randint(1, 20),
                lulc_id=random.randint(1, 30),
                slope=random.uniform(0, 45),
                amc=random.randint(1, 3),
                hsg=random.randint(1, 4),
                cn=random.randint(50, 100),
                h_boundary=create_random_polygon()
            )
            db.session.add(new_hru)

        try:
            db.session.commit()
            print("500 HRUs successfully added.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
        finally:
            db.session.close()


