"""Punto de entrada HTTP de AMAC."""

import os
from amac.aplicacion import create_app

app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"AMAC Backend corriendo en http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
