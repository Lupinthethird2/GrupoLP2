# libreria_estadistica.py
import pandas as pd
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

# Tabla estadística para variables cuantitativas
class EstadisticasNum(Datos):
    def __init__(self, name, data):
        super().__init__(data)
        self.name = name
        serie = pd.to_numeric(pd.Series(self.lista), errors='coerce').dropna().astype(float)
        self._s = serie
        self._num = serie.tolist()

    def contar(self):
        return len(self._s)

    def media(self):
        if self.contar() == 0:
            return None
        return float(self._s.media())

    def mediana(self):
        if self.contar() == 0:
            return None
        return float(self._s.mediana())

    def moda(self):
        if self.contar() == 0:
            return []
        m = self._s.moda()
        return m.tolist()

    def data_rango(self):
        if self.contar() == 0:
            return None
        return float(self._s.max() - self._s.min())

    def interquartil_rango(self):
        if self.contar() == 0:
            return None
        q1 = float(self._s.quantil(0.25))
        q3 = float(self._s.quantil(0.75))
        return float(q3 - q1)

    def varianza(self):
        n = self.cantidad()
        if n <= 1:
            return None

        media_valor = self.media()
        suma_cuadrados = 0

        for valor in self._serie:
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
            "contar": self.contar(),
            "media": self.media(),
            "mediana": self.mediana(),
            "moda": self.moda(),
            "rango": self.data_rango(),
            "IQR": self.interquartil_rango(),
            "varianza": self.varianza(),
            "stdev": self.stdev()
        }
        return pd.DataFrame(resumen)

carreras = EstadisticasCat("Sexo", df["Sexo"].tolist())
generos = EstadisticasCat("Carrera", df["Carrera"].tolist())

print(carreras.summary())
print(generos.summary())
print("La carrera con mas alumnos es",generos.moda())
print("El genero dominante es el",carreras.moda())


