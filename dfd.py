import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime


df = pd.read_excel('antropometrias.xlsx')

# Definir colores para el layout
colors = {'background':'#FDFEFE','text':'#FEFEFE'}
style1 = {'textAlign':'center', 'color':colors['text']}

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])




#CARTA PESO
carta_peso = dbc.Card(
    [
        dbc.CardHeader(html.Div(id='peso-jugador')),
        dbc.CardBody(
            [
                html.H4("Últimos 5 pesos", className="card-title"),  # Cambiar el título de la carta
                html.P(id='ultimos-pesos', className="card-text"),  # Mostrar los últimos pesos aquí
            ]
        ),
        dbc.CardFooter("AZUL: mantiene VERDE: bajo ROJO: subió ", style={'font-size': '12px'}),  # Aplicar estilo para reducir el tamaño de las letras
    ],
    style={"width": "18rem", "margin-left": "20px"},  # Agregar margen a la izquierda
)


#CARTA PESO
@app.callback(
    [dash.dependencies.Output('peso-jugador', 'children'),
     dash.dependencies.Output('ultimos-pesos', 'children')],
    [dash.dependencies.Input('selector2', 'value')]
)
def update_card_title(jugador):
    peso = df.loc[df['nombre'] == jugador, 'peso'].values[0]
    ultimos_pesos = df.loc[df['nombre'] == jugador, 'peso'].tail(5).tolist()
    
    # Obtener el peso anterior
    peso_anterior = ultimos_pesos[-2] if len(ultimos_pesos) >= 2 else peso
    
    # Determinar el color del texto según la comparación con el peso anterior
    if peso > peso_anterior:
        peso_style = {'color': 'green'}
    elif peso < peso_anterior:
        peso_style = {'color': 'red'}
    else:
        peso_style = {'color': 'blue'}
    
    # Crear elementos HTML con el estilo de color correspondiente
    peso_element = html.H5(className="card-title")
    peso_element.children = ["PESO ACTUAL: ", html.Span(f"{peso} kg", style=peso_style)]
    
    ultimos_pesos_element = html.P(className="card-text")
    
    # Crear elementos Span para los últimos pesos con espacios entre ellos
    ultimos_pesos_spans = []
    for peso in ultimos_pesos:
        if peso > peso_anterior:
            peso_span = html.Span(f"{peso} kg", style={'color': 'green', 'margin-right': '5px'})
        elif peso < peso_anterior:
            peso_span = html.Span(f"{peso} kg", style={'color': 'red', 'margin-right': '5px'})
        else:
            peso_span = html.Span(f"{peso} kg", style={'color': 'blue', 'margin-right': '5px'})
        ultimos_pesos_spans.append(peso_span)
    
    ultimos_pesos_element.children = ultimos_pesos_spans
    
    return peso_element, ultimos_pesos_element


#CARTA JUGADOR
carta_jugador = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src='/assets/Andujar.png',
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4(id="card-title", className="card-title", style={"text-align": "left"}),
                            html.Div([
                                html.Strong("Peso:", style={"text-align": "left"}),
                                html.Br(),
                                html.Span(id="card-peso", className="card-text", style={"text-align": "left"})
                            ], style={"text-align": "left"}),
                            html.Div([
                                html.Strong("Altura:", style={"text-align": "left"}),
                                html.Br(),
                                html.Span(id="card-altura", className="card-text", style={"text-align": "left"})
                            ], style={"text-align": "left"}),
                            html.Small(id="card-last-updated", className="card-text text-muted", style={"text-align": "left"}),
                        ],
                        style={"text-align": "left"}  # Alinear todo el contenido del cuerpo a la izquierda
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
            style={"justify-content": "flex-start"}  # Alinear la fila hacia la izquierda
        )
    ],
    className="mb-3",
    style={"maxWidth": "540px"},
)


#CARTA JUGADOR
@app.callback(
    [Output("card-title", "children"), Output("card-peso", "children"), Output("card-altura", "children"), Output("card-last-updated", "children")],
    Input("selector4", "value")  # Asegúrate de que el ID del selector sea correcto
)
def update_card_content(selected_name):
    # Aquí debes cargar tu dataframe df con los nombres, la información del peso, altura y fecha
    jugador = df.loc[df["nombre"] == selected_name].iloc[-1]  # Obtener el último jugador seleccionado
    
    nombre = jugador["nombre"]
    peso = jugador["peso"]
    altura = jugador["Talla"]
    fecha_actualizacion = jugador["fecha"]
    
    card_title = nombre
    card_peso = f"{peso} kg"
    card_altura = f"{altura} cm"
    card_last_updated = f"Fecha de actualización ({fecha_actualizacion.date()})"
    
    return card_title, card_peso, card_altura, card_last_updated



# CARTA ADIPOSA
carta_adiposa = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-adiposa", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0', 'color': 'white'}),
            html.P("Adiposa", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0', 'color': 'white'}),
        ]
    ),
    style={"width": "17rem", "height": "5.3rem", 'background-color': '#bf3939', 'border-radius': '5px 0 0 0'},
)




# CARTA ADIPOSA
@app.callback(
    Output("ultima-adiposa", "children"),
    Input("selector4", "value")
)
def update_adiposa(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'adiposa'
    adiposa_actualizada = df_filtrado.iloc[0]["adiposa"]
    
    # Formatear el valor de adiposa con dos decimales
    adiposa_actualizada = "{:.2f}".format(adiposa_actualizada)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return adiposa_actualizada





# CARTA MUSCULAR
carta_muscular = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-muscular", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0', 'color': 'white'}),
            html.P("Muscular", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0', 'color': 'white'}),
        ]
    ),
    style={"width": "16.8rem", "height": "5.3rem", 'background-color': '#bf3939', 'border-radius': '0 5px 0 0'},
)

# CARTA MUSCULAR
@app.callback(
    Output("ultima-muscular", "children"),
    Input("selector4", "value")
)
def update_muscular(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'muscular'
    muscular_actualizada = df_filtrado.iloc[0]["muscular"]
    
    # Formatear el valor de muscular con dos decimales
    muscular_actualizada = "{:.2f}".format(muscular_actualizada)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return muscular_actualizada



# CARTA Score Z adiposa
carta_score_z_adiposa = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-score-z-adiposa", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0', 'color': 'white'}),
            html.P("Score Z adiposa:", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0', 'color': 'white'}),
        ]
    ),
    style={"width": "17rem", "height": "5.3rem", 'background-color': '#bf3939', 'border-radius': '0 0 0 5px'},
)

# CARTA Score Z adiposa
@app.callback(
    Output("ultima-score-z-adiposa", "children"),
    Input("selector4", "value")
)
def update_score_z_adiposa(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'Score Z adiposa'
    score_z_adiposa_actualizado = df_filtrado.iloc[0]["Score Z adiposa:"]
    
    # Formatear el valor de Score Z adiposa con dos decimales
    score_z_adiposa_actualizado = "{:.2f}".format(score_z_adiposa_actualizado)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return score_z_adiposa_actualizado


# CARTA Score Z muscular
carta_score_z_muscular = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-score-z-muscular", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0', 'color': 'white'}),
            html.P("Score Z muscular:", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0', 'color': 'white'}),
        ]
    ),
    style={"width": "16.8rem", "height": "5.3rem", 'background-color': '#bf3939', 'border-radius': '0 0 5px 0'},
)

