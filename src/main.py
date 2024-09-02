import os
import re
import streetaddress as pa
import matplotlib.pyplot as plt
import pandas as pd

# Path to the folder containing the files
folder_path = "/Users/ousep/Projects/HudsonCountyRecords/Data/Raw"

# Get a list of all the files in the folder
file_list = os.listdir(folder_path)

# Initialize an empty list to store the dataframes
dfs = []

# Loop through each file and read it into a dataframe
for file in file_list:
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df["County"] = os.path.splitext(file)[0]
        dfs.append(df)

# Concatenate all the dataframes into a single dataframe
combined_df = pd.concat(dfs, ignore_index=True)


addr_fmt = pa.StreetAddressFormatter()
# Modify the selected code to operate on the "Property Location" field

# standardize property location
combined_df.loc[:, "Property Location"] = combined_df.loc[:, "Property Location"].apply(
    addr_fmt.abbrev_street_avenue_etc
)
combined_df.loc[:, "Property Location"] = combined_df.loc[:, "Property Location"].apply(
    addr_fmt.abbrev_direction
)
combined_df.loc[:, "Property Location"] = combined_df.loc[:, "Property Location"].apply(
    addr_fmt.append_TH_to_street
)


# standardize owner's mailing address
combined_df.loc[:, "Owner's Mailing Address"] = combined_df.loc[
    :, "Owner's Mailing Address"
].apply(addr_fmt.abbrev_street_avenue_etc)
combined_df.loc[:, "Owner's Mailing Address"] = combined_df.loc[
    :, "Owner's Mailing Address"
].apply(addr_fmt.abbrev_direction)
combined_df.loc[:, "Owner's Mailing Address"] = combined_df.loc[
    :, "Owner's Mailing Address"
].apply(addr_fmt.append_TH_to_street)

# Remove trailing special characters from 'Owner's Mailing Address' and 'Property Location'
combined_df.loc[:, "Owner's Mailing Address"] = combined_df.loc[
    :, "Owner's Mailing Address"
].str.rstrip(".!@#$%^&*()_+=-")
combined_df.loc[:, "Property Location"] = combined_df.loc[
    :, "Property Location"
].str.rstrip(".!@#$%^&*()_+=-")

# Print the combined dataframe
print(combined_df)


columns = combined_df.columns
print(columns)


# Print the filtered dataframe
print(filtered_df)

# Find rows where owner name ends with "LLC"
llc_rows = filtered_df[filtered_df["Owner's Name"].str.contains(r"L\.L\.C\.")]
llc_rows = filtered_df[
    filtered_df["Owner's Name"].str.contains(r"L[\W_]{0,1}L[\W_]{0,1}C")
]

# Print the rows where owner name ends with "LLC"
print(llc_rows)

# Find rows where property location is not the same as owners mailing address
filtered_df = combined_df[
    combined_df["Property Location"] != combined_df["Owner's Mailing Address"]
]


# Create a histogram with property class
property_class_histogram = filtered_df["Property Class"].value_counts().plot(kind="bar")

# Set the title and labels for the histogram
property_class_histogram.set_title("Property Class Histogram")
property_class_histogram.set_xlabel("Property Class")
property_class_histogram.set_ylabel("Count")

# Show the histogram
plt.show()

# Print the updated filtered dataframe
print(filtered_df)

# Filter the dataframe where property class is 1 or 2
f_df_res = filtered_df[filtered_df["Property Class"].isin(["1", "2"])]
# Create a histogram with Qual
Qual_histogram = f_df_res["Qual"].value_counts().plot(kind="bar")

# Set the title and labels for the histogram
Qual_histogram.set_title("Qual Histogram")
Qual_histogram.set_xlabel("Qual")
Qual_histogram.set_ylabel("Count")

# Show the histogram
plt.show()

# Calculate the frequency of Qual values
qual_frequency = f_df_res["Qual"].value_counts()

# Print the frequency of Qual values
print(qual_frequency)


# Calculate the frequency of Qual values
Owner_frequency = f_df_res["Owner's Name"].value_counts()


# Calculate the frequency of Qual values
OwnerAddr_frequency = (
    f_df_res.groupby(["Owner's Mailing Address", "City/State/Zip"])
    .size()
    .reset_index(name="Count")
)

