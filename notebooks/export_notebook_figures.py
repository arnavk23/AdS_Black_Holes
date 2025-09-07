
import nbformat
import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import numpy as np

NOTEBOOK_PATH = 'ModMax_dRGT_Thermo_Visualizations.ipynb'
FIGURES_DIR = 'figures'
os.makedirs(FIGURES_DIR, exist_ok=True)

with open(NOTEBOOK_PATH) as f:
    nb = nbformat.read(f, as_version=4)

ns = {}
fig_count = 1
for cell in nb.cells:
    if cell['cell_type'] == 'code':
        try:
            code = cell['source']
            if isinstance(code, list):
                code = ''.join(code)
            # Predefine variables that may be missing in some cells
            if 'S_corr' not in ns:
                ns['S_corr'] = np.nan
            if 'T_num' not in ns:
                ns['T_num'] = np.nan
            if 'C_num' not in ns:
                ns['C_num'] = np.nan
            exec(code, ns)
            figs = [plt.figure(i) for i in plt.get_fignums()]
            for fig in figs:
                # Only save figures that have at least one axis (not empty)
                if fig.axes:
                    fig_path = os.path.join(FIGURES_DIR, f'figure_{fig_count}.png')
                    fig.savefig(fig_path)
                    fig_count += 1
                plt.close(fig)
        except Exception as e:
            print(f"Error in cell {fig_count}: {e}")

# Generate summary table as figure_4.png
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ["S", "13.38"],
    ["T", "0.046"],
    ["M", "1.384"],
    ["F", "0.769"],
    ["G", "0.902"],
    ["U", "1.384"],
    ["C_P", "13.38"],
    ["V", "33.51"]
]
table = ax.table(cellText=table_data, colLabels=["Quantity", "Value"], loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'figure_4.png'))
plt.close(fig)
print(f"Exported {fig_count} figures to {FIGURES_DIR}/ (including summary table as figure_4.png)")
