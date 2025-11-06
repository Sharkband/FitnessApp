INSERT INTO Members (name, gender, email, phone, fitness_goal) VALUES
('Alice Smith', 'F', 'alice@fitness.com', '555-1001', 55),
('Bob Johnson', 'M', 'bob@fitness.com', '555-1002', 80),
('Charlie Davis', 'M', 'charlie@fitness.com', '555-1003', 70),
('Diana Lee', 'F', 'diana@fitness.com', '555-1004', 63),
('Ethan Walker', 'M', 'ethan@fitness.com', '555-1005', 50);

INSERT INTO Trainers (name, gender, email, phone, specialization) VALUES
('Sarah Coach', 'F', 'sarah@fitness.com', '555-2001', 'Strength'),
('Tom Flex', 'M', 'tom@fitness.com', '555-2002', 'Cardio'),
('Nick Power', 'M', 'nick@fitness.com', '555-2003', 'Yoga'),
('Linda Core', 'F', 'linda@fitness.com', '555-2004', 'Pilates'),
('James Fit', 'M', 'james@fitness.com', '555-2005', 'Crossfit');

INSERT INTO AdministrativeStaff (name, gender, email, phone, role) VALUES
('Anna Flag', 'F', 'anna@fitness.com', '555-3001', 'Manager'),
('Eric Cost', 'M', 'eric@fitness.com', '555-3002', 'Staff'),
('Grace Jones', 'F', 'grace@fitness.com', '555-3003', 'Staff'),
('Paul Smith', 'M', 'paul@fitness.com', '555-3004', 'Supervisor'),
('Kate Lancaster', 'F', 'kate@fitness.com', '555-3005', 'Staff');

INSERT INTO Rooms (room_name, capacity, status) VALUES
('Studio A', 25, 'Available'),
('Studio B', 30, 'Available'),
('Training Room 1', 10, 'Maintenance'),
('Training Room 2', 15, 'Available'),
('Bike Room', 20, 'Available');

INSERT INTO HealthMetrics (member_id, date_recorded, height, weight, heart_rate, body_fat_percentage) VALUES
(1, '2025-01-01', 165.0, 60.0, 80, 22.5),
(2, '2025-01-02', 178.0, 75.0, 85, 20.1),
(3, '2025-01-03', 182.0, 82.5, 78, 19.5),
(4, '2025-01-04', 160.0, 55.0, 72, 24.0),
(5, '2025-01-05', 170.0, 68.5, 88, 21.8);

INSERT INTO PersonalTrainingSessions (
    member_id, room_id, trainer_id, staff_id,
    session_date, start_time, end_time, status
) VALUES
(1, 1, 1, 1, '2025-02-01', '09:00', '10:00', 'Booked'),
(2, 2, 2, 2, '2025-02-01', '10:00', '11:00', 'Completed'),
(3, 4, 4, 3, '2025-02-02', '11:00', '12:00', 'Booked'),
(4, 4, 4, 4, '2025-02-03', '08:00', '09:00', 'Cancelled'),
(5, 5, 5, 5, '2025-02-04', '13:00', '14:00', 'Booked');

