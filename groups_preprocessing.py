# Import pandas as pd
import pandas as pd
import numpy as np
# Create a function with the name "preprocessing_data_clusters" that receives the dataframe "data" as a parameter and run all the code above
def preprocessing_groups_institutions(data):
    # Create a dataframe called institutions_groups with the column "instituciones" from groups_raw
    institutions_groups = data["instituciones"]

    # Create a dataframe called institutions_groups counting the unique values of the column "instituciones" from groups_raw
    institutions_groups = institutions_groups.value_counts()

    # Change the name of the column "instituciones" to "groups" in institutions_groups
    institutions_groups = institutions_groups.rename("groups")

    # Remove the strings "Categoría " from the column "Estado" in groups_raw
    data["Estado"] = data["Estado"].str.replace("Categoría ", "")

    # Values equals to "00" in the column "estado" in groups_raw are replaced by "Grupo reconocido"
    data["Estado"] = data["Estado"].replace("00", "Grupo reconocido")

    # Create a dataframe called institutions_gropus with the matrix of the values in the column "instituciones" and "estado" from groups_raw
    institutions_category = pd.crosstab(data["instituciones"], data["Estado"])

    # Extract the first four characters from the column "Año y mes de formación" in data
    data["Año y mes de formación"] = data["Año y mes de formación"].str[:4]

    # Change the name of the column "Año y mes de formación" to "anio" in data
    data = data.rename(columns={"Año y mes de formación": "anio"})

    # Create a dataframe called institutions_year with the unique values of "instituciones" and "anio" from groups_raw
    institutions_year = data[["instituciones", "anio"]].drop_duplicates()

    # From institutions_year, group by "instituciones" and filter by the lowest value of "anio"
    institutions_year = institutions_year.groupby("instituciones").min()

    # Create a dataframe called institutions_cleaned by merging institutions_groups, institutions_category and institutions_year
    institutions_cleaned = institutions_groups.to_frame().merge(institutions_category, left_index=True, right_index=True).merge(institutions_year, left_index=True, right_index=True)
    
    # Change the name of the column "groups" to "total_groups" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"groups": "total_groups"})

    # Change the name of the column "A" to "Group_A" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"A": "Group_A"})

    # Change the name of the column "A1" to "Group_A1" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"A1": "Group_A1"})

    # Change the name of the column "B" to "Group_B" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"B": "Group_B"})

    # Change the name of the column "C" to "Group_C" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"C": "Group_C"})

    # Change the name of the column "Grupo reconocido" to "Group_no_category" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"Grupo reconocido": "Group_no_category"})

    return institutions_cleaned

# Create a function with the name "preprocessing_groups_papers" that receives the dataframe "papers_raw" and "groups_raw" as a parameters and run all the code above. Return the dataframe "institutions_papers_3"

def preprocessing_groups_papers(papers_raw, groups_raw):

    # Create a dataframe called institutions_papers_1 with the matrix of the count of unique values in the column "codigo_grupo" and "publindex" from papers_raw    
    institutions_papers_1 = pd.crosstab(papers_raw["codigo_grupo"], papers_raw["Publindex"])

    # from the dataframe "groups_raw" select the columns "Código del grupo" and "instituciones" and save it in a dataframe called "institutions_groups_names", also change the column name to "codigo_grupo" and "instituciones"
    institutions_groups_names = groups_raw[["Código del grupo", "instituciones"]]
    institutions_groups_names.columns = ["codigo_grupo", "instituciones"]

    # from the dataframe "institutions_groups_names" filter the unique values and save the results in a dataframe called "institutions_groups_names_unique"
    institutions_groups_names_unique = institutions_groups_names.drop_duplicates(subset=['codigo_grupo'])

    # Merge the dataframe "institutions_groups_names" with the dataframe "institutions_papers_1" on the column "codigo_grupo"
    institutions_papers_2 = pd.merge(institutions_groups_names_unique, institutions_papers_1, on="codigo_grupo")

    # Remove the column "codigo_grupo" from the dataframe "institutions_papers_2"
    institutions_papers_2 = institutions_papers_2.drop(columns=["codigo_grupo"])

    # Create a dataframe called "institutions_papers_3" with the group by of the dataframe "institutions_papers_2" by the column "instituciones" and sum the values
    institutions_papers_3 = institutions_papers_2.groupby(["instituciones"]).sum()

    # Create a new column in the dataframe "institutions_papers_3" called "total" with the sum of the values of the dataframe "institutions_papers_3"
    institutions_papers_3["total"] = institutions_papers_3.sum(axis=1)

    return institutions_papers_3

