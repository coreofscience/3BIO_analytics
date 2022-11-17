# import libraries for data analysis
import pandas as pd

# Read data from this url "https://docs.google.com/spreadsheets/d/1jNY8oEnunCXo80_BWsRtl2ejN6CQstWgs4quDNQpE8Y/edit#gid=0" and save it as groups
groups_raw = pd.read_csv("https://docs.google.com/spreadsheets/d/1jNY8oEnunCXo80_BWsRtl2ejN6CQstWgs4quDNQpE8Y/export?format=csv&gid=0") 

# Create a dataframe called institutions_groups with the column "instituciones" from groups_raw
institutions_groups = groups_raw["instituciones"]

# Create a dataframe called institutions_groups counting the unique values of the column "instituciones" from groups_raw
institutions_groups = institutions_groups.value_counts()

# Change the name of the column "instituciones" to "groups" in institutions_groups
institutions_groups = institutions_groups.rename("groups")

# Remove the strings "Categoría " from the column "estado" in groups_raw
groups_raw["estado"] = groups_raw["estado"].str.replace("Categoría ", "")

# Values equals to "00" in the column "estado" in groups_raw are replaced by "Grupo reconocido"
groups_raw["estado"] = groups_raw["estado"].replace("00", "Grupo reconocido")

# Create a dataframe called institutions_gropus with the matrix of the values in the column "instituciones" and "estado" from groups_raw
institutions_category = pd.crosstab(groups_raw["instituciones"], groups_raw["estado"])

# Create a dataframe called institutions_year with the unique values of "instituciones" and "anio" from groups_raw
institutions_year = groups_raw[["instituciones", "anio"]].drop_duplicates()

# From institutions_year, group by "instituciones" and filter by the lowest value of "anio"
institutions_year = institutions_year.groupby("instituciones").min()

# Create a dataframe called institutions_cleaned by merging institutions_groups, institutions_category and institutions_year
institutions_cleaned = institutions_groups.to_frame().merge(institutions_category, left_index=True, right_index=True).merge(institutions_year, left_index=True, right_index=True)