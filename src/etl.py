import pandas as pd


def cargar_datos(ruta):
    """Carga todas las hojas del Excel."""
    return pd.read_excel(ruta, sheet_name=None)


def analizar_datos(hojas):
    """Analiza la estructura y calidad de los datos."""
    for nombre, df in hojas.items():
        print(f"\nHOJA: {nombre}")
        print(f"Filas: {len(df)}")
        print(f"Columnas: {len(df.columns)}")

        print("\nTipos de datos:")
        print(df.dtypes.to_string())

        print("\nValores nulos:")
        print(df.isnull().sum().to_string())

        print("\nDuplicados:")
        print(df.duplicated().sum())


if __name__ == "__main__":
    hojas = cargar_datos("data/reporte_quito.xlsx")
    analizar_datos(hojas)
