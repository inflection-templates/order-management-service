from typing import Optional
from app.config.config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class SMSService:
    
    @staticmethod
    def send_sms(phone: str, message: str) -> bool:
        """Send SMS via configured provider"""
        if settings.SMS_PROVIDER.lower() == "twilio":
            return SMSService._send_via_twilio(phone, message)
        elif settings.SMS_PROVIDER.lower() == "aws_sns":
            return SMSService._send_via_aws_sns(phone, message)
        else:
            logger.warning(f"SMS provider '{settings.SMS_PROVIDER}' not supported")
            return False
    
    @staticmethod
    def _send_via_twilio(phone: str, message: str) -> bool:
        """Send SMS via Twilio"""
        try:
            if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
                logger.warning("Twilio not configured, SMS not sent")
                return False
            
            # Try to import Twilio
            try:
                from twilio.rest import Client
            except ImportError:
                logger.error("Twilio library not installed. Run: pip install twilio")
                return False
            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message_obj = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone
            )
            
            logger.info(f"SMS sent successfully to {phone} via Twilio (SID: {message_obj.sid})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone} via Twilio: {str(e)}")
            return False
    
    @staticmethod
    def _send_via_aws_sns(phone: str, message: str) -> bool:
        """Send SMS via AWS SNS"""
        try:
            if not settings.AWS_REGION:
                logger.warning("AWS region not configured, SMS not sent")
                return False
            
            # Try to import boto3
            try:
                import boto3
            except ImportError:
                logger.error("boto3 library not installed. Run: pip install boto3")
                return False
            
            sns = boto3.client('sns', region_name=settings.AWS_REGION)
            
            response = sns.publish(
                PhoneNumber=phone,
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
            
            logger.info(f"SMS sent successfully to {phone} via AWS SNS (MessageId: {response['MessageId']})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone} via AWS SNS: {str(e)}")
            return False
    
    @staticmethod
    def send_otp_sms(phone: str, otp_code: str, purpose: str = "login") -> bool:
        """Send OTP via SMS"""
        message = f"Your verification code for {purpose}: {otp_code}. This code expires in 10 minutes."
        return SMSService.send_sms(phone, message)
    
    @staticmethod
    def send_password_reset_sms(phone: str, reset_link: str) -> bool:
        """Send password reset SMS"""
        message = f"Reset your password: {reset_link}. This link expires in 24 hours."
        return SMSService.send_sms(phone, message)
    
    @staticmethod
    def send_phone_verification_sms(phone: str, otp_code: str) -> bool:
        """Send phone verification SMS"""
        message = f"Your phone verification code: {otp_code}. This code expires in 10 minutes."
        return SMSService.send_sms(phone, message)
