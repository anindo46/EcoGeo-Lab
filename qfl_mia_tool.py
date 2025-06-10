import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# Function to calculate QFL and MIA
def qfl_and_mia_tool(df):
    # Ensure Q, F, L columns are present
    required_columns = ['Q', 'F', 'L']
    
    if all(col in df.columns for col in required_columns):
        # Q, F, L values from the uploaded CSV
        q = df['Q'].values
        f = df['F'].values
        l = df['L'].values
        
        # Calculate the MIA (Mineralogical Index of Alteration)
        mia = (q / (q + (f + l))) * 100
        
        # Adding the MIA as a new column
        df['MIA'] = mia
        
        # Plot QFL diagram
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # Simple triangular plot for QFL diagram
        ax.plot([0.5, 1], [0, 0.5], color='black', lw=1)  # Q axis line
        ax.plot([0, 0.5], [0.5, 0], color='black', lw=1)  # F axis line
        ax.plot([1, 0.5], [0, 1], color='black', lw=1)    # L axis line

        # Scatter plot of the points based on the Q, F, L values
        ax.scatter(q, f, c=mia, cmap='viridis', edgecolors='k', s=60)

        # Labeling the axes
        ax.set_xlabel("Q (Quartz)")
        ax.set_ylabel("F (Feldspar)")
        ax.set_title("QFL Plot")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        
        # Show the color bar for MIA values
        cbar = plt.colorbar(ax.collections[0], ax=ax)
        cbar.set_label('MIA (%)')

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        
        # Return the updated dataframe with MIA and the plot as a buffer
        return df, buf
    else:
        raise ValueError("CSV must contain columns: 'Q', 'F', and 'L'")

