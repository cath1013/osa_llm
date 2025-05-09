import pandas as pd
import os

def label_posa(data):
    """
    pOSA labeling: Cartwright, Overall/NonSupine
    """

    data = data.copy()

    # Step 1: Remove missing (invalid sample labels)
    before_drop = len(data)
    data = data.dropna(subset=["AHI_sup", "AHI_lat"])
    after_drop = len(data)
    print(f"invalid data sample removed (pOSA): {before_drop - after_drop} patients (remaining: {after_drop})")

    # Step 2: Labeling
    data["pOSA_Cartwright"] = (data["AHI_sup"] >= 2 * data["AHI_lat"]).astype(int)
    data["pOSA_OverallNonSupine"] = (data["AHI_total"] >= 1.5 * data["AHI_lat"]).astype(int)

    # Step 3: Remove normal patients (AHI_total < 5)
    before_filter = len(data)
    data = data[data["AHI_total"] >= 5]
    after_filter = len(data)
    print(f"normal patients removed (pOSA): {before_filter - after_filter} patients (remaining: {after_filter})")

    return data

def label_remosa(data):
    """
    REM-OSA labeling: 13번, 15번, isolated rem osa
    """

    data = data.copy()

    # Step 1: Remove missing (invalid sample labels)
    before_drop = len(data)
    data = data.dropna(subset=["AHI_REM", "AHI_NREM", "REM_sup_min", "REM_lat_min"])
    after_drop = len(data)
    print(f"invalid data sample removed (REMOSA): {before_drop - after_drop} patients (remaining: {after_drop})")

    # Step 2: Labeling
    remosa_13 = data[
        (data["AHI_total"] >= 5) &
        (data["AHI_REM"] >= 2 * data["AHI_NREM"]) &
        ((data["REM_sup_min"] + data["REM_lat_min"]) >= 10) &
        (data["AHI_NREM"] < 15)
    ].copy()
    remosa_13["REMOSA_13"] = 1

    remosa_15 = data[
        (data["AHI_total"] >= 5) &
        (data["AHI_REM"] >= 2 * data["AHI_NREM"])
    ].copy()
    remosa_15["REMOSA_15"] = 1

    isolated_remosa = data[
        (data["AHI_REM"] >= 2 * data["AHI_NREM"]) &
        ((data["REM_sup_min"] + data["REM_lat_min"]) >= 10) &
        (data["AHI_NREM"] < 15)
    ].copy()
    isolated_remosa["Isolated_REMOSA"] = 1

    return remosa_13, remosa_15, isolated_remosa

def save_labels(posa_data, remosa_13, remosa_15, isolated_remosa, output_folder="../dataset/labeling_output"):
    os.makedirs(output_folder, exist_ok=True)

    posa_data.to_csv(os.path.join(output_folder, "posa_labeled.csv"), index=False)
    remosa_13.to_csv(os.path.join(output_folder, "remosa_13.csv"), index=False)
    remosa_15.to_csv(os.path.join(output_folder, "remosa_15.csv"), index=False)
    isolated_remosa.to_csv(os.path.join(output_folder, "remosa_isolated.csv"), index=False)

    print(f"\n labeling files saved at: {output_folder}")
    print(f"- pOSA file: posa_labeled.csv")
    print(f"- REMOSA files: remosa_13.csv, remosa_15.csv, remosa_isolated.csv")

def run_labeling():
    file_path = os.path.join("..", "dataset", "eumc_cleaned_data.csv")
    data = pd.read_csv(file_path)

    numeric_columns = ["AHI_total", "AHI_sup", "AHI_lat", "AHI_REM", "AHI_NREM", "REM_sup_min", "REM_lat_min"]
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    print(f"\n initial dataset size: {len(data)} patients")

    # pOSA labeling
    posa_data = label_posa(data.copy())

    # REMOSA labeling
    remosa_13, remosa_15, isolated_remosa = label_remosa(data.copy())

    # Labeling results
    n_p_cartwright = posa_data["pOSA_Cartwright"].sum()
    n_p_overall = posa_data["pOSA_OverallNonSupine"].sum()

    n_remosa_13 = len(remosa_13)
    n_remosa_15 = len(remosa_15)
    n_isolated_remosa = len(isolated_remosa)

    print("\n final Labeling Results:")
    print(f"- pOSA Cartwright: {n_p_cartwright} / {len(posa_data)}")
    print(f"- pOSA Overall/NonSupine: {n_p_overall} / {len(posa_data)}")
    print(f"- REMOSA 13번: {n_remosa_13} patients")
    print(f"- REMOSA 15번: {n_remosa_15} patients")
    print(f"- Isolated REMOSA: {n_isolated_remosa} patients")

    save_labels(posa_data, remosa_13, remosa_15, isolated_remosa)

    print("\n all labeling completed.\n")

if __name__ == "__main__":
    run_labeling()
