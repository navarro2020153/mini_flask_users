from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import db, User

user_bp = Blueprint("user_bp", __name__)

# Página de inicio - lista de usuarios
@user_bp.route("/")
def index():
    users = User.query.all()
    return render_template("user_list.html", users=users)

# Registro de usuarios
@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        # Validaciones básicas
        if password != confirm:
            flash("Las contraseñas no coinciden")
            return redirect(url_for("user_bp.register"))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("El usuario o correo ya existe")
            return redirect(url_for("user_bp.register"))

        # Crear usuario nuevo
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Usuario registrado con éxito")
        return redirect(url_for("user_bp.login"))

    return render_template("register.html")

# Login
@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Inicio de sesión correcto")
            return redirect(url_for("user_bp.profile", id=user.id))
        else:
            flash("Correo o contraseña incorrectos")
            return redirect(url_for("user_bp.login"))

    return render_template("login.html")

# Perfil de usuario
@user_bp.route("/profile/<int:id>")
def profile(id):
    user = User.query.get_or_404(id)
    return render_template("profile.html", user=user)

# Editar usuario
@user_bp.route("/profile/<int:id>/edit", methods=["GET", "POST"])
def edit_profile(id):
    user = User.query.get_or_404(id)

    if request.method == "POST":
        user.username = request.form["username"]
        user.email = request.form["email"]

        if request.form["password"]:
            user.password = generate_password_hash(request.form["password"])

        db.session.commit()
        flash("Perfil actualizado correctamente")
        return redirect(url_for("user_bp.profile", id=user.id))

    return render_template("edit_profile.html", user=user)

# Eliminar usuario
@user_bp.route("/profile/<int:id>/delete", methods=["POST"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado")
    return redirect(url_for("user_bp.index"))

# Cerrar sesión
@user_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Sesión cerrada")
    return redirect(url_for("user_bp.login"))
