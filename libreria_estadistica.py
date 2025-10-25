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

print(carreras.summary())
print(generos.summary())
print("La carrera con mas alumnos es",generos.moda())
print("El genero dominante es el",carreras.moda())
