import flet as ft


def limpiar_todo(e, elementos_UI, controles_dinamicos):
        """Accion para boton limpiar; limpia dropdown, controles dinamicos, area de entradas y area de resultados"""
        elementos_UI["cantidad_dropdown"].value = None
        controles_dinamicos.clear()
        elementos_UI["area_entradas"].controls.clear()
        elementos_UI["area_resultados"].controls.clear()
        elementos_UI["cantidad_dropdown"].update()
        elementos_UI["area_entradas"].update()
        elementos_UI["area_resultados"].update()
        controles_dinamicos = []

def crear_entradas(e, controles_dinamicos, elementos_UI, crear_bloque_captura):
        """Accion para dropdown cantidad de sustancias; crea los controles 
            dinamicos necesarios segun la cantidad seleccionada,
            limpiando previamente cualquier captura o resultado existente."""
        controles_dinamicos.clear()
        elementos_UI["area_entradas"].controls.clear()
        elementos_UI["area_resultados"].controls.clear()

        if not elementos_UI["cantidad_dropdown"].value:
            elementos_UI["area_entradas"].update()
            elementos_UI["area_resultados"].update()
            return

        cantidad = int(elementos_UI["cantidad_dropdown"].value)

        for i in range(1, cantidad + 1):
            bloque = crear_bloque_captura(i, controles_dinamicos)
            elementos_UI["area_entradas"].controls.append(bloque)

        elementos_UI["area_entradas"].update()
        elementos_UI["area_resultados"].update()

def calcular_todo(e, elementos_UI, controles_dinamicos, calcular_temperatura_burbuja):
        """Accion para boton calcular; Calcula la presión de vapor para cada captura, validando que se hayan seleccionado sustancias y temperaturas válidas. Muestra errores específicos para cada captura si hay problemas."""
        elementos_UI["area_resultados"].controls.clear()

        if not controles_dinamicos:
            elementos_UI["area_resultados"].controls.append(
                ft.Text("Primero selecciona cuántas sustancias deseas calcular.")
            )
        if not elementos_UI["presion_sistema_tf"].value:
            elementos_UI["area_resultados"].controls.append(
                ft.Text("Por favor ingresa la presión del sistema.")
            )

            elementos_UI["area_resultados"].update()
            return
        

        errores = validar_capturas(controles_dinamicos, elementos_UI["presion_sistema_tf"].value)
        if errores:
            for error in errores:
                elementos_UI["area_resultados"].controls.append(
                    ft.Text(error, color=ft.Colors.RED)
                )
            elementos_UI["area_resultados"].update()
            return
        


        texto = calcular_temperatura_burbuja(controles_dinamicos, float(elementos_UI["presion_sistema_tf"].value))

        elementos_UI["area_resultados"].controls.append(
                ft.Card(
                    content=ft.Container(
                        width=900,
                        padding=15,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Resultados:",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(texto, selectable=True),
                            ],
                            spacing=10,
                        ),
                    )
                )
            )

        elementos_UI["area_resultados"].update()




def validar_capturas(controles_dinamicos, presion_sistema=None):
    """Valida que cada captura tenga una sustancia seleccionada, una temperatura numérica y una composición numérica entre 0 y 1. Devuelve una lista de errores encontrados."""
    errores = []
    for i, captura in enumerate(controles_dinamicos, start=1):
        dropdown = captura["dropdown"]
        composicion = captura["composicion"]

        if not dropdown.value:
            errores.append(f"Captura {i}: No se ha seleccionado ninguna sustancia.")

        if not presion_sistema:
            errores.append("No se ha ingresado la presión del sistema.")
        else:
            try:                
                presion_val = float(presion_sistema)
                if presion_val <= 0:
                    errores.append("La presión del sistema debe ser un número positivo.")
            except ValueError:
                errores.append("La presión del sistema debe ser un número válido.")

        if not composicion.value:
            errores.append(f"Captura {i}: No se ha ingresado ninguna composición.")
        else:
            try:
                comp_val = float(composicion.value)
                if not (0 <= comp_val <= 1):
                    errores.append(f"Captura {i}: La composición debe estar entre 0 y 1.")
            except ValueError:
                errores.append(f"Captura {i}: La composición debe ser un número válido.")

    return errores