import flet as ft
def distribucion_pagina(elementos_UI):
    return ft.Column(
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
                elementos_UI["cantidad_dropdown"],
                elementos_UI["area_entradas"],
                ft.Row([elementos_UI["btn_calcular"], elementos_UI["btn_limpiar"]]),
                ft.Divider(),
                ft.Text(
                    "Resultados y procedimiento:",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                elementos_UI["area_resultados"],
            ],
            spacing=15,
        )