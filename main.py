import math
import flet as ft
from antoine import SUSTANCIAS
from antoine import calcular_presion_antoine    
from UI import (
    crear_bloque_captura, 
    estilo_cantidad_sustancias, 
    estilo_boton_calcular, 
    estilo_boton_limpiar, 
    limpiar_todo, 
    calcular_todo, 
    crear_entradas, 
    distribucion_pagina

)


def main(page: ft.Page):
    page.title = "Calculadora de presión de vapor"
    page.window_width = 950
    page.window_height = 850
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20
    controles_dinamicos = []    

    elementos_UI={
        "area_entradas": ft.Column(spacing=12),
        "area_resultados": ft.Column(spacing=12),
        "cantidad_dropdown": estilo_cantidad_sustancias(lambda e: crear_entradas(e, controles_dinamicos, elementos_UI, crear_bloque_captura)),
        "btn_calcular": estilo_boton_calcular(lambda e: calcular_todo(e, elementos_UI, controles_dinamicos, calcular_presion_antoine)),
        "btn_limpiar": estilo_boton_limpiar(lambda e: limpiar_todo(e, elementos_UI, controles_dinamicos))
    }


    page.add(
        distribucion_pagina(elementos_UI)
    )


ft.app(target=main)