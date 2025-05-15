import pandas as pd
import numpy as np
import os

# load the dataset
file_path = os.path.join("..", "dataset", "250401_EUMC_SleepDC_CDM.xlsx")
df = pd.read_excel(file_path, sheet_name="Data", header=1)  

print(f"total number of rows before preprocessing: {len(df)}")

# step 1: keep only relevant PSG types (P, PE)
initial_count = len(df)
df = df[df["PSG_Type"].isin(["P", "PE"])]
removed_step1 = initial_count - len(df)
print(f"step 1: removed {removed_step1} rows (kept only PSG types P and PE)")
# print(df)

# step 2: remove patients with incomplete sleep questionnaires
sleep_scores = ["SSS", "PSQI_Total", "ESS_Total", "ISI_Total", "BQ_Risk"]
# print(df[sleep_scores])

# missing values are coded as 9999 -> convert to NaN
df[sleep_scores] = df[sleep_scores].replace(9999, np.nan)

# sleep questionnaire 총점 중 하나라도 결측이면 제거
before_step2 = len(df)
df = df.dropna(subset=sleep_scores)
removed_step2 = before_step2 - len(df)
print(f"step 2: removed {removed_step2} rows (removed rows with missing sleep questionnaire scores)")
print(len(df))


# save cleaned data
output_folder = os.path.join("..", "dataset")
# print(output_folder)
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(output_folder, "eumc_cleaned_data.xlsx")
df.to_excel(output_file, index=False)

print(f"final dataset size: {len(df)} rows")
print(f"preprocessing has done, saved at: {output_file}")

