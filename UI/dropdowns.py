import flet as ft
from antoine import SUSTANCIAS  


##Dropdown dinámico 
def opciones_sustancias():
    return [
        ft.dropdown.Option(
            key=nombre,
            text=f"{nombre} ({datos['formula']})"
        )
        for nombre, datos in SUSTANCIAS.items()
    ]

def crear_bloque_captura(indice, controles_dinamicos: list = []):
        """Genera un bloque de captura con un dropdown para seleccionar sustancia y
        un textfield para ingresar temperatura, agregando estos controles a la lista 
        de controles dinámicos."""

        
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

##Dropdown unico para definir cantidad de sustancias a calcular 

def estilo_cantidad_sustancias(crear_entradas):
    return ft.Dropdown(
            label="¿Cuántas sustancias quieres calcular?",
            width=300,
            options=[ft.dropdown.Option(str(i)) for i in range(1, 11)],
            on_select=crear_entradas,
        )