# TMS App - Business Flow and Functional Document

## 1. Purpose

TMS App is built for a large-scale bus transport company operating close to 100 buses across multiple routes. It covers passenger ticket booking through POS, cargo/parcel booking, trip and vehicle scheduling, and live GPS tracking, all inside Frappe/ERPNext using standard DocTypes, list views, forms, a Workspace, Reports and a Print Format - the same way any other ERPNext module works for a client.

## 2. Core Master Data

Bus Station: every pickup/drop point the company operates from. Fields cover station name, city, state, address and GPS coordinates, and act as the base for routes and cargo source/destination.

Bus Route: a lane between two stations (source and destination), with distance, estimated duration and a base fare. Each Bus Trip is scheduled against a Bus Route.

Bus Vehicle: the physical bus/coach - vehicle number, vehicle type (Standard, Deluxe, Sleeper, Luxury), total seats, driver name and contact, and current status (Active, Under Maintenance, Inactive). With ~100 buses, this becomes the fleet register.

Seat Layout: reusable seating templates (rows, columns, total seats) per vehicle type, so new vehicles can be configured quickly without redefining seating each time.

## 3. Operational Flow

Trip Scheduling: dispatch staff create a Bus Trip by picking a Route and a Vehicle, then set departure date/time, arrival time, available seats and fare. The Trip status moves through Scheduled, Departed, Completed or Cancelled as the day progresses. This is the record every ticket and cargo booking is linked back to.

Ticket Booking (POS flow): a booking clerk opens Bus Ticket Booking (or the POS screen once wired in), selects the Trip, enters customer name/contact and seat number, and the fare, discount and paid amount are captured. Payment Mode (Cash, Card, Online) and Status (Booked, Cancelled, Completed) are tracked on the same record, and a Sales Order link is kept for accounting reference - the same pattern used by the existing POS booking customisation in frappe_custom_app.

Cargo Booking: parcel/courier bookings capture sender and receiver details, source and destination station, an optional linked Trip, item description, weight and cargo charges. Status moves through Booked, In Transit, Delivered or Cancelled, and it also keeps a Sales Order link for billing.

Live Tracking: Bus Live Tracking stores GPS pings (latitude, longitude, speed, heading, timestamp, status) against a Vehicle and optionally a Trip. A tracking device or mobile app can push records here at intervals so dispatch can see where each bus is at any moment.

## 4. Day-to-day Usage by a Client

A new client using this app would: set up their Bus Stations and Routes once, register their fleet as Bus Vehicles with Seat Layouts, then every day create Bus Trips for the buses going out. Front counter or POS staff create Bus Ticket Booking and Cargo Booking records against those trips as customers arrive, and dispatch/tracking staff (or an automated GPS feed) keep Bus Live Tracking updated. Everything shows up in normal ERPNext list views and forms, with the TMS Workspace giving one place to reach every doctype.

## 5. Workspace, Reports and Print Format

The TMS Workspace groups the doctypes into Masters (Bus Station, Bus Route, Bus Vehicle, Seat Layout), Trips and Bookings (Bus Trip, Bus Ticket Booking, Cargo Booking) and Tracking (Bus Live Tracking), with quick-create shortcuts for the three doctypes staff use most often: Bus Ticket Booking, Cargo Booking and Bus Trip.

Bus Ticket Booking Summary is a ready-made Query Report listing trip, customer, seat, booking date, fare, discount, paid amount, payment mode and status - useful for daily reconciliation.

Bus Ticket Print is a standard Print Format for Bus Ticket Booking so a physical/PDF ticket can be handed to the passenger, mirroring how a normal POS invoice prints.

## 6. Module Mapping to ERPNext

TMS doctypes are designed to sit alongside core ERPNext rather than replace it. Bus Ticket Booking and Cargo Booking both keep a Sales Order link so revenue still flows through ERPNext's Accounts module for invoicing and payment entries. Bus Vehicle can optionally be mirrored as an Asset record in the Assets module for depreciation/maintenance tracking, and Driver details can later be linked to HR & Payroll (Employee) if drivers are added as staff. Stock/Buying is not required for the core flow since bus/cargo booking is a service, not an inventory item.

## 7. Setup Instructions

Install with the standard Frappe app flow: `bench get-app https://github.com/muhammadfaizanmf02-spec/tms_app` on your bench, then `bench --site your-site install-app tms_app`, then `bench --site your-site migrate` to create the doctypes. ERPNext must already be installed on the same site since Sales Order links are used.

## 8. Status

Repository scaffold, all 8 DocTypes (JSON + controller), the TMS Workspace, one Print Format and one Report are committed to this repository and ready to install on a site. Deep POS-screen integration for booking (similar to the existing frappe_custom_app booking POS) and the Bus Live Tracking ingestion endpoint are the next build phase once this base is confirmed on your bench.


Repository scaffold, all 8 DocTypes (JSON + controller), the TMS Workspace, one Print Format and one Report are committed to this repository and ready to install on a site. Deep POS-screen integration for booking (similar to the existing frappe_custom_app booking POS) and the Bus Live Tracking ingestion endpoint are the next build phase once this base is confirmed on your bench.
