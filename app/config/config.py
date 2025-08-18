from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    # App
    ENVIRONMENT: str = "development"
    SERVICE_NAME:str ="Order-Management-Service"
    BASE_URL:str = "http://localhost:12345"
    USER_ACCESS_TOKEN_SECRET:str="secret"
    CIPHER_SALT:str="salt"
    SERVICE_IDENTIFIER:str =f"{SERVICE_NAME}-{ENVIRONMENT}"

    # Authentication & JWT
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24

    # Multi-tenant
    DEFAULT_TENANT_ID: str = "default"
    TENANT_HEADER_NAME: str = "X-Tenant-ID"

    # OTP Configuration
    OTP_LENGTH: int = 6
    OTP_EXPIRE_MINUTES: int = 10
    OTP_MAX_ATTEMPTS: int = 3

    # Email Configuration
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_USE_TLS: bool = True
    FROM_EMAIL: str = "noreply@orderservice.com"

    # SMS Configuration
    SMS_PROVIDER: str = "twilio"  # twilio, aws_sns, etc.
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # External Authentication Providers
    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # GitHub OAuth
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""

    # Facebook OAuth
    FACEBOOK_CLIENT_ID: str = ""
    FACEBOOK_CLIENT_SECRET: str = ""

    # Twitter OAuth
    TWITTER_CLIENT_ID: str = ""
    TWITTER_CLIENT_SECRET: str = ""

    # GitLab OAuth
    GITLAB_CLIENT_ID: str = ""
    GITLAB_CLIENT_SECRET: str = ""

    # AWS Cognito
    AWS_COGNITO_USER_POOL_ID: str = ""
    AWS_COGNITO_CLIENT_ID: str = ""
    AWS_COGNITO_CLIENT_SECRET: str = ""
    AWS_REGION: str = "us-east-1"

    # Azure AD
    AZURE_CLIENT_ID: str = ""
    AZURE_CLIENT_SECRET: str = ""
    AZURE_TENANT_ID: str = ""

    # SAML
    SAML_SP_ENTITY_ID: str = ""
    SAML_SP_ACS_URL: str = ""
    SAML_IDP_METADATA_URL: str = ""
    SAML_IDP_SSO_URL: str = ""
    SAML_IDP_X509_CERT: str = ""

    # Feature Flags
    ENABLE_EMAIL_PASSWORD_AUTH: bool = True
    ENABLE_PHONE_OTP_AUTH: bool = True
    ENABLE_TWO_FACTOR_AUTH: bool = True
    ENABLE_SOCIAL_LOGIN: bool = True
    ENABLE_SAML_AUTH: bool = True
    ENABLE_COGNITO_AUTH: bool = True
    ENABLE_AZURE_AD_AUTH: bool = True

    #Database
    DB_USER_NAME: str = "dbuser"
    DB_USER_PASSWORD: str = "dbpassword"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "order_management"
    DB_POOL_SIZE: int = 10
    DB_POOL_RECYCLE: int = 1800
    DB_POOL_TIMEOUT: int = 30
    DB_DIALECT: str = "mysql"
    DB_DRIVER: str = "pymysql"
    DB_CONNECTION_STRING: str = f"{DB_DIALECT}+{DB_DRIVER}://{DB_USER_NAME}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Open-telemetry
    TRACING_ENABLED: bool = False
    TRACING_EXPORTER_TYPE: str = 'NoExporter'
    TRACING_COLLECTOR_ENDPOINT: str ='http://localhost:4317'
    JAEGER_AGENT_HOST: str = "localhost"
    JAEGER_AGENT_PORT: int = 6831
    METRICS_ENABLED: bool = False

    class Config:
        env_file = ".env"
        extra = "allow"

@lru_cache()
def get_settings():
    return Settings()
