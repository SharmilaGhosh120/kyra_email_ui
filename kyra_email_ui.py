import streamlit as st
from enhanced_email_sender import send_email
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="Ky’ra Email Sender", layout="centered")
st.title("📧 Ky’ra Email Sender Dashboard")
st.markdown("Send emails with HTML content and attachments to multiple recipients.")

# Input fields
to_emails = st.text_input("Recipient Email(s) [comma-separated]", placeholder="email1@example.com, email2@example.com")
subject = st.text_input("Subject", placeholder="Enter email subject")
html_content = st.text_area("HTML Content", height=200, placeholder="Enter HTML content, e.g., <p>Hello!</p>")
uploaded_files = st.file_uploader("Attachments (Optional)", accept_multiple_files=True, help="Upload PDFs or other files")

if st.button("Send Email", type="primary"):
    if not to_emails or not subject or not html_content:
        st.warning("Please fill all required fields: Recipient Email(s), Subject, and HTML Content.")
    else:
        try:
            # Process attachments
            attachments = []
            for uploaded_file in uploaded_files:
                with NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    attachments.append({
                        "path": tmp.name,
                        "filename": uploaded_file.name,
                        "type": uploaded_file.type
                    })

            # Send email
            recipient_list = [email.strip() for email in to_emails.split(",")]
            send_email(
                to_emails=recipient_list,
                subject=subject,
                html_content=html_content,
                attachments=attachments if attachments else None
            )
            st.success(f"✅ Email sent successfully to: {', '.join(recipient_list)}")
            
            # Clean up temporary files
            for attachment in attachments:
                os.unlink(attachment["path"])
        except Exception as e:
            st.error(f"❌ Failed to send email: {str(e)}")