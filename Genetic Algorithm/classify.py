import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

import pandas as pd
from keras.models import load_model

def getDummiesForEveryVariable(df):
    dummied_columns = []
    for column in df.columns:
        dummied_columns.append( pd.get_dummies( df[column], prefix = column) )
    dummied_columns = pd.concat( dummied_columns, axis = 1, join = 'inner')
    return dummied_columns

def write_output(output, id):
    file = open(f"Output_Files/output_file_{id}.txt", "w")
    i = 1
    for nota in output[1][0].numpy():
        if round(nota) == 1:
            break
        i += 1

    nota = i
    file.write(f"{nota}\n")
    
    climas = output[0]
    for p in climas[0].numpy():
        file.write(f"{p}\n")
    file.close()

def leer_columnas_eliminadas(nombre_modelo):
    columnas_eliminadas = []
    archivo = open(f"{nombre_modelo}")
    for linea in archivo:
        linea = linea.strip()
        columnas_eliminadas.append(linea)
    return columnas_eliminadas

def cargar_modelo(nombre_modelo):
    model = load_model(f"modelos/{nombre_modelo}/{nombre_modelo}.h5")
    # columnas_eliminadas = leer_columnas_eliminadas(f"modelos/{nombre_modelo}/columnas_eliminadas.txt")
    return model#, columnas_eliminadas

id_outfit = sys.argv[1]

firstLayer = sys.argv[2]
secondLayer = sys.argv[3]
thirdLayer = sys.argv[4]
hat = sys.argv[5]
shoes = sys.argv[6]
pants = sys.argv[7]

modelo = sys.argv[8]

model = cargar_modelo(modelo)

model_input = []
for encode in [firstLayer, secondLayer, thirdLayer, hat, shoes, pants]:
    for char in encode.split(","):
        model_input.append(int(char))

columns = ['cloth_category_1', 'cloth_subcategory_1', 'patron_1', 'sleeve_1',
       'skirt_1', 'neckline_1', 'material_1', 'fit_1', 'isCold_1', 'isRainy_1',
       'isWet_1', 'isTempered_1', 'isHot_1', 'nota_1', 'cloth_category_2',
       'cloth_subcategory_2', 'patron_2', 'sleeve_2', 'skirt_2', 'neckline_2',
       'material_2', 'fit_2', 'isCold_2', 'isRainy_2', 'isWet_2',
       'isTempered_2', 'isHot_2', 'nota_2', 'cloth_category_3',
       'cloth_subcategory_3', 'patron_3', 'sleeve_3', 'skirt_3', 'neckline_3',
       'material_3', 'fit_3', 'isCold_3', 'isRainy_3', 'isWet_3',
       'isTempered_3', 'isHot_3', 'nota_3', 'cloth_category_4',
       'cloth_subcategory_4', 'patron_4', 'sleeve_4', 'skirt_4', 'neckline_4',
       'material_4', 'fit_4', 'isCold_4', 'isRainy_4', 'isWet_4',
       'isTempered_4', 'isHot_4', 'nota_4', 'cloth_category_5',
       'cloth_subcategory_5', 'patron_5', 'sleeve_5', 'skirt_5', 'neckline_5',
       'material_5', 'fit_5', 'isCold_5', 'isRainy_5', 'isWet_5',
       'isTempered_5', 'isHot_5', 'nota_5', 'cloth_category_6',
       'cloth_subcategory_6', 'patron_6', 'sleeve_6', 'skirt_6', 'neckline_6',
       'material_6', 'fit_6', 'isCold_6', 'isRainy_6', 'isWet_6',
       'isTempered_6', 'isHot_6', 'nota_6']

# crear Dataframe con input 
d = {}
i = 0
while i < len(columns):
    d[columns[i]] = [model_input[i]]
    i += 1

df = pd.DataFrame(data=d)

# extraer notas
# variables_continuas = ["nota_1", "nota_2", "nota_3", "nota_4", "nota_5", "nota_6"]
# notas_df = df[variables_continuas].copy()

