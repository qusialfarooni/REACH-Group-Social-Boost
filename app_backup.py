import streamlit as st
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
import random
import string
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(
    page_title="REACH Social Boost",
    page_icon="📢",
    layout="wide"
)

# Custom CSS for REACH Group Branding
st.markdown("""
    <style>
    /* Main background and text */
    .stApp {
        background-color: #F7F8FA;
        color: #1F2937;
    }
    /* Font for the entire app */
    html, body, [class*="st-"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Corporate Headers */
    .main-header {
        color: #0B1F3A;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        padding-top: 1rem;
    }
    .sub-header {
        color: #C8A24A;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E5E7EB;
        width: 100%; /* Ensure it spans the width */
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0B1F3A;
        border-right: 1px solid #E6E8EC;
    }
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio > label {
        color: #FFFFFF !important;
    }
    .sidebar-section {
        color: #C8A24A !important;
        font-weight: 700;
        font-size: 0.9rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding-left: 1rem; /* Indent section titles */
        border-bottom: 1px solid rgba(200, 162, 74, 0.3); /* Gold accent line */
        padding-bottom: 0.3rem;
    }
    
    /* Cards and Containers */
    .reach-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }
    .reach-card h2, .reach-card h3 {
        color: #0B1F3A;
        margin-top: 0;
        margin-bottom: 1rem;
    }

    /* Buttons */
    .stButton > button {
        background-color: #0B1F3A;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #C8A24A; /* Gold accent on hover */
        color: #0B1F3A;
    }
    /* Primary buttons (e.g., Submit Engagement) */
    .stButton > button[kind="primary"] {
        background-color: #C8A24A;
        color: #0B1F3A;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #0B1F3A;
        color: white;
    }

    /* Text Inputs and Select Boxes */
    .stTextInput > div > div > input, .stSelectbox > div > div > div > div > div > input {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 8px 12px;
    }

    /* Success/Error Messages */
    .stAlert > div {
        border-radius: 8px;
    }
    .stAlert > div[data-testid="stAlert-success"] {
        background-color: #D1FAE5; /* Light green */
        color: #065F46; /* Darker green text */
        border-left: 5px solid #16A34A; /* Success green */
    }
    .stAlert > div[data-testid="stAlert-error"] {
        background-color: #FEE2E2; /* Light red */
        color: #991B1B; /* Darker red text */
        border-left: 5px solid #DC2626; /* Error red */
    }
    .stAlert > div[data-testid="stAlert-warning"] {
        background-color: #FEF3C7; /* Light yellow */
        color: #92400E; /* Darker yellow text */
        border-left: 5px solid #F59E0B; /* Warning orange */
    }

    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="reach-card" style="background-color: #0B1F3A; color: white; padding: 30px; margin-bottom: 20px;">'
            '<div class="main-header" style="color: white;">REACH Social Boost</div>'
            '<div class="sub-header" style="color: #C8A24A; border-bottom: 1px solid rgba(200, 162, 74, 0.5);">Employee advocacy dashboard for boosting company social media engagement.</div>'
            '</div>', unsafe_allow_html=True)

# File paths
USERS_FILE = "users.csv"
PASSWORD_RESETS_FILE = "password_resets.csv"
ENGAGEMENT_FILE = "engagement_points.csv"
POSTS_FILE = "posts.csv"
LOG_FILE = "notification_logs.csv"


# Create users file if not exists (now includes password)
if not os.path.exists(USERS_FILE):
    users_data = pd.DataFrame(columns=["name", "email", "department", "role", "status", "password"])
    # Seed with initial admin user
    initial_admin = pd.DataFrame([{
        "name": "Qusai Omar",
        "email": "qusialfarooni@gmail.com",
        "department": "Marketing",
        "role": "Admin",
        "status": "Active",
        "password": "12345"
    }])
    users_data = pd.concat([users_data, initial_admin], ignore_index=True)
    users_data.to_csv(USERS_FILE, index=False)

# Migration Logic: Merge old employees.csv into users.csv if it exists
OLD_EMPLOYEES_FILE = "employees.csv"
if os.path.exists(OLD_EMPLOYEES_FILE):
    try:
        current_users = pd.read_csv(USERS_FILE)
        old_employees = pd.read_csv(OLD_EMPLOYEES_FILE)
        
        new_users_to_add = []
        for _, row in old_employees.iterrows():
            emp_email = str(row['email']).strip()
            # Avoid duplicates by checking if the email already exists in users.csv
            if emp_email.lower() not in current_users['email'].str.lower().values:
                new_users_to_add.append({
                    "name": row['employee_name'],
                    "email": emp_email,
                    "department": row['department'],
                    "role": "Employee",
                    "status": row['status'],
                    "password": "12345"
                })
        
        if new_users_to_add:
            updated_users = pd.concat([current_users, pd.DataFrame(new_users_to_add)], ignore_index=True)
            updated_users.to_csv(USERS_FILE, index=False)
        
        # Mark as migrated by renaming the file
        os.rename(OLD_EMPLOYEES_FILE, OLD_EMPLOYEES_FILE + ".migrated")
    except Exception as e:
        st.error(f"Migration from employees.csv failed: {e}")

# Create password resets file if not exists
if not os.path.exists(PASSWORD_RESETS_FILE):
    reset_data = pd.DataFrame(columns=["email", "reset_code", "expiration_time"])
    reset_data.to_csv(PASSWORD_RESETS_FILE, index=False)

# Create engagement file if not exists
if not os.path.exists(ENGAGEMENT_FILE):
    engagement_data = pd.DataFrame(columns=[
        "employee_email",
        "post_title",
        "platform",
        "post_link",
        "liked",
        "commented",
        "shared",
        "points",
        "date"
    ])
    engagement_data.to_csv(ENGAGEMENT_FILE, index=False)

# Create posts file if not exists
if not os.path.exists(POSTS_FILE):
    posts_data = pd.DataFrame(columns=["platform", "post_title", "post_link", "date"])
    # Seed with an initial post
    initial_post = pd.DataFrame([{
        "platform": "LinkedIn",
        "post_title": "Welcome to REACH Social Boost!",
        "post_link": "https://www.linkedin.com/company/reach-group/",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    posts_data = pd.concat([posts_data, initial_post], ignore_index=True)
    posts_data.to_csv(POSTS_FILE, index=False)

# Create log file if not exists
if not os.path.exists(LOG_FILE):
    log_data = pd.DataFrame(columns=["date_time", "email", "status", "error_reason"])
    log_data.to_csv(LOG_FILE, index=False)

def log_notification(email, status, error=""):
    """Logs notification results to a CSV file."""
    log_entry = pd.DataFrame([{
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "email": email,
        "status": status,
        "error_reason": error
    }])
    old_logs = pd.read_csv(LOG_FILE)
    updated_logs = pd.concat([old_logs, log_entry], ignore_index=True)
    updated_logs.to_csv(LOG_FILE, index=False)

def send_email(receiver_email, subject, body):
    """Sends an email using SMTP settings from Streamlit secrets."""
    try:
        # Safely fetch SMTP configuration
        try:
            smtp_conf = st.secrets["smtp"]
        except Exception:
            return False, "SMTP configuration is missing. Please create C:\\Users\\Qusai\\.streamlit\\secrets.toml and add SMTP settings."
        
        # 2 & 3. Read values correctly from secrets
        sender_email = st.secrets["smtp"]["sender_email"]
        sender_password = st.secrets["smtp"]["sender_password"]
        smtp_server = st.secrets["smtp"]["smtp_server"]
        smtp_port = int(st.secrets["smtp"]["smtp_port"])
        
        # 4. Removes spaces from the app password before login
        sender_password = sender_password.replace(" ", "").strip()

        if not all([smtp_server, smtp_port, sender_email, sender_password]):
            return False, "Missing SMTP credentials in secrets (email, password, server, or port)."

        msg = MIMEMultipart()
        # 5. The From email matches the Gmail login email
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # 1. Use Gmail SMTP SSL correctly
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                # 6. The login uses provided variables
                server.login(sender_email, sender_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

        return True, None
    except smtplib.SMTPAuthenticationError as e:
        # 7. Shows the exact Gmail error if authentication fails
        return False, f"SMTP Authentication Failed: {str(e)}. Please verify your App Password and ensure it has no spaces."
    except Exception as e:
        return False, str(e)

def generate_reset_code(length=6):
    """Generates a random alphanumeric reset code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def send_reset_code_email(receiver_email, reset_code):
    """Sends an email with the password reset code."""
    subject = "REACH Social Boost - Password Reset Request"
    app_link = "http://localhost:8501" # Or the deployed app link
    body = (
        f"Hello,\n\nYou have requested a password reset for your REACH Social Boost account.\n\n"
        f"Your password reset code is: **{reset_code}**\n\n"
        f"Please use this code to reset your password within the app. "
        f"Go to the app and click on 'Forgot Password?' then enter this code.\n\n"
        f"App Link: {app_link}\n\n"
        f"If you did not request a password reset, please ignore this email.\n\n"
        f"Best regards,\nREACH Social Boost Team"
    )
    success, error = send_email(receiver_email, subject, body)
    if not success:
        log_notification(receiver_email, "Failed", f"Failed to send reset code email: {error}")
    return success, error


def notify_employees(platform, title, link, selected_emails):
    """Sends notifications to active employees via Microsoft Teams and Email."""
    # 1. Microsoft Teams Notification (Preferred)
    # Replace 'YOUR_TEAMS_WEBHOOK_URL' with your actual Microsoft Teams Incoming Webhook URL
    TEAMS_WEBHOOK_URL = "YOUR_TEAMS_WEBHOOK_URL"
    
    if TEAMS_WEBHOOK_URL != "YOUR_TEAMS_WEBHOOK_URL":
        teams_payload = {
            "text": f"📢 **New Social Media Post Published!**\n\n"
                    f"**Platform:** {platform}\n"
                    f"**Title:** {title}\n"
                    f"**Suggested Actions:** Like, Comment, and Share/Repost to boost our reach! 🚀\n\n"
                    f"**Link:** [Open Social Media Post]({link})"
        }
        try:
            requests.post(TEAMS_WEBHOOK_URL, json=teams_payload, timeout=5)
        except Exception as e:
            st.warning(f"Could not send Teams notification: {e}")

    # 2. Email Notification (Backup)
    if selected_emails:
        subject = f"New REACH Social Post: {title}"
        app_link = "http://localhost:8501"
        body = (
            f"Hello,\n\nA new company post has been published on {platform}.\n\n"
            f"1. Post Title: {title}\n"
            f"2. Post Link: {link}\n"
            f"3. Required Actions: Like, Comment, and Share/Repost\n"
            f"4. REACH Social Boost App Link: {app_link}\n"
            f"5. Reminder: After engaging with the post, please open REACH Social Boost and submit your completed actions to collect points.\n\n"
            f"Best regards,\nMarketing Team"
        )
        for email in selected_emails:
            send_email(email, subject, body)

# Login System
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.header("Login")
    login_email_input = st.text_input("Enter your company email to login")
    login_password_input = st.text_input("Enter your password", type="password")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="reach-card">', unsafe_allow_html=True)
        st.subheader("Login")
        login_email_input = st.text_input("Company Email")
        login_password_input = st.text_input("Password", type="password")
        
    if st.button("Login"):
        if os.path.exists(USERS_FILE):
            users = pd.read_csv(USERS_FILE)
            if users.empty:
                st.error("The user database is empty. Please add an Admin user to users.csv manually to proceed.")
            else:
                # 2. Strips spaces from email and password
                login_email = login_email_input.strip()
                login_password = login_password_input.strip()

                # 3. Compares email in lowercase
                user_match = users[users['email'].str.lower() == login_email.lower()]
                
                if user_match.empty:
                    # 6. Shows a clear error if the email is not found
                    st.error("Email not found. Please check your email address.")
                else:
                    user_data = user_match.iloc[0]
                    
                    # 1, 2, 3, 4. Converts password from CSV to string, removes spaces, and compares correctly
                    input_password_stripped = login_password.strip()
                    stored_password_stripped = str(user_data['password']).strip()

                    if input_password_stripped != stored_password_stripped:
                        # 6. Shows a clear error if the password does not match
                        st.error("Invalid password. Please try again.")
                    # 4. Checks that status is Active
                    elif user_data['status'] == 'Inactive':
                        st.error("Your account is inactive. Please contact an administrator.")
                    # 5. Checks that role is Admin or Employee
                    elif user_data['role'] not in ['Admin', 'Employee']:
                        st.error("Your account has an unrecognized role. Please contact an administrator.")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user_email = user_data['email'] # Store original casing
                        st.session_state.user_role = user_data['role']
                        st.session_state.user_name = user_data['name']
                        st.rerun()
        else:
            st.error("User database not found. Please create users.csv.")

    st.markdown("---")
    st.subheader("Forgot Password?")
    forgot_email_input = st.text_input("Enter your email to reset password", key="forgot_email")
    if st.button("Send Reset Code"):
        forgot_email = forgot_email_input.strip() # Strip spaces
        users = pd.read_csv(USERS_FILE)
        user_row = users[users['email'] == forgot_email]
        if user_row.empty or user_row.iloc[0]['status'] == 'Inactive':
            st.error("Email not found or account is inactive.")
        else:
            reset_code = generate_reset_code()
            expiration_time = datetime.now() + timedelta(minutes=15) # Code valid for 15 minutes

            # Store reset code
            reset_data = pd.read_csv(PASSWORD_RESETS_FILE)
            new_reset_entry = pd.DataFrame([{
                "email": forgot_email,
                "reset_code": reset_code,
                "expiration_time": expiration_time.strftime("%Y-%m-%d %H:%M:%S")
            }])
            updated_reset_data = pd.concat([reset_data, new_reset_entry], ignore_index=True)
            updated_reset_data.to_csv(PASSWORD_RESETS_FILE, index=False)

            # Send email
            success, error = send_reset_code_email(forgot_email, reset_code)
            if success:
                st.success("A password reset code has been sent to your email.")
            else:
                st.error(f"Failed to send reset code: {error}")

    st.markdown("---")
    st.subheader("Reset Password")
    reset_email = st.text_input("Your email", key="reset_email_confirm")
    received_code = st.text_input("Reset Code", key="received_code")
    new_password = st.text_input("New Password", type="password", key="new_password")
    confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")

    if st.button("Reset Password"):
        if new_password != confirm_new_password:
            st.error("New passwords do not match.")
        elif not new_password:
            st.error("Password cannot be empty.")
        else:
            reset_data = pd.read_csv(PASSWORD_RESETS_FILE)
            # Filter for valid, non-expired codes for this email
            valid_codes = reset_data[
                (reset_data["email"] == reset_email) &
                (reset_data["reset_code"] == received_code)
            ]
            
            if valid_codes.empty:
                st.error("Invalid or expired reset code.")
            else:
                # Check expiration
                latest_code_entry = valid_codes.sort_values(by="expiration_time", ascending=False).iloc[0]
                expiration_time = datetime.strptime(latest_code_entry["expiration_time"], "%Y-%m-%d %H:%M:%S")

                if datetime.now() > expiration_time:
                    st.error("Reset code has expired.")
                else:
                    users = pd.read_csv(USERS_FILE)
                    if reset_email not in users["email"].values:
                        st.error("User not found.")
                    else:
                        users.loc[users["email"] == reset_email, "password"] = new_password
                        users.to_csv(USERS_FILE, index=False)
                        
                        # Remove used reset code
                        reset_data = reset_data.drop(valid_codes.index)
                        reset_data.to_csv(PASSWORD_RESETS_FILE, index=False)
                        
                        st.success("Your password has been reset successfully. You can now log in.")
    st.stop()

# Sidebar Menu based on Role
if st.session_state.user_role == "Admin":
    menu_options = ["Employee Engagement", "Leaderboard", "Admin - Manage Posts", "Admin - Manage Users", "Admin - Manage Admins", "Change Password"]
else:
    menu_options = ["Employee Engagement", "Leaderboard", "Change Password"]

menu = st.sidebar.radio("Choose Page", menu_options)

st.sidebar.divider()
st.sidebar.write(f"Logged in as: **{st.session_state.user_name}**")
st.sidebar.write(f"Role: {st.session_state.user_role}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()


if menu == "Employee Engagement":
    st.markdown('<div class="main-header">Employee Engagement</div>', unsafe_allow_html=True)

    # Card for Employee Email
    st.markdown('<div class="reach-card">', unsafe_allow_html=True)
    st.subheader("Your Information")
    employee_email = st.text_input("Your company email", value=st.session_state.user_email, disabled=True, key="employee_email_display")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Fetch all posts
    posts = pd.read_csv(POSTS_FILE)
    
    if posts.empty:
        st.markdown('<div class="reach-card"><p>No posts available to engage with.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="reach-card">', unsafe_allow_html=True)
        st.subheader("Select Post")
        # Create a list of post titles for selection, showing newest first and including platform/date
        post_options_display = [f"{row['post_title']} ({row['platform']} - {row['date'].split(' ')[0]})" for index, row in posts.iloc[::-1].iterrows()]
        selected_post_display = st.selectbox("Choose the post you engaged with:", post_options_display, key="post_selector")
        
        # Find the actual post data based on the selected display string
        selected_index = post_options_display.index(selected_post_display)
        selected_post = posts.iloc[::-1].iloc[selected_index] # Get the corresponding row from the reversed DataFrame
        platform = selected_post["platform"]
        post_link = selected_post["post_link"]
        st.markdown('</div>', unsafe_allow_html=True)

        col_left, col_right = st.columns(2) # Define columns here

        with col_left:
            st.markdown('<div class="reach-card">', unsafe_allow_html=True)
            st.subheader("Post Details")
            st.write(f"**Platform:** {platform}")
            st.link_button("Open Social Media Post", post_link)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right: # Corrected from col_b to col_right
            st.markdown('<div class="reach-card">', unsafe_allow_html=True)
            st.subheader("Mark Your Actions")
            liked = st.checkbox("I liked the post")
            commented = st.checkbox("I commented on the post")
            shared = st.checkbox("I shared / reposted the post")
            
            points_preview = (5 if liked else 0) + (10 if commented else 0) + (20 if shared else 0)
            st.markdown(f"**Points to Earn: {points_preview}**")

        if st.button("Submit Engagement", type="primary", key="submit_engagement_button"):
            if employee_email == "":
                st.error("Please enter your email first.")
            else:
                # Check for duplicate submission
                engagement_data = pd.read_csv(ENGAGEMENT_FILE)
                already_submitted = not engagement_data[
                    (engagement_data["employee_email"] == employee_email) & 
                    (engagement_data["post_link"] == post_link) # Check by post link for uniqueness
                ].empty

                if already_submitted:
                    st.warning(f"You have already submitted engagement for '{selected_post['post_title']}'. Duplicate claims are not allowed.")
                else:
                    points = 0
                    if liked: points += 5
                    if commented: points += 10
                    if shared: points += 20

                    if points == 0:
                        st.warning("Please select at least one action you performed.")
                    else:
                        new_record = pd.DataFrame([{
                            "employee_email": employee_email,
                            "post_title": selected_post['post_title'], # Use selected_post['post_title']
                            "platform": platform,
                            "post_link": post_link,
                            "liked": liked,
                            "commented": commented,
                            "shared": shared,
                            "points": points,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }])

                        updated_data = pd.concat([engagement_data, new_record], ignore_index=True)
                        updated_data.to_csv(ENGAGEMENT_FILE, index=False)

                        st.success(f"Success! You earned {points} points for your engagement on '{selected_post['post_title']}'.")
            st.markdown('</div>', unsafe_allow_html=True) # Close the col_right card


elif menu == "Leaderboard":
    st.markdown('<div class="main-header">Leaderboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">See who\'s leading the engagement!</div>', unsafe_allow_html=True)

    def highlight_top_3(row):
        """Applies a background color to the top 3 rows."""
        if row.name == 0: # First place
            return ['background-color: #C8A24A; color: white; font-weight: bold;'] * len(row)
        elif row.name == 1: # Second place
            return ['background-color: #C0C0C0; color: white; font-weight: bold;'] * len(row)
        elif row.name == 2: # Third place
            return ['background-color: #CD7F32; color: white; font-weight: bold;'] * len(row)
        return [''] * len(row)

    data = pd.read_csv(ENGAGEMENT_FILE)
    users = pd.read_csv(USERS_FILE)

    if data.empty:
        st.markdown('<div class="reach-card"><p>No engagement submitted yet.</p></div>', unsafe_allow_html=True)
    else:
        # Merge engagement data with user data to get department info
        merged_data = data.merge(users[['email', 'department']], left_on='employee_email', right_on='email', how='left')
        
        st.markdown('<div class="reach-card">', unsafe_allow_html=True)
        st.subheader("Leaderboard Filters")
        col_filter, col_empty = st.columns([0.5, 0.5])
        with col_filter:
            departments = ["All Departments"] + sorted(users['department'].unique().tolist())
            selected_dept = st.selectbox("Filter by Department", departments, key="dept_filter")
            if selected_dept != "All Departments":
                merged_data = merged_data[merged_data['department'] == selected_dept]
        
        if merged_data.empty:
            st.info(f"No engagement found for the {selected_dept} department.")
        else:
            # Aggregate points by email and department
            leaderboard = merged_data.groupby(["employee_email", "department"])["points"].sum().reset_index()
            leaderboard = leaderboard.sort_values(by="points", ascending=False).reset_index(drop=True)
            
            leaderboard = leaderboard.rename(columns={
                "employee_email": "Employee Email",
                "department": "Department",
                "points": "Total Points"
            })

            st.dataframe(leaderboard.style.apply(highlight_top_3, axis=1), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)


elif menu == "Admin - Manage Posts":
    st.markdown('<div class="main-header">Admin - Manage Posts</div>', unsafe_allow_html=True)
    
    # Proactive check for SMTP configuration with safe logic
    try:
        _ = st.secrets["smtp"]
    except Exception:
        st.error("SMTP configuration is missing. Please create C:\\Users\\Qusai\\.streamlit\\secrets.toml and add SMTP settings.")
        st.stop()
    st.markdown('<div class="reach-card">', unsafe_allow_html=True)
    st.subheader("Publish New Post")
    with st.form("new_post_form", clear_on_submit=True):
        new_platform = st.selectbox("Platform", ["LinkedIn", "Twitter", "Facebook", "Instagram", "Other"], key="new_post_platform")
        new_title = st.text_input("Post Title", key="new_post_title")
        new_link = st.text_input("Post Link", key="new_post_link")
        
        st.markdown("---")
        st.subheader("Select Email Recipients")
        users_df = pd.read_csv(USERS_FILE)
        active_users = users_df[users_df["status"] == "Active"]
        active_user_emails = active_users["email"].tolist()

        select_all = st.checkbox("Select All Active Users", key="select_all_recipients")
        if select_all:
            recipients = st.multiselect("Select users to notify:", active_user_emails, default=active_user_emails, key="recipients_multiselect")
        else:
            recipients = st.multiselect("Select users to notify:", active_user_emails, key="recipients_multiselect")

        submitted_post = st.form_submit_button("Publish & Notify Employees", type="primary")

        if submitted_post:
            if new_title == "" or new_link == "":
                st.error("Please provide both a post title and a link.")
            else:
                # Save to posts database
                new_post = pd.DataFrame([{
                    "platform": new_platform,
                    "post_title": new_title,
                    "post_link": new_link,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                old_posts = pd.read_csv(POSTS_FILE)
                updated_posts = pd.concat([old_posts, new_post], ignore_index=True)
                updated_posts.to_csv(POSTS_FILE, index=False)
                
                if recipients:
                    # Trigger notifications for selected employees
                    notify_employees(new_platform, new_title, new_link, recipients)
                    st.success(f"Post published and notifications sent to {len(recipients)} employees!")
                else:
                    st.warning("No employees selected for notification. Post published without email notifications.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="reach-card">', unsafe_allow_html=True)
    st.subheader("System Test")
    st.write("Send a test notification to verify the notification system configuration.")
    
    if st.button("Send Test Notification", key="send_test_notification_button"):
        test_email = st.session_state.user_email # Send test to logged-in admin
        test_subject = "REACH Social Boost - Test Notification"
        test_msg = "TEST ONLY: This is a test notification from REACH Social Boost. If you received this message, the notification system is working."
        
        success, error = send_email(test_email, test_subject, test_msg)
        
        if success:
            st.success("Notification sent successfully")
            log_notification(test_email, "Sent")
        else:
            st.error(f"Notification failed: {error}")
            log_notification(test_email, "Failed", error)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="reach-card">', unsafe_allow_html=True)
    st.subheader("Post History")
    st.dataframe(pd.read_csv(POSTS_FILE), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="reach-card">', unsafe_allow_html=True)
    st.subheader("Notification Logs")
    if os.path.exists(LOG_FILE):
        logs = pd.read_csv(LOG_FILE)
        st.dataframe(logs.sort_values(by="date_time", ascending=False), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Admin - Manage Users":
    st.header("Admin - Manage Users")

    st.subheader("Add New User")
    with st.form("add_user_form", clear_on_submit=True):
        name = st.text_input("Employee Name", key="add_name")
        email = st.text_input("Employee Email", key="add_email")
        department = st.selectbox(
            "Department",
            ["Marketing", "Sales", "HR", "Operations", "Finance", "IT", "Other"],
            key="add_department"
        )
        password = st.text_input("Password", type="password", key="add_password")
        role = st.selectbox("Role", ["Employee", "Admin"], key="add_role")
        submitted_add = st.form_submit_button("Add User")

        if submitted_add:
            if name == "" or email == "" or password == "":
                st.error("Please provide name, email, and password.")
            else:
                new_user = pd.DataFrame([{
                    "name": name,
                    "email": email,
                    "department": department,
                    "role": role,
                    "status": "Active",
                    "password": password
                }])
                old_users = pd.read_csv(USERS_FILE)
                updated_users = pd.concat([old_users, new_user], ignore_index=True)
                updated_users.to_csv(USERS_FILE, index=False)
                st.success("User added successfully.")

    st.divider()
    st.subheader("Edit User Status")
    users = pd.read_csv(USERS_FILE)
    if not users.empty:
        user_to_edit = st.selectbox(
            "Select user to edit status:",
            users["email"].tolist(),
            format_func=lambda x: f"{users[users['email'] == x]['name'].iloc[0]} ({x})"
        )

        if user_to_edit:
            current_status = users[users["email"] == user_to_edit]["status"].iloc[0]
            new_status = st.radio(
                f"Set status for {user_to_edit}:",
                ["Active", "Inactive"],
                index=0 if current_status == "Active" else 1
            )

            if st.button("Update User Status"):
                users.loc[users["email"] == user_to_edit, "status"] = new_status
                updated_users = users
                updated_users.to_csv(USERS_FILE, index=False)
                st.success(f"Status for {user_to_edit} updated to {new_status}.")

        st.divider()
        st.subheader("Delete User")
        user_to_delete = st.selectbox(
            "Select user to delete:",
            users["email"].tolist(),
            key="delete_user_select",
            format_func=lambda x: f"{users[users['email'] == x]['name'].iloc[0]} ({x})"
        )
        if st.button("Permanently Delete User", type="primary"):
            if user_to_delete == st.session_state.user_email:
                st.error("You cannot delete your own account while logged in.")
            else:
                updated_users = users[users["email"] != user_to_delete]
                updated_users.to_csv(USERS_FILE, index=False)
                st.success(f"User {user_to_delete} has been deleted.")
                st.rerun()
    else:
        st.info("No users to edit yet. Add some users first.")

    st.divider()
    st.subheader("Current Users List")
    users = pd.read_csv(USERS_FILE)

    search_term = st.text_input("Search users by name:", "")
    if search_term:
        users = users[users["name"].str.contains(search_term, case=False, na=False)]

    # Hide password column from the UI and exports for security
    display_users = users.drop(columns=["password"], errors="ignore")
    st.dataframe(display_users, use_container_width=True)

elif menu == "Admin - Manage Admins":
    if st.session_state.user_role != "Admin":
        st.error("You do not have permission to access this page.")
        st.stop()

    st.header("Admin - Manage Admins")
    st.subheader("Promote Employee to Admin")

    users = pd.read_csv(USERS_FILE)
    # Filter for active employees who are not already admins
    eligible_employees = users[(users["role"] == "Employee") & (users["status"] == "Active")]

    if eligible_employees.empty:
        st.info("No active employees available to promote to Admin.")
    else:
        employee_to_promote_email = st.selectbox(
            "Select an active employee to promote to Admin:",
            eligible_employees["email"].tolist(),
            format_func=lambda x: f"{users[users['email'] == x]['name'].iloc[0]} ({x})"
        )

        if st.button("Promote to Admin"):
            users.loc[users["email"] == employee_to_promote_email, "role"] = "Admin"
            users.to_csv(USERS_FILE, index=False)
            st.success(f"User {employee_to_promote_email} has been promoted to Admin.")
            st.info(f"The newly promoted admin can now log in and set their own password via the 'Change Password' page.")
            st.rerun()

elif menu == "Change Password":
    st.header("Change Password")

    user_email = st.session_state.user_email
    users = pd.read_csv(USERS_FILE)
    user_data = users[users['email'] == user_email].iloc[0]
    stored_password = str(user_data['password']).strip()

    current_password_input = st.text_input("Current Password", type="password", key="current_password_change")
    new_password_input = st.text_input("New Password", type="password", key="new_password_change")
    confirm_new_password_input = st.text_input("Confirm New Password", type="password", key="confirm_new_password_change")

    if st.button("Update Password"):
        if current_password_input.strip() != stored_password:
            st.error("Incorrect current password.")
        elif not new_password_input.strip():
            st.error("New password cannot be empty.")
        elif new_password_input != confirm_new_password_input:
            st.error("New password and confirmation do not match.")
        else:
            users.loc[users["email"] == user_email, "password"] = new_password_input.strip()
            users.to_csv(USERS_FILE, index=False)
            st.success("Your password has been updated successfully.")
            # Log out after password change for security
            st.session_state.logged_in = False
            st.rerun()