# CARTA Score Z muscular
@app.callback(
    Output("ultima-score-z-muscular", "children"),
    Input("selector4", "value")
)
def update_score_z_muscular(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'Score Z muscular'
    score_z_muscular_actualizado = df_filtrado.iloc[0]["Score Z muscular:"]
    
    # Formatear el valor de Score Z muscular con dos decimales
    score_z_muscular_actualizado = "{:.2f}".format(score_z_muscular_actualizado)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return score_z_muscular_actualizado





# CARTA MASA SUPERIOR (KG)
carta_masa_superior = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-msuperiorkg", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0', 'color': 'withe'}),
            html.P("Masa Superior (kg)", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0', 'color': 'withe'}),
        ]
    ),
    style={"width": "17rem", "height": "5.3rem", 'background-color': '#bf3939', 'border-radius': '5px 0 0 0'},
)


# CARTA MASA SUPERIOR (KG)
@app.callback(
    Output("ultima-msuperiorkg", "children"),
    Input("selector4", "value")
)
def update_msuperiorkg(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'msuperiorkg'
    msuperiorkg_actualizado = df_filtrado.iloc[0]["mSuperiorkg"]
    
    # Formatear el valor de Masa Superior con dos decimales
    msuperiorkg_actualizado = "{:.2f}".format(msuperiorkg_actualizado)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return msuperiorkg_actualizado





#CARTA MASA MEDIA (KG)
carta_masa_media = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-mMediakg", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0', 'color': 'withe'}),
            html.P("Masa Media (kg):", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0', 'color': 'withe'}),
        ]
    ),
    style={"width": "17rem", "height": "5.3rem", 'background-color': '#bf3939', 'border-radius': '0 0 0 0'},
)


#CARTA MASA MEDIA (KG)
@app.callback(
    Output("ultima-mMediakg", "children"),
    Input("selector4", "value")
)
def update_mMediakg(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'mMediakg'
    mMediakg_actualizado = df_filtrado.iloc[0]["mMediakg"]
    
    # Formatear el valor de Masa Media con dos decimales
    mMediakg_actualizado = "{:.2f}".format(mMediakg_actualizado)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return mMediakg_actualizado



#CARTA MASA INFERIOR (KG)
carta_masa_inferior = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-mInferiorkg", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0', 'color': 'withe'}),
            html.P("Masa Inferior (kg):", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0', 'color': 'withe'}),
        ]
    ),
    style={"width": "17rem", "height": "5.3rem", 'background-color': '#bf3939', 'border-radius': '0 0 0 5px'},
)



#CARTA MASA INFERIOR (KG)
@app.callback(
    Output("ultima-mInferiorkg", "children"),
    Input("selector4", "value")
)
def update_mInferiorkg(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'mInferiorkg'
    mInferiorkg_actualizado = df_filtrado.iloc[0]["mInferiorkg"]
    
    # Formatear el valor de Masa Inferior con dos decimales
    mInferiorkg_actualizado = "{:.2f}".format(mInferiorkg_actualizado)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return mInferiorkg_actualizado




# CARTA MASA SUPERIOR (%)
carta_masa_superior_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-mSuperior", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0',  'color': '#bf3939'}),
            html.P("Masa Superior (%)", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0',  'color': '#bf3939'}),
        ]
    ),
    style={"width": "17rem", "height": "5.3rem", 'background-color': '#2b2a2a', 'border-radius': '0 5px 0 0'},
)




# CARTA MASA SUPERIOR (%)
@app.callback(
    Output("ultima-mSuperior", "children"),
    Input("selector4", "value")
)
def update_mSuperior(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'mSuperior%'
    mSuperior_actualizado = df_filtrado.iloc[0]["mSuperior%"]
    
    # Formatear el valor de Masa Superior con dos decimales
    mSuperior_actualizado = "{:.2f}".format(mSuperior_actualizado)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return mSuperior_actualizado







# CARTA MASA MEDIA (%)
carta_masa_media_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-mmediaporcentaje", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0', 'color': '#bf3939'}),
            html.P("Masa Media (%)", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0', 'color': '#bf3939'}),
        ]
    ),
    style={"width": "17rem", "height": "5.3rem", 'background-color': '#2b2a2a', 'border-radius': '0 0 0 0'},
)

# CARTA MASA MEDIA (%)
@app.callback(
    Output("ultima-mmediaporcentaje", "children"),
    Input("selector4", "value")
)
def update_mmediaporcentaje(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'mMedia%'
    mmediaporcentaje_actualizado = df_filtrado.iloc[0]["mMedia%"]
    
    # Formatear el valor de Masa Media con dos decimales
    mmediaporcentaje_actualizado = "{:.2f}".format(mmediaporcentaje_actualizado)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return mmediaporcentaje_actualizado




# CARTA MASA INFERIOR (%)
carta_masa_inferior_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="ultima-minferiorporcentaje", className="card-title", style={'text-align': 'left', 'font-size': '1.5rem', 'margin-bottom': '0', 'color': '#bf3939'}),
            html.P("Masa Inferior (%)", className="card-text", style={'text-align': 'left', 'font-size': '1.3rem', 'margin-top': '0', 'color': '#bf3939'}),
        ]
    ),
    style={"width": "17rem", "height": "5.3rem", 'background-color': '#2b2a2a', 'border-radius': '0 0 5px 0'},
)

# CARTA MASA INFERIOR (%)
@app.callback(
    Output("ultima-minferiorporcentaje", "children"),
    Input("selector4", "value")
)
def update_minferiorporcentaje(nombre):
    # Filtrar el DataFrame según el nombre seleccionado
    df_filtrado = df[df["nombre"] == nombre]
    
    # Ordenar el DataFrame por la columna 'fecha' de forma descendente
    df_filtrado = df_filtrado.sort_values("fecha", ascending=False)
    
    # Obtener el valor más reciente de la columna 'mInferior%'
    minferiorporcentaje_actualizado = df_filtrado.iloc[0]["mInferior%"]
    
    # Formatear el valor de Masa Inferior con dos decimales
    minferiorporcentaje_actualizado = "{:.2f}".format(minferiorporcentaje_actualizado)
    
    # Retornar el valor actualizado con dos decimales como contenido del título de la carta
    return minferiorporcentaje_actualizado



















