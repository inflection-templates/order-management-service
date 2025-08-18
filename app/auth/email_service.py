import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import Optional
from app.config.config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class EmailService:
    
    @staticmethod
    def send_email(
        to_email: str, 
        subject: str, 
        body: str, 
        is_html: bool = False,
        from_email: Optional[str] = None
    ) -> bool:
        """Send email via SMTP"""
        try:
            if not settings.SMTP_HOST or not settings.FROM_EMAIL:
                logger.warning("SMTP not configured, email not sent")
                return False
            
            msg = MimeMultipart()
            msg['From'] = from_email or settings.FROM_EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MimeText(body, 'html' if is_html else 'plain'))
            
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            
            if settings.SMTP_USE_TLS:
                server.starttls()
            
            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_invitation_email(to_email: str, invitation_link: str, inviter_name: str = None) -> bool:
        """Send user invitation email"""
        subject = "You're invited to join our platform"
        
        body = f"""
Hello,

You have been invited to join our platform{f' by {inviter_name}' if inviter_name else ''}.

Click the link below to accept your invitation and set up your account:
{invitation_link}

This invitation will expire in 24 hours.

If you didn't expect this invitation, you can safely ignore this email.

Best regards,
The Team
        """.strip()
        
        return EmailService.send_email(to_email, subject, body)
    
    @staticmethod
    def send_welcome_email(to_email: str, user_name: str = None) -> bool:
        """Send welcome/onboarding email"""
        subject = "Welcome to our platform!"
        
        body = f"""
Hello{f' {user_name}' if user_name else ''},

Welcome to our platform! Your account has been successfully created.

Here are some next steps to get you started:
1. Complete your profile information
2. Explore the dashboard
3. Contact support if you need any help

We're excited to have you on board!

Best regards,
The Team
        """.strip()
        
        return EmailService.send_email(to_email, subject, body)
    
    @staticmethod
    def send_password_reset_email(to_email: str, reset_link: str) -> bool:
        """Send password reset email"""
        subject = "Password Reset Request"
        
        body = f"""
Hello,

You requested to reset your password. Click the link below to reset it:
{reset_link}

This link will expire in 24 hours.

If you didn't request this password reset, you can safely ignore this email.

Best regards,
The Team
        """.strip()
        
        return EmailService.send_email(to_email, subject, body)
    
    @staticmethod
    def send_verification_email(to_email: str, verification_link: str) -> bool:
        """Send email verification email"""
        subject = "Please verify your email address"
        
        body = f"""
Hello,

Please verify your email address by clicking the link below:
{verification_link}

This link will expire in 24 hours.

If you didn't create an account with us, you can safely ignore this email.

Best regards,
The Team
        """.strip()
        
        return EmailService.send_email(to_email, subject, body)
    
    @staticmethod
    def send_otp_email(to_email: str, otp_code: str, purpose: str = "login") -> bool:
        """Send OTP via email"""
        subject = f"Your verification code for {purpose}"
        
        body = f"""
Hello,

Your verification code is: {otp_code}

This code will expire in 10 minutes.

If you didn't request this code, please contact support immediately.

Best regards,
The Team
        """.strip()
        
        return EmailService.send_email(to_email, subject, body)
