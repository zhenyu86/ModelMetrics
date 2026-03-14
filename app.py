from flask import Flask, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, TokenLog


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize login manager
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login."""
        return User.query.get(int(user_id))

    # Template context processor for global variables
    @app.context_processor
    def inject_config():
        """Inject configuration variables into all templates."""
        return dict(
            project_name=app.config.get('PROJECT_NAME', '资源管理系统'),
            project_short_name=app.config.get('PROJECT_SHORT_NAME', 'RMS'),
            resource_name=app.config.get('RESOURCE_NAME', '资源'),
            resource_name_plural=app.config.get('RESOURCE_NAME_PLURAL', '资源'),
            resource_unit=app.config.get('RESOURCE_UNIT', '个'),
            action_add=app.config.get('ACTION_ADD', '增加'),
            action_reduce=app.config.get('ACTION_REDUCE', '扣减'),
            action_consume=app.config.get('ACTION_CONSUME', '消耗'),
            ui_text=app.config.get('UI_TEXT', {}),
            code_name=app.config.get('CODE_NAME', '兑换码'),
        )

    # Register blueprints
    from auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    @login_required
    def index():
        """Redirect to appropriate dashboard based on user role."""
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("user.dashboard"))

    from admin import admin as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from user import user as user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 Not Found errors."""
        return "<h1>404 - Page Not Found</h1>", 404

    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 Internal Server errors."""
        db.session.rollback()
        return "<h1>500 - Server Error</h1>", 500

    return app


if __name__ == "__main__":
    """Run the application."""
    app = create_app()
    with app.app_context():
        # Create database if not exists
        db_name = app.config.get('DATABASE_NAME', 'token_db')
        from sqlalchemy import text
        try:
            db.session.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            db.session.commit()
        except Exception:
            pass  # Database might already exist or no permission
        
        # Create all tables
        db.create_all()
        
        # Create default admin user if not exists
        admin_username = app.config.get('DEFAULT_ADMIN_USERNAME', 'root')
        if not User.query.filter_by(username=admin_username).first():
            admin_user = app.config.get('DEFAULT_ADMIN_USERNAME', 'root')
            admin_password = app.config.get('DEFAULT_ADMIN_PASSWORD', 'root123')
            admin_email = app.config.get('DEFAULT_ADMIN_EMAIL', 'root@example.com')
            root = User(username=admin_user, email=admin_email, is_admin=True, total_tokens=0)
            root.set_password(admin_password)
            db.session.add(root)
            db.session.commit()
            print(f"Default admin user created: {admin_user} / {admin_password}")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
