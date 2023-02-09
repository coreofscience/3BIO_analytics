"""This module provides functions for preprocessing data for clustering."""
# Import pandas as pd
import pandas as pd
# Create a function with the name "preprocessing_data_clusters"
# that receives the dataframe "data" as a parameter and run all the code above

def preprocessing_groups_institutions(data):
    """Preprocess the data for clustering."""
    # Create a dataframe called institutions_groups with the column
    # "instituciones" from groups_raw
    institutions_groups = data["instituciones"]

    # Create a dataframe called institutions_groups counting the
    # unique values of the column "instituciones" from groups_raw
    institutions_groups = institutions_groups.value_counts()

    # Change the name of the column "instituciones" to "groups"
    # in institutions_groups
    institutions_groups = institutions_groups.rename("groups")

    # Remove the strings "Categoría " from the column "Estado"
    # in groups_raw
    data["Estado"] = data["Estado"].str.replace("Categoría ", "")

    # Values equals to "00" in the column "estado" in groups_raw are
    # replaced by "Grupo reconocido"
    data["Estado"] = data["Estado"].replace("00", "Grupo reconocido")

    # Create a dataframe called institutions_gropus with the matrix
    # of the values in the column "instituciones" and "estado" from groups_raw
    institutions_category = pd.crosstab(data["instituciones"], data["Estado"])

    # Extract the first four characters from the column "Año y mes
    # de formación" in data
    data["Año y mes de formación"] = data["Año y mes de formación"].str[:4]

    # Change the name of the column "Año y mes de formación" to "anio" in data
    data = data.rename(columns={"Año y mes de formación": "anio"})

    # Create a dataframe called institutions_year with the unique
    # values of "instituciones" and "anio" from groups_raw
    institutions_year = data[["instituciones", "anio"]].drop_duplicates()

    # From institutions_year, group by "instituciones" and filter by
    # the lowest value of "anio"
    institutions_year = institutions_year.groupby("instituciones").min()

    # Create a dataframe called institutions_cleaned by merging
    # institutions_groups, institutions_category and institutions_year
    institutions_cleaned = institutions_groups.to_frame().merge(institutions_category,
    left_index=True, right_index=True).merge(institutions_year,
    left_index=True, right_index=True)

    # Change the name of the column "groups" to "total_groups"
    # in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"groups": "total_groups"})

    # Change the name of the column "A" to "Group_A" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"A": "Group_A"})

    # Change the name of the column "A1" to "Group_A1" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"A1": "Group_A1"})

    # Change the name of the column "B" to "Group_B" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"B": "Group_B"})

    # Change the name of the column "C" to "Group_C" in institutions_cleaned
    institutions_cleaned = institutions_cleaned.rename(columns={"C": "Group_C"})

    # Change the name of the column "Grupo reconocido" to
    # "Group_no_category" in institutions_cleaned
    rename_dict = {"Grupo reconocido": "Group_no_category"}
    institutions_cleaned = institutions_cleaned.rename(columns=rename_dict)

    # Create a column named "instituciones" in the dataframe
    # "institution_groups" with the values in index column
    institutions_cleaned['instituciones'] = institutions_cleaned.index
    # Move the column "instituciones" to the first position
    cols = [col for col in institutions_cleaned.columns if col != 'instituciones']
    new_cols = ['instituciones'] + cols
    institutions_cleaned = institutions_cleaned[new_cols]

    return institutions_cleaned

# Create a function with the name "preprocessing_groups_papers"
# that receives the dataframe "papers_raw" and "groups_raw" as a
# parameters and run all the code above. Return the dataframe "institutions_papers_3"

def preprocessing_groups_papers(papers_raw, groups_raw):
    """This module provides functions for preprocessing data for papers."""
    # Create a dataframe called institutions_papers_1 with the
    # matrix of the count of unique values in the column "codigo_grupo"
    # and "publindex" from papers_raw
    institutions_papers_1 = pd.crosstab(papers_raw["codigo_grupo"], papers_raw["Publindex"])

    # from the dataframe "groups_raw" select the columns
    # "Código del grupo" and "instituciones" and save it in a
    # dataframe called "institutions_groups_names", also change
    # the column name to "codigo_grupo" and "instituciones"
    institutions_groups_names = groups_raw[["Código del grupo", "instituciones"]]
    institutions_groups_names.columns = ["codigo_grupo", "instituciones"]

    # from the dataframe "institutions_groups_names" filter the
    # unique values and save the results in a dataframe called
    # "institutions_groups_names_unique"
    institutions_groups_names_unique = institutions_groups_names.drop_duplicates(subset=['codigo_grupo'])

    # Merge the dataframe "institutions_groups_names" with the
    # dataframe "institutions_papers_1" on the column "codigo_grupo"
    institutions_papers_2 = pd.merge(institutions_groups_names_unique,
    institutions_papers_1, on="codigo_grupo")

    # Remove the column "codigo_grupo" from the dataframe "institutions_papers_2"
    institutions_papers_2 = institutions_papers_2.drop(columns=["codigo_grupo"])

    # Create a dataframe called "institutions_papers_3"
    # with the group by of the dataframe "institutions_papers_2"
    # by the column "instituciones" and sum the values
    institutions_papers_3 = institutions_papers_2.groupby(["instituciones"]).sum()

    # Create a new column in the dataframe "institutions_papers_3"
    # called "total" with the sum of the values of the dataframe "institutions_papers_3"
    institutions_papers_3["total"] = institutions_papers_3.sum(axis=1)

    institutions_papers_3.columns = [
        f'Paper_{str(col)}' for col in institutions_papers_3.columns
    ]

    return institutions_papers_3