# Definir el contenido de cada solapa
tab1_content = html.Div([
    html.Div([
        html.Div([
            html.Label('JUGADOR', style={'margin-right': '10px', 'font-size': '16px'}),
            dcc.Dropdown(
                id='selector',
                options=[{'label': i, 'value': i} for i in df['nombre'].unique()],
                value=df['nombre'].unique()[0],
                style={'width': '300px', 'margin-right': '80px', 'font-size': '16px'}
            )
        ], style={'display': 'flex', 'align-items': 'center'}),
        
        html.Div([
            html.Label('FECHA', style={'margin-right': '10px', 'font-size': '16px'}),
            dcc.DatePickerRange(
                id='selector_fecha',
                min_date_allowed=min(df['fecha']),
                max_date_allowed=max(df['fecha']),
                start_date=min(df['fecha']),
                end_date=max(df['fecha']),
                style={'width': '600px', 'margin-right': '80px', 'font-size': '16px'}
            )
        ], style={'display': 'flex', 'align-items': 'center'})
        
    ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    
    html.Div([
        html.Div([dcc.Graph(id='Waterfall_peso')],
                 style={'width': '50%', 'float': 'left', 'display': 'inline-block'}),
    
        html.Div([dcc.Graph(id='Bar_AdiMusc')],
                 style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
    
    ], style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}),
    
    html.Div([
        html.Div([dcc.Graph(id='Bar_masas')],
                 style={'width': '100%', 'display': 'inline-block'}),
    
        html.Div([dcc.Graph(id='Bar_6p')],
                 style={'width': '50%', 'display': 'inline-block'}),
    
        html.Div([dcc.Graph(id='Bar_imo')],
                 style={'width': '50%', 'display': 'inline-block'}),
    
    ], style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}),
    
    html.Div([
        html.Div([dcc.Graph(id='scatter_punet2')],
                 style={'width': '50%', 'margin': '0 auto'})
    ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center'})
], id="tab-1")





tab2_content = html.Div([
    html.Div([
        html.Div([
            html.Label('JUGADOR', style={'margin-right': '10px', 'font-size': '16px'}),
            dcc.Dropdown(
                id='selector2',
                options=[{'label': i, 'value': i} for i in df['nombre'].unique()],
                value=df['nombre'].unique()[0],
                style={'width': '300px', 'margin-right': '80px', 'font-size': '16px'}
            )
        ], style={'display': 'flex', 'align-items': 'center'}),

        html.Div([
            html.Label('FECHA', style={'margin-right': '10px', 'font-size': '16px'}),
            dcc.DatePickerRange(
                id='selector_fecha2',
                min_date_allowed=min(df['fecha']),
                max_date_allowed=max(df['fecha']),
                start_date=min(df['fecha']),
                end_date=max(df['fecha']),
                style={'width': '600px', 'margin-right': '80px', 'font-size': '16px'}
            )
        ], style={'display': 'flex', 'align-items': 'center'}),

    ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-bottom': '10px'}),

    carta_peso,  # Agregar la carta al layout

    html.Div([
        html.Div([dcc.Graph(id='estanadar_general')],
                 style={'width': '50%', 'display': 'inline-block'}),

        html.Div([dcc.Graph(id='semaforo')],
                 style={'width': '50%', 'display': 'inline-block'}),

    ], style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}),

    html.Div([
        html.Div([dcc.Graph(id='semaforo_adiposa')],
                 style={'width': '50%', 'display': 'inline-block'}),

        html.Div([dcc.Graph(id='semaforo_muscular')],
                 style={'width': '50%', 'display': 'inline-block'}),

    ], style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}),

    html.Div([dcc.Graph(id='punnett', style={'width': '50%', 'margin': '0 auto'})],
             style={'width': '100%', 'display': 'flex', 'justify-content': 'center'})
], id="tab-2")






tab3_content = html.Div([
    html.Div([
        html.Label('POSICIÓN', style={'margin-right': '10px', 'font-size': '16px'}),
        dcc.Dropdown(
            id='selector_posicion',
            options=[{'label': i, 'value': i} for i in df['posición'].unique()],
            value=df['posición'].unique()[0],
            style={'width': '300px', 'margin-right': '80px', 'font-size': '16px'}
        ),
        
        html.Label('FECHA', style={'margin-right': '10px', 'font-size': '16px'}),
        dcc.DatePickerRange(
            id='selector_fecha3',
            min_date_allowed=min(df['fecha']),
            max_date_allowed=max(df['fecha']),
            start_date=min(df['fecha']),
            end_date=max(df['fecha']),
            style={'width': '600px', 'margin-right': '80px', 'font-size': '16px'}
        ),
        ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-bottom': '10px'}),
    
    html.Div([dcc.Graph(id='6pliegues_posición')],
             style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}),
    html.Div([dcc.Graph(id='imo_posición')],
             style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}),
    html.Div([dcc.Graph(id='promedio_talla')],
             style={'width': '50%', 'display': 'inline-block', 'text-align': 'center'}),
    html.Div([dcc.Graph(id='promedio_peso')],
             style={'width': '50%', 'display': 'inline-block', 'text-align': 'center'}),
    html.Div([dcc.Graph(id='promedio_talla_plantel')],
             style={'width': '50%', 'display': 'inline-block', 'text-align': 'center'}),
    html.Div([dcc.Graph(id='promedio_peso_plantel')],
             style={'width': '50%', 'display': 'inline-block', 'text-align': 'center'})                                                   
], id="tab-3")






tab4_content = html.Div(
    [
        # Contenido de la pestaña 4
        html.Div(
            [
                html.Div(
                    [
                        html.Label('JUGADOR', style={'margin-right': '10px', 'font-size': '16px'}),
                        dcc.Dropdown(
                            id='selector4',
                            options=[{'label': i, 'value': i} for i in df['nombre'].unique()],
                            value=df['nombre'].unique()[0],
                            style={'width': '300px', 'margin-right': '80px', 'font-size': '16px'},
                        ),
                    ],
                    style={'display': 'flex', 'align-items': 'center'},
                ),
                html.Div(
                    [
                        html.Label('FECHA', style={'margin-right': '10px', 'font-size': '16px'}),
                        dcc.DatePickerRange(
                            id='selector_fecha4',
                            min_date_allowed=min(df['fecha']),
                            max_date_allowed=max(df['fecha']),
                            start_date=min(df['fecha']),
                            end_date=max(df['fecha']),
                            style={'width': '600px', 'margin-right': '80px', 'font-size': '16px'},
                        ),
                    ],
                    style={'display': 'flex', 'align-items': 'center'},
                ),
            ],
            style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-bottom': '10px'},
        ),
        html.Div(
            [
                html.Div(
                    [
                        carta_jugador,
                        html.Div(
                            [carta_adiposa, carta_muscular],
                            style={'display': 'flex', 'justify-content': 'left', 'align-items': 'flex-start'},

                        ),
                        html.Div(
                            [carta_score_z_adiposa, carta_score_z_muscular],
                            style={'display': 'flex', 'justify-content': 'left', 'align-items': 'flex-start'}
                        ),
                        html.H2('MASA MUSCULAR', style={'text-align': 'left', 'margin-top': '180px', 'margin-left': '130px'}),
                        
                        html.Div(
                            [carta_masa_superior,carta_masa_superior_2],
                            style={'display': 'flex', 'justify-content': 'left', 'align-items': 'flex-start'}
                        ),
                        html.Div(
                            [carta_masa_media, carta_masa_media_2],
                            style={'display': 'flex', 'justify-content': 'left', 'align-items': 'flex-start'}
                        ),
                        html.Div(
                            [carta_masa_inferior, carta_masa_inferior_2],
                            style={'display': 'flex', 'justify-content': 'left', 'align-items': 'flex-start'}
                        )
                    ],
                    style={'width': '40%', 'display': 'inline-block', 'text-align': 'center', 'margin-left': '100px', 'margin-top': '20px'},
                ),
                html.Div(
                    [
                        dcc.Graph(id='grafico_torta', style={'width': '90%', 'height': '500px', 'margin-right': '50px', 'justify-content': 'left', 'margin-top': '0px'}),
                        dcc.Graph(id='punnet4', style={'width': '80%', 'height': '500px', 'margin-left': '100px', 'justify-content': 'left'})
                    ],
                    style={'width': '60%', 'display': 'inline-block', 'text-align': 'center'},
                ),
            ],
            style={'width': '100%', 'display': 'flex', 'justify-content': 'flex-start', 'align-items': 'flex-start'},
        ),
    ],
    id="tab-4",
)








app.title = "DASHBOARD EDLP"

#FALTA AGREGAR EL IMPORT DE EXCEL


app.layout = html.Div([
    html.Div(
        [
            html.Img(src='/assets/ESCUDO_EDLP.png', style={'height': '95px', 'width': '60px', 'margin-bottom': '20px'}),
            html.H1("DASHBOARD NUTRICIÓN ESTUDIANTES DE LA PLATA", style={'text-align': 'center', 'font-size': '30px', 'margin-bottom': '20px', 'color': 'white'}),
        ],
        style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'background-color': 'black', 'padding': '10px'}
    ),
    dbc.Tabs(
        [
            dbc.Tab(tab1_content, label="INFORME EVOLUTIVO INDIVIDUAL", label_style={'color': 'black', 'background-color': 'white'}, active_label_style={'color': 'red'}),
            dbc.Tab(tab2_content, label="DASH DE GESTIÓN", label_style={'color': 'black', 'background-color': 'white'}, active_label_style={'color': 'red'}),
            dbc.Tab(tab3_content, label="INFORME COLECTIVO", label_style={'color': 'black', 'background-color': 'white'}, active_label_style={'color': 'red'}),
            dbc.Tab(tab4_content, label="INFORME INDIVIDUAL", label_style={'color': 'black', 'background-color': 'white'}, active_label_style={'color': 'red'})
        ],
        style={'background-color': 'black', 'padding': '0px', 'margin-bottom': '10px'}
    )
], style={'position': 'relative'})




#DASH 1

@app.callback(Output('Waterfall_peso', 'figure'),
              [Input('selector_fecha', 'start_date'), Input('selector_fecha', 'end_date'), Input('selector', 'value')])
def actualizar_graph_peso(start_date, end_date, selector):
    df_filtered = df[(df['nombre'] == selector) & (df['fecha'] >= start_date) & (df['fecha'] <= end_date)]
    
     # Convertir la columna de peso en una lista para usar como eje y

    return{
        'data': [go.Waterfall(
            name='.',
            orientation="v",
            measure=["absolute", "relative", "total", "relative", "total"],
            x=df_filtered["fecha"],
            textposition="inside",
            text=df_filtered["peso"],
            y=df_filtered["dif"],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "green"}},
            decreasing={"marker": {"color": "red"}},
            totals={"marker": {"color": "blue", "line": {"color": "white", "width": 3}}}
        )],

        'layout': go.Layout(
            title = f"Evolución de peso",
            xaxis_title = "FECHA",
            yaxis_title = "PESO (Kg)",
            font=dict(size=18),
            showlegend = True,
            legend_title = "",
            plot_bgcolor='rgba(0,0,0,0)'
        )
    }


