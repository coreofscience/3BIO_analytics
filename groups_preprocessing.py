# Import pandas as pd
import pandas as pd
# Create a function with the name "preprocessing_data_clusters" that receives the dataframe "data" as a parameter and run all the code above
def preprocessing_groups_institutions(data):
    # Create a dataframe called institutions_groups with the column "instituciones" from groups_raw
    institutions_groups = data["instituciones"]

    # Create a dataframe called institutions_groups counting the unique values of the column "instituciones" from groups_raw
    institutions_groups = institutions_groups.value_counts()

    # Change the name of the column "instituciones" to "groups" in institutions_groups
    institutions_groups = institutions_groups.rename("groups")

    # Remove the strings "Categoría " from the column "estado" in groups_raw
    data["estado"] = data["estado"].str.replace("Categoría ", "")

    # Values equals to "00" in the column "estado" in groups_raw are replaced by "Grupo reconocido"
    data["estado"] = data["estado"].replace("00", "Grupo reconocido")

    # Create a dataframe called institutions_gropus with the matrix of the values in the column "instituciones" and "estado" from groups_raw
    institutions_category = pd.crosstab(data["instituciones"], data["estado"])

    # Create a dataframe called institutions_year with the unique values of "instituciones" and "anio" from groups_raw
    institutions_year = data[["instituciones", "anio"]].drop_duplicates()

    # From institutions_year, group by "instituciones" and filter by the lowest value of "anio"
    institutions_year = institutions_year.groupby("instituciones").min()

    # Create a dataframe called institutions_cleaned by merging institutions_groups, institutions_category and institutions_year
    institutions_cleaned = institutions_groups.to_frame().merge(institutions_category, left_index=True, right_index=True).merge(institutions_year, left_index=True, right_index=True)
    
    return institutions_cleaned