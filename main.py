import math
import flet as ft
from antoine import SUSTANCIAS


def opciones_sustancias():
    return [
        ft.dropdown.Option(
            key=nombre,
            text=f"{nombre} ({datos['formula']})"
        )
        for nombre, datos in SUSTANCIAS.items()
    ]


def calcular_presion_antoine(nombre_sustancia, temperatura):
    datos = SUSTANCIAS[nombre_sustancia]
    A = datos["A"]
    B = datos["B"]
    C = datos["C"]

    valor_ln = A - (B / (temperatura + C))
    presion = math.exp(valor_ln)

    aviso = ""
    if temperatura < datos["t_min"] or temperatura > datos["t_max"]:
        aviso = (
            f"\nAviso: la temperatura {temperatura:.2f} °C está fuera del intervalo "
            f"recomendado [{datos['t_min']} a {datos['t_max']}] °C."
        )

    procedimiento = (
        f"Sustancia: {nombre_sustancia} ({datos['formula']})\n"
        f"A = {A}\n"
        f"B = {B}\n"
        f"C = {C}\n"
        f"t = {temperatura:.2f} °C\n\n"
        f"Procedimiento:\n"
        f"P = Exp(A - B/(t + C))\n"
        f"P = Exp({A} - {B}/({temperatura:.2f} + {C}))\n"
        f"P = Exp({A} - {B/(temperatura + C):.6f})\n"
        f"P = Exp({valor_ln:.6f})\n"
        f"P = {presion:.6f} kPa"
        f"{aviso}"
    )

    return procedimiento


def main(page: ft.Page):
    page.title = "Calculadora de presión de vapor"
    page.window_width = 950
    page.window_height = 850
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    controles_dinamicos = []
    area_entradas = ft.Column(spacing=12)
    area_resultados = ft.Column(spacing=12)

    def crear_bloque_captura(indice):
        dd_sustancia = ft.Dropdown(
            label=f"Sustancia {indice}",
            width=420,
            options=opciones_sustancias(),
        )

        tf_temperatura = ft.TextField(
            label=f"Temperatura {indice} (°C)",
            width=220,
            hint_text="Ejemplo: 25",
        )

        controles_dinamicos.append(
            {
                "dropdown": dd_sustancia,
                "temperatura": tf_temperatura,
            }
        )

        return ft.Card(
            content=ft.Container(
                padding=15,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"Captura {indice}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Row(
                            controls=[dd_sustancia, tf_temperatura],
                            wrap=True,
                        ),
                    ],
                    spacing=10,
                ),
            )
        )

    def crear_entradas(e):
        controles_dinamicos.clear()
        area_entradas.controls.clear()
        area_resultados.controls.clear()

        if not cantidad_dropdown.value:
            area_entradas.update()
            area_resultados.update()
            return

        cantidad = int(cantidad_dropdown.value)

        for i in range(1, cantidad + 1):
            bloque = crear_bloque_captura(i)
            area_entradas.controls.append(bloque)

        area_entradas.update()
        area_resultados.update()

    def calcular_todo(e):
        area_resultados.controls.clear()

        if not controles_dinamicos:
            area_resultados.controls.append(
                ft.Text("Primero selecciona cuántas sustancias deseas calcular.")
            )
            area_resultados.update()
            return

        for i, captura in enumerate(controles_dinamicos, start=1):
            dd_sustancia = captura["dropdown"]
            tf_temperatura = captura["temperatura"]

            if not dd_sustancia.value:
                area_resultados.controls.append(
                    ft.Text(
                        f"Error en captura {i}: selecciona una sustancia.",
                        color=ft.Colors.RED,
                    )
                )
                continue

            if not tf_temperatura.value or not tf_temperatura.value.strip():
                area_resultados.controls.append(
                    ft.Text(
                        f"Error en captura {i}: ingresa una temperatura.",
                        color=ft.Colors.RED,
                    )
                )
                continue

            try:
                t = float(tf_temperatura.value)
            except ValueError:
                area_resultados.controls.append(
                    ft.Text(
                        f"Error en captura {i}: la temperatura debe ser numérica.",
                        color=ft.Colors.RED,
                    )
                )
                continue

            texto = calcular_presion_antoine(dd_sustancia.value, t)

            area_resultados.controls.append(
                ft.Card(
                    content=ft.Container(
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

        area_resultados.update()

    def limpiar_todo(e):
        cantidad_dropdown.value = None
        controles_dinamicos.clear()
        area_entradas.controls.clear()
        area_resultados.controls.clear()
        cantidad_dropdown.update()
        area_entradas.update()
        area_resultados.update()

    cantidad_dropdown = ft.Dropdown(
        label="¿Cuántas sustancias quieres calcular?",
        width=300,
        options=[ft.dropdown.Option(str(i)) for i in range(1, 11)],
        on_select=crear_entradas,
    )

    btn_calcular = ft.ElevatedButton("Calcular", on_click=calcular_todo)
    btn_limpiar = ft.OutlinedButton("Limpiar todo", on_click=limpiar_todo)

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Cálculo de presión de vapor con ecuación de Antoine",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Selecciona cuántas sustancias quieres calcular y después captura la sustancia y su temperatura."
                ),
                ft.Divider(),
                cantidad_dropdown,
                area_entradas,
                ft.Row([btn_calcular, btn_limpiar]),
                ft.Divider(),
                ft.Text(
                    "Resultados y procedimiento:",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                area_resultados,
            ],
            spacing=15,
        )
    )


ft.app(target=main)