def preprocessing_groups_researchers(researchers_raw, groups_raw):
    """This module provides functions for preprocessing data for researchers."""
    # from groups_raw dataframe, change the name of the column
    # "Código del grupo" to "codigo_grupo", select "codigo_grupo"
    # and "instituciones" and save the data in a variable called "groups_raw_1"
    groups_raw_1 = groups_raw.rename(columns={'Código del grupo': 'codigo_grupo'})[['codigo_grupo', 'instituciones']]

    # merge researchers_raw and groups_raw_1 on "codigo_grupo"
    # and save the data in a variable called "researchers_raw_1"
    researchers_raw_1 = researchers_raw.merge(groups_raw_1, on='codigo_grupo', how='left') # There is a mistake here

    # create a new dataframe called "researchers_raw_2" from
    # "researchers_raw_1" and select "Nombre" and "instituciones"
    researchers_raw_2 = researchers_raw_1[['Nombre', 'instituciones']]

    # Group the data by "instituciones" and count the number
    # of values in column "Nombre", save the data in dataframe
    # called "researchers_raw_3"
    researchers_raw_3 = researchers_raw_2.groupby(['instituciones']).size().reset_index(name='counts')
    # Change the name of the column "counts" to "researchers_total"
    researchers_raw_total = researchers_raw_3.rename(columns={'counts': 'researchers_total'})

    # form researchers_raw_1, select "Posgrado" and "instituciones"
    # and save the data in a variable called "researchers_raw_4"
    researchers_raw_4 = researchers_raw_1[['Posgrado', 'instituciones']]

    # Change the values in "Posgrado", "Maestría/magister" or
    # "Maestría/Magister" to "magister", "Doctorado" to "doctorate",
    # "Especialización" to "specialization", "Especialidad médica" or
    # "Especialidad Médica" to "medical_specialization", "Pregrado/universitario"
    # or "Pregrado/Universitario" to "undergrad". Save the data in a variable called
    # "researchers_raw_5"
    researchers_raw_5 = researchers_raw_4.replace({'Posgrado': {'Maestría/magister': 'magister', 'Maestría/Magister': 'magister', 'Doctorado': 'doctorate', 'Especialización': 'specialization', 'Especialidad médica': 'medical_specialization', 'Especialidad Médica': 'medical_specialization', 'Pregrado/universitario': 'undergrad', 'Pregrado/Universitario': 'undergrad'}})

    # From researchers_raw_5, remove values in column "Posgrado"
    # that are not in the list ["magister", "doctorate", "specialization",
    # "medical_specialization", "undergrad"], save the data in a variable
    # called "researchers_raw_5"
    researchers_raw_5 = researchers_raw_5[researchers_raw_5['Posgrado'].isin(['magister', 'doctorate', 'specialization', 'medical_specialization', 'undergrad'])]

    # From researchers_raw_5, group the data by "instituciones" and
    # "Posgrado" and count the number of values in column "Posgrado",
    # save the data in a variable called "researchers_raw_6"
    researchers_raw_6 = researchers_raw_5.groupby(['instituciones', 'Posgrado']).size().reset_index(name='counts')

    # Create a matrix with the values in column "Posgrado" as
    # columns and the values in column "instituciones" as rows,
    # save the data in a variable called "researchers_raw_7"
    researchers_raw_7 = researchers_raw_6.pivot(index='instituciones', columns='Posgrado', values='counts')

    # Fill the missing values with 0 and save the data in a
    # variable called "researchers_raw_formation"
    researchers_raw_formation = researchers_raw_7.fillna(0)

    # Merge researchers_raw_formation and researchers_raw_total on
    # "instituciones" and save the data in a variable called "researchers"
    institutions_researchers = researchers_raw_formation.merge(researchers_raw_total, on='instituciones', how='left')

    return institutions_researchers
