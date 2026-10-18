from flask import Flask, render_template, request

app = Flask(__name__)

PRECIO_TARRO = 9000

# Usuarios permitidos: contraseña y rol que aparece en el saludo
USUARIOS = {
    "juan": {"clave": "admin", "rol": "Administrador"},
    "pepe": {"clave": "user", "rol": "Usuario"},
}


def calcular_descuento(edad):
    """Descuento según la edad: 15% entre 18 y 30, 25% sobre 30."""
    if 18 <= edad <= 30:
        return 0.15
    if edad > 30:
        return 0.25
    return 0


def calcular_compra(nombre, edad, cantidad):
    total_sin_descuento = cantidad * PRECIO_TARRO
    porcentaje = calcular_descuento(edad)
    monto_descuento = round(total_sin_descuento * porcentaje)
    total_pagar = total_sin_descuento - monto_descuento

    return {
        "nombre": nombre,
        "edad": edad,
        "total_sin_descuento": total_sin_descuento,
        "porcentaje": round(porcentaje * 100),
        "monto_descuento": monto_descuento,
        "total_pagar": total_pagar,
    }


def autenticar(usuario, contrasena):
    datos = USUARIOS.get(usuario.strip().lower())
    if datos and datos["clave"] == contrasena:
        return f"Bienvenido {datos['rol']} {usuario.strip().lower()}"
    return None


@app.template_filter("pesos")
def formato_pesos(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = None
    error = None
    datos = {"nombre": "", "edad": "", "cantidad": ""}

    if request.method == "POST":
        datos = {
            "nombre": request.form.get("nombre", "").strip(),
            "edad": request.form.get("edad", "").strip(),
            "cantidad": request.form.get("cantidad", "").strip(),
        }

        if not datos["nombre"]:
            error = "Debes ingresar tu nombre."
        elif not datos["edad"] or not datos["cantidad"]:
            error = "Debes completar la edad y la cantidad de tarros."
        else:
            try:
                edad = int(datos["edad"])
                cantidad = int(datos["cantidad"])
            except ValueError:
                error = "La edad y la cantidad deben ser números enteros."
            else:
                if edad < 0:
                    error = "La edad no puede ser negativa."
                elif cantidad <= 0:
                    error = "La cantidad de tarros debe ser mayor que cero."
                else:
                    resultado = calcular_compra(datos["nombre"], edad, cantidad)

    return render_template(
        "ejercicio1.html", resultado=resultado, error=error, datos=datos
    )


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    mensaje = None
    error = None
    usuario = ""

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        if not usuario or not contrasena:
            error = "Debes ingresar tu nombre y tu contraseña."
        else:
            mensaje = autenticar(usuario, contrasena)
            if mensaje is None:
                error = "Usuario o contraseña incorrectos"

    return render_template(
        "ejercicio2.html", mensaje=mensaje, error=error, usuario=usuario
    )


@app.errorhandler(404)
def pagina_no_encontrada(_error):
    return render_template("error.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
