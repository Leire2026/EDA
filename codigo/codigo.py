import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns

ine = pd.read_csv(r"data/ine_original_2.csv", sep=",", decimal=",", encoding="latin1")
ine

ine_comp = pd.read_csv(r"data/ine_original_serie_completa.csv", sep=",", decimal=",", encoding="latin1")
ine_comp

#depuracion y limpieza base
ine.info()
ine.describe(include="all")

ine.isnull()

len(ine)*0.97

ine_dep = ine.dropna(axis= 1, thresh=len(ine)*0.97)
ine_dep

ine_dep.info()
ine_dep.isnull()
ine_dep.fillna(0, inplace=True)

#análisis bases y elaboracion gráficas

for i, valor in enumerate(ine_dep.iloc[:, 0]):
    print(i, valor)

for i, valor in enumerate(ine_comp.iloc[:, 0]):
    print(i, valor)

piramides = ine_comp.iloc[268:]
piramides

df_long = piramides.melt(
    id_vars="Parametros",
    var_name="Año",
    value_name="Poblacion"
)

df_long["Sexo"] = df_long["Parametros"].apply(
    lambda x: "Hombres" if "Hombres" in x else "Mujeres"
)

df_long["Edad"] = df_long["Parametros"].str.split("_").str[-1]

df_long.loc[df_long["Sexo"] == "Hombres", "Poblacion"] *= -1

orden_edades = [
    "85ymasanios",
    "80a84anios",
    "75a79anios",
    "70a74anios",
    "65a69anios",
    "60a64anios",
    "55a59anios",
    "50a54anios",
    "45a49anios",
    "40a44anios",
    "35a39anios",
    "30a34anios",
    "25a29anios",
    "20a24anios",
    "15a19anios",
    "10a14anios",
    "5a9anios",
    "0a4anios",
]

df_long["Edad"] = pd.Categorical(
    df_long["Edad"],
    categories=orden_edades,
    ordered=True
)


años = ["1975", "1985", "1995", "2005", "2015", "2024"]


fig, axes = plt.subplots(2, 3, figsize=(20, 14))

axes = axes.flatten()

for ax, año in zip(axes, años):

    data = df_long[df_long["Año"] == año]

    sns.barplot(
        data=data,
        x="Poblacion",
        y="Edad",
        hue="Sexo",
        dodge=False,
        palette={
            "Hombres": "steelblue",
            "Mujeres": "lightcoral"
        },
        ax=ax
    )


    ax.axvline(0, color="black", linewidth=1)


    ax.set_title(f"Pirámide poblacional {año}", fontsize=14)


    ticks = ax.get_xticks()
    ax.set_xticklabels([abs(int(t)) for t in ticks])


    xmin, xmax = ax.get_xlim()

    ax.text(
        xmin * 0.8,          # izquierda
        1,                # parte superior
        "Hombres",
        fontsize=12,
        fontweight="bold",
        color="steelblue",
        ha="center"
    )

    ax.text(
        xmax * 0.8,          
        1,
        "Mujeres",
        fontsize=12,
        fontweight="bold",
        color="lightcoral",
        ha="center"
    )

    ax.legend().remove()


handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper right")

plt.tight_layout()

plt.show()



edad_media = ine_comp.iloc[6]


años = ine_comp.columns[1:]


valores = edad_media[1:].astype(float)


plt.figure(figsize=(12,6))

sns.lineplot(
    x=años,
    y=valores,
    marker="o"
)


plt.text(
    x=años[0],
    y=valores.iloc[0],
    s=round(valores.iloc[0], 2),
    ha='right'
)


plt.text(
    x=años[-1],
    y=valores.iloc[-1],
    s=round(valores.iloc[-1], 2),
    ha='left'
)


plt.title("Evolución de la Edad Media de la Población")
plt.xlabel("Año")
plt.ylabel("Edad media (años)")

plt.xticks(rotation=60)

plt.show()


filas_interes = [0, 76, 77, 78, 91]

evolucion_pob = ine_dep.loc[filas_interes].copy()

evolucion_pob




poblacion = evolucion_pob[evolucion_pob[" Parametro"] == "Pob_Total_Total"]


anios = evolucion_pob.columns[1:]


valores = poblacion.iloc[0, 1:].astype(float)


plt.figure(figsize=(12,6))
plt.plot(anios, valores, marker='o', linewidth=2, label='Población total')


for x, y in zip(anios, valores):
    plt.text(x, y, f'{int(y):,}', ha='center', va='bottom', fontsize=8)