# df = df.drop(variables_continuas, axis=1)


# codificar entrada con one-hot
dummied_df = getDummiesForEveryVariable(df)

# listado de todas las columnas de one-hot posibles
df_columns = [    
    "cloth_category_1_1",
    "cloth_subcategory_1_1",
    "cloth_subcategory_1_2",
    "cloth_subcategory_1_4",
    "cloth_subcategory_1_5",
    "cloth_subcategory_1_6",
    "cloth_subcategory_1_7",
    "cloth_subcategory_1_8",
    "cloth_subcategory_1_9",
    "patron_1_1",
    "patron_1_2",
    "patron_1_3",
    "patron_1_4",
    "patron_1_5",
    "patron_1_6",
    "patron_1_7",
    "sleeve_1_1",
    "sleeve_1_2",
    "sleeve_1_3",
    "skirt_1_1",
    "skirt_1_2",
    "skirt_1_3",
    "neckline_1_1",
    "neckline_1_2",
    "neckline_1_3",
    "neckline_1_4",
    "material_1_1",
    "material_1_2",
    "material_1_3",
    "material_1_4",
    "material_1_5",
    "material_1_6",
    "fit_1_1",
    "fit_1_2",
    "fit_1_3",
    "isCold_1_0",
    "isCold_1_1",
    "isRainy_1_0",
    "isRainy_1_1",
    "isWet_1_0",
    "isWet_1_1",
    "isTempered_1_0",
    "isTempered_1_1",
    "isHot_1_0",
    "isHot_1_1",
    "nota_1_1",
    "nota_1_2",
    "nota_1_3",
    "nota_1_4",
    "nota_1_5",
    "cloth_category_2_0",
    "cloth_category_2_2",
    "cloth_subcategory_2_0",
    "cloth_subcategory_2_1",
    "cloth_subcategory_2_2",
    "cloth_subcategory_2_3",
    "cloth_subcategory_2_4",
    "cloth_subcategory_2_5",
    "patron_2_0",
    "patron_2_1",
    "patron_2_2",
    "patron_2_3",
    "patron_2_4",
    "patron_2_5",
    "patron_2_6",
    "patron_2_7",
    "sleeve_2_0",
    "sleeve_2_1",
    "sleeve_2_2",
    "sleeve_2_3",
    "skirt_2_0",
    "skirt_2_1",
    "skirt_2_3",
    "neckline_2_0",
    "neckline_2_1",
    "neckline_2_2",
    "neckline_2_3",
    "neckline_2_4",
    "material_2_0",
    "material_2_1",
    "material_2_2",
    "material_2_3",
    "material_2_4",
    "material_2_5",
    "material_2_6",
    "fit_2_0",
    "fit_2_1",
    "fit_2_2",
    "fit_2_3",
    "isCold_2_0",
    "isCold_2_1",
    "isRainy_2_0",
    "isRainy_2_1",
    "isWet_2_0",
    "isWet_2_1",
    "isTempered_2_0",
    "isTempered_2_1",
    "isHot_2_0",
    "isHot_2_1",
    "nota_2_0",
    "nota_2_1",
    "nota_2_2",
    "nota_2_3",
    "nota_2_4",
    "nota_2_5",
    "cloth_category_3_0",
    "cloth_category_3_3",
    "cloth_subcategory_3_0",
    "cloth_subcategory_3_1",
    "cloth_subcategory_3_2",
    "cloth_subcategory_3_3",
    "cloth_subcategory_3_4",
    "cloth_subcategory_3_6",
    "patron_3_0",
    "patron_3_1",
    "patron_3_2",
    "patron_3_3",
    "patron_3_4",
    "patron_3_6",
    "patron_3_7",
    "sleeve_3_0",
    "sleeve_3_1",
    "sleeve_3_2",
    "sleeve_3_3",
    "skirt_3_0",
    "skirt_3_2",
    "skirt_3_3",
    "neckline_3_0",
    "neckline_3_1",
    "neckline_3_2",
    "neckline_3_4",
    "material_3_0",
    "material_3_1",
    "material_3_2",
    "material_3_3",
    "material_3_4",
    "material_3_5",
    "material_3_6",
    "fit_3_0",
    "fit_3_1",
    "fit_3_2",
    "fit_3_3",
    "isCold_3_0",
    "isCold_3_1",
    "isRainy_3_0",
    "isRainy_3_1",
    "isWet_3_0",
    "isWet_3_1",
    "isTempered_3_0",
    "isTempered_3_1",
    "isHot_3_0",
    "isHot_3_1",
    "nota_3_0",
    "nota_3_1",
    "nota_3_2",
    "nota_3_3",
    "nota_3_4",
    "nota_3_5",
    "cloth_category_4_0",
    "cloth_category_4_4",
    "cloth_subcategory_4_0",
    "cloth_subcategory_4_1",
    "cloth_subcategory_4_2",
    "cloth_subcategory_4_3",
    "cloth_subcategory_4_4",
    "cloth_subcategory_4_5",
    "cloth_subcategory_4_6",
    "cloth_subcategory_4_7",
    "cloth_subcategory_4_8",
    "cloth_subcategory_4_9",
    "cloth_subcategory_4_10",
    "patron_4_0",
    "patron_4_6",
    "patron_4_7",
    "sleeve_4_0",
    "skirt_4_0",
    "neckline_4_0",
    "material_4_0",
    "material_4_5",
    "material_4_6",
    "fit_4_0",
    "fit_4_1",
    "fit_4_2",
    "isCold_4_0",
    "isCold_4_1",
    "isRainy_4_0",
    "isRainy_4_1",
    "isWet_4_0",
    "isTempered_4_0",
    "isTempered_4_1",
    "isHot_4_0",
    "isHot_4_1",
    "nota_4_0",
    "nota_4_2",
    "nota_4_3",
    "nota_4_4",
    "cloth_category_5_5",
    "cloth_subcategory_5_1",
    "cloth_subcategory_5_2",
    "cloth_subcategory_5_3",
    "cloth_subcategory_5_4",
    "cloth_subcategory_5_5",
    "cloth_subcategory_5_6",
    "cloth_subcategory_5_7",
    "cloth_subcategory_5_8",
    "cloth_subcategory_5_9",
    "cloth_subcategory_5_10",
    "cloth_subcategory_5_11",
    "patron_5_0",
    "patron_5_6",
    "sleeve_5_0",
    "skirt_5_0",
    "neckline_5_0",
    "material_5_0",
    "material_5_4",
    "fit_5_0",
    "fit_5_1",
    "fit_5_2",
    "fit_5_3",
    "isCold_5_0",
    "isCold_5_1",
    "isRainy_5_0",
    "isRainy_5_1",
    "isWet_5_0",
    "isWet_5_1",
    "isTempered_5_0",
    "isTempered_5_1",
    "isHot_5_0",
    "isHot_5_1",
    "nota_5_2",
    "nota_5_3",
    "nota_5_4",
    "nota_5_5",
    "cloth_category_6_6",
    "cloth_subcategory_6_1",
    "cloth_subcategory_6_2",
    "cloth_subcategory_6_3",
    "cloth_subcategory_6_4",
    "cloth_subcategory_6_5",
    "cloth_subcategory_6_6",
    "cloth_subcategory_6_7",
    "cloth_subcategory_6_8",
    "cloth_subcategory_6_9",
    "cloth_subcategory_6_10",
    "cloth_subcategory_6_11",
    "cloth_subcategory_6_12",
    "cloth_subcategory_6_13",
    "cloth_subcategory_6_14",
    "cloth_subcategory_6_15",
    "patron_6_1",
    "patron_6_2",
    "patron_6_3",
    "patron_6_4",
    "patron_6_5",
    "patron_6_6",
    "patron_6_7",
    "sleeve_6_1",
    "sleeve_6_2",
    "sleeve_6_3",
    "skirt_6_1",
    "skirt_6_2",
    "skirt_6_3",
    "neckline_6_1",
    "neckline_6_2",
    "neckline_6_4",
    "material_6_1",
    "material_6_2",
    "material_6_3",
    "material_6_4",
    "material_6_6",
    "fit_6_1",
    "fit_6_2",
    "fit_6_3",
    "isCold_6_0",
    "isCold_6_1",
    "isRainy_6_0",
    "isRainy_6_1",
    "isWet_6_0",
    "isWet_6_1",
    "isTempered_6_0",
    "isTempered_6_1",
    "isHot_6_0",
    "isHot_6_1",
    "nota_6_1",
    "nota_6_2",
    "nota_6_3",
    "nota_6_4",
    "nota_6_5"
]

