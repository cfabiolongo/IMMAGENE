import pandas as pd
from tqdm import tqdm

from ollama_inference import ask_ollama_stream

# home:
# llama3:8b-instruct-q8_0, qwen2.5:14b-instruct-q6_K

# work:
# llama3.3:70b-instruct-fp16, qwen2.5:14b-instruct-q8_0

text_model = "llama3:8b-instruct-q8_0"

# Prompt predefiniti per ogni tipo
system_prompts = {
    "beliefs": """Extract only beliefs (without other text) separated by semicolon, and single-word (possible other words as additional belief arguments), related to an actor from the text of a scene beliefs related to verb can have two arguments. The belief ACTOR(X) must be present, where X is the main subject of the scene. For example: The car runs on the highway —→ ACTOR(CAR),  RUN(CAR, HIGHWAY). Connect multi-words concept with underscore.""",
    "goal": """You are a virtual assistant. Formulate briefly a single goal to carry out for the described scene. No additional text.""",
    "action": """You are a virtual assistant. Formulate very briefly the most appropriate action to achieve the Goal, for the described scene, without additional text or explanation. No other text is admitted."""
}

temp = 0.8

results = []

# Carica il file Excel
df = pd.read_excel("inferences/image_descriptions_t08_34b.xlsx")
df = df.head(5)


# Filtra le descrizioni non nulle
descriptions = df["description"].fillna("empty").tolist()

# Inizializza una lista per salvare le risposte
beliefs = []
goals = []
actions = []

# description inference
for prompt in tqdm(descriptions, desc="Inferenza descrizione immagini"):
    print(f"\nDescription:\n {prompt}\n")

    # Beliefs
    print(f"\nBeliefs:")
    beliefs_outcome = ask_ollama_stream(prompt, system_prompts["beliefs"], temp, text_model)
    beliefs.append(beliefs_outcome)

    # Goals
    print(f"\nGoal:")
    goal_outcome = ask_ollama_stream(prompt, system_prompts["goal"], temp, text_model)
    goals.append(goal_outcome)

    # Actions
    action_with_goal = system_prompts["action"]+" Goal: "+ goal_outcome
    print(f"\nAction:")
    action_outcome = ask_ollama_stream(prompt,  action_with_goal, temp, text_model)
    actions.append(action_outcome)

# Aggiunge le risposte a una nuova colonna
df['beliefs'] = beliefs
df['goals'] = goals
df['actions'] = actions

# Salva in un nuovo file Excel
df.to_excel("inferences/image_descriptions_t08_34b_plus_actions.xlsx", index=False)
print("\n✅ goals+actions creati con successo.")