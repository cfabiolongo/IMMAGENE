import pandas as pd

# Carica il file Excel
file_path = 'meta_mismatch_llama4:17b-scout.xlsx'
df = pd.read_excel(file_path)

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

# Somme totali
total_ground_truth = df['ground_truth_ft_number'].sum()
total_extracted = df['extracted_features'].sum()

# Rapporto estratti / ground truth in percentuale
extracted_to_ground_truth_ratio = ((total_extracted / total_ground_truth) * 100) if total_ground_truth > 0 else 0

# Stampa risultati
print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1_score:.3f}\n")

print(f"Totale ground_truth_ft_number: {total_ground_truth}")
print(f"Totale extracted_features: {total_extracted}")
print(f"Rapporto extracted/ground_truth: {extracted_to_ground_truth_ratio:.2f}%")