# Corrected data: GPT-4 (32K) is still in 2023
import matplotlib.pyplot as plt
# Updated data for the plot
models_corrected = ['GPT-1', 'GPT-2', 'GPT-3', 'GPT-3.5', 'GPT-4 (early 2023)', 'GPT-4 (mid 2023)', 'GPT-4 (late 2023)', 'GPT-4-Turbo', 'Claude 3', 'Gemini 1.5 Pro']
years_corrected = [2018, 2019, 2020, 2022, 2023, 2023, 2023, 2023, 2024, 2024]
context_lengths_corrected = [512, 1024, 2048, 4096, 8192, 16384, 32768, 128000, 200000, 1000000]

# Create the updated bar chart
plt.figure(figsize=(12, 7))
bars_corrected = plt.bar(models_corrected, context_lengths_corrected, color='skyblue')

# Add labels and title
plt.xlabel('Models')
plt.ylabel('Context Size (Tokens)')
plt.title('Progress of Large Language Model Context Sizes')

# Adjust y-axis to better display smaller values
plt.yscale('log')
plt.yticks([500, 1000, 2000, 4000, 8000, 16000, 32000, 128000, 200000, 1000000],
           ['512', '1K', '2K', '4K', '8K', '16K', '32K', '128K', '200K', '1M'])

# Annotate bars with corrected release years
for bar, year in zip(bars_corrected, years_corrected):
    plt.text(bar.get_x() + bar.get_width() / 2 - 0.1, 
             bar.get_height(), 
             str(year), 
             ha='center', 
             va='bottom')

# Show the updated plot
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()