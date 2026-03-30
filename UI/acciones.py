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

def calcular_todo(e, elementos_UI, controles_dinamicos, calcular_presion_antoine):
        """Accion para boton calcular; Calcula la presión de vapor para cada captura, validando que se hayan seleccionado sustancias y temperaturas válidas. Muestra errores específicos para cada captura si hay problemas."""
        elementos_UI["area_resultados"].controls.clear()

        if not controles_dinamicos:
            elementos_UI["area_resultados"].controls.append(
                ft.Text("Primero selecciona cuántas sustancias deseas calcular.")
            )
            elementos_UI["area_resultados"].update()
            return

        for i, captura in enumerate(controles_dinamicos, start=1):
            dd_sustancia = captura["dropdown"]
            tf_temperatura = captura["temperatura"]

            if not dd_sustancia.value:
                elementos_UI["area_resultados"].controls.append(
                    ft.Text(
                        f"Error en captura {i}: selecciona una sustancia.",
                        color=ft.Colors.RED,
                    )
                )
                continue

            if not tf_temperatura.value or not tf_temperatura.value.strip():
                elementos_UI["area_resultados"].controls.append(
                    ft.Text(
                        f"Error en captura {i}: ingresa una temperatura.",
                        color=ft.Colors.RED,
                    )
                )
                continue

            try:
                t = float(tf_temperatura.value)
            except ValueError:
                elementos_UI["area_resultados"].controls.append(
                    ft.Text(
                        f"Error en captura {i}: la temperatura debe ser numérica.",
                        color=ft.Colors.RED,
                    )
                )
                continue

            texto = calcular_presion_antoine(dd_sustancia.value, t)

            elementos_UI["area_resultados"].controls.append(
                ft.Card(
                    content=ft.Container(
                        width=900,
                        padding=15,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    f"Resultado {i}",
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