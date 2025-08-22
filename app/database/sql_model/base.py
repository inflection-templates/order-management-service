from sqlmodel import SQLModel

# SQLModel base class - all models should inherit from SQLModel directly
# No need for declarative_base() in SQLModel
__all__ = ["SQLModel"]