plt.title('Evolución de la población total (2009-2024)')
plt.xlabel('Año')
plt.ylabel('Población (millones)')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()


nacimientos = evolucion_pob[evolucion_pob[" Parametro"] == "Total_Nacimientos"].iloc[0, 1:].astype(float)
defunciones = evolucion_pob[evolucion_pob[" Parametro"] == "Total_Defunciones"].iloc[0, 1:].astype(float)

anios = evolucion_pob.columns[1:]


offset = max(nacimientos.max(), defunciones.max()) * 0.005  # 0.5% del valor máximo

plt.figure(figsize=(12,6))

plt.plot(anios, nacimientos, marker='o', linewidth=2, label='Nacimientos')
plt.plot(anios, defunciones, marker='o', linewidth=2, label='Defunciones')


for x, y in zip(anios, nacimientos):
    plt.text(x, y + offset, f'{int(y):,}', ha='center', va='bottom', fontsize=8)

for x, y in zip(anios, defunciones):
    plt.text(x, y - offset, f'{int(y):,}', ha='center', va='top', fontsize=8)

plt.title('Evolución de nacimientos y defunciones (2009-2024)')
plt.xlabel('Año')
plt.ylabel('Número de personas')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()


saldo_vegetativo = evolucion_pob[evolucion_pob[" Parametro"] == "Saldo_Vegetativo"].iloc[0, 1:].astype(float)
saldo_migratorio = evolucion_pob[evolucion_pob[" Parametro"] == "Saldo_Migratorio"].iloc[0, 1:].astype(float)


anios = evolucion_pob.columns[1:]


offset = max(abs(saldo_vegetativo).max(), abs(saldo_migratorio).max()) * 0.01

plt.figure(figsize=(12,6))

plt.plot(anios, saldo_vegetativo, marker='o', linewidth=2, label='Saldo vegetativo')
plt.plot(anios, saldo_migratorio, marker='o', linewidth=2, label='Saldo migratorio')


for x, y in zip(anios, saldo_vegetativo):
    plt.text(x, y + offset, f'{int(y):,}', ha='center', va='bottom', fontsize=8)


for x, y in zip(anios, saldo_migratorio):
    plt.text(x, y + offset, f'{int(y):,}', ha='center', va='bottom', fontsize=8)

plt.title('Evolución del saldo vegetativo y migratorio (2009-2024)')
plt.xlabel('Año')
plt.ylabel('Número de personas')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()

piramide_ext = ine_dep.iloc[372:, [0, -1]].reset_index(drop=True)
piramide_ext

piramide_ext.columns = piramide_ext.columns.str.strip()

df_long = piramide_ext.melt(
    id_vars="Parametro",
    var_name="Año",
    value_name="Poblacion"
)

df_long["Sexo"] = df_long["Parametro"].apply(
    lambda x: "Hombres" if "Hombres" in x else "Mujeres"
)

df_long["Edad"] = df_long["Parametro"].str.split("_").str[-1]


df_long.loc[df_long["Sexo"] == "Hombres", "Poblacion"] *= -1


data_2024 = df_long[df_long["Año"] == "2024"]


orden_edades = [
    "85ymasanios","80a84anios","75a79anios","70a74anios","65a69anios",
    "60a64anios","55a59anios","50a54anios","45a49anios","40a44anios",
    "35a39anios","30a34anios","25a29anios","20a24anios","15a19anios",
    "10a14anios","5a9anios","0a4anios"
]

data_2024["Edad"] = pd.Categorical(
    data_2024["Edad"],
    categories=orden_edades,
    ordered=True
)

# Gráfica
plt.figure(figsize=(10,8))

sns.barplot(
    data=data_2024,
    x="Poblacion",
    y="Edad",
    hue="Sexo",
    dodge=False,
    palette={"Hombres": "steelblue", "Mujeres": "lightcoral"}
)

plt.axvline(0, color="black", linewidth=1)
plt.title("Pirámide poblacional. Población extranjera 2024")

plt.legend()
plt.tight_layout()
plt.show()

comportamiento_nat = ine_dep.iloc[[0, 1, 11] + list(range(79, 91))].copy()
comportamiento_nat

graf_df = comportamiento_nat.iloc[:3].copy()

# Renombrar las categorías
graf_df[" Parametro"] = graf_df[" Parametro"].replace({
    "Total_Nacimientos": "Total nacimientos",
    "Nac_Esp_Todaslasedades": "Nacimientos de madres españolas",
    "Nac_Ext_Todaslasedades": "Nacimientos de madres nacidas en el extranjero"
})


