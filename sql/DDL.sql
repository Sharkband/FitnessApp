CREATE TABLE Members(
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    gender VARCHAR(10),
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    fitness_goal INT 
);

CREATE TABLE Trainers(
    trainer_id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    gender VARCHAR(10),
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    specialization VARCHAR(100)
);

CREATE TABLE AdministrativeStaff(
    staff_id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    gender VARCHAR(10),
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50)
);

CREATE TABLE Rooms(
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(80) NOT NULL,
    capacity INT NOT NULL,
    status VARCHAR(20) DEFAULT 'Available'
);

CREATE TABLE HealthMetrics(
    metric_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL REFERENCES Members(member_id),
    date_recorded DATE NOT NULL,
    height NUMERIC(5,2),
    weight NUMERIC(5,2), 
    heart_rate INT,
    body_fat_percentage NUMERIC(4,2)
);

CREATE TABLE PersonalTrainingSessions(
    session_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL REFERENCES Members(member_id),
    room_id INT NOT NULL REFERENCES Rooms(room_id),
    trainer_id INT NOT NULL REFERENCES Trainers(trainer_id),
    staff_id INT NOT NULL REFERENCES AdministrativeStaff(staff_id),
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL, 
    status VARCHAR(20)
);

CREATE VIEW LatestMemberMetrics AS
SELECT
    m.member_id,
    m.name,
    hm.date_recorded,
    hm.weight,
    hm.heart_rate,
    hm.body_fat_percentage
FROM Members AS m
LEFT JOIN HealthMetrics AS hm 
ON m.member_id = hm.member_id
WHERE hm.date_recorded = (
    SELECT MAX(h.date_recorded) FROM 
    HealthMetrics AS h
    where h.member_id = m.member_id
);

CREATE INDEX member_name ON
Members(name);


CREATE OR REPLACE FUNCTION no_room_double_booking()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM PersonalTrainingSessions p
        WHERE p.room_id = NEW.room_id
          AND p.session_date = NEW.session_date
          AND p.status = 'Booked'
          AND p.session_id != NEW.session_id
          AND NOT (
                NEW.end_time <= p.start_time
                OR NEW.start_time >= p.end_time
              )
    ) THEN
        RAISE EXCEPTION 'Room is already booked for this time.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER no_room_double
BEFORE INSERT OR UPDATE
ON PersonalTrainingSessions
FOR EACH ROW
EXECUTE FUNCTION no_room_double_booking()

