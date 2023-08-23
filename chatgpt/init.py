import pandas as pd

# csvを読み込む
df = pd.read_csv("data.csv")

# txtを初期化
with open("default.txt", "r") as f:
    default = f.read()

# with open("prompt.txt", "w") as f:
#     f.write("")

with open("prompt.txt", "w") as f:
    f.write(default + "\n" * 3)


first = 0
end = 5

df = df[first:end]

for tag in df["tag"]:
    prompt = f'The parent is "{tag}"\nThe query is "{tag}"in "Programming Languages".'
    with open("prompt.txt", "a") as f:
        f.write(prompt + "\n")
