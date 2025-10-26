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
        s = 0.0
        for x in self._num:
            s += x
        return float(s / n)

    def mediana(self):
        n = self.cantidad()
        if n == 0:
            return None
        s = sorted(self._num)
        mid = n // 2
        if n % 2 == 1:
            return float(s[mid])
        else:
            return float((s[mid - 1] + s[mid]) / 2)

    def moda(self):
        if not self._num:
            return []
        freq = {}
        for x in self._num:
            freq[x] = freq.get(x, 0) + 1
        max_f = max(freq.values())
        modos = [k for k, v in freq.items() if v == max_f]
        return modos

    def rango(self):
        if self.contar() == 0:
            return None
        return float(self._s.max() - self._s.min())


    def _percentil(self, p):
        n = self.cantidad()
        if n == 0:
            return None
        s = sorted(self._num)
        if p <= 0:
            return float(s[0])
        if p >= 100:
            return float(s[-1])
        # posición real
        k = (p / 100.0) * (n - 1)
        f = int(math.floor(k))
        c = int(math.ceil(k))
        if f == c:
            return float(s[int(k)])
        df = k - f
        return float(s[f] * (1 - df) + s[c] * df)

    def rango_intercuartilico(self):
        q1 = self._percentil(25)
        q3 = self._percentil(75)
        if q1 is None or q3 is None:
            return None
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
            "cantidad": self.cantidad(),
            "media": self.media(),
            "mediana": self.mediana(),
            "moda": self.moda(),
            "rango": self.rango(),
            "IQR": self.rango_intercuartilico(),
            "varianza": self.varianza(),
            "desviacion_estandar": self.desviacion_estandar()
        }
        return pd.DataFrame(resumen)

carreras = EstadisticasCat("Sexo", df["Sexo"].tolist())
generos = EstadisticasCat("Carrera", df["Carrera"].tolist())

print(carreras.summary())
print(generos.summary())
print("La carrera con mas alumnos es",generos.moda())
print("El genero dominante es el",carreras.moda())