@app.callback(
    Output('Bar_AdiMusc', 'figure'),
    [Input('selector_fecha', 'start_date'), Input('selector_fecha', 'end_date'), Input('selector', 'value')]
)
def actualizar_graph_masa(start_date, end_date, selector):
    df_filtered = df[(df['nombre'] == selector) & (df['fecha'] >= start_date) & (df['fecha'] <= end_date)]
    
    # Calcular los coeficientes de la línea de tendencia
    coef = np.polyfit(np.arange(len(df_filtered['adiposa/muscular'])), df_filtered['adiposa/muscular'], 1)
    tendencia = np.poly1d(coef)
    
    return {
        'data': [
            go.Bar(
                x=df_filtered['fecha'],
                y=df_filtered['adiposa'],
                name='Adiposa',
                marker_color='rgb(55, 83, 109)'
            ),
            go.Bar(
                x=df_filtered['fecha'],
                y=df_filtered['muscular'],
                name='Muscular',
                marker_color='rgb(26, 118, 255)'
            ),
            go.Scatter(
                x=df_filtered['fecha'], 
                y=df_filtered['adiposa/muscular'], 
                mode='markers', 
                name='Adiposa/Muscular'
            ),
            go.Scatter(
                x=df_filtered['fecha'],
                y=tendencia(np.arange(len(df_filtered['adiposa/muscular']))),
                mode='lines',
                name='Línea de tendencia'
            )
        ],
        'layout': go.Layout(
            title = f"Evolución de masas",
            xaxis_title = "FECHA",
            yaxis_title = "MASA",
            font=dict(size=18),
            showlegend = True,
            legend_title = "",
            plot_bgcolor='rgba(0,0,0,0)'
        )
    }



@app.callback(Output('Bar_masas', 'figure'),
              [Input('selector_fecha', 'start_date'), Input('selector_fecha', 'end_date'), Input('selector', 'value')])
def actualizar_graph_masas(start_date, end_date, selector):
    df_filtered = df[(df['nombre'] == selector) & (df['fecha'] >= start_date) & (df['fecha'] <= end_date)]
    
     # Convertir la columna de peso en una lista para usar como eje y

    return{
        'data': [go.Bar(x=df_filtered['adiposo'],
                y=df_filtered['fecha'],
                name='Adiposa',
                marker_color='#abd0ed',
                orientation='h',),
                go.Bar(x=df_filtered['muscularr'],
                y=df_filtered['fecha'],
                name='Muscular',
                marker_color='#68aee3',
                orientation='h',
                ),
                go.Bar(x=df_filtered['osea'],
                y=df_filtered['fecha'],
                name='Osea',
                marker_color='#337db5',
                orientation='h',
                ),
                go.Bar(x=df_filtered['residual'],
                y=df_filtered['fecha'],
                name='residual',
                marker_color='#022138',
                orientation='h',
                )],

        'layout': go.Layout(
    title = f"Evolución de la distribución de masas",
    xaxis_title = "",
    yaxis_title = "",
    font=dict(size=18),
    showlegend = True,
    legend_title = "",
    plot_bgcolor='rgba(0,0,0,0)',
    barmode='group'
)
    }





@app.callback(Output('Bar_imo', 'figure'),
              [Input('selector_fecha', 'start_date'), Input('selector_fecha', 'end_date'), Input('selector', 'value')])
