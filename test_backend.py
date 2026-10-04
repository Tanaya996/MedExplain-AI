import backend

text = """COMPLETE BLOOD COUNT (CBC) REPORT

Hemoglobin (HGB)        15.2  g/dL   13.8 - 17.2
Hematocrit (HCT)        45.5  %      40.7 - 50.3
Platelet Count (PLT)    250   x10^3/uL 150 - 450
Mean Corpuscular Volume (MCV) 88.5 fL  80.0 - 100.0
Mean Corpuscular MCH Concentration (MCHC) 33.4 g/dL 32.0 - 36.0
Mean Corpuscular Hemoglobin (MCH) 29.5 pg 27.0 - 33.0"""

print("Running process_cbc_report...")
results_df, final_report = backend.process_cbc_report(text, "TEST_001")
print("Done!")
