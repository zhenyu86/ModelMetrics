from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, TokenLog, VerificationCode
from forms import EditProfileForm

# Create user blueprint
user = Blueprint("user", __name__)


@user.route("/dashboard")
@login_required
def dashboard():
    """User dashboard showing token stats and recent activity."""
    recent_logs = TokenLog.query.filter_by(user_id=current_user.id).order_by(TokenLog.timestamp.desc()).limit(5).all()
    return render_template("user_dashboard.html", user=current_user, recent_logs=recent_logs)


@user.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile management - edit profile and change password."""
    form = EditProfileForm(obj=current_user)
    
    if request.method == "POST":
        action = request.form.get("action", "")
        
        if action == "profile":
            if form.validate_on_submit():
                current_user.username = form.username.data
                current_user.email = form.email.data
                db.session.commit()
                flash("Profile updated successfully.", "success")
            return redirect(url_for("user.profile"))
        
        elif action == "password":
            new_password = request.form.get("new_password", "").strip()
            confirm_password = request.form.get("confirm_password", "").strip()
            
            if not new_password:
                flash("Please enter a new password.", "warning")
            elif new_password != confirm_password:
                flash("Passwords do not match.", "danger")
            elif len(new_password) < 6:
                flash("Password must be at least 6 characters.", "warning")
            else:
                current_user.set_password(new_password)
                db.session.commit()
                flash("Password changed successfully.", "success")
            return redirect(url_for("user.profile"))
    
    return render_template("edit_profile.html", form=form)


@user.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Legacy route for password change (kept for compatibility)."""
    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
        elif len(new_password) < 6:
            flash("Password must be at least 6 characters.", "warning")
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash("Password changed successfully.", "success")
            return redirect(url_for("user.profile"))
    return render_template("change_password.html")


@user.route("/consume", methods=["POST"])
@login_required
def consume():
    """Route for user to consume tokens."""
    try:
        amount = int(request.form.get("amount", 0))
    except ValueError:
        flash("Please enter a valid number.", "warning")
        return redirect(url_for("user.dashboard"))
    
    if amount <= 0:
        flash("Amount must be greater than 0.", "warning")
        return redirect(url_for("user.dashboard"))
    
    if current_user.remaining_tokens < amount:
        flash("Insufficient tokens! Please contact admin.", "danger")
        return redirect(url_for("user.dashboard"))
    
    current_user.used_tokens += amount
    log = TokenLog(user_id=current_user.id, operator_id=current_user.id, action="consume", amount=amount)
    db.session.add(log)
    db.session.commit()
    flash(f"Successfully consumed {amount} Tokens.", "success")
    return redirect(url_for("user.dashboard"))


@user.route("/logs")
@login_required
def logs():
    """User's token operation log page."""
    logs = TokenLog.query.filter_by(user_id=current_user.id).order_by(TokenLog.timestamp.desc()).all()
    return render_template("user_logs.html", user=current_user, logs=logs)


@user.route("/redeem", methods=["GET", "POST"])
@login_required
def redeem():
    """Verification code redemption page for users to add tokens."""
    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()
        
        if not code:
            flash("Please enter a verification code.", "warning")
        else:
            vc = VerificationCode.query.filter_by(code=code, is_used=False).first()
            if not vc:
                flash("Verification code does not exist or has been used.", "danger")
            else:
                vc.is_used = True
                vc.used_by = current_user.id
                from datetime import datetime
                vc.used_at = datetime.now()
                
                current_user.total_tokens += vc.tokens
                log = TokenLog(user_id=current_user.id, operator_id=current_user.id, action="add", amount=vc.tokens)
                db.session.add(log)
                db.session.commit()
                flash(f"Redemption successful! {vc.tokens} Tokens have been added to your account.", "success")
                return redirect(url_for("user.dashboard"))
    
    return render_template("user_redeem.html")
