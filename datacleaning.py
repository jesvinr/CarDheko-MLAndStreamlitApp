import pandas as pd
import ast

def conversion(df, city):
    # car detail
    d1 = df["new_car_detail"]
    # Apply the conversion to each entry in the Series
    d1 = d1.apply(convert_to_dict)

    # Now, normalize the data in d1
    car_det = pd.json_normalize(d1)  # Use d1 which is now a Series of dicts

    # Combine the normalized DataFrame with the original DataFrame (if needed)
    d1 = pd.concat([d1.drop(columns=['new_car_detail']), car_det], axis=1)
    d1.drop("new_car_detail", axis=1, inplace=True)
    d1.drop(columns=['trendingText.imgUrl','trendingText.heading', 'trendingText.desc'], axis=1, inplace=True)

    # car overview
    d2 = df["new_car_overview"]
    d2 = d2.apply(convert_to_dict)
    d2 = cars_overview(d2)

    # car specification
    columns = ['Max Power', 'Seats', 'Displacement', 'Max Power Engine', 'Max Torque', 'No of Cylinder',
            'Values per Cylinder', 'Value Configuration', 'Fuel Supply System', 'BoreX Stroke',
            'Turbo Charger', 'Super Charger', 'Length', 'Width', 'Height', 'Rear Tread',
            'Gear Box', 'Drive Type', 'Seating Capacity', 'Steering Type', 'Turning Radius',
            'Front Brake Type', 'Rear Brake Type', 'Tyre Type', 'No Door Numbers']

    d3 = pd.DataFrame(columns=columns)
    # Apply the conversion to each entry in the Series
    d3_json = df["new_car_specs"]
    d3_json = d3_json.apply(convert_to_dict)

    for spec_data in d3_json:
        
        # Initialize a dictionary to hold the data for each row
        row_data = {col: None for col in columns}
        
        # Extract top-level features and populate the dictionary
        for top_feature in spec_data['top']:
            key = top_feature['key']
            value = top_feature['value']
            if key in row_data:
                row_data[key] = value
        
        # Extract nested features and populate the dictionary
        for category in spec_data['data']:
            features = category['list']
            for feature in features:
                key = feature['key']
                value = feature['value']
                if key in row_data:
                    row_data[key] = value
        
        # Add the row_data as a new row to the DataFrame
        d3 = pd.concat([d3, pd.DataFrame([row_data])], ignore_index=True)
        d3['city'] = city
    full_data = pd.concat([d1, d2, d3], axis=1)
    return full_data

def convert_to_dict(entry):
    try:
        # If entry is a string representation of a dictionary, convert it
        return ast.literal_eval(entry)
    except (ValueError, SyntaxError):
        return {}

def cars_overview(data):
    flat_data = []
    for entry in data:
        flat_dict = {}
        for item in entry['top']:
            flat_dict[item['key']] = item['value']
        flat_data.append(flat_dict)
    return pd.DataFrame(flat_data)

