Patient age range: 20, 45
Six symptoms to be commented out: Headache, Rash, Fever, Eye Pain, Weakness/Fatigue, Myalgia
Fig 1 data is more relavent to our needs as opposed to fig 6 (more relevant for 2024)  
Patients were given 3.25 * 10^3 PFU of 45AZ5 DENV-1 infection strain (at end of paper/methods) in early paper it says 
patients given 0.5 mL of 6.5*10^4 PFU/mL suspension. Check which is correct and how to annotate
treatments: acetaminophen, oral fluids, antinausea medication (not all received tx) 
RNAemia and viremia measured by RT-qPCR and Vero cell plaque assay respectively
waickman2022_s1 has lots of details: patient ID numbers, lab values, hospitalizations, etc

xlsx data info: "BLOD" = below limit of detection 
Fig 1A = DENV-1 RNA content in serum assessed by qRT-PCR ; participants are 201-209 

"""
Waickman et al. 2022 (DOI: 10.1126/scitranslmed.abo5019)
====================================================================
Study summary:
---------------
This dengue human infection model (DHIM) study evaluated the safety and
virologic/immunologic kinetics following challenge of flavivirus-naive
adults with Dengue virus serotype-1 (DENV-1) strain 45AZ5.
Nine volunteers received a single subcutaneous inoculation.

Dataset corresponds to Fig. 1 (viremia and RNAemia kinetics following
DENV-1 challenge). 
• Figure 1a: DENV-1 RNAemia (RT-qPCR)
• Figure 1b: DENV-1 Viremia (Vero plaque assay)
• Figure 1c: NS1 antigenemia (ELISA)

Excluded: Figures 2-6. Immunological and inflammatory response datasets
(IgM/IgG/IgA) ELISA, ELISPOT, cytokine panels, correlation analyses)
These represent host immune or inflammatory responses, not pathogen load.

Temporal variable:
-------------------
• TimeDays = days post-inoculation.

Data source:
------------
Raw dataset: Supplementary Data S1 (Excel file “waickman2022_s1.xlsx”),
available with Waickman et al. 2022 Sci Transl Med.

FIX THIS!!!!!!!!!!!!!!!
• Symptoms (headache, rash, fever, eye pain, fatigue, myalgia) reported
  but not time-resolved; commented out below.
• Treatments: acetaminophen, oral fluids, antinausea medication.
• Inoculum: 3.25 × 10³ PFU of 45AZ5
"""

import os, sys
import pandas as pd

# Import schema utilities
THIS_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from schema import enforce_schema, coerce_types


def load_and_format(base_dir=None):
    """Load DENV-1 DHIM viral kinetics dataset (Fig. 1)."""
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    xlsx_path = os.path.join(base_dir, "data", "waickman2022_s1.xlsx")
    df_raw = pd.read_excel(xlsx_path)

    # Drop empty rows, reshape long
    df_raw = df_raw.dropna(how="all")
    df_raw.columns = df_raw.columns.map(str)
    df = df_raw.melt(id_vars="Day", var_name="IndivID", value_name="PathogenLoad")
    df = df.dropna(subset=["PathogenLoad"])
    df["IndivID"] = df["IndivID"].astype(int)
    df["TimeDays"] = df["Day"]
    df = df.drop(columns=["Day"])

    # Replace baseline / non-detectable values (≤1 log₁₀ GE/mL equivalent)
    df.loc[df["PathogenLoad"] <= 1.0, "PathogenLoad"] = pd.NA

    # Core metadata
    df["StudyID"] = "waickman2022"
    df["Pathogen"] = "Dengue"
    df["IndSpecies"] = "human"
    # df["Symptoms1"] = "R51"     # Headache
    # df["Symptoms2"] = "R21"     # Rash
    # df["Symptoms3"] = "R50.9"   # Fever
    # df["Symptoms4"] = "H57.1"   # Eye pain
    df["Treatment1"] = "Acetaminophen"
    df["Treatment2"] = "Oral fluids"
    df["Treatment3"] = "Antinausea medication"
    df["SampleSource"] = "serum"
    df["SampleMethod"] = "blood draw (serum)"
    df["AgeRng1"] = 20
    df["AgeRng2"] = 45
    df["Subtype"] = "DENV-1 45AZ5"
    df["PlatformType"] = "RT-qPCR"
    df["DOI"] = "10.1126/scitranslmed.abo5019"
    df["Units"] = "PFU/ml" #check this 
    df["Targets"] = "DENV-1 genome (RNA)"
    df["PlatformTech"] = "RT-qPCR and Vero cell plaque assay"

    # Hospitalization (from Supplementary Table S1)
    hosp_map = {1: "N", 2: "N", 3: "Y", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "Y"}
    df["Hospitalized"] = df["IndivID"].map(hosp_map)

    df = enforce_schema(df)
    df = coerce_types(df)
    return df


if __name__ == "__main__":
    df = load_and_format()
    print(df.head(10))
