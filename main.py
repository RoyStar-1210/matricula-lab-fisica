

from vistas.ventana_principal import VentanaPrincipal
from base_datos.conexion import inicializar_bd


def main():
    inicializar_bd()

    app = VentanaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()
