# %%
import yfinance as yf 
import pandas as pd
import matplotlib.pyplot as plt

# Excepción personalizada
class OpcionInvalidaException(Exception):
    def __init__(self, mensaje="Opción no válida. Por favor, pulse 1 para índices, 2 para bonos, 3 para materias primas."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

# Clase genérica para manejar activos financieros
class ActivoFinanciero:
    def __init__(self, nombre, simbolo):
        self.nombre = nombre
        self.simbolo = simbolo
        self._data = pd.DataFrame()  # DataFrame para almacenar los datos históricos

    def cargar_datos(self, start='2015-01-01', end='2024-01-01'):
        self._data = yf.download(self.simbolo, start=start, end=end)
        if self._data.empty:
            print(f"No se encontraron datos para {self.nombre} ({self.simbolo}).")
        else:
            print(f"Datos cargados para {self.nombre} ({self.simbolo}).")

    def graficar(self, ax, color='blue'):
        if self._data.empty:
            print(f"No hay datos para graficar de {self.nombre}.")
            return
        ax.plot(self._data.index, self._data['Close'], label=f'{self.nombre}', color=color)

# Clase visualizador financiero
class VisualizadorFinanciero:
    def __init__(self):
        self.indices = []  # Lista de instancias de ActivoFinanciero para índices
        self.bonos = []    # Lista de instancias de ActivoFinanciero para bonos
        self.materias_primas = []  # Lista de instancias de ActivoFinanciero para materias primas

    def agregar_activos(self, lista_activos, tipo_activo):
        for activo in lista_activos:
            nombre, simbolo = activo
            nuevo_activo = ActivoFinanciero(nombre, simbolo)
            if tipo_activo == 'indice':
                self.indices.append(nuevo_activo)
            elif tipo_activo == 'bono':
                self.bonos.append(nuevo_activo)
            elif tipo_activo == 'materia_prima':
                self.materias_primas.append(nuevo_activo)
            print(f"{nombre} ({simbolo}) ha sido agregado como {tipo_activo}.")

    def cargar_datos(self, lista_activos, start='2015-01-01', end='2024-01-01'):
        for activo in lista_activos:
            activo.cargar_datos(start=start, end=end)

    def graficar_multiples_ejes(self, lista_activos, **kwargs):
        if not lista_activos:
            print("No hay activos para graficar.")
            return
        
        fig, ax1 = plt.subplots(figsize=(10, 6))

        colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'cyan', 'magenta', 'yellow']
        num_ejes = min(len(lista_activos), len(colors))

        # Graficar el primer activo
        lista_activos[0].graficar(ax1, color=colors[0])
        ax1.tick_params(axis='y', labelcolor=colors[0])
        ax1.set_yticks([])  # Eliminar etiquetas del eje Y del primer eje

        ax_extra = []
        handles_labels = [ax1.get_legend_handles_labels()]  # Guardar leyenda del primer eje

        for i in range(1, num_ejes):
            ax = ax1.twinx()  # Crear nuevo eje Y
            ax.spines['right'].set_position(('outward', 0))  # Coloca los ejes adicionales en la misma posición
            lista_activos[i].graficar(ax, color=colors[i])
            ax.tick_params(axis='y', labelcolor=colors[i])
            ax.spines['right'].set_visible(False)  # Elimina los ejes verticales adicionales (spines)
            ax.set_yticks([])  # Elimina las etiquetas del eje Y
            handles_labels.append(ax.get_legend_handles_labels())  # Guardar leyendas de cada eje
            ax_extra.append(ax)

        # Combinar las leyendas de todos los ejes
        handles, labels = zip(*handles_labels)
        handles = sum(handles, [])  # Combinar los handles
        labels = sum(labels, [])  # Combinar las etiquetas

        # Añadir la leyenda para todos los activos
        ax1.legend(handles, labels, loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

        fig.tight_layout()
        fig.suptitle(kwargs.get('titulo', 'Comparación de Activos con Múltiples Ejes Y'))
        plt.show()

# Clase para manejar la lógica del menú y la excepción
class Menu:
    def __init__(self, visualizador):
        self.visualizador = visualizador

    def mostrar_menu(self):
        try:
            opcion = input("Seleccione una opción: 1 para índices, 2 para bonos, 3 para graficar materias primas: ")
            if opcion == '1':
                self.mostrar_indices()
            elif opcion == '2':
                self.mostrar_bonos()
            elif opcion == '3':
                self.mostrar_materias_primas()
            else:
                raise OpcionInvalidaException()  # Lanza la excepción si la opción es inválida
        except OpcionInvalidaException as e:
            print(e)

    def mostrar_indices(self):
        self.visualizador.cargar_datos(self.visualizador.indices, start='2000-01-01')
        self.visualizador.graficar_multiples_ejes(
            self.visualizador.indices,
            titulo='Comparación de Índices Globales con Múltiples Ejes Y'
        )

    def mostrar_bonos(self):
        self.visualizador.cargar_datos(self.visualizador.bonos, start='2000-01-01')
        self.visualizador.graficar_multiples_ejes(
            self.visualizador.bonos,
            titulo='Comparación de Bonos con Múltiples Ejes Y'
        )

    def mostrar_materias_primas(self):
        self.visualizador.cargar_datos(self.visualizador.materias_primas, start='2000-01-01')
        self.visualizador.graficar_multiples_ejes(
            self.visualizador.materias_primas,
            titulo='Comparación de Materias Primas con Múltiples Ejes Y'
        )

# Crear una instancia del visualizador financiero
visualizador = VisualizadorFinanciero()

# Agregar índices, bonos y materias primas
visualizador.agregar_activos([
    ('S&P 500', '^GSPC'),
    ('Nasdaq 100', '^NDX'),
    ('Dow Jones', '^DJI'),
    ('Russell', '^RUT'),
    ('FTSE 100', '^FTSE'),
    ('Eurostoxx', '^STOXX50E'),
    ('CAC40', '^FCHI'),
    ('Hang Seng Index', '^HSI'),
    ('Nikkei 225', '^N225'),
    ('IBOVESPA', '^BVSP'),
], 'indice')

visualizador.agregar_activos([
    ('Bono del Tesoro 10 años', '^TNX'),
    ('Bono del Tesoro 30 años', '^TYX'),
    ('Bono del Tesoro 5 años', '^FVX'),
    ('2-Year Yield Futures', '2YY=F'),
    ('10-Year T-Note Futures', 'ZN=F'),
], 'bono')

visualizador.agregar_activos([
    ('Oro', 'GC=F'),
    ('Petróleo Crudo', 'CL=F'),
    ('Plata', 'SI=F'),
    ('Platinum', 'PL=F'),
    ('Copper', 'HG=F'),
    ('Nat Gas', 'NG=F'),
    ('Brent', 'BZ=F'),
    ('Corn', 'ZC=F'),
    ('Soy Bean', 'ZL=F'),
], 'materia_prima')

# Crear una instancia del menú
menu = Menu(visualizador)

# Mostrar el menú al usuario
menu.mostrar_menu()

# %%