# Create a function with the name "preprocessing_researches_papers" that receives the dataframe "groups_raw" and "researchers" as a parameters and run all the code above. Return the dataframe "researchers_selectedXInstitucion"
def preprocessing_researches_papers(researchers, groups_raw):
    # create a variable called "researchers_raw" from the url "https://docs.google.com/spreadsheets/d/1jNY8oEnunCXo80_BWsRtl2ejN6CQstWgs4quDNQpE8Y/export?format=csv&gid=0"
    #researchers_url = "https://drive.google.com/file/d/143u1k6A-LZDhhSGvREzNaXYT4aUEZlGN/view?usp=share_link"
    #researchers_raw = 'https://drive.google.com/uc?id=' + researchers_url.split('/')[-2]
    #researchers = pd.read_csv(researchers_raw)
    # select the columns  "codigo_grupo", "categoria","posgrado", "fin vinculacion"] from researchers and savae it in a variable called researchers_cleaned
    researchers_selected = researchers[["codigo_grupo", "nombre","categoria","posgrado", "fin vinculacion"]]
    groups_instituciones = groups_raw[["Código del grupo", "instituciones"]]

    #update the column "codigo del grupo" to "codigo_grupo" in groups_instituciones
    groups_instituciones = groups_instituciones.rename(columns={"Código del grupo": "codigo_grupo"})

    # Merge the dataframe "researchers_selected" with the dataframe "groups_instituciones" on the column "codigo_grupo"
    researchers_selected = pd.merge(researchers_selected, groups_instituciones, on="codigo_grupo")

    #drop duplicates from researchers_selected
    researchers_selected = researchers_selected.drop_duplicates()

    total_integrantes= researchers_selected.groupby(['codigo_grupo']).size().reset_index(name='cantidad_integrantes')

    #update the value of the column "categoria" to null where column "categoria" is equal to "Investigador Jefferson Torres" of the dataframe "researchers_selected"
    researchers_selected.loc[researchers_selected["categoria"] == "Investigador Jefferson Torres", "categoria"] = np.nan

    #update the value of the column "categoria" to "Sin_categoria" where column "categoria" is equal to NaN"
    researchers_selected["categoria"] = researchers_selected["categoria"].fillna("Sin_categoria")

    categoriaXgrupo = pd.crosstab(researchers_selected["codigo_grupo"], researchers_selected["categoria"])
    research_posgrado = pd.crosstab(researchers_selected["codigo_grupo"], researchers_selected["posgrado"])

    categoria_posgrado_grupo = pd.merge(categoriaXgrupo, research_posgrado, on="codigo_grupo")

    researchers_selected = pd.merge(researchers_selected, categoria_posgrado_grupo, on="codigo_grupo")

    #delete columns "categoria", "posgrado" and "fin vinculacion" in researchers_selected
    researchers_selected = researchers_selected.drop(columns=["nombre", "categoria", "fin vinculacion", "Técnico - nivel superior",
    "Primaria","Primaria incompleta", "Secundario", "Técnico - nivel medio", "posgrado","No informado","Perfeccionamiento",
    "Especialidad médica"])

    researchers_selected = pd.merge(researchers_selected, total_integrantes, on="codigo_grupo")
    
    researchers_selected = researchers_selected.drop_duplicates()

    #group by dataframe "researchers_selected"  by "instituciones" and count the values
    researchers_selectedXInstitucion = researchers_selected.groupby("instituciones").sum()

    return researchers_selectedXInstitucion






