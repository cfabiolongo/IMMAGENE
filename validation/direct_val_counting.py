import pandas as pd
import re
def estrai_numeri(stringa):
    # Trova tutti i numeri (interi o decimali) e rimuove eventuali punti finali
    numero = re.findall(r'\d+', stringa)
    return numero

# Carica il file Excel
file_path = 'direct_image_descr_gemma3-27b-90b_dipa_guided.xlsx'
df = pd.read_excel(file_path)



# True Positive
# TP = len(df[(df['response'] == "TRUE") & (df['ground_truth_ft_number'] > 0)])
# # False Positive
# FP = len(df[(df['response'] == "TRUE") & (df['ground_truth_ft_number'] == 0)])
# # False Negative
# FN = len(df[(df['response'] == "FALSE") & (df['ground_truth_ft_number'] > 0)])
# # True Negative
# TN = len(df[(df['response'] == "FALSE") & (df['ground_truth_ft_number'] == 0)])

# True Positive
TP = len(df[(df['response'] == True) & (df['ground_truth_ft_number'] > 0)])
# False Positive
FP = len(df[(df['response'] == True) & (df['ground_truth_ft_number'] == 0)])
# False Negative
FN = len(df[(df['response'] == False) & (df['ground_truth_ft_number'] > 0)])
# True Negative
TN = len(df[(df['response'] == False) & (df['ground_truth_ft_number'] == 0)])

print(f"TP: {TP}, FP: {FP}, FN: {FN}, TN: {TN}")

# Metriche
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
denominator = TP + FP + FN + TN
accuracy = (TP + TN) / denominator if denominator > 0 else 0

non_allucination_rate = ((denominator / df.shape[0]) * 100)
print(f"Allucinations rate: {100-non_allucination_rate:.2f}%")


# direct LLM assessment
try:
    numeric_values = pd.to_numeric(df['ground_truth_ft_number'], errors='coerce').fillna(0)
    total_ground_truth = numeric_values.sum()
except Exception:
    total_ground_truth = 0

try:
    numeric_values = pd.to_numeric(df['extracted_features'], errors='coerce').fillna(0)
    total_extracted = numeric_values.sum()
except Exception:
    total_extracted = 0
    

# Rapporto estratti / ground truth in percentuale
extracted_to_ground_truth_ratio = ((total_extracted / total_ground_truth) * 100) if total_ground_truth > 0 else 0

# Stampa risultati
print(f"\nAccuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1_score:.3f}\n")

print(f"Totale ground_truth_ft_number: {total_ground_truth}")
print(f"Totale extracted_features: {total_extracted}")
print(f"Rapporto extracted/ground_truth: {extracted_to_ground_truth_ratio:.2f}%")