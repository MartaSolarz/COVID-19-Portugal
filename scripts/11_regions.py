import matplotlib.ticker as ticker
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import imageio
import os

df = pd.read_csv('../data/regions.csv', index_col='data', parse_dates=True, dayfirst=True,
                 usecols=['data', 'confirmados', 'confirmados_arsnorte', 'confirmados_arscentro',
                          'confirmados_arslvt', 'confirmados_arsalentejo', 'confirmados_arsalgarve',
                          'confirmados_acores', 'confirmados_madeira'])

df_weekly = df.resample('W').sum()

df_weekly = df_weekly.iloc[:-1]
shapefile_path = './data/gadm41_PRT_1.shp'
gdf = gpd.read_file(shapefile_path)

region_mapping = {
    'confirmados_arsnorte': ['Aveiro', 'Braga', 'Bragança', 'Porto', 'Viana do Castelo', 'Vila Real'],
    'confirmados_arscentro': ['Castelo Branco', 'Coimbra', 'Guarda', 'Leiria', 'Santarém', 'Viseu'],
    'confirmados_arslvt': ['Lisboa', 'Setúbal'],
    'confirmados_arsalentejo': ['Beja', 'Évora', 'Portalegre'],
    'confirmados_arsalgarve': ['Faro'],
    'confirmados_acores': ['Azores'],
    'confirmados_madeira': ['Madeira']
}

gdf['unit'] = None
for unit, regions in region_mapping.items():
    gdf.loc[gdf['NAME_1'].isin(regions), 'unit'] = unit

gdf_units = gdf.dissolve(by='unit', aggfunc='sum')

def generate_gif(units, gif_name, max_cases, name):
    if not os.path.exists('maps'):
        os.makedirs('maps')

    for i, (week, data) in enumerate(df_weekly.iterrows()):
        fig, ax = plt.subplots(1, 1, figsize=(15, 15))

        gdf_units['cases'] = gdf_units.index.map(lambda x: data[x] if x in data else 0)

        gdf_filtered = gdf_units[gdf_units.index.isin(units)]

        def fmt(x, pos):
            if x >= 1e6:
                return f'{x * 1e-6:.1f}M'
            elif x >= 1e3:
                return f'{x * 1e-3:.0f}K'
            else:
                return f'{x:.0f}'

        norm = mcolors.Normalize(vmin=0, vmax=max_cases)
        sm = plt.cm.ScalarMappable(cmap='Reds', norm=norm)
        sm.set_array([])

        gdf_filtered.plot(column='cases', ax=ax, legend=False,
                          cmap='Reds',
                          edgecolor='black',
                          linewidth=0.8,
                          norm=norm)

        cbar = fig.colorbar(sm, ax=ax, orientation="vertical", fraction=0.036, pad=0.04)
        cbar.ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt))
        cbar.set_label("Number of Cases", fontsize=12)

        for x, y, label in zip(gdf_filtered.geometry.centroid.x, gdf_filtered.geometry.centroid.y,
                               gdf_filtered['cases']):
            ax.text(x, y, str(int(label)), fontsize=12, ha='center', va='center', color='black')

        plt.title(f'Total COVID-19 Cases in {name} - until {week.date()}', fontsize=18)
        plt.axis('off')

        plt.savefig(f'maps/{gif_name}_{i}.png')
        plt.close()

    images = []
    for filename in sorted(os.listdir('maps')):
        if filename.startswith(gif_name) and filename.endswith('.png'):
            images.append(imageio.imread(os.path.join('maps', filename)))

    imageio.mimsave(f'./plots/11_{gif_name}.gif', images, duration=10, loop=0)

    for filename in sorted(os.listdir('maps')):
        if filename.startswith(gif_name) and filename.endswith('.png'):
            os.remove(os.path.join('maps', filename))


generate_gif(['confirmados_arsnorte', 'confirmados_arscentro', 'confirmados_arslvt', 'confirmados_arsalentejo',
              'confirmados_arsalgarve'], 'continental_portugal', 1600000, 'Continental Portugal')
generate_gif(['confirmados_madeira'], 'madeira', 14000, 'Madeira')
generate_gif(['confirmados_acores'], 'azores', 16000, 'Azores')

print('GIFs created successfully!')