# inicializar dataframe con esas columnas pero lleno de 0
d = {}
for c in df_columns:
    d[c] = [0]
all_columns_df = pd.DataFrame(data=d)

# setear en 1 las columnas correspondientes
for c in dummied_df:
    all_columns_df[c] = 1

# listado de columnas eliminadas en el pre-procesamiento
deleted_columns = [
    "nota_2_0",
    "nota_3_0",
    "nota_4_0",
    "isCold_1_1",
    "isRainy_1_1",
    "isWet_1_1",
    "isTempered_1_1",
    "isHot_1_1",
    "isCold_2_1",
    "isRainy_2_1",
    "isWet_2_1",
    "isTempered_2_1",
    "isHot_2_1",
    "isCold_3_1",
    "isRainy_3_1",
    "isWet_3_1",
    "isTempered_3_1",
    "isHot_3_1",
    "isCold_4_1",
    "isRainy_4_1",
    "isTempered_4_1",
    "isHot_4_1",
    "isCold_5_1",
    "isRainy_5_1",
    "isWet_5_1",
    "isTempered_5_1",
    "isHot_5_1",
    "isCold_6_1",
    "isRainy_6_1",
    "isWet_6_1",
    "isTempered_6_1",
    "isHot_6_1",
    "cloth_category_1_1",
    "skirt_1_1",
    "skirt_1_2",
    "skirt_1_3",
    "cloth_subcategory_2_0",
    "patron_2_0",
    "sleeve_2_0",
    "skirt_2_0",
    "skirt_2_1",
    "skirt_2_3",
    "neckline_2_0",
    "material_2_0",
    "fit_2_0",
    "cloth_subcategory_3_0",
    "patron_3_0",
    "sleeve_3_0",
    "skirt_3_0",
    "skirt_3_2",
    "skirt_3_3",
    "neckline_3_0",
    "material_3_0",
    "fit_3_0",
    "cloth_subcategory_4_0",
    "patron_4_0",
    "sleeve_4_0",
    "skirt_4_0",
    "neckline_4_0",
    "material_4_0",
    "fit_4_0",
    "cloth_category_5_5",
    "sleeve_5_0",
    "skirt_5_0",
    "neckline_5_0",
    "cloth_category_6_6",
    "sleeve_6_1",
    "sleeve_6_2",
    "sleeve_6_3",
    "neckline_6_1",
    "neckline_6_2",
    "neckline_6_4"
]

# eliminar columnas del df
all_columns_df = all_columns_df.drop(deleted_columns, axis = 1)

# concatenar notas y variables categoricas
# input = pd.concat( [notas_df, all_columns_df], axis = 1, join = 'inner')

# conversión final
x = all_columns_df.to_numpy()

# cargar modelo
# model = load_model('NeuralClassifier.h5')

# realizar predicción sobre la entrada
try:
    prediction = model(x, training = False)
except Exception as e:
    print("Error en", id_outfit)
    print(e)
    
# escribir predicción en archivo correspondiente
write_output(prediction, id_outfit)


