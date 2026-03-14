from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField("用户名", validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("确认密码", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("注册")

    def validate_username(self, field):
        """Check if username is already taken."""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已被使用")

    def validate_email(self, field):
        """Check if email is already registered."""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已被注册")


class LoginForm(FlaskForm):
    """User login form."""
    username = StringField("用户名", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField("登录")


class AdminUserForm(FlaskForm):
    """Admin user management form."""
    username = StringField("用户名", validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    total_tokens = IntegerField("总量", validators=[DataRequired()])
    submit = SubmitField("保存")

    def __init__(self, original_username=None, *args, **kwargs):
        """Initialize form with original username for validation."""
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, field):
        """Check if username is already taken (excluding current user)."""
        if field.data != self.original_username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError("用户名已被使用")


class EditProfileForm(FlaskForm):
    """User profile edit form."""
    username = StringField("用户名", validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    submit = SubmitField("保存")

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        """Initialize form with original data for validation."""
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, field):
        """Check if username is already taken (excluding current user)."""
        if field.data != self.original_username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError("用户名已被使用")

    def validate_email(self, field):
        """Check if email is already registered (excluding current user)."""
        if field.data != self.original_email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError("邮箱已被注册")
