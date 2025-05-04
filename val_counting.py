import pandas as pd

# Carica il file Excel
file_path = 'meta_overall_mistral_7b-instruct-fp16.xlsx'
df = pd.read_excel(file_path)

# True Positive
TP = len(df[(df['response'] == True) & (df['ground_truth_ft_number'] > 0)])
# False Positive
FP = len(df[(df['response'] == True) & (df['ground_truth_ft_number'] == 0)])
# False Negative
FN = len(df[(df['response'] == False) & (df['ground_truth_ft_number'] > 0)])
# True Negative
TN = len(df[(df['response'] == False) & (df['ground_truth_ft_number'] == 0)])

# Metriche
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
denominator = TP + FP + FN + TN
accuracy = (TP + TN) / denominator if denominator > 0 else 0

# Stampa risultati
print(f"Accuracy: {accuracy:.3f}\n")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1_score:.3f}")
