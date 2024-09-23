
import pandas as pd
import numpy as np




# OBJET Cas
# - Attributes:
#   - numero_cas: int
#   - nom: str
#   - config_cas: dict
#   - df_cas: pd.DataFrame



class Cas():
    def __init__(self, nom:str, groupe:int, config_cas:dict):
        self.nom = nom
        self.groupe = groupe
        self.config_cas = config_cas


    def create_df_lineaire(self):
        Appui_lineique = list()
        for i, seg in enumerate(self.config_cas['liste_points_pour_groupe_lineaire']):
            # print(seg)
            df = self.df_cas[self.df_cas['Nom point'].isin(seg)].copy()
            # Calcul et somme de la distance entre les points
            df.loc[:,'dX'] = df.loc[:,'X'].diff()
            df.loc[:,'dY'] = df.loc[:,'Y'].diff()
            df.loc[:,'dZ'] = df.loc[:,'Z'].diff()
            # Calculate the Euclidean distance between consecutive points
            df['distance'] = np.sqrt(df['dX']**2 + df['dY']**2 + df['dZ']**2)
            # Fill NaN for the first row with 0 (since no previous point exists)
            df['distance'] = df['distance'].fillna(0)
            # display(df)
            # Total length is the sum of all distances
            total_length = df['distance'].sum()
            # print(f'Total length: {total_length}')
            app = dict()
            app['Segments'] = self.config_cas['segments_pour_groupe_lineaire'].split(';')[i]
            app['RFx_kN/ml'] = round(df['RFx_kN'].sum() / (total_length/1000),1)
            app['RFy_kN/ml'] = round(df['RFy_kN'].sum() / (total_length/1000),1)
            app['RFz_kN/ml'] = round(df['RFz_kN'].sum() / (total_length/1000),1)
            Appui_lineique.append(app)
        
        self.df_cas_lineique = pd.DataFrame(Appui_lineique)


    

            


        