import pandas as pd

# Carica il file Excel
file_path = 'inferences/meta_zero-shot_overall_qwen_llama.xlsx'
df = pd.read_excel(file_path)

df['ground_truth_ft_number'] = pd.to_numeric(df['ground_truth_ft_number'], errors='coerce').fillna(0)
df['extracted_features'] = pd.to_numeric(df['extracted_features'], errors='coerce').fillna(0)
df['response'] = df['response'].astype(bool)

print("\n---------- OVERALL SCORES ----------\n")

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

# Calcola gli errori assoluti
absolute_errors = (df['extracted_features'] - df['ground_truth_ft_number']).abs()

# Calcola le statistiche
mae = absolute_errors.mean()
min_error = absolute_errors.min()
max_error = absolute_errors.max()

print(f"Mean Absolute Error (MAE): {mae:.3f}")
print(f"Minimum Absolute Error: {min_error:.3f}")
print(f"Maximum Absolute Error: {max_error:.3f}")

print("\n---------- SUBSET SCORES ----------\n")


# Rimuove righe con valori mancanti
# df = df.dropna(subset=['input_file_image_name', 'matched_file_image_name'])

# Estrai la parte prima di "_diff" e aggiungi ".jpg"
df['reference_clean'] = df['reference'].apply(lambda x: x.split('_diff')[0])

# Verifica corrispondenza
df['match'] = df['reference_clean'] == df['file_input']

# Calcola accuracy
accuracy = df['match'].mean()
print(f"MATCHES percentage: {accuracy:.2%}")
if accuracy==0: exit(0)


print("\n---------- MATCH SCORES ----------\n")

# Filtra mismatch
df_match = df[df['match'] != False]

# True Positive
TP = len(df_match[(df_match['response'] == True) & (df_match['ground_truth_ft_number'] > 0)])
# False Positive
FP = len(df_match[(df_match['response'] == True) & (df_match['ground_truth_ft_number'] == 0)])
# False Negative
FN = len(df_match[(df_match['response'] == False) & (df_match['ground_truth_ft_number'] > 0)])
# True Negative
TN = len(df_match[(df_match['response'] == False) & (df_match['ground_truth_ft_number'] == 0)])

print(f"TP: {TP}, FP: {FP}, FN: {FN}, TN: {TN}")

# Metriche
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
denominator = TP + FP + FN + TN
accuracy = (TP + TN) / denominator if denominator > 0 else 0

non_allucination_rate = ((denominator / df_match.shape[0]) * 100)
print(f"Allucinations rate: {100-non_allucination_rate:.2f}%")

# Somme totali
total_ground_truth = df_match['ground_truth_ft_number'].sum()
total_extracted = df_match['extracted_features'].sum()

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

mae = (df_match['extracted_features'] - df_match['ground_truth_ft_number']).abs().mean()
print(f"Mean Absolute Error (MAE): {mae:.3f}")




print("\n---------- NON-MATCH SCORES ----------\n")

# Filtra mismatch
df_non_match = df[df['match'] == False]

# True Positive
TP = len(df_non_match[(df_non_match['response'] == True) & (df_non_match['ground_truth_ft_number'] > 0)])
# False Positive
FP = len(df_non_match[(df_non_match['response'] == True) & (df_non_match['ground_truth_ft_number'] == 0)])
# False Negative
FN = len(df_non_match[(df_non_match['response'] == False) & (df_non_match['ground_truth_ft_number'] > 0)])
# True Negative
TN = len(df_non_match[(df_non_match['response'] == False) & (df_non_match['ground_truth_ft_number'] == 0)])

print(f"TP: {TP}, FP: {FP}, FN: {FN}, TN: {TN}")

# Metriche
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
denominator = TP + FP + FN + TN
accuracy = (TP + TN) / denominator if denominator > 0 else 0

non_allucination_rate = ((denominator / df_non_match.shape[0]) * 100)
print(f"Allucinations rate: {100-non_allucination_rate:.2f}%")

# Somme totali
total_ground_truth = df_non_match['ground_truth_ft_number'].sum()
total_extracted = df_non_match['extracted_features'].sum()

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

mae = (df_non_match['extracted_features'] - df_non_match['ground_truth_ft_number']).abs().mean()
print(f"Mean Absolute Error (MAE): {mae:.3f}")