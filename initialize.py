import mysql.connector as mysql

def initialize():
    db = mysql.connect(
        host="localhost",  # Change this to your MySQL host
        user="root",       # Change this to your MySQL username
        passwd="admin"     # Change this to your MySQL password
    )
    cursor = db.cursor()
    # Create the database
    cursor.execute("CREATE DATABASE IF NOT EXISTS FlightOpsDb")
    cursor.execute("USE FlightOpsDb")
    
    # Create airports table
    cursor.execute("""CREATE TABLE IF NOT EXISTS airports (icao_id VARCHAR(255) PRIMARY KEY, civilian_name VARCHAR(255), latitude FLOAT, longitude FLOAT)""")
    
    # Create aircrafts table
    cursor.execute("""CREATE TABLE IF NOT EXISTS aircrafts (registration_code VARCHAR(255) PRIMARY KEY, flight_range FLOAT, model VARCHAR(255), weight_capacity FLOAT, fuel_capacity FLOAT,
            passenger_capacity INT, fuel_efficiency FLOAT, status VARCHAR(255), manufacturer VARCHAR(255), manufacture_date DATE, home_airport_id VARCHAR(255), latest_arrival_airport_id VARCHAR(255),
            FOREIGN KEY (home_airport_id) REFERENCES airports(icao_id), FOREIGN KEY (latest_arrival_airport_id) REFERENCES airports(icao_id))""")
    
    # Create flights table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (id INT AUTO_INCREMENT PRIMARY KEY, scheduled_departure_datetime DATETIME, scheduled_arrival_datetime DATETIME, actual_departure_datetime DATETIME,
            actual_arrival_datetime DATETIME, passenger_count INT, projected_fuel_consumption FLOAT, actual_fuel_consumption FLOAT, distance FLOAT, aircraft_id VARCHAR(255), arrival_airport VARCHAR(255),
            departure_airport VARCHAR(255), FOREIGN KEY (aircraft_id) REFERENCES aircrafts(registration_code), FOREIGN KEY (arrival_airport) REFERENCES airports(icao_id), FOREIGN KEY (departure_airport) REFERENCES airports(icao_id))""")
    
    # Create maintenance_schedule table
    cursor.execute("""CREATE TABLE IF NOT EXISTS maintenance_schedule (id INT AUTO_INCREMENT PRIMARY KEY, suggested_date DATE, description TEXT, aircraft_id VARCHAR(255),
            maintenance_location VARCHAR(255), FOREIGN KEY (aircraft_id) REFERENCES aircrafts(registration_code), FOREIGN KEY (maintenance_location) REFERENCES airports(icao_id))""")
    
    # Create maintenance_log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_log (id INT AUTO_INCREMENT PRIMARY KEY, service_start DATE, service_finish DATE, description TEXT, aircraft_id VARCHAR(255),
            maintenance_location VARCHAR(255), FOREIGN KEY (aircraft_id) REFERENCES aircrafts(registration_code), FOREIGN KEY (maintenance_location) REFERENCES airports(icao_id))""")
    
    # Insert sample data into airports table
    cursor.executemany("""INSERT IGNORE INTO airports (icao_id, civilian_name, latitude, longitude) VALUES (%s, %s, %s, %s)""", [
        ('KSUS', 'Spirit of St. Louis Airport', 38.6621, -90.6523),
        ('KSGF', 'Springfield-Branson National Airport', 37.2457, -93.3886),
        ('KCOU', 'Columbia Regional Airport', 38.8181, -92.2196),
        ('KCPS', 'St. Louis Downtown Airport', 38.5707, -90.1567),
        ('KEVV', 'Evansville Regional Airport', 38.0360, -87.5324)
    ])
    
    # Insert sample data into aircrafts table
    cursor.executemany("""INSERT IGNORE INTO aircrafts (registration_code, flight_range, model, weight_capacity, fuel_capacity,
        passenger_capacity, fuel_efficiency, status, manufacturer, manufacture_date, home_airport_id, latest_arrival_airport_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, [
        ('N739TA', 1200, 'TecNam P2006T', 822, 200, 4, 0.5, 'Active', 'TecNam', '2015-06-15', 'KSUS', 'KSGF'),
        ('N1544C', 800, 'Cessna 172SP', 835, 200, 4, 0.4, 'Active', 'Cessna', '2010-05-20', 'KSUS', 'KCOU'),
        ('N30TL', 800, 'Cessna 172 G1000', 870, 200, 4, 0.4, 'Active', 'Cessna', '2012-07-18', 'KSUS', 'KCPS'),
        ('N8177Y', 1000, 'Piper Saratoga', 1206, 400, 6, 0.6, 'Active', 'Piper', '2021-11-05', 'KSUS', 'KEVV')
    ])
    
    db.commit()
    db.close()

if __name__ == "__main__":
    initialize()
