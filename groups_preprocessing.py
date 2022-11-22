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
    institutions_papers_1 = pd.crosstab(papers_raw["codigo_grupo"], papers_raw["publindex"])

    # from the dataframe "groups_raw" select the columns "codigo del grupo" and "instituciones" and save it in a dataframe called "institutions_groups_names", also change the column name to "codigo_grupo" and "instituciones"
    institutions_groups_names = groups_raw[["codigo del grupo", "instituciones"]]
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





