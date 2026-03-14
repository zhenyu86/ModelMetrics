from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, db, TokenLog, VerificationCode
from forms import AdminUserForm
import random
import string

# Create admin blueprint
admin = Blueprint("admin", __name__)


@admin.before_request
def restrict_to_admins():
    """Restrict access to admin users only."""
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Only administrators can access this page.", "warning")
        return redirect(url_for("index"))


@admin.route("/dashboard")
@login_required
def dashboard():
    """Admin dashboard showing all users and token statistics."""
    search_query = request.args.get("search", "").strip()
    if search_query:
        users = User.query.filter(
            User.is_admin == False,
            (User.username.ilike(f"%{search_query}%")) | 
            (User.email.ilike(f"%{search_query}%"))
        ).order_by(User.id).all()
    else:
        users = User.query.filter(User.is_admin == False).order_by(User.id).all()
    return render_template("admin_dashboard.html", users=users, search_query=search_query)


@admin.route("/user/add", methods=["GET", "POST"])
@login_required
def add_user():
    """Route for admin to add new users."""
    form = AdminUserForm()
    
    username = ""
    email = ""
    total_tokens = "0"
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        total_tokens = request.form.get("total_tokens", "0").strip()
        
        has_error = False
        
        if not username:
            flash("Please enter a username.", "warning")
            has_error = True
        elif len(username) < 3:
            flash("Username must be at least 3 characters.", "warning")
            has_error = True
        elif User.query.filter_by(username=username).first():
            flash("Username is already taken.", "warning")
            has_error = True
        
        if not email:
            flash("Please enter an email.", "warning")
            has_error = True
        elif User.query.filter_by(email=email).first():
            flash("Email is already in use.", "warning")
            has_error = True
        
        if not has_error:
            try:
                tokens = int(total_tokens) if total_tokens else 0
            except ValueError:
                tokens = 0
            
            user = User(
                username=username,
                email=email,
                is_admin=False,
                total_tokens=tokens
            )
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()
            flash(f"User {user.username} has been created. Default password: password123", "success")
            return redirect(url_for("admin.dashboard"))
    
    return render_template("edit_user.html", form=form, user=None, 
                          default_username=username, default_email=email, default_tokens=total_tokens)


