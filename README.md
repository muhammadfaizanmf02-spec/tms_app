# tms_app

Transport Management System (TMS) app for Frappe/ERPNext - Bus Ticketing, Cargo Booking, Trip Scheduling, POS integration.

## Overview

tms_app is a custom Frappe app that adds a full Transport Management System on top of ERPNext, covering bus ticketing (POS style), cargo/parcel booking, trip scheduling, live bus tracking, and revenue reporting, while integrating with core ERPNext modules (Accounts, Assets, HR & Payroll, Buying & Stock).

## Module: Transport Management

### Planned DocTypes

DocType 1: Bus Station / Stop (Master). Fields: Station Name, City, Station Code, GPS Location.

DocType 2: Bus Route (Master). Fields: Route Name, Origin Station, Destination Station, Distance (km), Intermediate Stops (Child Table), Base Fare.

DocType 3: Bus Vehicle (Master). Fields: Registration No, Vehicle Model, Capacity, Fuel Type, Linked Asset (Link to ERPNext Asset).

DocType 4: Seat Layout (Master). Fields: Layout Name, Total Rows, Seats per Row, Layout Type (2x2, 2x1 Executive).

DocType 5: Bus Trip / Schedule. Fields: Trip ID, Bus Vehicle, Route, Departure Time, Arrival Time, Driver (Link to Employee), Conductor (Link to Employee), Status (Scheduled, In-Transit, Completed, Cancelled).

DocType 6: Bus Ticket Booking. Fields: Ticket ID, Trip ID, Passenger Name, Mobile, Origin, Destination, Selected Seat No, Ticket Price, Payment Method (Cash/Card/QR), Status (Booked, Cancelled), Linked Sales Invoice.

DocType 7: Cargo Booking. Fields: Tracking ID, Sender Name/Phone, Receiver Name/Phone, Origin Station, Destination Station, Parcel Type, Weight (kg), Cargo Freight Charge, Status (Booked, Loaded, In-Transit, Delivered), Linked Sales Invoice.

DocType 8: Bus Live Tracking. Fields: Trip ID, Bus Registration, Current Latitude, Current Longitude, Last Updated Time, Speed.

### Module Mappings with Core ERPNext

Accounts: On submitting a Bus Ticket Booking or Cargo Booking, auto-generate and submit a Sales Invoice (or Payment Entry) against a default Walk-in Customer, posting revenue to "Bus Ticket Revenue" or "Cargo Freight Revenue" accounts.

Assets: Bus Vehicle links directly to an ERPNext Asset for fuel tracking and maintenance logs.

HR & Payroll: Driver/Conductor trips on the Bus Trip DocType feed trip allowance data into Payroll.

Buying & Stock: Fuel Entry logging tied to Bus Vehicles via Stock Entry / Purchase Receipt.

### Workspace & UI

A dedicated "Transport Management" Workspace with shortcuts/cards: POS Ticketing Desk, Cargo Booking Desk, Active Trips & Schedules, Daily Revenue & Occupancy Reports.

A custom Page "Bus Ticket POS": a visual seat grid (HTML/JS) showing available/selected/booked seats for quick booking.

### Reports & Print Formats

Query Reports: Daily Route-wise Revenue Summary, Bus Occupancy Rate Report, Cargo Manifest Report (Per Trip).

Print Formats: Thermal Bus Ticket Print Format (80mm) with QR Code, Cargo Booking Receipt & Waybill Print Format.

## Setup

Get the app from this repository:

bench get-app tms_app https://github.com/muhammadfaizanmf02-spec/tms_app.git

Install it on a site:

bench --site your-site-name install-app tms_app

## Documentation

See FUNCTIONAL_DOC.md and TECHNICAL_DOC.md (to be added) for detailed workflow, user roles, and architecture documentation.

## License

MIT