def dropUnwantedColumn(df):
    # ----------------------------------------- Dropping unwanted column ------------------------------------------#
    df.drop("Kms Driven", axis=1, inplace = True)        # kms == kms driven
    df.drop("Ownership", axis=1, inplace=True)           # Ownership == owner
    df.drop("owner", axis=1, inplace=True)               # owner = ownerNo
    df.drop("priceSaving", axis=1, inplace =True)        # no data present
    df.drop("priceFixedText", axis=1, inplace =True)     # no data present
    df.drop("priceActual", axis=1, inplace=True)         # low data present
    df.drop("Front Brake Type", axis=1, inplace=True)    # user dont see this
    df.drop("Rear Brake Type", axis=1, inplace = True)   # user dont see this
    df.drop("Max Power Engine", axis=1, inplace=True)    # no data present
    df.drop("Fuel Supply System", axis=1, inplace=True)  # no data present
    df.drop("BoreX Stroke", axis=1, inplace=True)        # low data preset
    df.drop("Max Power", axis=1, inplace=True)           # data is too complex for neat clean
    df.drop("Max Torque", axis=1, inplace=True)          # data is too complex for neat clean
    df.drop("centralVariantId", axis=1, inplace =True)   # no use in prediction 
    df.drop("variantName", axis=1, inplace=True)         # no use in prediction
    df.drop("Seating Capacity", axis=1, inplace=True)    # seats == seating capacity
    df.drop("Value Configuration", axis=1, inplace=True) # user may not known this
    df.drop("ft", axis=1, inplace=True)                  # ft == Fuel Type
    df.drop("it", axis=1, inplace=True)                  # all row value = 0
    df.drop("Rear Tread", axis=1, inplace=True)
    df.drop("Engine Displacement", axis=1, inplace=True)
    df.drop("transmission", axis=1, inplace=True)       # transmission == Transmission
    df.drop("RTO", axis=1, inplace=True)                   
    df = df.rename(columns={'bt': 'brand type'})
    df = df.loc[:,~df.columns.duplicated()].copy()
    return df


#Price
def convert_to_number(value):
    value = value.lower().replace(' ', '')  # Remove spaces and convert to lowercase
        
    if 'lakh' in value:
        return float(value.replace('lakh', '')) * 1e5
    elif 'crore' in value:
        return float(value.replace('crore', '')) * 1e7
    else:
        return float(value)

def convert_numeric_columns_to_int(df):
    object_cols = df.select_dtypes(include='object').columns    
    for col in object_cols:
        # Check if all values in the column can be converted to a float
        if df[col].apply(lambda x: x.replace('.', '', 1).isdigit() if isinstance(x, str) else False).all():
            df[col] = df[col].astype(float).astype(int)  # Convert to float first to handle decimal points, then to int
        else:
            df[col] = df[col].astype(str)  # Keep the column as strings if any non-numeric value is present
    
    return df

    

