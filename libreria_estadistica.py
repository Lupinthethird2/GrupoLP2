#Carga y lectura de los datos en excel
import pandas as pd
df = pd.read_excel("data_unalm_estudiantes_var.xlsx")

# libreria_estadistica.py
# Clase de Basee 
class Datos:
    def __init__(self, lista):
        self.lista = lista
    def cantidad(self):
        return len(self.lista)
    def mostrar(self):
        return self.lista
    def ordenar(self):

        return sorted(self.lista)


# Tabla estadistica para variables cualitativas
class EstadisticasCat(Datos):
    def __init__(self, name, data):
        super().__init__(data)
        self.name = name
        self._cat = [str(x) for x in self.lista if pd.notna(x)]

    def frecuencia(self):
        freq = {}
        for valor in self._cat:
            freq[valor] = freq.get(valor, 0) + 1
        return freq

    def porcentaje(self):
        total = len(self._cat)
        freq = self.frecuencia()
        return {k: (v / total) * 100 for k, v in freq.items()}

    def moda(self):
        freq = self.frecuencia()
        max_f = max(freq.values())
        return [k for k, v in freq.items() if v == max_f]

    def summary(self):
        freq = self.frecuencia()
        perc = self.porcentaje()
        resumen = []
        for categoria in freq:
            resumen.append({
                "variable": self.name,
                "categoria": categoria,
                "frecuencia": freq[categoria],
                "porcentaje": round(perc[categoria], 2)
            })
        return pd.DataFrame(resumen)

carreras = EstadisticasCat("Sexo", df["Sexo"].tolist())
generos = EstadisticasCat("Carrera", df["Carrera"].tolist())

# Graficos de barras
import seaborn as sns
import matplotlib.pyplot as plt

tabla_genero = generos.summary()

ax = sns.barplot(data=tabla_genero, x="categoria", y="porcentaje", palette="pastel")

plt.title("Porcentaje de estudiantes por sexo")
plt.xlabel("Sexo")
plt.ylabel("Porcentaje")

for index, row in tabla_genero.iterrows():
    ax.text(index, row.porcentaje + 1, f'{row.porcentaje:.1f}%', color='black', ha="center") 
    
plt.show()

tabla_carrera = carreras.summary()
ac = sns.barplot(data=tabla_carrera, x="categoria", y="porcentaje", palette="pastel")
plt.title("Porcentaje de estudiantes por Carreras")
plt.xlabel("Carreras")
plt.ylabel("Porcentaje")
for index, row in tabla_carrera.iterrows():
    ac.text(index, row.porcentaje + 1, f'{row.porcentaje:.1f}%', color='black', ha="center") 
plt.ylim(0, 18)
plt.xticks(rotation=45, ha="right",fontsize=7)   # etiquetas diagonales
plt.tight_layout()
plt.show()

# Tabla estadística para variables cuantitativas
class EstadisticasNum(Datos):
    def __init__(self, name, data):
        super().__init__(data)
        self.name = name
        serie = pd.to_numeric(pd.Series(self.lista), errors='coerce').dropna().astype(float)
        self._s = serie
        self._num = serie.tolist()

    def cantidad(self):
        return len(self._s)

    def media(self):
        n = self.cantidad()
        if n == 0:
            return None
        suma = 0
        for valor in self._num:
            suma += valor
        return float(suma / n)

    def mediana(self):
        n = self.cantidad()
        if n == 0:
            return None
        datos_ordenados = sorted(self._num)
        mitad = n // 2
        if n % 2 == 0:
            mediana = (datos_ordenados[mitad - 1] + datos_ordenados[mitad]) / 2
        else:
            mediana = datos_ordenados[mitad]
        return float(mediana)

    def moda(self):
        if not self._num:
            return []
        frecuencias = {}
        for valor in self._num:
            if valor in frecuencias:
                frecuencias[valor] += 1
            else:
                frecuencias[valor] = 1
        max_frec = max(frecuencias.values())
        modas = [valor for valor, freq in frecuencias.items() if freq == max_frec]
        return modas

    def rango(self):
        if self.cantidad() == 0:
            return None
        return float(self._s.max() - self._s.min())


    def _percentil(self, p):
        n = self.cantidad()
        if n == 0:
            return None
<<<<<<< Updated upstream
        s = sorted(self._num)
        if p <= 0:
            return float(s[0])
        if p >= 100:
            return float(s[-1])
        k = (p / 100.0) * (n - 1)
        f = int(k)
        c = f if k == f else f + 1
        if f == c:
            return float(s[int(k)])
        df = k - f
        return float(s[f] * (1 - df) + s[c] * df)

    def rango_intercuartilico(self):
        q1 = self._percentil(25)
        q3 = self._percentil(75)
        if q1 is None or q3 is None:
            return None
=======
>>>>>>> Stashed changes
        q1 = float(self._s.quantile(0.25))
        q3 = float(self._s.quantile(0.75))
        return float(q3 - q1)

    def varianza(self):
        n = self.cantidad()
        if n <= 1:
            return None

        media_valor = self.media()
        suma_cuadrados = 0

        for valor in self._num:
            diferencia = valor - media_valor
            suma_cuadrados += diferencia ** 2

        varianza_muestral = suma_cuadrados / (n - 1)
        return float(varianza_muestral)

    def desviacion_estandar(self):
        varianza_muestral = self.varianza()
        if varianza_muestral is None:
            return None

        desviacion = varianza_muestral ** 0.5
        return float(desviacion)

    def summary(self):
        resumen = {
            "variable": self.name,
            "cantidad": self.cantidad(),
            "media": self.media(),
            "mediana": self.mediana(),
            "moda": self.moda(),
            "rango": self.rango(),
            "IQR": self.rango_intercuartilico(),
            "varianza": self.varianza(),
            "stdev": self.desviacion_estandar()
        }
        return pd.DataFrame(resumen)


import pandas as pd
df_postulantes = pd.read_excel("Postulantes.xlsx", skiprows=2)
print(df_postulantes.head())

<<<<<<< Updated upstream
=======
from libreria_estadistica import EstadisticasCat, EstadisticasNum
>>>>>>> Stashed changes
datos_sexo = df_postulantes["SEXO"].tolist()
analizador_sexo = EstadisticasCat("SEXO", datos_sexo)
print(analizador_sexo.summary())

datos_puntaje = df_postulantes["PUNTAJE FINAL"].tolist()
analizador_puntaje = EstadisticasNum("PUNTAJE FINAL", datos_puntaje)
print(analizador_puntaje.summary())

# Prueba de Matematicas (estadisticas totales)
da_mat = df_postulantes["PUNTAJE MATEMÁTICAS"].tolist()
a_puntaje = EstadisticasNum("PUNTAJE MATEMÁTICAS", da_mat)
print(a_puntaje.summary())

# Histograma
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

plt.figure(figsize=(8, 5))
plt.hist(da_mat, bins=20, color='green', edgecolor='black')
plt.title("Histograma - Puntaje de Matemáticas")
plt.xlabel("Puntaje de Matemáticas")
plt.ylabel("Frecuencia")
plt.grid(axis='y', alpha=0.75)
ax = plt.gca()  
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()

'''
<<<<<<< Updated upstream

carreras = EstadisticasCat("Sexo", df["Sexo"].tolist())
generos = EstadisticasCat("Carrera", df["Carrera"].tolist())
>>>>>>> Stashed changes

print(carreras.summary())
print(generos.summary())
print("La carrera con mas alumnos es",generos.moda())
print("El genero dominante es el",carreras.moda())
'''
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes

print("Libreria de estadistica cargada correctamente")



