import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import imageio
import os


df = pd.read_csv('../data/data.csv', index_col='data', parse_dates=True, dayfirst=True,
                 usecols=['data', 'confirmados', 'confirmados_arsnorte', 'confirmados_arscentro',
                          'confirmados_arslvt', 'confirmados_arsalentejo', 'confirmados_arsalgarve',
                          'confirmados_acores', 'confirmados_madeira'])

df_weekly = df.resample('W').sum()

shapefile_path = '../data/gadm41_PRT_1.shp'
gdf = gpd.read_file(shapefile_path)

# In order to merge regions into units, we need to create a mapping between regions and units
region_mapping = {
    'confirmados_arsnorte': ['Aveiro', 'Braga', 'Bragança', 'Porto', 'Viana do Castelo', 'Vila Real'],
    'confirmados_arscentro': ['Castelo Branco', 'Coimbra', 'Guarda', 'Leiria', 'Santarém', 'Viseu'],
    'confirmados_arslvt': ['Lisboa', 'Setúbal'],
    'confirmados_arsalentejo': ['Beja', 'Évora', 'Portalegre'],
    'confirmados_arsalgarve': ['Faro'],
    'confirmados_acores': ['Azores'],
    'confirmados_madeira': ['Madeira']
}

# Create a new column 'unit' and assign a unit to each region
gdf['unit'] = None
for unit, regions in region_mapping.items():
    gdf.loc[gdf['NAME_1'].isin(regions), 'unit'] = unit

gdf_units = gdf.dissolve(by='unit', aggfunc='sum')

max_cases = df_weekly.max().max()

def generate_gif(units, gif_name):
    if not os.path.exists('maps'):
        os.makedirs('maps')

    for i, (week, data) in enumerate(df_weekly.iterrows()):
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))

        gdf_units['cases'] = gdf_units.index.map(lambda x: data[x] if x in data else 0)


        gdf_filtered = gdf_units[gdf_units.index.isin(units)]

        gdf_filtered.plot(column='cases', ax=ax, legend=True,
                          cmap='Reds',
                          norm=mcolors.LogNorm(vmin=1, vmax=max_cases + 1),
                          legend_kwds={'label': "Number of cases"})

        plt.title(f'COVID-19 Cases - Week {week.date()}')
        plt.axis('off')

        plt.savefig(f'maps/{gif_name}_{i}.png')
        plt.close()


    images = []
    for filename in sorted(os.listdir('maps')):
        if filename.startswith(gif_name) and filename.endswith('.png'):
            images.append(imageio.imread(os.path.join('maps', filename)))

    imageio.mimsave(f'{gif_name}.gif', images, duration=1)

    for filename in sorted(os.listdir('maps')):
        if filename.startswith(gif_name) and filename.endswith('.png'):
            os.remove(os.path.join('maps', filename))


generate_gif(['confirmados_arsnorte', 'confirmados_arscentro', 'confirmados_arslvt', 'confirmados_arsalentejo',
              'confirmados_arsalgarve'], 'continental_portugal')
generate_gif(['confirmados_madeira'], 'madeira')
generate_gif(['confirmados_acores'], 'azores')

print('GIFs created successfully!')

# Kolory się słabo zmieniają, zrobic coś z tym
# Dodać zmieniającą się liczbą przypadków
# dodac tytul z regionem
# skala legendy nie 10^1 itd tylko normalnie nie logarytmicznie
# wieskze te regiony
# zapetlic gify