def cleanData(full_data):
    # ----------------------------------------- Cleaning ------------------------------------------------------------- #
    # columns done ["Gear box", rear tread, km, height] 
    full_data["Gear Box"] = full_data["Gear Box"].str[0]
    full_data["Gear Box"] = full_data["Gear Box"].fillna("5")

    # cleaning column => km
    full_data["km"] = full_data["km"].str.replace(",", "")
    full_data["km"] = full_data["km"].astype(int)


    #cleaning height column
    full_data["Height"] = full_data["Height"].str.replace(r"\s*mm", "",  regex=True)
    full_data["Height"] = full_data["Height"].str.replace(" ", "")
    full_data["Height"] = full_data["Height"].str.replace(",", "")
    full_data.loc[full_data["Height"]=="1498-1501", "Height"] =1500
    full_data["Height"] = full_data["Height"].fillna("")


    m = full_data[full_data["Height"]!=""]["Height"].astype(int).mean()
    full_data.loc[full_data["Height"] == "", "Height"] = m
    full_data["Height"] = full_data["Height"].astype(int)

    # turning radius
    full_data["Turning Radius"] = full_data["Turning Radius"].str.replace(r"\s*m[a-z]*", "", regex=True)
    full_data["Turning Radius"] = full_data["Turning Radius"].fillna("")

    full_data["Turning Radius"] = pd.to_numeric(full_data["Turning Radius"], errors='coerce')
    mean_turning_radius = full_data.groupby("oem")["Turning Radius"].mean().round(2)
    full_data["Turning Radius"] = full_data["Turning Radius"].fillna(full_data["oem"].map(mean_turning_radius))
    m = mean_turning_radius.mean()  # some car brand, all cars have no turning data
    full_data["Turning Radius"] = full_data["Turning Radius"].fillna(m.round(2))
    full_data["Turning Radius"] = full_data["Turning Radius"].astype('float')

    # no of doors
    full_data["No Door Numbers"] = full_data["No Door Numbers"].fillna(4)

    # registration year => filling data with model year to replace nan & removing month
    full_data["Registration Year"] = full_data["Registration Year"].fillna(full_data["modelYear"])
    full_data["Registration Year"]  = full_data["Registration Year"].str.extract(r'(\d{4})')
    full_data["Registration Year"] = full_data["Registration Year"].astype('Int64')
    full_data["Registration Year"] = full_data["Registration Year"].fillna(full_data["modelYear"])

    # for turbo charger
    mapppingForChargers = {"No":"no", "NO":"no", "Yes": "yes", "YES":"yes", "Twin": "twin", "Turbo":"turbo"}
    full_data["Turbo Charger"] = full_data["Turbo Charger"].replace(mapppingForChargers)
    full_data["Turbo Charger"] = full_data["Turbo Charger"].fillna("no")


    # SuperCharger
    full_data["Super Charger"] = full_data["Super Charger"].replace(mapppingForChargers)
    full_data["Super Charger"] = full_data["Super Charger"].fillna("no")


    #Steering type
    # array(['Power', 'Electric', 'Manual', 'power', None, 'Electrical','Electronic', 'EPAS'], dtype=object)
    full_data["Steering Type"] = full_data["Steering Type"].str.lower()
    full_data["Steering Type"] = full_data["Steering Type"].fillna("Manual")


    #Drive type
    DriveTypeMappings = {"Front Wheel Drive":"FWD", "2 WD":"2WD", "4X4":"4x4", "FWD ":"FWD", "4X2": "4x2",
                            "Two Wheel Drive": "2WD", "RWD(with MTT)": "RWD with MTT",
                            "Rear Wheel Drive with ESP":"RWD with ESP"}
    full_data["Drive Type"] = full_data["Drive Type"].replace(DriveTypeMappings)
    full_data["Drive Type"] = full_data["Drive Type"].fillna("FWD") # that is the most common drive type


    # Type type
    full_data["Tyre Type"] = full_data["Tyre Type"].str.lower()
    full_data["Tyre Type"] = full_data["Tyre Type"].replace(r"tyre[s]*\s*", "", regex=True)
    full_data["Tyre Type"] = full_data["Tyre Type"].replace(",", "")
    full_data["Tyre Type"] = full_data["Tyre Type"].replace(".", "")
    full_data["Tyre Type"] = full_data["Tyre Type"].replace(r"\s*", "", regex=True)
    TyreTypeMappings = {"tubeless,radial": "tubeless radial", "tubelessradial":"tubeless radial", "tubeless,radials": "tubeless radial",
                        "tubeless,runflat": "tubeless runflat","radial,tubeless": "tubeless radial",
                        "run-flat": "runflat","tubless,radial": "tubeless radial", "radial,tubless":"tubeless radial",
                        "tubeless.runflat":"tubeless runflat", "radialtubeless": "tubeless radial", "tubelessradials":"tubeless radial",
                        "tubelessmudterrain": "tubeless mud terrain"}
    full_data["Tyre Type"] = full_data["Tyre Type"].replace(TyreTypeMappings)
    full_data["Tyre Type"] = full_data["Tyre Type"].fillna("radial")


    #Width
    full_data["Width"] = full_data["Width"].str.replace(r'\s*mm', "", regex=True)
    full_data["Width"] = full_data["Width"].str.replace(",", "")
    temp = pd.to_numeric(full_data['Width'], errors='coerce')

    meanWidth = int(temp.mean())
    changeWidth = int(abs(meanWidth - temp.iloc[0]))
    nearestWidth = temp.iloc[0]
    for i in range(1,len(temp)):
        if changeWidth > abs(temp.iloc[i]-meanWidth):
            nearestWidth = temp.iloc[i]
            changeWidth = int(abs(temp.iloc[i]-meanWidth))
    full_data["Width"] = full_data["Width"].fillna(nearestWidth).astype(int)


    # Length
    full_data["Length"] = full_data["Length"].str.replace(r'\s*mm', "", regex=True)
    full_data["Length"] = full_data["Length"].str.replace(",", "", regex=True)
    temp = pd.to_numeric(full_data['Length'], errors='coerce')

    meanLength = int(temp.mean())
    changeLength = int(abs(meanWidth - temp.iloc[0]))
    nearestLength = temp.iloc[0]
    for i in range(1,len(temp)):
        if changeLength > abs(temp.iloc[i]-meanLength):
            nearestLength = temp.iloc[i]
            changeLength = int(abs(temp.iloc[i]-meanLength))
    full_data["Length"] = full_data["Length"].fillna(nearestLength).astype(int) 


    #Seats
    full_data["Seats"] = full_data["Seats"].str.replace(" Seats", "")
    full_data["Seats"] = full_data["Seats"].fillna("4").astype(int)


    # valve per cylinder
    full_data["Values per Cylinder"] = full_data["Values per Cylinder"].fillna("4").astype(int)

    full_data["price"] = full_data["price"].str.replace("₹ ", "")
    full_data["price"] = full_data["price"].str.replace(" ", "")
    full_data["price"] = full_data["price"].str.replace(",", "")

    full_data["price"] = full_data["price"].apply(convert_to_number).astype(int)


    #insurace
    full_data["Insurance Validity"] = full_data["Insurance Validity"].fillna("Insurance Validity")
    full_data["Insurance Validity"] = full_data["Insurance Validity"].str.replace(" insurance","")


    #Fuel type
    full_data["Fuel Type"] = full_data["Fuel Type"].fillna("Diesel")


    # Transmission
    full_data["Transmission"] = full_data["Transmission"].fillna("Manual")


    #Year of manufacture
    full_data["Year of Manufacture"] = full_data["Year of Manufacture"].fillna(full_data["modelYear"]).astype(int)


    # Number of cylinder
    full_data["No of Cylinder"] = full_data["No of Cylinder"].fillna('4')
    full_data["No of Cylinder"] = full_data["No of Cylinder"].astype(int)


    # full_data["no door numbers"] = full_data["no door numbers"].fillna('4')


    full_data["Displacement"] = full_data["Displacement"].replace('None', None)
    full_data["Displacement"] = pd.to_numeric(full_data["Displacement"], errors='coerce')
    # Step 3: Fill NaN values with 0
    full_data["Displacement"] = full_data["Displacement"].fillna(0).astype(int)

    df.columns = df.columns.str.lower()


    full_data["no door numbers"] = full_data["no door numbers"].replace('nan', None)
    full_data["no door numbers"] = pd.to_numeric(full_data["no door numbers"], errors='coerce')
    full_data["no door numbers"] = full_data["no door numbers"].fillna(4).astype(int)

    # Convert all object type columns to lowercase
    full_data[full_data.select_dtypes(include='object').columns] = full_data.select_dtypes(include='object').apply(lambda col: col.str.lower())

    full_data = convert_numeric_columns_to_int(full_data)
    return full_data
    



cityNames = ["chennai", "bangalore", "delhi", "hyderabad", "jaipur"]
final_df = pd.DataFrame()
for i in cityNames:
    df = pd.read_excel('D:\\python\\VsCodePythonWorkplace\\car_dheko_project\\datasets\\'+i+'_cars.xlsx')
    df = conversion(df, i)
    print("xlsx to dataframe conversion completed for {} city data".format(i))

    df = dropUnwantedColumn(df)
    print("Unwanted data dropped for {} city data".format(i))

    df_clean = cleanData(df)
    print("Data cleaning completed for {} city data".format(i))

    if len(final_df)==0:
        final_df = df_clean
    else:
        final_df = pd.concat([final_df,df_clean], ignore_index=True, sort=False)
    print("preprocessing completed for {} city data".format(i))

print("Writing in cvs file for future purpose...")
final_df.to_csv('D:\\python\\VsCodePythonWorkplace\\car_dheko_project\\datasets\\AllCarDetail.csv',index=False,mode='w')
print("Final data written in AllCarDetail.csv")


