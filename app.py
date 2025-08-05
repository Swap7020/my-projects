import streamlit as st
from auth import get_user_contact
from auth import create_user_table, add_user, login_user
from backend import create_booking_table, save_booking, get_all_bookings, get_user_bookings, update_booking_status

# ---------- INITIAL SETUP ----------
st.set_page_config(page_title="Driver Booking App", layout="centered")

create_user_table()
create_booking_table()

# ---------- LOGIN SESSION HANDLING ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# ---------- LOGIN / SIGNUP ----------
if not st.session_state.logged_in:
    st.title("🔐 Login to Continue")

    menu = st.selectbox("Login / Sign Up", ["Login", "Sign Up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Login":
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user[0]
                st.session_state.role = user[2]
                st.success(f"Welcome {user[0]} ({user[2]})")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    else:
        role = st.radio("Select Role", ["User", "Driver"])
        contact = st.text_input("contact  Info (phone/Email)")
        if st.button("Create Account"):
            try:
                add_user(username, password, role,contact)
                st.success("Account created! Please log in.")
            except:
                st.warning("Username already exists.")
    st.stop()

# ---------- LOGOUT BUTTON ----------
with st.sidebar:
    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.success("You have been logged out.")
        st.rerun()

# ---------- AFTER LOGIN ----------
st.title("🚗 Temporary Driver Booking App")
st.write(f"Logged in as: **{st.session_state.username}** ({st.session_state.role})")

# ---------- USER VIEW ----------
if st.session_state.role == "User":
    st.header("📅 Book a Driver")

    location = st.text_input("Pickup Location")
    date = st.date_input("Date")
    time = st.time_input("Time")
    duration = st.selectbox("Duration (in hours)", [1, 2, 3, 4, 5, 6])
    vehicle_type = st.selectbox("Vehicle Type", ["Car", "SUV", "Truck", "Other"])

    if st.button("Book Now"):
        save_booking(
            user=st.session_state.username,
            location=location,
            date=str(date),
            time=str(time),
            duration=duration,
            vehicle_type=vehicle_type
        )
        st.success("✅ Booking placed!")

    st.subheader("📋 Your Bookings")
    user_bookings = get_user_bookings(st.session_state.username)
    if not user_bookings:
        st.info("No bookings made yet.")
    else:
        for booking in user_bookings:
            user_contact = get_user_contact(booking[1])
            st.text(f"Contact: {user_contact}")
            st.text(f"Booking #{booking[0]} | {booking[3]} {booking[4]} - {booking[6]}")
            st.text(f"Status: {booking[7]}")
            st.markdown("---")

# ---------- DRIVER VIEW ----------
elif st.session_state.role == "Driver":
    st.header("👨‍✈️ Available Bookings")

    bookings = get_all_bookings()
    pending_bookings = [b for b in bookings if b[7] == "Pending"]

    if not pending_bookings:
        st.info("No pending bookings.")
    else:
        for booking in pending_bookings:
            st.subheader(f"📍 Booking ID: {booking[0]}")
            st.text(f"User: {booking[1]}")
            st.text(f"Location: {booking[2]}")
            st.text(f"Date: {booking[3]} | Time: {booking[4]}")
            st.text(f"Duration: {booking[5]} hr(s)")
            st.text(f"Vehicle: {booking[6]}")
            st.text(f"Status: {booking[7]}")

            if st.button(f"✅ Accept Booking #{booking[0]}", key=f"accept_{booking[0]}"):
                update_booking_status(booking[0], "Accepted by " + st.session_state.username)
                st.success(f"Booking #{booking[0]} accepted.")
                st.rerun()
            st.markdown("---")
