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
        background-color: #f6f7f8; /* Light Background */
        color: #3e454b; /* Dark Charcoal */
    }
    /* Font for the entire app */
    html, body, [class*="st-"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    h1, h2, h3 {
        color: #3e454b !important;
    }

    .hero-card {
        background-color: #3e454b !important;
        background-image: none !important;
        padding: 36px 42px !important;
        border-radius: 14px !important;
        margin-bottom: 32px !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12) !important;
    }

    .hero-card .main-header {
        color: #ffffff !important;
        font-size: 40px !important;
        font-weight: 800 !important;
        margin-bottom: 10px !important;
    }

    .hero-card .sub-header {
        color: #ffffff !important;
        font-size: 18px !important;
        border-bottom: 2px solid #d0323a !important;
        padding-bottom: 14px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #3e454b; /* Dark Charcoal */
        border-right: 1px solid #5b6770; /* Grey Blue */
        /* Optional: Add a background image to the sidebar */
        /* background-image: linear-gradient(rgba(11, 31, 58, 0.85), rgba(11, 31, 58, 0.85)), url("YOUR_IMAGE_URL_HERE"); */
        /* background-size: cover; */
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
        color: #d0323a !important; /* Primary Red */
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] label {
        font-weight: 600 !important;
    }

    .sidebar-section {
        color: #d0323a !important; /* Primary Red */
        font-weight: 700;
        font-size: 0.9rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding-left: 1rem;
        border-bottom: 1px solid rgba(208, 50, 58, 0.3); /* Primary Red accent line */
        padding-bottom: 0.3rem;
    }
    
    /* Cards and Containers */
    .reach-card {
        background-color: #ffffff; /* White Cards */
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #5b6770; /* Grey Blue */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }
    .reach-card h2, .reach-card h3 {
        color: #3e454b; /* Dark Charcoal */
        margin-top: 0;
        margin-bottom: 1rem;
    }

    /* Buttons */
    .stButton > button {
        background-color: #3e454b; /* Dark Charcoal */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #d0323a; /* Primary Red */
        color: white;
    }
    /* Primary buttons (e.g., Submit Engagement) */
    .stButton > button[kind="primary"] {
        background-color: #d0323a; /* Primary Red */
        color: white;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #b82d34; /* Dark Red */
        color: white;
    }

    /* Text Inputs and Select Boxes */
    .stTextInput > div > div > input, .stSelectbox > div > div > div > div > div > input {
        border-radius: 8px;
        border: 1px solid #5b6770; /* Grey Blue */
        padding: 8px 12px;
    }

    .page-intro-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 6px solid #d0323a;
        border-radius: 16px;
        padding: 22px 26px;
        margin: 18px 0 28px 0;
        box-shadow: 0 6px 18px rgba(62, 69, 75, 0.08);
    }

    .intro-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 24px;
    }

    .page-intro-card h2 {
        color: #3e454b !important;
        font-size: 26px;
        font-weight: 800;
        margin: 0 0 8px 0;
    }

    .page-intro-card p {
        color: #5b6770 !important;
        font-size: 15px;
        margin: 0;
    }

    .intro-badges {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        justify-content: flex-end;
    }

    .intro-badge {
        background: rgba(208, 50, 58, 0.10);
        color: #b82d34;
        border: 1px solid rgba(208, 50, 58, 0.25);
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

def page_intro(title, description, badges=None):
    badges_html = ""
    if badges:
        badges_html = f'<div class="intro-badges">{" ".join([f"<span class=\"intro-badge\">{badge}</span>" for badge in badges])}</div>'

    # Flatten HTML to prevent Markdown parser from escaping closing tags
    intro_html = f'<div class="page-intro-card"><div class="intro-content"><div><h2>{title}</h2><p>{description}</p></div>{badges_html}</div></div>'
    st.markdown(intro_html, unsafe_allow_html=True)

# File paths
USERS_FILE = "users.csv"
PASSWORD_RESETS_FILE = "password_resets.csv"
ENGAGEMENT_FILE = "engagement_points.csv"
POSTS_FILE = "posts.csv"
LOG_FILE = "notification_logs.csv"

APP_LINK = st.secrets.get("app", {}).get("url", "http://localhost:8501")

# Create users file if not exists
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
else:
    users_data = pd.read_csv(USERS_FILE)

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
        "employee_name",
        "employee_email",
        "department",
        "post_title",
        "campaign_name",
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
    posts_data = pd.DataFrame(columns=["platform", "post_title", "campaign_name", "post_link", "date"])
    # Seed with an initial post
    initial_post = pd.DataFrame([{
        "platform": "LinkedIn",
        "post_title": "Welcome to REACH Social Boost!",
        "campaign_name": "General",
        "post_link": "https://www.linkedin.com/company/reach-group/",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    posts_data = pd.concat([posts_data, initial_post], ignore_index=True)
    posts_data.to_csv(POSTS_FILE, index=False)
else:
    # Migration logic for campaign_name
    posts_df = pd.read_csv(POSTS_FILE)
    if "campaign_name" not in posts_df.columns:
        posts_df["campaign_name"] = "General"
        posts_df.to_csv(POSTS_FILE, index=False)
    # Migration for engagement points
    eng_df = pd.read_csv(ENGAGEMENT_FILE)
    if "campaign_name" not in eng_df.columns:
        eng_df["campaign_name"] = "General"
        eng_df.to_csv(ENGAGEMENT_FILE, index=False)
    # Migration for employee_name and department in engagement
    if "employee_name" not in eng_df.columns:
        eng_df["employee_name"] = ""
    if "department" not in eng_df.columns:
        eng_df["department"] = ""
    eng_df.to_csv(ENGAGEMENT_FILE, index=False)

def calculate_badges(points):
    """Returns list of badges based on total points."""
    badges = []
    if points >= 50: badges.append("🏅 Social Supporter")
    if points >= 150: badges.append("🏆 LinkedIn Champion")
    if points >= 300: badges.append("💎 Brand Ambassador")
    return badges

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
        # 1 & 2. Read SMTP credentials from st.secrets safely
        smtp_conf = st.secrets.get("smtp", {})
        if not smtp_conf:
            return False, "SMTP configuration is missing. Email notifications will not be sent."
        
        sender_email = smtp_conf.get("sender_email", "")
        sender_password = smtp_conf.get("sender_password", "")
        smtp_server = smtp_conf.get("smtp_server", "")
        try:
            smtp_port = int(smtp_conf.get("smtp_port", 465))
        except (ValueError, TypeError):
            smtp_port = 465
        
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
    body = (
        f"Hello,\n\nYou have requested a password reset for your REACH Social Boost account.\n\n"
        f"Your password reset code is: **{reset_code}**\n\n"
        f"Please use this code to reset your password within the app. "
        f"Go to the app and click on 'Forgot Password?' then enter this code.\n\n"
        f"App Link: {APP_LINK}\n\n"
        f"If you did not request a password reset, please ignore this email.\n\n"
        f"Best regards,\nREACH Social Boost Team"
    )
    success, error = send_email(receiver_email, subject, body)
    if not success:
        log_notification(receiver_email, "Failed", f"Failed to send reset code email: {error}")
    return success, error


def notify_employees(title, campaign_name, platform_links, selected_emails):
    """Sends notifications to active employees via Microsoft Teams and Email."""
    # 1. Microsoft Teams Notification (Preferred)
    TEAMS_WEBHOOK_URL = "YOUR_TEAMS_WEBHOOK_URL"
    if TEAMS_WEBHOOK_URL != "YOUR_TEAMS_WEBHOOK_URL":
        teams_links = "\n".join([f"- **{p}:** {link}" for p, link in platform_links.items()])
        teams_payload = {
            "text": f"📢 **New Social Media Post Published!**\n\n"
                    f"**Campaign:** {campaign_name}\n"
                    f"**Title:** {title}\n\n"
                    f"**Platform Links:**\n{teams_links}\n\n"
                    f"**Suggested Actions:**\n- Like the post\n- Leave a meaningful comment\n- Share or repost if relevant\n\n"
                    f"**Action Required:** [Submit Engagement]({APP_LINK}) to collect points!"
        }
        try:
            requests.post(TEAMS_WEBHOOK_URL, json=teams_payload, timeout=5)
        except Exception as e:
            st.warning(f"Could not send Teams notification: {e}")

    # 2. Email Notification (Backup)
    if selected_emails:
        subject = f"📢 Action Required: New Social Post - {title}"
        links_text = "\n".join([f"🔗 {p}: {link}" for p, link in platform_links.items()])
        body = (
            f"Hello team,\n\n"
            f"A new company social media post is now live.\n\n"
            f"Your support can help increase REACH Group’s visibility and engagement across our platforms.\n\n"
            f"Campaign: {campaign_name}\n"
            f"Post Title: {title}\n\n"
            f"Please support the post on the available platforms:\n\n"
            f"{links_text}\n\n"
            f"Suggested actions:\n"
            f"- Like the post\n"
            f"- Leave a meaningful comment\n"
            f"- Share or repost if relevant\n\n"
            f"After engaging, please open REACH Social Boost and submit your completed actions to collect points.\n\n"
            f"App Link: {APP_LINK}\n\n"
            f"Thank you for supporting our brand presence.\n\n"
            f"Best regards,\n"
            f"Marketing Team"
        )
        for email in selected_emails:
            send_email(email, subject, body)

# Login System
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'remembered_email' not in st.session_state:
    st.session_state.remembered_email = ''
if 'remember_me_checked' not in st.session_state:
    st.session_state.remember_me_checked = False
if 'show_reset_password_form' not in st.session_state:
    st.session_state.show_reset_password_form = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ''
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''
if 'user_role' not in st.session_state:
    st.session_state.user_role = ''

# Sidebar Menu based on Role
if not st.session_state.logged_in:
    # Public view: Only show Engagement and Login
    menu_options = ["Employee Engagement", "Admin Login"]
else:
    # Logged in view
    if st.session_state.user_role == "Admin":
        menu_options = ["Employee Engagement", "Leaderboard", "Admin - Manage Posts", "Admin - Manage Users", "Admin - Manage Admins", "Admin - Reports", "Change Password"]
    else:
        # Logged in as Employee: Show core engagement features and settings
        menu_options = ["Employee Engagement", "Leaderboard", "Change Password"]

menu = st.sidebar.radio("Choose Page", menu_options)

st.sidebar.divider()
if st.session_state.logged_in:
    st.sidebar.write(f"Logged in as: **{st.session_state.user_name}**")
    st.sidebar.write(f"Role: {st.session_state.user_role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ''
        st.session_state.user_name = ''
        st.session_state.user_role = ''
        st.rerun()
else:
    st.sidebar.info("Public Access: Admin features are hidden.")


if menu == "Employee Engagement":
    # Calculate badges for Employee Engagement page
    user_role = st.session_state.get('user_role', 'User')
    user_email = st.session_state.get('user_email', '')
    eng_points_df = pd.read_csv(ENGAGEMENT_FILE)
    user_total_points = eng_points_df[eng_points_df["employee_email"] == user_email]["points"].sum()
    posts_df = pd.read_csv(POSTS_FILE)
    active_posts_count = posts_df['post_title'].nunique() # Count unique post titles

    page_intro(
        "Employee Engagement",
        "Open the post, complete your actions, and submit your engagement to collect points.",
        badges=[f"Role: {user_role}", f"Your Points: {user_total_points}", f"Active Posts: {active_posts_count}"]
    )

    st.subheader("Your Information")
    col_info1, col_info2 = st.columns(2)
    is_admin_logged_in = st.session_state.logged_in

    with col_info1:
        emp_name = st.text_input("Full Name (Required)", value=st.session_state.get('user_name', ''), disabled=is_admin_logged_in, key="eng_name_input")
        emp_email = st.text_input("Company Email (Optional)", value=st.session_state.get('user_email', ''), disabled=is_admin_logged_in, key="eng_email_input")
    with col_info2:
        dept_options = ["", "Marketing", "Sales", "HR", "Operations", "Finance", "IT", "Other"]
        current_dept = st.session_state.get('user_department', '')
        default_dept_idx = dept_options.index(current_dept) if current_dept in dept_options else 0
        emp_dept = st.selectbox("Department (Required)", dept_options, index=default_dept_idx, disabled=is_admin_logged_in, key="eng_dept_select")
    
    # Feature 3 & 4: Badges Display
    eng_points = pd.read_csv(ENGAGEMENT_FILE)
    current_user_email = st.session_state.get('user_email', '')
    if current_user_email:
        user_points = eng_points[eng_points["employee_email"] == current_user_email]["points"].sum()
        user_badges = calculate_badges(user_points)
        if user_badges:
            st.markdown(f"**Your Badges:** {' '.join(user_badges)}")
    
    
    # Fetch all posts
    posts = pd.read_csv(POSTS_FILE)
    
    if posts.empty:
        st.markdown('<div class="reach-card"><p>No posts available to engage with.</p></div>', unsafe_allow_html=True)
    else:
        st.subheader("Select Post")
        # Create a list of post titles for selection, showing newest first and including platform/date
        post_options_display = [f"{row['post_title']} ({row['platform']} - {row['date'].split(' ')[0]})" for index, row in posts.iloc[::-1].iterrows()]
        selected_post_display = st.selectbox("Choose the post you engaged with:", post_options_display, key="post_selector")
        
        # Find the actual post data based on the selected display string
        selected_index = post_options_display.index(selected_post_display)
        selected_post = posts.iloc[::-1].iloc[selected_index] # Get the corresponding row from the reversed DataFrame
        platform = selected_post["platform"]
        post_link = selected_post["post_link"]
        campaign_name = selected_post.get("campaign_name", "General")

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Post Details")
            st.write(f"**Campaign:** {campaign_name}")
            st.write(f"**Platform:** {platform}")
            st.link_button("Open Social Media Post", post_link)

        with col_right:
            st.subheader("Mark Your Actions")
            liked = st.checkbox("👍 I liked the post (+5 pts)")
            commented = st.checkbox("💬 I commented on the post (+10 pts)")
            shared = st.checkbox("🔁 I shared / reposted the post (+20 pts)")
            
            points_preview = (5 if liked else 0) + (10 if commented else 0) + (20 if shared else 0)
            st.markdown(f"**Total points to earn: {points_preview}**")

        if st.button("Submit Engagement", type="primary", key="submit_engagement_button_logged_in"):
            points = 0
            if liked: points += 5
            if commented: points += 10
            if shared: points += 20

            if not emp_name.strip():
                st.error("Please enter your full name.")
            elif not emp_dept:
                st.error("Please select your department.")
            elif points == 0:
                st.error("Please select at least one action.")
            else:
                # Check for duplicate submission
                engagement_data = pd.read_csv(ENGAGEMENT_FILE)
                
                if emp_email.strip():
                    # Rule 5: If email provided, use it for duplicate prevention
                    already_submitted = not engagement_data[
                        (engagement_data["employee_email"] == emp_email.strip()) & 
                        (engagement_data["post_link"] == post_link)
                    ].empty
                else:
                    # Rule 6: If email not provided, use name + department + post/platform
                    already_submitted = not engagement_data[
                        (engagement_data["employee_name"] == emp_name.strip()) & 
                        (engagement_data["department"] == emp_dept) & 
                        (engagement_data["post_link"] == post_link)
                    ].empty

                if already_submitted:
                    st.warning(f"You have already submitted engagement for '{selected_post['post_title']}'. Duplicate claims are not allowed.")
                else:
                    new_record = pd.DataFrame([{
                        "employee_name": emp_name.strip(),
                        "employee_email": emp_email.strip() if emp_email else "",
                        "department": emp_dept,
                        "post_title": selected_post['post_title'],
                        "campaign_name": campaign_name,
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

elif menu == "Admin Login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Admin Login")
        default_email_value = st.session_state.remembered_email
        login_email_input = st.text_input("Email", value=default_email_value, key="login_email_input_main")
        login_password_input = st.text_input("Password", type="password", key="login_password_input_main")
        remember_me_checkbox = st.checkbox("Remember Me", value=st.session_state.remember_me_checked, key="remember_me_checkbox")
        
        if st.button("Login", key="login_button_main", type="primary", use_container_width=True):
            if os.path.exists(USERS_FILE):
                users = pd.read_csv(USERS_FILE)
                if users.empty:
                    st.error("The user database is empty. Please add an Admin user to users.csv manually to proceed.")
                else:
                    login_email = login_email_input.strip()
                    login_password = login_password_input.strip()
                    user_match = users[users['email'].str.lower() == login_email.lower()]
                    
                    if user_match.empty:
                        st.error("Email not found. Please check your email address.")
                    else:
                        user_data = user_match.iloc[0]
                        input_password_stripped = login_password.strip()
                        stored_password_stripped = str(user_data['password']).strip()

                        if input_password_stripped != stored_password_stripped:
                            st.error("Invalid password. Please try again.")
                        elif user_data['status'] == 'Inactive':
                            st.error("Your account is inactive. Please contact an administrator.")
                        elif user_data['role'] not in ['Admin', 'Employee']:
                            st.error("Your account has an unrecognized role. Please contact an administrator.")
                        else:
                            st.session_state.logged_in = True
                            st.session_state.user_email = user_data['email']
                            st.session_state.user_role = user_data['role']
                            st.session_state.user_name = user_data['name']
                            st.session_state.user_department = user_data['department']

                            if remember_me_checkbox:
                                st.session_state.remembered_email = login_email
                                st.session_state.remember_me_checked = True
                            else:
                                st.session_state.remembered_email = ''
                                st.session_state.remember_me_checked = False
                            st.rerun()
            else:
                st.error("User database not found. Please create users.csv.")
        
        if st.button("Forgot password?", key="forgot_password_link", help="Click to reset your password"):
            st.session_state.show_reset_password_form = not st.session_state.show_reset_password_form
            st.rerun()

        if st.session_state.get('show_reset_password_form'):
            st.subheader("Reset Password")
            st.markdown("---")
            st.markdown("<h5>Send Reset Code</h5>", unsafe_allow_html=True)
            forgot_email_input = st.text_input("Enter your email to send reset code", key="forgot_email_input")
            if st.button("Send Reset Code", key="send_reset_code_button", use_container_width=True):
                forgot_email = forgot_email_input.strip()
                users = pd.read_csv(USERS_FILE)
                user_row = users[users['email'].str.lower() == forgot_email.lower()]
                if user_row.empty or user_row.iloc[0]['status'] == 'Inactive':
                    st.error("Email not found or account is inactive.")
                else:
                    reset_code = generate_reset_code()
                    expiration_time = datetime.now() + timedelta(minutes=15)
                    reset_data = pd.read_csv(PASSWORD_RESETS_FILE)
                    new_reset_entry = pd.DataFrame([{
                        "email": forgot_email,
                        "reset_code": reset_code,
                        "expiration_time": expiration_time.strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    pd.concat([reset_data, new_reset_entry], ignore_index=True).to_csv(PASSWORD_RESETS_FILE, index=False)
                    success, error = send_reset_code_email(forgot_email, reset_code)
                    if success: st.success("A password reset code has been sent to your email.")
                    else: st.error(f"Failed to send reset code: {error}")

            st.markdown("---")
            st.markdown("<h5>Apply Reset Code</h5>", unsafe_allow_html=True)
            reset_email_inp = st.text_input("Your email (for reset)", key="reset_email_confirm")
            received_code = st.text_input("Reset Code", key="received_code")
            new_password = st.text_input("New Password", type="password", key="new_password")
            confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")

            if st.button("Reset Password", key="reset_password_button_apply", type="primary", use_container_width=True):
                if new_password != confirm_new_password:
                    st.error("New passwords do not match.")
                elif not new_password.strip():
                    st.error("Password cannot be empty.")
                else:
                    reset_data = pd.read_csv(PASSWORD_RESETS_FILE)
                    valid_codes = reset_data[(reset_data["email"].str.lower() == reset_email_inp.lower()) & (reset_data["reset_code"] == received_code)]
                    if valid_codes.empty:
                        st.error("Invalid or expired reset code.")
                    else:
                        latest_code_entry = valid_codes.sort_values(by="expiration_time", ascending=False).iloc[0]
                        expiration_time = datetime.strptime(latest_code_entry["expiration_time"], "%Y-%m-%d %H:%M:%S")
                        if datetime.now() > expiration_time:
                            st.error("Reset code has expired.")
                        else:
                            users = pd.read_csv(USERS_FILE)
                            if reset_email_inp.lower() not in users["email"].str.lower().values:
                                st.error("User not found.")
                            else:
                                users.loc[users["email"].str.lower() == reset_email_inp.lower(), "password"] = new_password.strip()
                                users.to_csv(USERS_FILE, index=False)
                                reset_data = reset_data.drop(valid_codes.index)
                                reset_data.to_csv(PASSWORD_RESETS_FILE, index=False)
                                st.success("Your password has been reset successfully. You can now log in.")
                                st.session_state.show_reset_password_form = False
                                st.rerun()


elif menu == "Leaderboard":
    if not st.session_state.logged_in:
        st.error("Please login to view the Leaderboard.")
        st.stop()
        
    page_intro("Leaderboard", "Track top employees, departments, and monthly engagement performance.")

    def format_leaderboard(df):
        """Applies a background color to the top 3 rows."""
        def style_rows(row):
            if row.name == 0: return ['background-color: #C8A24A; color: white; font-weight: bold;'] * len(row)
            if row.name == 1: return ['background-color: #C0C0C0; color: white; font-weight: bold;'] * len(row)
            if row.name == 2: return ['background-color: #CD7F32; color: white; font-weight: bold;'] * len(row)
            return [''] * len(row)
        return df.style.apply(style_rows, axis=1)

    data = pd.read_csv(ENGAGEMENT_FILE)
    users = pd.read_csv(USERS_FILE)

    if data.empty:
        st.markdown('<div class="reach-card"><p>No engagement submitted yet.</p></div>', unsafe_allow_html=True)
    else:
        # Feature 3: Monthly Rewards Section
        st.subheader("🌟 Monthly Rewards")
        current_month = datetime.now().strftime("%Y-%m")
        monthly_data = data[data["date"].str.startswith(current_month)]
        
        if not monthly_data.empty:
            m_winners = monthly_data.groupby("employee_email")["points"].sum().sort_values(ascending=False).head(3)
            cols = st.columns(3)
            place_names = ["🥇 1st Place", "🥈 2nd Place", "🥉 3rd Place"]
            for i, (email, pts) in enumerate(m_winners.items()):
                cols[i].metric(place_names[i], f"{pts} pts", email.split('@')[0])
            
            # Top Dept of month
            m_merged = monthly_data.merge(users[['email', 'department']], left_on='employee_email', right_on='email', how='left')
            if not m_merged.empty and "points" in m_merged.columns:
                if "department" not in m_merged.columns:
                    m_merged["department"] = "Unknown"
                else:
                    m_merged["department"] = m_merged["department"].fillna("Unknown")
                
                dept_points_m = m_merged.groupby("department")["points"].sum()
                if not dept_points_m.empty:
                    top_dept_m = dept_points_m.idxmax()
                    st.success(f"🏢 **Top Department of the Month:** {top_dept_m}")
        else:
            st.info("Engagement for the current month is just starting!")

        # Merge engagement data with user data to get department info
        merged_data = data.merge(users[['email', 'department']], left_on='employee_email', right_on='email', how='left')
        
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

            # Add Badges to leaderboard
            leaderboard["Badges"] = leaderboard["Total Points"].apply(lambda x: "".join(calculate_badges(x)))
        st.markdown("---")
        st.subheader("🏢 Department Leaderboard")
        if not merged_data.empty and "points" in merged_data.columns:
            if "department" not in merged_data.columns:
                merged_data["department"] = "Unknown"
            else:
                merged_data["department"] = merged_data["department"].fillna("Unknown")

            dept_stats = merged_data.groupby("department").agg(
                Total_Points=("points", "sum"),
                Participating_Employees=("employee_email", "nunique"),
                Completed_Engagements=("employee_email", "count")
            ).reset_index().sort_values(by="Total_Points", ascending=False)
            
            dept_stats.columns = ["Department", "Points", "Employees", "Engagements"]
            st.table(dept_stats)
        else:
            st.info("No department leaderboard data available yet.")
        
        # Feature 4: Campaign Summary Section
        st.markdown("---")
        st.subheader("📊 Campaign Impact")
        camp_stats = data.groupby("campaign_name").agg(
            Total_Points=("points", "sum"),
            Submissions=("employee_email", "count")
        ).reset_index()
        
        for _, row in camp_stats.iterrows():
            with st.expander(f"Campaign: {row['campaign_name']}"):
                st.write(f"Points: {row['Total_Points']} | Submissions: {row['Submissions']}")
                c_data = data[data["campaign_name"] == row["campaign_name"]]
                top_emp = c_data.groupby("employee_email")["points"].sum().idxmax()
                st.write(f"Top Contributor: {top_emp}")


elif menu == "Admin - Manage Posts":
    if st.session_state.user_role != "Admin":
        st.error("Access Denied.")
        st.stop()
        
    page_intro("Admin - Manage Posts", "Create social media posts, select platforms, and notify employees.")
    
    # 3. Proactive check for SMTP configuration safely without crashing the app
    if not st.secrets.get("smtp"):
        st.warning("SMTP configuration is missing. Email notifications will not be sent. Please set up SMTP credentials in Streamlit Secrets.")

    st.subheader("Publish New Post")

    # Platform selection outside form for dynamic link inputs
    selected_platforms = st.multiselect(
        "Select Platforms", 
        ["LinkedIn", "Facebook", "Instagram", "Twitter / X", "Other"], 
        key="new_post_platforms"
    )
    
    platform_links = {}
    if selected_platforms:
        for p in selected_platforms:
            platform_links[p] = st.text_input(f"{p} Post Link", key=f"link_{p}")

    with st.form("new_post_form"):
        new_title = st.text_input("Post Title", key="new_post_title")
        new_campaign = st.text_input("Campaign Name (e.g., ISO Certification, Eid)", key="new_campaign")
        
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
            if new_title == "" or not selected_platforms:
                st.error("Please provide a post title and select at least one platform.")
            elif any(not platform_links[p].strip() for p in selected_platforms):
                st.error("Please provide a link for all selected platforms.")
            else:
                campaign = new_campaign if new_campaign else "General"
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Option A: Save one row per platform in posts.csv
                new_posts_rows = []
                for p, link in platform_links.items():
                    new_posts_rows.append({
                        "platform": p,
                        "post_title": new_title,
                        "campaign_name": campaign,
                        "post_link": link.strip(),
                        "date": now
                    })
                
                old_posts = pd.read_csv(POSTS_FILE)
                updated_posts = pd.concat([old_posts, pd.DataFrame(new_posts_rows)], ignore_index=True)
                updated_posts.to_csv(POSTS_FILE, index=False)
                
                if recipients:
                    notify_employees(new_title, campaign, platform_links, recipients)
                    st.success(f"Post published and notifications sent to {len(recipients)} employees!")
                else:
                    st.warning("No employees selected for notification. Post published without email notifications.")

    st.subheader("System Test")
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

    st.subheader("Post History")
    st.dataframe(pd.read_csv(POSTS_FILE), use_container_width=True, hide_index=True)

    st.subheader("Edit Post")
    posts_df_to_edit = pd.read_csv(POSTS_FILE)
    if not posts_df_to_edit.empty:
        # Create a display ID to uniquely identify posts for the edit selection
        posts_df_to_edit['edit_id'] = posts_df_to_edit['post_title'] + " [" + posts_df_to_edit['platform'] + "] (" + posts_df_to_edit['date'] + ")"
        
        post_to_edit_id = st.selectbox("Select a post to modify:", posts_df_to_edit['edit_id'].tolist(), key="post_edit_select")
        
        # Retrieve the current data for the selected post
        selected_row = posts_df_to_edit[posts_df_to_edit['edit_id'] == post_to_edit_id].iloc[0]
        
        with st.form("edit_post_form"):
            updated_title = st.text_input("Edit Post Title", value=selected_row['post_title'])
            updated_campaign = st.text_input("Edit Campaign Name", value=selected_row['campaign_name'])
            updated_link = st.text_input("Edit Post Link", value=selected_row['post_link'])
            
            if st.form_submit_button("Save Changes", type="primary"):
                # Find the index of the row to update
                idx = posts_df_to_edit[posts_df_to_edit['edit_id'] == post_to_edit_id].index
                posts_df_to_edit.loc[idx, 'post_title'] = updated_title
                posts_df_to_edit.loc[idx, 'campaign_name'] = updated_campaign
                posts_df_to_edit.loc[idx, 'post_link'] = updated_link
                
                # Save back to CSV after removing the temporary ID column
                posts_df_to_edit.drop(columns=['edit_id']).to_csv(POSTS_FILE, index=False)
                st.success("Post updated successfully!")
                st.rerun()
    else:
        st.info("No posts available to edit.")

    st.subheader("Delete Post")
    posts_df_to_del = pd.read_csv(POSTS_FILE)
    if not posts_df_to_del.empty:
        # Create a display ID to uniquely identify posts for the admin
        posts_df_to_del['display_id'] = posts_df_to_del['post_title'] + " [" + posts_df_to_del['platform'] + "] (" + posts_df_to_del['date'] + ")"
        
        post_to_delete = st.selectbox("Select a post to permanently delete:", posts_df_to_del['display_id'].tolist(), key="post_delete_select")
        
        if st.button("Delete Selected Post", type="primary", key="confirm_delete_post"):
            # Locate the exact index of the selected post
            idx = posts_df_to_del[posts_df_to_del['display_id'] == post_to_delete].index
            # Drop the row and the temporary display column, then save
            new_posts_df = posts_df_to_del.drop(idx).drop(columns=['display_id'])
            new_posts_df.to_csv(POSTS_FILE, index=False)
            st.success(f"Post successfully deleted.")
            st.rerun()
    else:
        st.info("No posts available to delete.")

    st.subheader("Notification Logs")
    if os.path.exists(LOG_FILE):
        logs = pd.read_csv(LOG_FILE)
        st.dataframe(logs.sort_values(by="date_time", ascending=False), use_container_width=True, hide_index=True)

elif menu == "Admin - Manage Users":
    if st.session_state.user_role != "Admin":
        st.error("Access Denied.")
        st.stop()
        
    page_intro("Admin - Manage Users", "Manage employees, roles, status, and access.")

    st.subheader("Add New User")
    with st.form("add_user_form", clear_on_submit=True):
        name = st.text_input("User Name", key="add_name")
        email = st.text_input("User Email", key="add_email")
        department = st.selectbox(
            "Department",
            ["Marketing", "Sales", "HR", "Operations", "Finance", "IT", "Other"],
            key="add_department"
        )
        password = st.text_input("Password", type="password", key="add_password")
        role = st.selectbox("Role", ["Employee", "Admin"], key="add_role")
        submitted_add = st.form_submit_button("Add User", type="primary")

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

    st.subheader("Edit User Status")
    users = pd.read_csv(USERS_FILE)
    if not users.empty:
        user_to_edit = st.selectbox(
            "Select user to edit status:",
            users["email"].tolist(),
            key="edit_status_select",
            format_func=lambda x: f"{users[users['email'] == x]['name'].iloc[0]} ({x})"
        )

        if user_to_edit:
            current_status = users[users["email"] == user_to_edit]["status"].iloc[0]
            new_status = st.radio(
                f"Set status for {user_to_edit}:",
                ["Active", "Inactive"],
                index=0 if current_status == "Active" else 1,
                key="status_radio"
            )

            if st.button("Update User Status", key="update_user_status_button"):
                users.loc[users["email"] == user_to_edit, "status"] = new_status
                updated_users = users
                updated_users.to_csv(USERS_FILE, index=False)
                st.success(f"Status for {user_to_edit} updated to {new_status}.")
    else:
        st.info("No users to edit yet. Add some users first.")

    st.subheader("Delete User")
    users = pd.read_csv(USERS_FILE) # Reload users to reflect any status changes
    if not users.empty:
        user_to_delete = st.selectbox(
            "Select user to delete:",
            users["email"].tolist(),
            key="delete_user_select",
            format_func=lambda x: f"{users[users['email'] == x]['name'].iloc[0]} ({x})"
        )
        if st.button("Permanently Delete User", type="primary", key="delete_user_button"):
            if user_to_delete == st.session_state.user_email:
                st.error("You cannot delete your own account while logged in.")
            else:
                updated_users = users[users["email"] != user_to_delete]
                updated_users.to_csv(USERS_FILE, index=False)
                st.success(f"User {user_to_delete} has been deleted.")
                st.rerun()
    else:
        st.info("No users to delete.")

    st.subheader("Current Users List")
    users = pd.read_csv(USERS_FILE)

    search_term = st.text_input("Search users by name:", key="user_search_input")
    if search_term:
        users = users[users["name"].str.contains(search_term, case=False, na=False)]

    # Hide password column from the UI and exports for security
    display_users = users.drop(columns=["password"], errors="ignore")
    st.dataframe(display_users, use_container_width=True, hide_index=True)

elif menu == "Admin - Manage Admins":
    if st.session_state.user_role != "Admin":
        st.error("You do not have permission to access this page.")
        st.stop()

    page_intro("Admin - Manage Admins", "Promote active users to admin and manage admin access.")
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
            key="promote_employee_select",
            format_func=lambda x: f"{users[users['email'] == x]['name'].iloc[0]} ({x})"
        )

        if st.button("Promote to Admin", type="primary", key="promote_button"):
            users.loc[users["email"] == employee_to_promote_email, "role"] = "Admin"
            users.to_csv(USERS_FILE, index=False)
            st.success(f"User {employee_to_promote_email} has been promoted to Admin.")
            st.info(f"The newly promoted admin can now log in and set their own password via the 'Change Password' page.")
            st.rerun()

elif menu == "Admin - Reports":
    if st.session_state.user_role != "Admin":
        st.error("Access Denied.")
        st.stop()
    
    page_intro("Admin - Monthly Reports", "View and export monthly engagement performance reports.")
    
    col1, col2 = st.columns(2)
    month = col1.selectbox("Month", range(1, 13), index=datetime.now().month - 1)
    year = col2.selectbox("Year", range(2024, 2030), index=0)
    
    if st.button("Generate & Export Report", type="primary"):
        pattern = f"{year}-{month:02d}"
        eng = pd.read_csv(ENGAGEMENT_FILE)
        m_eng = eng[eng["date"].str.startswith(pattern)]
        
        if m_eng.empty:
            st.warning("No data found for the selected period.")
        else:
            # Create a simple CSV summary
            report_data = {
                "Metric": [
                    "Total Engagements",
                    "Total Points Generated",
                    "Unique Employees Engaged",
                    "Most Active Campaign"
                ],
                "Value": [
                    len(m_eng),
                    m_eng["points"].sum(),
                    m_eng["employee_email"].nunique(),
                    m_eng["campaign_name"].value_counts().idxmax() if not m_eng.empty else "N/A"
                ]
            }
            report_df = pd.DataFrame(report_data)
            
            # Offer Download
            csv = report_df.to_csv(index=False).encode('utf-8')
            st.success("Report summary generated below!")
            st.table(report_df)
            
            # Visualization: Engagement by Platform
            st.markdown("---")
            st.subheader("Engagement Activity by Platform")
            platform_stats = m_eng['platform'].value_counts()
            st.bar_chart(platform_stats)
            
            # Visualization: Points by Department
            st.markdown("---")
            st.subheader("Total Points by Department")
            report_users = pd.read_csv(USERS_FILE)
            dept_points_df = m_eng.merge(report_users[['email', 'department']], left_on='employee_email', right_on='email', how='left')
            
            if not dept_points_df.empty and "points" in dept_points_df.columns:
                if "department" not in dept_points_df.columns:
                    dept_points_df["department"] = "Unknown"
                else:
                    dept_points_df["department"] = dept_points_df["department"].fillna("Unknown")
                
                dept_viz_data = dept_points_df.groupby('department')['points'].sum()
                if not dept_viz_data.empty:
                    st.bar_chart(dept_viz_data)
                else:
                    st.info("No department data to display for this month.")
            
            st.download_button(
                label="📥 Download Monthly Report (CSV)",
                data=csv,
                file_name=f"monthly_report_{year}_{month:02d}.csv",
                mime="text/csv"
            )

elif menu == "Change Password":
    if not st.session_state.logged_in:
        st.error("Please login first to change your password.")
        st.stop()
        
    st.markdown('<div class="main-header">Change Password</div>', unsafe_allow_html=True)
    st.subheader("Update Your Password")

    user_email = st.session_state.user_email
    users = pd.read_csv(USERS_FILE)
    user_data = users[users['email'].str.lower() == user_email.lower()].iloc[0] # Case-insensitive lookup
    stored_password = str(user_data['password']).strip()

    current_password_input = st.text_input("Current Password", type="password", key="current_password_change")
    new_password_input = st.text_input("New Password", type="password", key="new_password_change")
    confirm_new_password_input = st.text_input("Confirm New Password", type="password", key="confirm_new_password_change")

    if st.button("Update Password", type="primary", key="update_password_button"):
        if current_password_input.strip() != stored_password:
            st.error("Incorrect current password.")
        elif not new_password_input.strip():
            st.error("New password cannot be empty.")
        elif new_password_input != confirm_new_password_input:
            st.error("New password and confirmation do not match.")
        else:
            users.loc[users["email"].str.lower() == user_email.lower(), "password"] = new_password_input.strip()
            users.to_csv(USERS_FILE, index=False)
            st.success("Your password has been updated successfully.")
            # Log out after password change for security
            st.session_state.logged_in = False
            st.rerun()