# Find owner's name, building description, min sale date, max sale date, and average sale price for each record in OwnerAddr_frequency
owner_addresses = []
owner_names = []
building_descs = []
min_sale_dates = []
max_sale_dates = []
avg_sale_prices = []

for address, city_state_zip in zip(
    OwnerAddr_frequency["Owner's Mailing Address"],
    OwnerAddr_frequency["City/State/Zip"],
):
    owner_address = address
    owner_name = (
        f_df_res.loc[
            (f_df_res["Owner's Mailing Address"] == address)
            & (f_df_res["City/State/Zip"] == city_state_zip),
            "Owner's Name",
        ]
        .unique()
        .tolist()
    )
    building_desc = (
        f_df_res.loc[
            (f_df_res["Owner's Mailing Address"] == address)
            & (f_df_res["City/State/Zip"] == city_state_zip),
            "Building Desc",
        ]
        .apply(lambda x: x[:2])
        .unique()
        .tolist()
    )
    min_sale_date = f_df_res.loc[
        (f_df_res["Owner's Mailing Address"] == address)
        & (f_df_res["City/State/Zip"] == city_state_zip),
        "Sale Date",
    ].min()
    max_sale_date = f_df_res.loc[
        (f_df_res["Owner's Mailing Address"] == address)
        & (f_df_res["City/State/Zip"] == city_state_zip),
        "Sale Date",
    ].max()
    avg_sale_price = f_df_res.loc[
        (f_df_res["Owner's Mailing Address"] == address)
        & (f_df_res["City/State/Zip"] == city_state_zip),
        "Sale Price",
    ].mean()
    owner_addresses.append(owner_address)
    owner_names.append(owner_name)
    building_descs.append(building_desc)
    min_sale_dates.append(min_sale_date)
    max_sale_dates.append(max_sale_date)
    avg_sale_prices.append(avg_sale_price)

# Create a dataframe with owner addresses, city/state/zip, and names
owner_table = pd.DataFrame(
    {
        "Owner's Mailing Address": owner_addresses,
        "City/State/Zip": OwnerAddr_frequency["City/State/Zip"],
        "Count": OwnerAddr_frequency["Count"],
        "Owner's Name": owner_names,
        "Building Description": building_descs,
        "Min Sale Date": min_sale_dates,
        "Max Sale Date": max_sale_dates,
        "Average Sale Price": avg_sale_prices,
    }
)

# Print the owner table
print(owner_table)

# Print the owner's names
print(owner_names)
owner_addresses = []
owner_names = []
building_descs = []
min_sale_dates = []
max_sale_dates = []
avg_sale_prices = []

for address in OwnerAddr_frequency.index:
    owner_address = address
    owner_name = (
        f_df_res.loc[f_df_res["Owner's Mailing Address"] == address, "Owner's Name"]
        .unique()
        .tolist()
    )
    building_desc = (
        f_df_res.loc[f_df_res["Owner's Mailing Address"] == address, "Building Desc"]
        .apply(lambda x: x[:2])
        .unique()
        .tolist()
    )
    min_sale_date = f_df_res.loc[
        f_df_res["Owner's Mailing Address"] == address, "Sale Date"
    ].min()
    max_sale_date = f_df_res.loc[
        f_df_res["Owner's Mailing Address"] == address, "Sale Date"
    ].max()
    avg_sale_price = f_df_res.loc[
        f_df_res["Owner's Mailing Address"] == address, "Sale Price"
    ].mean()
    owner_addresses.append(owner_address)
    owner_names.append(owner_name)
    building_descs.append(building_desc)
    min_sale_dates.append(min_sale_date)
    max_sale_dates.append(max_sale_date)
    avg_sale_prices.append(avg_sale_price)

# Create a dataframe with owner addresses and names
owner_table = pd.DataFrame(
    {
        "Owner's Mailing Address": owner_addresses,
        "Count": OwnerAddr_frequency,
        "Owner's Name": owner_names,
        "Building Description": building_descs,
        "Min Sale Date": min_sale_dates,
        "Max Sale Date": max_sale_dates,
        "Average Sale Price": avg_sale_prices,
    }
)

# Print the owner table
print(owner_table)

# Print the owner's names
print(owner_names)

# 0 jersey city, NJ 07306')

print(tt)
pa.__all__
