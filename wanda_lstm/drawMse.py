import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Open and read the file
with open("mse_drop03.txt", "r") as f:
    mse_data = f.readlines()

# Step 2: Initialize an empty list to save MSE and Validation MSE
parsed_data = []

# Step 3: Parse each line to extract MSE and Validation MSE
for line in mse_data:
    if "Epoch" in line and "MSE =" in line:
        parts = line.split("MSE =")
        epoch = int(parts[0].split()[1][:-1])
        mse = float(parts[1].split(",")[0].strip())

        # 檢查並提取 Validation MSE
        if "Validation" in parts[1]:
            val_mse = float(parts[2].strip())
        else:
            val_mse = None

        print(
            f"Epoch: {epoch}, MSE: {mse}, Validation MSE: {val_mse}"
        )  # 打印每一行的結果

        parsed_data.append((epoch, mse, val_mse))
# Step 4: Convert data to DataFrame and ignore rows with missing Validation MSE
mse_df = pd.DataFrame(parsed_data, columns=["Epoch", "MSE", "Validation MSE"])

# Step 5: Plot MSE and Validation MSE curves
plt.figure(figsize=(10, 6))
plt.plot(mse_df["Epoch"], mse_df["MSE"], label="Training MSE", color="blue")
plt.plot(
    mse_df["Epoch"], mse_df["Validation MSE"], label="Validation MSE", color="orange"
)

# Step 6: Customize the plot
plt.xlabel("Epoch")
plt.ylabel("MSE")
plt.title("Training and Validation MSE per Epoch, Dropout = 0.3, Timestep = 24")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Step 7: Show the plot
plt.show()