@admin.route("/user/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    """Route for admin to edit user details."""
    user = User.query.get_or_404(user_id)
    form = AdminUserForm(obj=user)
    
    if request.method == "POST":
        action = request.form.get("action", "")
        
        if action == "password":
            new_password = request.form.get("new_password", "").strip()
            if not new_password:
                flash("Please enter a new password.", "warning")
            elif len(new_password) < 6:
                flash("Password must be at least 6 characters.", "warning")
            else:
                user.set_password(new_password)
                db.session.commit()
                flash("Password changed successfully.", "success")
            return redirect(url_for("admin.edit_user", user_id=user_id))
        
        elif action == "tokens":
            add_tokens_str = request.form.get("add_tokens", "").strip()
            reduce_tokens_str = request.form.get("reduce_tokens", "").strip()
            
            if not add_tokens_str and not reduce_tokens_str:
                flash("Please enter the number of tokens to add or reduce.", "warning")
            else:
                if add_tokens_str:
                    try:
                        amount = int(add_tokens_str)
                        if amount > 0:
                            user.total_tokens += amount
                            log = TokenLog(user_id=user.id, operator_id=current_user.id, action="add", amount=amount)
                            db.session.add(log)
                            flash(f"Added {amount} Tokens.", "success")
                    except ValueError:
                        flash("Token amount must be a number.", "warning")
                
                if reduce_tokens_str:
                    try:
                        amount = int(reduce_tokens_str)
                        if amount > 0:
                            if amount > user.remaining_tokens:
                                flash("Cannot reduce more tokens than remaining.", "warning")
                            else:
                                user.total_tokens -= amount
                                log = TokenLog(user_id=user.id, operator_id=current_user.id, action="reduce", amount=amount)
                                db.session.add(log)
                                flash(f"Reduced {amount} Tokens.", "success")
                    except ValueError:
                        flash("Token amount must be a number.", "warning")
                
                db.session.commit()
            return redirect(url_for("admin.edit_user", user_id=user_id))
        
        else:
            flash("Invalid action.", "warning")
            return redirect(url_for("admin.edit_user", user_id=user_id))
    
    return render_template("edit_user.html", form=form, user=user)


@admin.route("/user/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    """Route for admin to delete a user."""
    if current_user.id == user_id:
        flash("You cannot delete yourself.", "danger")
        return redirect(url_for("admin.dashboard"))
    user = User.query.get_or_404(user_id)
    username = user.username
    # Delete user's token logs first
    TokenLog.query.filter_by(user_id=user_id).delete()
    # Delete verification codes used by this user
    VerificationCode.query.filter_by(used_by=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    flash(f"User {username} has been deleted.", "info")
    return redirect(url_for("admin.dashboard"))


@admin.route("/user/<int:user_id>/add_tokens", methods=["POST"])
@login_required
def add_tokens(user_id):
    """Route for admin to add tokens to a user from dashboard."""
    user = User.query.get_or_404(user_id)
    amount = int(request.form.get("amount", 0))
    if amount <= 0:
        flash("Please enter a positive number.", "warning")
        return redirect(url_for("admin.dashboard"))
    user.total_tokens += amount
    log = TokenLog(user_id=user.id, operator_id=current_user.id, action="add", amount=amount)
    db.session.add(log)
    db.session.commit()
    flash(f"Added {amount} Tokens to user {user.username}.", "success")
    return redirect(url_for("admin.dashboard"))


@admin.route("/user/<int:user_id>/reset_password", methods=["POST"])
@login_required
def reset_password(user_id):
    """Route for admin to reset a user's password."""
    user = User.query.get_or_404(user_id)
    new_password = request.form.get("new_password", "").strip()
    if not new_password:
        new_password = "password123"
    if len(new_password) < 6:
        flash("Password must be at least 6 characters.", "warning")
        return redirect(url_for("admin.dashboard"))
    user.set_password(new_password)
    db.session.commit()
    flash(f"Password for user {user.username} has been reset to: {new_password}", "success")
    return redirect(url_for("admin.dashboard"))


@admin.route("/user/<int:user_id>/reduce_tokens", methods=["POST"])
@login_required
def reduce_tokens(user_id):
    """Route for admin to reduce a user's tokens."""
    user = User.query.get_or_404(user_id)
    amount = int(request.form.get("amount", 0))
    if amount <= 0:
        flash("Please enter a positive number.", "warning")
        return redirect(url_for("admin.dashboard"))
    if amount > user.remaining_tokens:
        flash("Cannot reduce more tokens than remaining.", "warning")
        return redirect(url_for("admin.dashboard"))
    user.total_tokens -= amount
    log = TokenLog(user_id=user.id, operator_id=current_user.id, action="reduce", amount=amount)
    db.session.add(log)
    db.session.commit()
    flash(f"Reduced {amount} Tokens from user {user.username}.", "success")
    return redirect(url_for("admin.dashboard"))


@admin.route("/user/<int:user_id>/logs")
@login_required
def user_logs(user_id):
    """Route to view a specific user's token logs."""
    user = User.query.get_or_404(user_id)
    logs = TokenLog.query.filter_by(user_id=user_id).order_by(TokenLog.timestamp.desc()).all()
    return render_template("user_logs.html", user=user, logs=logs)


@admin.route("/user/<int:user_id>/clear_logs", methods=["POST"])
@login_required
def clear_logs(user_id):
    """Route for admin to clear a user's token logs."""
    user = User.query.get_or_404(user_id)
    TokenLog.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash(f"Token logs for user {user.username} have been cleared.", "success")
    return redirect(url_for("admin.dashboard"))


@admin.route("/users/delete_all", methods=["POST"])
@login_required
def delete_all_users():
    """Route for admin to delete all non-admin users."""
    users = User.query.filter(User.is_admin == False).all()
    count = 0
    for user in users:
        TokenLog.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        count += 1
    db.session.commit()
    flash(f"Deleted {count} users.", "info")
    return redirect(url_for("admin.dashboard"))


@admin.route("/logs")
@login_required
def all_logs():
    """Route to view all token operation logs."""
    search_query = request.args.get("search", "").strip()
    if search_query:
        target_user = User.query.filter(
            User.is_admin == False,
            User.username.ilike(f"%{search_query}%")
        ).first()
        if target_user:
            logs = TokenLog.query.filter_by(user_id=target_user.id).order_by(TokenLog.timestamp.desc()).all()
        else:
            logs = []
    else:
        logs = TokenLog.query.order_by(TokenLog.timestamp.desc()).all()
    return render_template("admin_logs.html", logs=logs, search_query=search_query)


@admin.route("/logs/clear_all", methods=["POST"])
@login_required
def clear_all_logs():
    """Route for admin to clear all token logs."""
    TokenLog.query.delete()
    db.session.commit()
    flash("All operation logs have been cleared.", "success")
    return redirect(url_for("admin.all_logs"))


def generate_code():
    """Generate a random 8-character verification code."""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(8))