def actualizar_graph_masass(start_date, end_date, selector):
    df_filtered = df[(df['nombre'] == selector) & (df['fecha'] >= start_date) & (df['fecha'] <= end_date)]

    return{
        'data': [go.Bar(x=df_filtered['fecha'],
                y=df_filtered['imo'],
                name='IMO',
                marker_color='#c4a90e'
                )
                
                ],
        'layout': go.Layout(
            title = f"EVOLUCIÓN IMO",
            xaxis_title = "",
            yaxis_title = "",
            font=dict(size=18),
            showlegend = True,
            legend_title = "",
            plot_bgcolor='rgba(0,0,0,0)'
        )
    }







@app.callback(Output('Bar_6p', 'figure'),
              [Input('selector_fecha', 'start_date'), Input('selector_fecha', 'end_date'), Input('selector', 'value')])
def actualizar_graph_pliegues(start_date, end_date, selector):
    df_filtered = df[(df['nombre'] == selector) & (df['fecha'] >= start_date) & (df['fecha'] <= end_date)]
    
     # Convertir la columna de peso en una lista para usar como eje y

    return{
        'data': [go.Bar(x=df_filtered['fecha'],
                y=df_filtered['pliegues'],
                name='PROMEDIO PLIEGUES',
                marker_color='#20c40e'
                )
                
                ],
        'layout': go.Layout(
            title = f"EVOLUCIÓN 6 PLIEGUES",
            xaxis_title = "",
            yaxis_title = "",
            font=dict(size=18),
            showlegend = True,
            legend_title = "",
            plot_bgcolor='rgba(0,0,0,0)'
        )
    }





@app.callback(Output('scatter_punet2', 'figure'),
              [Input('selector_fecha', 'start_date'), Input('selector_fecha', 'end_date'), Input('selector', 'value')])
def actualizar_graph_pliegues2(start_date, end_date, selector):
    df_filtered = df[(df['nombre'] == selector) & (df['fecha'] >= start_date) & (df['fecha'] <= end_date)]
    
    df_filtered['Masa Adiposa (%):'] *= 100
    df_filtered['Masa Muscular (%):'] *= 100

    fig = px.scatter(df_filtered, x="Masa Adiposa (%):", y="Masa Muscular (%):")

    fig.add_shape(type='line', line=dict(dash='dash', color='gray'), x0=12.5, y0=50, x1=21.6, y1=50)
    fig.add_shape(type='line', line=dict(dash='dash', color='gray'), x0=17.05, y0=45, x1=17.05, y1=55.1)

# Agregar texto en los ejes x e y
    fig.update_layout(
    xaxis_title="",
    yaxis_title=""
)

# Agregar texto "1" en las coordenadas (53, 14)
    fig.add_annotation(x=15, y=52.5, text="OPTIMO", showarrow=False, font=dict(size=20))
    fig.add_annotation(x=19.55, y=52.5, text="SUBIR M.M", showarrow=False, font=dict(size=20))
    fig.add_annotation(x=15, y=47.5, text="SUBIR M.M. BAJAR M.G.", showarrow=False, font=dict(size=20))
    fig.add_annotation(x=19.55, y=47.5, text="BAJAR M.G.", showarrow=False, font=dict(size=20))


