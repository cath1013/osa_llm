import pandas as pd
import os

def run_labeling():
    file_path = os.path.join("dataset", "eumc_cleaned_data.xlsx")
    data = pd.read_excel(
        file_path,
        dtype={
            "AHI_REM": float,
            "AHI_NREM": float,
            "REM_sup_min": float,
            "REM_lat_min": float,
            "AHI_total": float,
        }
    )
    print(f"initial dataset size: {len(data)} patients")


    #print(data[["AHI_sup", "AHI_lat", "AHI_total"]].dtypes)
    #print(data[["AHI_sup", "AHI_lat", "AHI_total"]].head())


    data = label_remosa(data)

def label_remosa(data):
    # step 1: remove missing values 
    data = data.dropna(subset=["AHI_REM", "AHI_NREM"]).copy()
    print(f"valid remosa samples (after removing missing AHI_REM and AHI_NREM): {len(data)}")

    # create copies of data for each criteria
    data_13 = data.copy()
    data_15 = data.copy()
    data_isolated = data.copy()

    # criteria 13: (AHI_total ≥ 5) and (AHI_REM ≥ 2 * AHI_NREM) and ((REM_sup_min+REM_lat_min) ≥ 10) and (AHI_NREM < 15)
    data_13 = data_13.dropna(subset=["REM_sup_min", "REM_lat_min", "AHI_total"])
    data_13["remosa_13"] = (
        (data_13["AHI_total"] >= 5) & 
        (data_13["AHI_REM"] >= 2 * data_13["AHI_NREM"]) & 
        ((data_13["REM_sup_min"] + data_13["REM_lat_min"]) >= 10) & 
        (data_13["AHI_NREM"] < 15)
    ).astype(int)
    print(f"remosa 13 valid samples: {len(data_13)}")
    print(f"remosa 13 positive cases: {data_13['remosa_13'].sum()}")  # sum of 1s

    # criteria 15: (AHI_total ≥ 5) and (AHI_REM ≥ 2 * AHI_NREM)
    data_15 = data_15.dropna(subset=["AHI_total"])
    data_15["remosa_15"] = (
        (data_15["AHI_total"] >= 5) & 
        (data_15["AHI_REM"] >= 2 * data_15["AHI_NREM"])
    ).astype(int)
    print(f"remosa 15 valid samples: {len(data_15)}")
    print(f"remosa 15 positive cases: {data_15['remosa_15'].sum()}")  # sum of 1s

    # isolated remosa: (AHI_REM ≥ 2 * AHI_NREM) and ((REM_sup_min + REM_lat_min) ≥ 10) and (AHI_NREM < 15)
    data_isolated = data_isolated.dropna(subset=["REM_sup_min", "REM_lat_min"])
    data_isolated["isolated_remosa"] = (
        (data_isolated["AHI_REM"] >= 2 * data_isolated["AHI_NREM"]) & 
        ((data_isolated["REM_sup_min"] + data_isolated["REM_lat_min"]) >= 10) & 
        (data_isolated["AHI_NREM"] < 15)
    ).astype(int)
    print(f"isolated remosa valid samples: {len(data_isolated)}")
    print(f"isolated remosa positive cases: {data_isolated['isolated_remosa'].sum()}")

    # save results
    save_labels(data_13, data_15, data_isolated)

    return data_13, data_15, data_isolated

def save_labels(data_13, data_15, data_isolated, output_folder="dataset/labeling_remosa"):
    os.makedirs(output_folder, exist_ok=True)

    # save each criteria separately
    data_13.to_excel(os.path.join(output_folder, "remosa_criteria_13.xlsx"), index=False)
    data_15.to_excel(os.path.join(output_folder, "remosa_criteria_15.xlsx"), index=False)
    data_isolated.to_excel(os.path.join(output_folder, "remosa_isolated.xlsx"), index=False)

if __name__ == "__main__":
    run_labeling()