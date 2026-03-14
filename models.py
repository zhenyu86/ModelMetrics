from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and token management."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    total_tokens = db.Column(db.Integer, default=0)
    used_tokens = db.Column(db.Integer, default=0)

    def set_password(self, pwd):
        """Set password hash from plain password."""
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        """Verify password against stored hash."""
        return check_password_hash(self.password_hash, pwd)

    @property
    def remaining_tokens(self):
        """Calculate remaining tokens (total - used)."""
        return max(self.total_tokens - self.used_tokens, 0)

    def __repr__(self):
        return f"<User {self.username}>"


class TokenLog(db.Model):
    """Token log model to track all token operations."""
    __tablename__ = "token_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    operator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(20))
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship("User", backref=db.backref("logs", lazy="dynamic"), foreign_keys=[user_id])
    operator = db.relationship("User", foreign_keys=[operator_id])


class VerificationCode(db.Model):
    """Verification code model for token redemption."""
    __tablename__ = "verification_codes"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    tokens = db.Column(db.Integer, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    used_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship("User", foreign_keys=[used_by])
