import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="NEXORA 2026",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SAMPLE DATA ----------------
if "tickets" not in st.session_state:
    st.session_state.tickets = []

if "student" not in st.session_state:
    st.session_state.student = {
        "name": "Nemo",
        "student_id": "NX2026-001",
        "course": "Data Science with AI",
        "email": ""
    }

# ---------------- ISSUE CLASSIFIER ----------------
def classify_issue(message):
    text = message.lower()

    categories = {
        "Payment": ["payment", "fee", "fees", "refund", "transaction"],
        "Attendance": ["attendance", "absent", "present"],
        "Course": ["course", "class", "lesson", "subject", "learning"],
        "Technical": ["login", "password", "website", "error", "technical"],
        "Certificate": ["certificate", "certification"],
    }

    for category, keywords in categories.items():
        if any(word in text for word in keywords):
            priority = (
                "High" if any(word in text for word in
                ["urgent", "emergency", "blocked", "deadline"])
                else "Medium"
            )
            return category, priority

    return "General", "Medium"


# ---------------- SIDEBAR ----------------
st.sidebar.title("🎓 NEXORA 2026")
st.sidebar.caption("Student Support Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "My Profile",
        "Academic Progress",
        "Student Support",
        "Admin Dashboard"
    ]
)

st.sidebar.divider()
st.sidebar.write("Logged in as")
st.sidebar.write(f"👤 {st.session_state.student['name']}")
st.sidebar.caption("Prototype mode")


# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("🎓 Student Dashboard")
    st.write(
        f"Welcome, {st.session_state.student['name']}! "
        "Manage your academic journey here."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Attendance", "90%")
    col2.metric("Assignments", "8/10")
    col3.metric("Course Progress", "80%")
    col4.metric("Support Tickets", len(st.session_state.tickets))

    st.divider()
    st.subheader("📚 My Course")
    st.info("Data Science with AI")

    st.progress(0.8, text="Learning progress: 80%")

    st.subheader("📢 Announcements")
    st.success("Welcome to NEXORA! Keep learning and tracking your progress.")
    st.warning("Please check your attendance and assignment records regularly.")

    st.subheader("🆘 Need Help?")
    st.write(
        "Visit Student Support to submit a complaint "
        "and receive an automatically suggested category."
    )


# ---------------- STUDENT PROFILE ----------------
elif page == "My Profile":
    st.title("👤 My Profile")

    with st.form("profile_form"):
        name = st.text_input(
            "Full Name",
            value=st.session_state.student["name"]
        )
        student_id = st.text_input(
            "Student ID",
            value=st.session_state.student["student_id"]
        )
        course = st.text_input(
            "Enrolled Course",
            value=st.session_state.student["course"]
        )
        email = st.text_input(
            "Email",
            value=st.session_state.student["email"]
        )

        submitted = st.form_submit_button("Save Profile")

        if submitted:
            if name.strip() and student_id.strip():
                st.session_state.student = {
                    "name": name.strip(),
                    "student_id": student_id.strip(),
                    "course": course.strip(),
                    "email": email.strip()
                }
                st.success("Profile updated successfully!")
            else:
                st.error("Name and Student ID are required.")


# ---------------- ACADEMIC PROGRESS ----------------
elif page == "Academic Progress":
    st.title("📊 Academic Progress")

    st.subheader("Course: Data Science with AI")

    subjects = pd.DataFrame({
        "Subject": [
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning"
        ],
        "Progress (%)": [85, 70, 65, 50],
        "Status": [
            "In Progress",
            "In Progress",
            "In Progress",
            "In Progress"
        ]
    })

    st.dataframe(subjects, use_container_width=True, hide_index=True)

    st.subheader("Attendance")
    st.progress(0.9, text="90% attendance")

    st.subheader("Assignments")
    st.write("Completed: 8 out of 10")
    st.progress(0.8)


# ---------------- STUDENT SUPPORT ----------------
elif page == "Student Support":
    st.title("🤖 AI Student Support")
    st.write(
        "Describe your issue below. The system will "
        "suggest a category and priority automatically."
    )

    with st.form("support_form"):
        student_name = st.text_input(
            "Your Name",
            value=st.session_state.student["name"]
        )

        issue = st.text_area(
            "Describe your issue",
            placeholder="Example: I have a problem with my course payment..."
        )

        submitted = st.form_submit_button("Submit Complaint")

        if submitted:
            if student_name.strip() and issue.strip():
                category, priority = classify_issue(issue)

                ticket = {
                    "Ticket ID": f"NX-{1001 + len(st.session_state.tickets)}",
                    "Student": student_name.strip(),
                    "Issue": issue.strip(),
                    "Category": category,
                    "Priority": priority,
                    "Status": "Open",
                    "Date": datetime.now().strftime("%d-%m-%Y %H:%M")
                }

                st.session_state.tickets.append(ticket)

                st.success("Your complaint has been submitted!")
                st.write(f"**Ticket ID:** {ticket['Ticket ID']}")
                st.write(f"**Suggested Category:** {category}")
                st.write(f"**Priority:** {priority}")
                st.info("Your ticket is currently Open.")
            else:
                st.error("Please enter your name and issue.")

    st.divider()
    st.subheader("📋 My Support Tickets")

    my_tickets = [
        t for t in st.session_state.tickets
        if t["Student"].lower() == st.session_state.student["name"].lower()
    ]

    if my_tickets:
        st.dataframe(
            pd.DataFrame(my_tickets),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("You have not submitted any tickets yet.")


# ---------------- ADMIN DASHBOARD ----------------
elif page == "Admin Dashboard":
    st.title("🛠️ Admin Dashboard")
    st.write("Monitor student support requests.")

    tickets = st.session_state.tickets

    total = len(tickets)
    open_count = sum(t["Status"] == "Open" for t in tickets)
    resolved = sum(t["Status"] == "Resolved" for t in tickets)
    high_priority = sum(t["Priority"] == "High" for t in tickets)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tickets", total)
    col2.metric("Open", open_count)
    col3.metric("Resolved", resolved)
    col4.metric("High Priority", high_priority)

    st.divider()
    st.subheader("📋 Manage Complaints")

    if tickets:
        for i, ticket in enumerate(tickets):
            with st.expander(
                f"{ticket['Ticket ID']} | {ticket['Category']} | "
                f"{ticket['Status']}"
            ):
                st.write(f"**Student:** {ticket['Student']}")
                st.write(f"**Issue:** {ticket['Issue']}")
                st.write(f"**Priority:** {ticket['Priority']}")
                st.write(f"**Submitted:** {ticket['Date']}")

                new_status = st.selectbox(
                    "Update Status",
                    ["Open", "In Progress", "Resolved"],
                    index=[
                        "Open", "In Progress", "Resolved"
                    ].index(ticket["Status"]),
                    key=f"status_{i}"
                )

                if new_status != ticket["Status"]:
                    ticket["Status"] = new_status
                    st.success("Ticket status updated.")
    else:
        st.info("No complaints have been submitted yet.")

    if tickets:
        st.subheader("📈 Complaints by Category")
        category_data = pd.DataFrame(tickets)
        st.bar_chart(category_data["Category"].value_counts())


# ---------------- FOOTER ----------------
st.sidebar.divider()
st.sidebar.caption("NEXORA 2026 | Prototype")