# MA BIEN MM BIEN
    fig.add_shape(
    type='rect',
    x0=12.5,
    y0=50,
    x1=17.05,
    y1=55.1,
    fillcolor='rgba(0, 128, 0, 0.2)',
    line=dict(color='rgba(0, 128, 0, 0.2)')
)
# MA MAL MM BIEN
    fig.add_shape(
    type='rect',
    x0=17.05,
    y0=50,
    x1=21.6,
    y1=55.1,
    fillcolor='rgba(255, 165, 0, 0.2)',
    line=dict(color='rgba(255, 165, 0, 0.2)')
)
    fig.add_shape(
    type='rect',
    x0=17.05,
    y0=50,
    x1=21.6,
    y1=45,
    fillcolor='rgba(255, 165, 0, 0.2)',
    line=dict(color='rgba(255, 165, 0, 0.2)')
)


    fig.add_shape(
    type='rect',
    x0=12.5,
    y0=50,
    x1=17.05,
    y1=45,
    fillcolor='rgba(255, 0, 0, 0.2)',
    line=dict(color='rgba(255, 0, 0, 0.2)')
)




    fig.update_layout(plot_bgcolor='white')
    fig.update_layout(
        title={
            'text': f'CUADRANTE PUNNETT',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')

    return fig



#DASH 2



@app.callback(Output('estanadar_general', 'figure'),
              [Input('selector2', 'value'), Input('selector_fecha2', 'start_date'), Input('selector_fecha2', 'end_date')])
def update_estandar_general(selector_value, start_date, end_date):

    df_filtered = df[(df['nombre'] == selector_value) & (df['fecha'].between(start_date, end_date))]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_filtered['fecha'],
                    y=df_filtered['adiposa'],
                    name='MASA ADIPOSA',
                    marker_color='#ca0dd4'
                    ))
    fig.add_trace(go.Bar(x=df_filtered['fecha'],
                    y=df_filtered['muscularr'],
                    name='MASA MUSCULAR',
                    marker_color='#d40d59'
                    ))
    fig.add_trace(go.Bar(x=df_filtered['fecha'],
                    y=df_filtered['peso'],
                    name='PESO',
                    marker_color='#d40d1a'
                    ))


    fig.update_layout(
        title={
            'text': f'ESTANDARIZACIÓN GENERAL',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')
    
    return fig






@app.callback(Output('semaforo', 'figure'),
              [Input('selector2', 'value'), Input('selector_fecha2', 'start_date'), Input('selector_fecha2', 'end_date')])
def update_semaforo(selector_value, start_date, end_date):
    # filtrar el DataFrame según los valores de entrada
    df_filtered = df[(df['nombre'] == selector_value) & (df['fecha'].between(start_date, end_date))]
    
    # mapear los valores de la columna "pliegues" a colores y categorías
    def map_color_and_category(value):
        if value >= 25 and value <= 34.9:
            return {'color': '#27AE60', 'category': 'Alto Rendimiento'}
        elif value >= 35 and value <= 39.9:
            return {'color': '#E79F3B', 'category': 'Deportista'}
        elif value < 25:
            return {'color': '#2BBCF7', 'category': 'Elite'}
        elif value >= 40 and value <= 50:
            return {'color': '#FFC300', 'category': 'Promedio'}
        else:
            return {'color': '#F9603B', 'category': 'Población General'}

    colors_and_categories = df_filtered['pliegues'].apply(map_color_and_category)

    # crear el gráfico de barras
    fig = go.Figure(
        go.Bar(
            x=df_filtered['fecha'],
            y=df_filtered['pliegues'],
            marker_color=[c['color'] for c in colors_and_categories],
            text=[c['category'] for c in colors_and_categories],
            textposition='auto'
        )
    )

    fig.update_layout(
        title={
            'text': f'SEMAFORO 6 PLIEGUES',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')
    return fig





@app.callback(Output('semaforo_adiposa', 'figure'),
              [Input('selector2', 'value'), Input('selector_fecha2', 'start_date'), Input('selector_fecha2', 'end_date')])
def update_punnett2(selector_value, start_date, end_date):
    # Filtrar el DataFrame según los valores de entrada
    df_filtered = df[(df['nombre'] == selector_value) & (df['fecha'].between(start_date, end_date))]
    df_filtered['Masa Adiposa (%):'] *= 100

        # mapear los valores de la columna "pliegues" a colores y categorías
    def map_color_and_category(value):
        if value >= 20:
            return {'color': '#F9603B', 'category': 'Alta'}
        elif value >= 17.5 and value < 20:
            return {'color': '#FFC300', 'category': 'Aceptable'}
        elif value >= 15 and value < 17.5:
            return {'color': '#E79F3B', 'category': 'Óptimo'}
        elif value < 15:
            return {'color': '#2BBCF7', 'category': 'Elite'}

    colors_and_categories = df_filtered['Masa Adiposa (%):'].apply(map_color_and_category)

    # crear el gráfico de barras
    fig = go.Figure(
        go.Bar(
            x=df_filtered['fecha'],
            y=df_filtered['Masa Adiposa (%):'],
            marker_color=[c['color'] for c in colors_and_categories],
            text=[c['category'] for c in colors_and_categories],
            textposition='auto'
        )
    )
    fig.update_layout(
        title={
            'text': f'SEMAFORO MASA GRASA',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')
    
    
    return fig



@app.callback(Output('semaforo_muscular', 'figure'),
              [Input('selector2', 'value'), Input('selector_fecha2', 'start_date'), Input('selector_fecha2', 'end_date')])
def update_semaforo_muscular(selector_value, start_date, end_date):
    # Filtrar el DataFrame según los valores de entrada
    df_filtered = df[(df['nombre'] == selector_value) & (df['fecha'].between(start_date, end_date))]
    df_filtered['Masa Muscular (%):'] *= 100

    def map_color_and_category(value):
        if value > 52.5:
            return {'color': '#2BBCF7', 'category': 'Elite'}
        elif value >= 50 and value <= 52.5:
            return {'color': '#F9603B', 'category': 'Alto Rendimiento'}
        elif value >= 48.5 and value < 50:
            return {'color': '#FFC300', 'category': 'Medio'}
        elif value < 48.5:
            return {'color': '#E79F3B', 'category': 'Baja'}

    colors_and_categories = df_filtered['Masa Muscular (%):'].apply(map_color_and_category)

    # Crear el gráfico de barras
    fig = go.Figure(
        go.Bar(
            x=df_filtered['fecha'],
            y=df_filtered['Masa Muscular (%):'],
            marker_color=[c['color'] for c in colors_and_categories],
            text=[c['category'] for c in colors_and_categories],
            textposition='auto'
        )
    )
    fig.update_layout(
        title={
            'text': 'SEMÁFORO MASA MUSCULAR',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')

    return fig






@app.callback(Output('punnett', 'figure'),
              [Input('selector2', 'value'), Input('selector_fecha2', 'start_date'), Input('selector_fecha2', 'end_date')])
def update_punnett(selector_value, start_date, end_date):

    df_filtered = df[(df['nombre'] == selector_value) & (df['fecha'].between(start_date, end_date))]
    df_filtered['Masa Adiposa (%):'] *= 100
    df_filtered['Masa Muscular (%):'] *= 100

    fig = px.scatter(df_filtered, x="Masa Adiposa (%):", y="Masa Muscular (%):")

    fig.add_shape(type='line', line=dict(dash='dash', color='gray'), x0=12.5, y0=50, x1=21.6, y1=50)
    fig.add_shape(type='line', line=dict(dash='dash', color='gray'), x0=17.05, y0=45, x1=17.05, y1=55.1)

# Agregar texto en los ejes x e y
    fig.update_layout(
    xaxis_title="Masa Adiposa (%)",
    yaxis_title="Masa Muscular (%)"
)

# Agregar texto "1" en las coordenadas (53, 14)
    fig.add_annotation(x=15, y=52.5, text="OPTIMO", showarrow=False, font=dict(size=20))
    fig.add_annotation(x=19.55, y=52.5, text="SUBIR M.M", showarrow=False, font=dict(size=20))
    fig.add_annotation(x=15, y=47.5, text="SUBIR M.M. BAJAR M.G.", showarrow=False, font=dict(size=20))
    fig.add_annotation(x=19.55, y=47.5, text="BAJAR M.G.", showarrow=False, font=dict(size=20))


# MA BIEN MM BIEN
    fig.add_shape(
    type='rect',
    x0=12.5,
    y0=50,
    x1=17.05,
    y1=55.1,
    fillcolor='rgba(0, 128, 0, 0.2)',
    line=dict(color='rgba(0, 128, 0, 0.2)')
)
# MA MAL MM BIEN
    fig.add_shape(
    type='rect',
    x0=17.05,
    y0=50,
    x1=21.6,
    y1=55.1,
    fillcolor='rgba(255, 165, 0, 0.2)',
    line=dict(color='rgba(255, 165, 0, 0.2)')
)
    fig.add_shape(
    type='rect',
    x0=17.05,
    y0=50,
    x1=21.6,
    y1=45,
    fillcolor='rgba(255, 165, 0, 0.2)',
    line=dict(color='rgba(255, 165, 0, 0.2)')
)


    fig.add_shape(
    type='rect',
    x0=12.5,
    y0=50,
    x1=17.05,
    y1=45,
    fillcolor='rgba(255, 0, 0, 0.2)',
    line=dict(color='rgba(255, 0, 0, 0.2)')
)




    fig.update_layout(plot_bgcolor='white')
    fig.update_layout(
        title={
            'text': f'CUADRANTE PUNNETT',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')

    return fig



#DASH 3



@app.callback(Output('6pliegues_posición', 'figure'),
              [Input('selector_fecha3', 'start_date'), Input('selector_fecha3', 'end_date'), Input('selector_posicion', 'value')])
def actualizar_6pliegues_posición(start_date, end_date, posicion):
    df_filtered = df[(df['fecha'] >= start_date) & (df['fecha'] <= end_date) & (df['posición'] == posicion)]
    
    # Calcular el promedio de 'pliegues' por jugador
    df_avg = df_filtered.groupby('nombre')['pliegues'].mean().reset_index()
    
    # Mapear los valores de la columna "pliegues" a colores y categorías
    def map_color_and_category(value):
        if 25 <= value <= 34.9:
            return {'color': '#27AE60', 'category': 'Alto Rendimiento'}
        elif 35 <= value <= 39.9:
            return {'color': '#E79F3B', 'category': 'Deportista'}
        elif value < 25:
            return {'color': '#2BBCF7', 'category': 'Elite'}
        elif 40 <= value <= 50:
            return {'color': '#FFC300', 'category': 'Promedio'}
        else:
            return {'color': '#F9603B', 'category': 'Población General'}

    fig = go.Figure(data=go.Bar(
        x=df_avg['pliegues'],  # Utilizar los promedios calculados
        y=df_avg['nombre'],  # Utilizar los nombres de los jugadores
        orientation='h',
        marker=dict(
            color=[map_color_and_category(value)['color'] for value in df_avg['pliegues']]  # Utilizar los promedios calculados
        )
    ))
    #ALTO RENDIMIENTO
    fig.add_shape(
        type='line',
        x0=25,
        y0=0,
        x1=25,
        y1=len(df_avg),
        line=dict(dash='dash', color='#27AE60', width=1)
    )
    #DEPORTISTA
    fig.add_shape(
        type='line',
        x0=35,
        y0=0,
        x1=35,
        y1=len(df_avg),
        line=dict(dash='dash', color='#E79F3B', width=1)
    )
    #PROMEDIO
    fig.add_shape(
        type='line',
        x0=40,
        y0=0,
        x1=40,
        y1=len(df_avg),
        line=dict(dash='dash', color='#FFC300', width=1)
    )
    #NO APTO
    fig.add_shape(
        type='line',
        x0=50,
        y0=0,
        x1=50,
        y1=len(df_avg),
        line=dict(dash='dash', color='#F9603B', width=1)
    )


    y_shift = 0.2


    fig.add_annotation(
        x=25,
        y=len(df_avg),
        yshift=y_shift,
        text='ELITE',
        showarrow=False,
        font=dict(color='#27AE60')
    )

    fig.add_annotation(
        x=35,
        y=len(df_avg),
        yshift=y_shift,
        text='ALTO RENDIMIENTO',
        showarrow=False,
        font=dict(color='#E79F3B')
    )


    fig.add_annotation(
        x=40,
        y=len(df_avg),
        yshift=y_shift,
        text='APTO',
        showarrow=False,
        font=dict(color='#FFC300')
    )



    fig.add_annotation(
        x=50,
        y=len(df_avg),
        yshift=y_shift,
        text='NO APTO',
        showarrow=False,
        font=dict(color='#F9603B')
    )
    


    fig.update_layout(
        title={
            'text': f'6 PLIEGUES {posicion}',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')
    return fig




@app.callback(Output('imo_posición', 'figure'),
              [Input('selector_fecha3', 'start_date'), Input('selector_fecha3', 'end_date'), Input('selector_posicion', 'value')])
def actualizar_imo_posición(start_date, end_date, posicion):
    df_filtered = df[(df['fecha'] >= start_date) & (df['fecha'] <= end_date) & (df['posición'] == posicion)]
    
    # Calcular el promedio de 'pliegues' por jugador
    df_avg = df_filtered.groupby('nombre')['imo'].mean().round(2).reset_index()

    # Mapear los valores de la columna "pliegues" a colores y categorías
    def map_color_and_category(value):
        if value > 4:
            return {'color': '#27AE60', 'category': 'VERDE'}
        elif 3.9 <= value < 4:
            return {'color': '#E79F3B', 'category': 'AMARILLA'}
        elif 3.7 <= value < 3.9:
            return {'color': '#FCA311', 'category': 'NARANJA'}
        else:
            return {'color': '#FF0000', 'category': 'ROJA'}

    fig = go.Figure(data=go.Bar(
        x=df_avg['imo'],  # Utilizar los promedios calculados
        y=df_avg['nombre'],  # Utilizar los nombres de los jugadores
        orientation='h',
        marker=dict(
            color=[map_color_and_category(value)['color'] for value in df_avg['imo'].round(2)]  # Utilizar los promedios calculados
        )
    ))
    
    elite_color = map_color_and_category(0)['color']
    deportista_color = '#F9603B'
    
    if posicion == 'ARQUERO':
        line_position = 4.3
    elif posicion == 'DEFENSOR CENTRAL':
        line_position = 4.4
    elif posicion == 'DEFENSOR LATERAL':
        line_position = 4.2
    elif posicion == 'VOLANTE INT. ENLACE':
        line_position = 4.3
    elif posicion == 'CENTRO DELANTERO':
        line_position = 4.2
    elif posicion == 'DELANTERO':
        line_position = 4.1
    elif posicion == 'VOLANTE LATERAL':
        line_position = 4.2
    else:
        line_position = 4.1
    
    fig.add_shape(
        type='line',
        x0=line_position,
        y0=0,
        x1=line_position,
        y1=len(df_avg),
        line=dict(dash='dash', color='#000000', width=1)
    )
    
    y_shift = 0.2
    
    fig.add_annotation(
        x=line_position,
        y=len(df_avg),
        yshift=y_shift,
        text='IMO ESPECIFICO',
        showarrow=False,
        font=dict(color='#000000')
    )    
    
    fig.update_layout(
        title={
            'text': f'IMO PROMEDIO {posicion}',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')

    return fig





@app.callback(Output('promedio_talla', 'figure'),
              [Input('selector_fecha3', 'start_date'), Input('selector_fecha3', 'end_date')])
def actualizar_promedio_talla(start_date, end_date):
    df_filtered = df[(df['fecha'] >= start_date) & (df['fecha'] <= end_date)]

    df_avg = df_filtered.groupby('nombre')['Talla'].mean().reset_index()

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df_avg['Talla'].mean(),
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [165, 196]},
               'bar': {'color': "green"},
               'steps': [
                   {'range': [165, 180], 'color': "lightgray"},
                   {'range': [180, 196], 'color': "lightgray"}]
               }
    ))
    fig.update_layout(
        title={
            'text': 'PROMEDIO TALLA PLANTEL',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')

    return fig





@app.callback(Output('promedio_peso', 'figure'),
              [Input('selector_fecha3', 'start_date'), Input('selector_fecha3', 'end_date')])
def actualizar_promedio_peso(start_date, end_date):
    df_filtered = df[(df['fecha'] >= start_date) & (df['fecha'] <= end_date)]

    df_avg = df_filtered.groupby('nombre')['peso'].mean().reset_index()


    fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=df_avg['peso'].mean(),
    domain={'x': [0, 1], 'y': [0, 1]},
    gauge={'axis': {'range': [65, 94]},
           'bar': {'color': "#fcec0a"},
           'steps': [
               {'range': [0, 100], 'color': "lightgray"},
               {'range': [0, 100], 'color': "lightgray"}]
           }
    ))
    fig.update_layout(
        title={
            'text': 'PROMEDIO PESO PLANTEL',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')
    
    return fig




@app.callback(Output('promedio_talla_plantel', 'figure'),
              [Input('selector_fecha3', 'start_date'), Input('selector_fecha3', 'end_date')])
def actualizar_promedio_talla_plantel(start_date, end_date):
    df_filtered = df[(df['fecha'] >= start_date) & (df['fecha'] <= end_date)]

    df_promedio = df.groupby("posición")["Talla"].mean().reset_index()

    text_values = []  # Lista para almacenar los valores de texto

    for index, row in df_promedio.iterrows():
        rounded_value = round(row["Talla"])  # Redondear el valor de la talla promedio
        int_value = int(rounded_value)  # Convertir el valor redondeado en entero
        text_values.append(int_value)

    fig = go.Figure(data=go.Bar(
        x=df_promedio["Talla"],
        y=df_promedio["posición"],
        orientation='h',
        marker=dict(color='green'),  # Establecer el color de las barras
        text=text_values,  # Agregar los valores de texto a las barras
        textposition='auto'  # Posición automática del texto
    ))
    fig.update_layout(
        title={
            'text': 'PROMEDIO TALLA POR POSICIÓN',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')

    return fig





@app.callback(Output('promedio_peso_plantel', 'figure'),
              [Input('selector_fecha3', 'start_date'), Input('selector_fecha3', 'end_date')])
def actualizar_promedio_peso_plantel(start_date, end_date):
    df_filtered = df[(df['fecha'] >= start_date) & (df['fecha'] <= end_date)]

    df_promedio = df.groupby("posición")["peso"].mean().reset_index()

    text_values = []  # Lista para almacenar los valores de texto

    for index, row in df_promedio.iterrows():
        rounded_value = round(row["peso"])  # Redondear el valor del peso promedio
        int_value = int(rounded_value)  # Convertir el valor redondeado en entero
        text_values.append(int_value)

    fig = go.Figure(data=go.Bar(
        x=df_promedio["peso"],
        y=df_promedio["posición"],
        orientation='h',
        marker=dict(color='#fcec0a'),  # Establecer el color de las barras
        text=text_values,  # Agregar los valores de texto a las barras
        textposition='auto'  # Posición automática del texto
    ))
    fig.update_layout(
        title={
            'text': 'PROMEDIO PESO POR POSICIÓN',
            'x': 0.5,
            'font': {'size': 24}
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    fig.update_layout(plot_bgcolor='white')

    return fig







#DASH 4




@app.callback(Output('grafico_torta', 'figure'),
              [Input('selector_fecha4', 'start_date'), Input('selector_fecha4', 'end_date'), Input('selector4', 'value')])
def actualizar_grafico_torta(start_date, end_date, selector):
    df_filtered = df[(df['nombre'] == selector) & (df['fecha'] >= start_date) & (df['fecha'] <= end_date)]

    # Multiplicar los valores por 100
    df_filtered['Masa Muscular (%):'] *= 100
    df_filtered['Masa Adiposa (%):'] *= 100
    df_filtered['Masa Residual (%):'] *= 100
    df_filtered['Masa Ósea Cuerpo (%):'] *= 100
    df_filtered['Masa de la Piel (%):'] *= 100

    # Obtener los valores reales para cada categoría
    masa_muscular = df_filtered['Masa Muscular (%):'].sum()
    masa_adiposa = df_filtered['Masa Adiposa (%):'].sum()
    masa_residual = df_filtered['Masa Residual (%):'].sum()
    masa_osea = df_filtered['Masa Ósea Cuerpo (%):'].sum()
    masa_piel = df_filtered['Masa de la Piel (%):'].sum()

    # Calcular el total de masa
    total_masa = masa_muscular + masa_adiposa + masa_residual + masa_osea + masa_piel

    # Calcular los porcentajes de cada categoría
    porcentaje_muscular = masa_muscular / total_masa
    porcentaje_adiposa = masa_adiposa / total_masa
    porcentaje_residual = masa_residual / total_masa
    porcentaje_osea = masa_osea / total_masa
    porcentaje_piel = masa_piel / total_masa

    # Etiquetas de las categorías
    categorias = ['Masa Muscular', 'Masa Adiposa', 'Masa Residual', 'Masa Ósea Cuerpo', 'Masa de la Piel']

    # Valores para el gráfico de torta
    valores = [porcentaje_muscular, porcentaje_adiposa, porcentaje_residual, porcentaje_osea, porcentaje_piel]

    # Colores personalizados para cada categoría
    colores = ['#fc0303', '#8c0606', '#3b0a0a', '#8c5b5b', '#f5dada']

    # Crear el objeto de gráfico de torta con colores personalizados
    fig = go.Figure(data=[go.Pie(labels=categorias, values=valores, marker=dict(colors=colores))])
    fig.update_layout(
    title={
    'text': 'DISTRIBUCIÓN DE MASAS',
    'x': 0.23,
    'font': {'size': 24}
    })
    fig.update_layout(plot_bgcolor='white')


    return fig






@app.callback(Output('punnet4', 'figure'),
              [Input('selector_fecha4', 'start_date'), Input('selector_fecha4', 'end_date'), Input('selector4', 'value')])
def actualizar_punnet4(start_date, end_date, selector):

    df_filtered = df[(df['nombre'] == selector) & (df['fecha'] >= start_date) & (df['fecha'] <= end_date)]
    df_filtered['Masa Adiposa (%):'] *= 100
    df_filtered['Masa Muscular (%):'] *= 100
    

    fig = px.scatter(df_filtered, x="Masa Adiposa (%):", y="Masa Muscular (%):")

    fig.add_shape(type='line', line=dict(dash='dash', color='gray'), x0=12.5, y0=50, x1=21.6, y1=50)
    fig.add_shape(type='line', line=dict(dash='dash', color='gray'), x0=17.05, y0=45, x1=17.05, y1=55.1)

# Agregar texto en los ejes x e y
    fig.update_layout(
    xaxis_title="",
    yaxis_title=" "
)

# Agregar texto "1" en las coordenadas (53, 14)
    fig.add_annotation(x=15, y=52.5, text="OPTIMO", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=19.55, y=52.5, text="SUBIR M.M", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=15, y=47.5, text="SUBIR M.M. BAJAR M.G.", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=19.55, y=47.5, text="BAJAR M.G.", showarrow=False, font=dict(size=12))


# MA BIEN MM BIEN
    fig.add_shape(
    type='rect',
    x0=12.5,
    y0=50,
    x1=17.05,
    y1=55.1,
    fillcolor='rgba(0, 128, 0, 0.2)',
    line=dict(color='rgba(0, 128, 0, 0.2)')
)
# MA MAL MM BIEN
    fig.add_shape(
    type='rect',
    x0=17.05,
    y0=50,
    x1=21.6,
    y1=55.1,
    fillcolor='rgba(255, 165, 0, 0.2)',
    line=dict(color='rgba(255, 165, 0, 0.2)')
)
    fig.add_shape(
    type='rect',
    x0=17.05,
    y0=50,
    x1=21.6,
    y1=45,
    fillcolor='rgba(255, 165, 0, 0.2)',
    line=dict(color='rgba(255, 165, 0, 0.2)')
)


    fig.add_shape(
    type='rect',
    x0=12.5,
    y0=50,
    x1=17.05,
    y1=45,
    fillcolor='rgba(255, 0, 0, 0.2)',
    line=dict(color='rgba(255, 0, 0, 0.2)')
)

    fig.update_layout(plot_bgcolor='white')

    return fig







if __name__ == '__main__':
    app.run_server(debug=True)