@admin.route("/codes", methods=["GET", "POST"])
@login_required
def verification_codes():
    """Route for admin to manage verification codes."""
    if request.method == "POST":
        action = request.form.get("action", "")
        
        if action == "generate":
            count = int(request.form.get("count", 1))
            tokens = int(request.form.get("tokens", 0))
            
            if tokens <= 0:
                flash("Token amount must be greater than 0.", "warning")
            else:
                created = 0
                for _ in range(count):
                    code = generate_code()
                    while VerificationCode.query.filter_by(code=code).first():
                        code = generate_code()
                    vc = VerificationCode(code=code, tokens=tokens)
                    db.session.add(vc)
                    created += 1
                db.session.commit()
                flash(f"Successfully generated {created} verification codes, each with {tokens} Tokens.", "success")
        
        elif action == "manual":
            code = request.form.get("code", "").strip().upper()
            tokens_str = request.form.get("tokens", "0").strip()
            
            if not code:
                flash("Please enter a verification code.", "warning")
            elif len(code) < 4:
                flash("Verification code must be at least 4 characters.", "warning")
            elif VerificationCode.query.filter_by(code=code).first():
                flash("Verification code already exists.", "warning")
            else:
                try:
                    token_amount = int(tokens_str) if tokens_str else 0
                    if token_amount <= 0:
                        flash("Token amount must be greater than 0.", "warning")
                    else:
                        vc = VerificationCode(code=code, tokens=token_amount)
                        db.session.add(vc)
                        db.session.commit()
                        flash(f"Verification code {code} has been created with {token_amount} Tokens.", "success")
                except ValueError:
                    flash("Token amount must be a number.", "warning")
        
        elif action == "delete":
            code_id = request.form.get("code_id")
            vc = VerificationCode.query.get(code_id)
            if vc:
                db.session.delete(vc)
                db.session.commit()
                flash("Verification code has been deleted.", "success")
        
        elif action == "clear_used":
            VerificationCode.query.filter_by(is_used=True).delete()
            db.session.commit()
            flash("All used verification codes have been cleared.", "success")
    
    search_query = request.args.get("search", "").strip()
    filter_status = request.args.get("filter", "all")
    
    query = VerificationCode.query
    
    if search_query:
        if filter_status == "used":
            query = query.join(User, VerificationCode.used_by == User.id).filter(
                (VerificationCode.code.ilike(f"%{search_query}%")) |
                (User.username.ilike(f"%{search_query}%"))
            )
        else:
            subquery = User.query.filter(User.username.ilike(f"%{search_query}%")).with_entities(User.id).subquery()
            query = query.filter(
                (VerificationCode.code.ilike(f"%{search_query}%")) |
                (VerificationCode.used_by.in_(subquery))
            )
    
    if filter_status == "unused":
        query = query.filter(VerificationCode.is_used == False)
    elif filter_status == "used":
        query = query.filter(VerificationCode.is_used == True)
    
    codes = query.order_by(VerificationCode.created_at.desc()).all()
    return render_template("admin_codes.html", codes=codes, search_query=search_query, filter_status=filter_status)
