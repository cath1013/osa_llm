import pandas as pd
import os

def run_labeling():
    file_path = os.path.join("..", "dataset", "eumc_cleaned_data.xlsx")
    data = pd.read_excel(
        file_path,
        dtype={
            "AHI_sup": float,
            "AHI_lat": float,
            "AHI_total": float
        }
    )
    print(f"initial dataset size: {len(data)} patients")

    #print(data[["AHI_sup", "AHI_lat", "AHI_total"]].dtypes)
    #print(data[["AHI_sup", "AHI_lat", "AHI_total"]].head())


    data = label_posa(data)

def label_posa(data):

    # step 1: remove missing values
    data = data.dropna(subset=["AHI_sup", "AHI_lat"]).copy()  # remove entire rows if any of specified columns contain NaN/NA values
    print(f"valid pOSA samples: {len(data)}")


    # labeling (1 -> posa)
    data["Cartwright"] = (data["AHI_sup"] >= 2 * data["AHI_lat"]).astype(int)
    data["Overall"] = (data["AHI_total"] >= 1.5 * data["AHI_lat"]).astype(int)
    print(len(data["Cartwright"])) # print total rows
    print(len(data["Overall"]))

    # step 3: filter only patients with AHI_total >= 5
    data = data[data["AHI_total"] >= 5]
    print(f"total pOSA patients: {len(data)}")

    # count
    n_cartwright = data["Cartwright"].sum()  # sum of 1s
    n_overall = data["Overall"].sum()
    n_both = data[(data["Cartwright"] == 1) & (data["Overall"] == 1)].shape[0]
    print(f"cartwright: {n_cartwright}")  
    print(f"overall: {n_overall}")
    print(f"both: {n_both}")

    save_labels(data)

    return data




def save_labels(data, output_folder="../dataset/labeling_posa"):
    os.makedirs(output_folder, exist_ok=True)

    # save the full dataset with both labels
    output_file = os.path.join(output_folder, "posa.xlsx")
    data.to_excel(output_file, index=False)

    # optionally, save separate files for each criteria
    cartwright_only = data[data["Cartwright"] == 1]
    overall_only = data[data["Overall"] == 1]
    both = data[(data["Cartwright"] == 1) & (data["Overall"] == 1)]

    cartwright_only.to_excel(os.path.join(output_folder, "posa_cartwright.xlsx"), index=False)
    overall_only.to_excel(os.path.join(output_folder, "posa_overall.xlsx"), index=False)
    both.to_excel(os.path.join(output_folder, "posa_both.xlsx"), index=False)

if __name__ == "__main__":
    run_labeling()