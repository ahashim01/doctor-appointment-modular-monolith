# Doctor Appointment System (Modular Monolith)

This project implements a **Doctor Appointment Booking** backend using **Django** and **Python**, demonstrating **four different architecture styles** in one **modular monolith**:

1. **Doctor Availability** (Layered Architecture)  
2. **Appointment Booking** (Clean Architecture)  
3. **Appointment Confirmation** (Simplest Architecture)  
4. **Doctor Appointment Management** (Hexagonal Architecture)

---

## Table of Contents

1. [Overview](#overview)  
2. [Project Structure](#project-structure)  
3. [How to Run](#how-to-run)  
4. [How to Test](#how-to-test)  
5. [API Usage](#api-usage)  
   - [Doctor Availability](#doctor-availability-layered-architecture)  
   - [Appointment Booking](#appointment-booking-clean-architecture)  
   - [Appointment Confirmation](#appointment-confirmation-simplest-architecture)  
   - [Doctor Appointment Management](#doctor-appointment-management-hexagonal-architecture)  
6. [Why Modular Monolith?](#why-modular-monolith)  
7. [Architectural Summaries](#architectural-summaries)  

---

## Overview

**Goal**: Provide a backend that:
- Lets the **Doctor** define availability slots.
- Allows **Patients** to book free slots.
- Sends (logs) **confirmation notifications** for newly booked appointments.
- Enables the **Doctor** to manage appointments (view upcoming, mark complete, cancel).

**Tech Stack**:
- **Python 3.12**, **Django 5.1**, **Django REST Framework**
- **SQLite** for simplicity
- **Docker** for containerization (optional local usage without Docker is also supported)

---

## Project Structure

```plaintext
doctor_appointment_app/
├── doctor_appointment_app/   # Main Django project files (settings, urls)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── doctor_availability/      # Layered Architecture
│   ├── models.py
│   ├── views.py
│   ├── services.py
│   ├── tests/
│   └── ...
├── appointment_booking/      # Clean Architecture
│   ├── domain/
│   ├── application/
│   ├── interface_adapters/
│   ├── infrastructure/
│   ├── tests/
│   └── ...
├── appointment_confirmation/ # Simplest Architecture
│   ├── confirmation_service.py
│   └── tests/
├── appointment_management/   # Hexagonal Architecture
│   ├── domain/
│   ├── ports/
│   ├── adapters/
│   ├── infrastructure/
│   ├── tests/
│   └── ...
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## How to Run

### Option A: Run with Docker (Recommended)

1. **Build** the Docker image:
   ```bash
   docker build -t doctor-appointment-app .
   ```
2. **Run** the container:
   ```bash
   docker run -p 8000:8000 doctor-appointment-app
   ```
3. Open [http://localhost:8000](http://localhost:8000) in your browser.

> The container automatically applies migrations (using SQLite) and starts the Django development server. Data is stored in a local SQLite file inside the container.

### Option B: Run Locally (Without Docker)

1. **Create** and **activate** a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```
4. **Run the Django server**:
   ```bash
   python manage.py runserver
   ```
5. Visit [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## How to Test

**Run tests** with one command:

- **Via Docker**:
  ```bash
  docker run doctor-appointment-app sh -c "python manage.py test"
  ```
- **Locally**:
  ```bash
  python manage.py test
  ```

Tests are organized by module (unit, integration). See each module’s `tests/` folder for details.

---

## API Usage

Below are the **API endpoints** for each module, along with **sample cURL** requests. Adjust the payloads as needed.

### Doctor Availability (Layered Architecture)

1. **List All Slots**  
   - **Endpoint**: `GET /api/doctor_availability/slots/`  
   - **Example cURL**:
     ```bash
     curl -X GET http://localhost:8000/api/doctor_availability/slots/
     ```
   - **Response** (JSON):
     ```json
     [
       {
         "id": "67c11053-8619-48d0-9f74-c3652abc2345",
         "time": "2025-01-24T16:30:00Z",
         "doctor": "11111111-1111-1111-1111-111111111111",
         "doctor_name": "Dr. Ahmed",
         "is_reserved": false,
         "cost": "200.00"
       },
       ...
     ]
     ```

2. **Create a New Slot**  
   - **Endpoint**: `POST /api/doctor_availability/slots/`  
   - **Body** (JSON):
     ```json
     {
       "time": "2025-02-10T09:00:00Z",
       "doctor": "11111111-1111-1111-1111-111111111111",
       "cost": 200.00
     }
     ```
   - **Example cURL**:
     ```bash
     curl -X POST http://localhost:8000/api/doctor_availability/slots/ \
       -H "Content-Type: application/json" \
       -d '{
         "time": "2025-02-10T09:00:00Z",
         "doctor": "11111111-1111-1111-1111-111111111111",
         "cost": 200.00
       }'
     ```

---

### Appointment Booking (Clean Architecture)

1. **Book an Appointment**  
   - **Endpoint**: `POST /api/appointment_booking/book/`  
   - **Body** (JSON):
     ```json
     {
       "slot_id": "67c11053-8619-48d0-9f74-c3652abc2345",
       "patient_id": "22222222-2222-2222-2222-222222222222",
       "patient_name": "Alice"
     }
     ```
   - **Example cURL**:
     ```bash
     curl -X POST http://localhost:8000/api/appointment_booking/book/ \
       -H "Content-Type: application/json" \
       -d '{
         "slot_id": "67c11053-8619-48d0-9f74-c3652abc2345",
         "patient_id": "22222222-2222-2222-2222-222222222222",
         "patient_name": "Alice"
       }'
     ```
   - **Response** (JSON):
     ```json
     {
       "id": "39c33a60-e5b7-4234-8d0d-93f64f240edd",
       "slot_id": "67c11053-8619-48d0-9f74-c3652abc2345",
       "patient_id": "22222222-2222-2222-2222-222222222222",
       "patient_name": "Alice",
       "reserved_at": "2025-02-08T12:00:00Z"
     }
     ```

---

### Appointment Confirmation (Simplest Architecture)

- **No direct API endpoints**.  
- The confirmation **logs** the details once an appointment is successfully created by the Appointment Booking module.  
- Check your **Django logs** to see the logged message (e.g., “Appointment Confirmation: [details]”).

---

### Doctor Appointment Management (Hexagonal Architecture)

1. **View Upcoming Appointments**  
   - **Endpoint**: `GET /api/appointment_management/upcoming/`  
   - **Example cURL**:
     ```bash
     curl -X GET http://localhost:8000/api/appointment_management/upcoming/
     ```
   - **Response** (JSON):
     ```json
     [
       {
         "id": "39c33a60-e5b7-4234-8d0d-93f64f240edd",
         "patient_name": "Alice",
         "reserved_at": "2025-02-08T12:00:00Z",
         "is_completed": false,
         "is_canceled": false
       },
       ...
     ]
     ```

2. **Mark an Appointment Completed**  
   - **Endpoint**: `POST /api/appointment_management/<appointment_id>/complete/`  
   - **Example cURL**:
     ```bash
     curl -X POST http://localhost:8000/api/appointment_management/39c33a60-e5b7-4234-8d0d-93f64f240edd/complete/
     ```
   - **Response** (JSON):
     ```json
     { "detail": "Appointment marked as completed." }
     ```

3. **Cancel an Appointment**  
   - **Endpoint**: `POST /api/appointment_management/<appointment_id>/cancel/`  
   - **Example cURL**:
     ```bash
     curl -X POST http://localhost:8000/api/appointment_management/39c33a60-e5b7-4234-8d0d-93f64f240edd/cancel/
     ```
   - **Response** (JSON):
     ```json
     { "detail": "Appointment canceled." }
     ```

---

## Why Modular Monolith?

- **Single Codebase/Deployment**: It’s still one Django project, one database, one server.
- **Modularity**: Each module has **clear boundaries**:
  - **Doctor Availability** -> Manages slots.
  - **Appointment Booking** -> Handles booking logic.
  - **Appointment Confirmation** -> Minimal logic for notifications.
  - **Appointment Management** -> Hexagonal approach for managing appointments.
- **Cross-Module Communication**: Modules interact via **function calls** or service interfaces (e.g., `SlotService`).

---

## Architectural Summaries

1. **Doctor Availability (Layered)**  
   - Traditional 3-layer approach (Models, Views, Services).  
   - Provides `SlotService` to create or list slots.

2. **Appointment Booking (Clean)**  
   - **Domain** (entities), **Use Cases**, **Interface Adapters** (serializers/controllers), **Infrastructure** (ORM).  
   - Orchestrates slot validation through `SlotService` and logs confirmation via `appointment_confirmation`.

3. **Appointment Confirmation (Simplest)**  
   - Single function `send_appointment_confirmation` that **logs** info.  
   - Called when a new appointment is booked.

4. **Appointment Management (Hexagonal)**  
   - **Domain** service (`DoctorAppointmentManagementService`) for mark completed/cancel.  
   - **Ports** define repository interfaces.  
   - **Adapters** implement data access (Django) and inbound controllers (REST endpoints).

---