graf_df = graf_df.set_index(" Parametro")


graf_df_t = graf_df.T


plt.figure(figsize=(14, 7))

for columna in graf_df_t.columns:
    plt.plot(
        graf_df_t.index,
        graf_df_t[columna],
        marker='o',
        linewidth=2,
        label=columna
    )
    
    
    for x, y in zip(graf_df_t.index, graf_df_t[columna]):
        plt.text(
            x,
            y + 150,              # separación vertical
            f"{int(y):,}".replace(",", "."),
            ha='center',
            fontsize=8
        )


plt.title("Evolución de los nacimientos (2009-2024)", fontsize=14)
plt.xlabel("Año")
plt.ylabel("Número de nacimientos")
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()


plt.show()


barras_df = comportamiento_nat.iloc[12:15].copy()


barras_df[" Parametro"] = barras_df[" Parametro"].replace({
    "Prim_Hijo_Total": "Edad primer hijo total",
    "Prim_Hijo_Esp": "Edad primer hijo nacional",
    "Prim_Hijo_Ext": "Edad primer hijo extranjeras"
})


barras_df = barras_df.set_index(" Parametro")


barras_df_t = barras_df.T


x = np.arange(len(barras_df_t.index))
width = 0.25


plt.figure(figsize=(14, 7))


for i, columna in enumerate(barras_df_t.columns):
    barras = plt.bar(
        x + i * width,
        barras_df_t[columna],
        width=width,
        label=columna
    )

    
    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura + (max(barras_df_t.max()) * 0.01),
            f"{altura:.2f}",
            ha='center',
            va='bottom',
            fontsize=8,
            rotation=0
        )

plt.xticks(x + width, barras_df_t.index, rotation=45)
plt.xlabel("Año")
plt.ylabel("Edad")
plt.title("Evolución en la edad del primer hijo por procedencia (2009-2024)")
plt.legend()
plt.tight_layout()


plt.show()

barras_df = comportamiento_nat.iloc[6:9].copy()


barras_df[" Parametro"] = barras_df[" Parametro"].replace({
    "Tasa_Global_Fec_Total": "Tasa global de fecundidad",
    "Tasa_Global_Fec_Espaniola": "Tasa global de fecundidad nacional",
    "Tasa_Global_Fec_Extranjera": "Tasa global de fecundidad extranjeras"
})


barras_df = barras_df.set_index(" Parametro")


barras_df_t = barras_df.T


x = np.arange(len(barras_df_t.index))
width = 0.25


plt.figure(figsize=(14, 7))


for i, columna in enumerate(barras_df_t.columns):
    barras = plt.bar(
        x + i * width,
        barras_df_t[columna],
        width=width,
        label=columna
    )

    
    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura + (max(barras_df_t.max()) * 0.01),
            f"{altura:.2f}",
            ha='center',
            va='bottom',
            fontsize=8,
            rotation=0
        )


plt.xticks(x + width, barras_df_t.index, rotation=45)
plt.xlabel("Año")
plt.ylabel("Nacimientos por 1.000 mujeres en edad fértil")
plt.title("Evolución en la tasa de fecundidad por origen de la madre (2009-2024)")
plt.legend()
plt.tight_layout()


plt.show()

barras_df = comportamiento_nat.iloc[9:12].copy()


barras_df[" Parametro"] = barras_df[" Parametro"].replace({
    "Tasa_Global_Fec_Total": "Indicador coyuntural de fecundidad",
    "Tasa_Global_Fec_Espaniola": "Indicador coyuntural de fecundidad nacional",
    "Tasa_Global_Fec_Extranjera": "Indicador coyuntural de fecundidad extranjeras"
})


barras_df = barras_df.set_index(" Parametro")


barras_df_t = barras_df.T


x = np.arange(len(barras_df_t.index))
width = 0.25


plt.figure(figsize=(14, 7))


for i, columna in enumerate(barras_df_t.columns):
    barras = plt.bar(
        x + i * width,
        barras_df_t[columna],
        width=width,
        label=columna
    )

    
    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura + (max(barras_df_t.max()) * 0.01),
            f"{altura:.2f}",
            ha='center',
            va='bottom',
            fontsize=8,
            rotation=0
        )


plt.xticks(x + width, barras_df_t.index, rotation=45)
plt.xlabel("Año")
plt.ylabel("Número medio de hijos")
plt.title("Indicador coyuntural de fecundidad por origen de la madre (2009-2024)")
plt.legend()
plt.tight_layout()

a
plt.show()