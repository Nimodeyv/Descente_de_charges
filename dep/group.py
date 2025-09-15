
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from dep.fonctions import split_premier, split_deuxieme
from dep.config import * # workbook, config, data


# OBJET Group:  
# - Attributes:
#     - groupe_id : int
#     - liste_cas : list
#     - df_coordonnees : pd.DataFrame
#     - df_ddc_individuelle : pd.DataFrame
#     - df_ddc_individuelle_points : pd.DataFrame
#     - df_ddc_combinee : pd.DataFrame
#     - df_ddc_combinee_points : pd.DataFrame
# - Methods:  
#     - load_coordonnees() 
#     - load_ddc_individuelle()
#     - load_ddc_combinee()
#     - merge_points_charges()
#     - plot_graphes_reperage_points()
#     - calc_scale_factor()
#     - sort_df()


###############################################################################################
# Création de la classe Group à partir du numéro de groupe

class Group():
    def __init__(self, Groupe_id):
        self.groupe_id = Groupe_id

    ###############################################################
    # Méthode de chargement des données de coordonnées des points
    
    def load_coordonnees(self):
        df = pd.read_csv(f'./input_data/Groupe {self.groupe_id}_Coordonées Points.csv', sep=';', header=2)  
        # Remove first line which contains the unit
        df = df.drop(0)
        df_coord_0 = df[['Point', 'Nom point', 'X', 'Y', 'Z']]
        df_coord_1 = df[['Point.1', 'Nom point.1', 'X.1', 'Y.1', 'Z.1']]
        # Rename columns of df_coord_1
        df_coord_1.columns = ['Point', 'Nom point', 'X', 'Y', 'Z']
        # Remove row if 'Nom point.1' is '-'  
        df_coord_1= df_coord_1[df_coord_1['Z'] != '-'] # On élimine les points qui n'ont pas de valeurs de Z
        df_coord = pd.concat([df_coord_0, df_coord_1], axis=0)
        
        # convert all values from df_coord to integer
        df_coord['X'] = df_coord['X'].apply(lambda x: int(float(x)))
        df_coord['Y'] = df_coord['Y'].apply(lambda x: int(float(x)))
        df_coord['Z'] = df_coord['Z'].apply(lambda x: int(float(x)))
        
        # Reset index
        df_coord.reset_index(drop=True, inplace=True)
        
        # From df_coord, Split each row of column 'Nom point' to get axe_lettre and axe_chiffre
        df_coord['axe_lettre'] = df_coord.apply(lambda x: split_premier(x['Nom point'], '_'), axis=1)
        df_coord['axe_chiffre'] = df_coord.apply(lambda x: split_deuxieme(x['Nom point'], '_'), axis=1) 

        # If colum 'Nom point' contains '-', then replace colum 'Nom point' by the values of column 'Point
        df_coord['Nom point'] = df_coord.apply(lambda x: x['Point'] if '-' in x['Nom point'] else x['Nom point'], axis=1)
        

        self.df_coordonnees = df_coord


    ###############################################################
    # Méthode de chargement des données de DDC individuelle

    def load_ddc_individuelle(self):
        df = pd.read_csv(f'./input_data/Groupe {self.groupe_id}_DDC individuelle.csv', sep=';', header=2)
        # Remove first line which contains the unit
        df = df.drop(0)
        # Remove row if column Point contains "Total
        df = df[df['Point'] != 'Total']
        df['RFx'] = df['RFx'].apply(lambda x: int(float(x)))
        df['RFy'] = df['RFy'].apply(lambda x: int(float(x)))
        df['RFz'] = df['RFz'].apply(lambda x: int(float(x)))
        df['RFx_kN'] = df['RFx']/100
        df['RFy_kN'] = df['RFy']/100
        df['RFz_kN'] = df['RFz']/100
        # Replace all values in column RFx_kN by "" if absolute value of RFz_kN is less than data['tableau_charges']['axe_RFx']['valeur_mini_affichage_kN']
        df['Iteration_#'] = df.apply(lambda x: int(split_premier(x['Cas'],'-')), axis=1)
        df['Type_chargement'] = df.apply(lambda x: split_deuxieme(x['Cas'], '-'), axis=1)
        # If colum 'Nom point' contains '-', then replace colum 'Nom point' by the values of column 'Point
        df['Nom point'] = df.apply(lambda x: x['Point'] if '-' in x['Nom point'] else x['Nom point'], axis=1)
        # Reset index
        df.reset_index(drop=True, inplace=True)
        
        self.df_ddc_individuelle = df


    ###############################################################
    # Méthode de chargement des données de DDC combinée

    def load_ddc_combinee(self):
        with open(f'./input_data/Groupe {self.groupe_id}_DDC combinée.csv', 'r') as f:
            lines = f.readlines()
        # print(lines)
        # Process the lines manually, splitting when needed, e.g., by detecting headers:
        nom_tables = []
        tables = []
        current_table = []
        for line in lines:
            if ('Enveloppe : Réactions aux appuis' in line or
                'Groupe : Points hors groupes' in line):
                pass
            elif (';;;;;;;;;;;;;\n' in line) or (';;;;;;;;;;;;;;;;;;;;\n' in line):
                if line.split(';')[0]:
                    nom_tables.append(line.split(';')[0].replace('\ufeff', ''))                
            elif 'Point;Nom point;RFxmin;Cas;RFxmax;Cas;RFymin;Cas;RFymax;Cas;RFzmin;Cas;RFzmax;Cas;;;;;;;\n' in line:
                if current_table:
                    tables.append(pd.DataFrame(current_table))  # Convert collected rows to DataFrame
                current_table = []  # Start a new table
                current_table.append(line.strip().split(';')) 
            else:
                current_table.append(line.strip().split(';'))  # Append row to current table

        # Append the last table
        if current_table:
            tables.append(pd.DataFrame(current_table))

        df = pd.DataFrame() 
        for i, t in enumerate(tables):
            t = t.iloc[:, :14]
            t.columns = t.iloc[0]
            # Remove first two rows of each t
            t = t.drop([0,1], axis=0)
            t.columns = ['Point', 'Nom point', 'RFxmin', 'Cas_RFxmin', 'RFxmax', 'Cas_RFxmax', 'RFymin', 'Cas_RFymin', 'RFymax', 'Cas_RFymax', 'RFzmin', 'Cas_RFzmin', 'RFzmax', 'Cas_RFzmax']
            t['Designation'] = nom_tables[i]
            df = pd.concat([df, t], axis=0)

        df['RFxmin'] = df['RFxmin'].apply(lambda x: int(float(x)))
        df['RFxmax'] = df['RFxmax'].apply(lambda x: int(float(x)))
        df['RFymin'] = df['RFymin'].apply(lambda x: int(float(x)))
        df['RFymax'] = df['RFymax'].apply(lambda x: int(float(x)))
        df['RFzmin'] = df['RFzmin'].apply(lambda x: int(float(x)))
        df['RFzmax'] = df['RFzmax'].apply(lambda x: int(float(x)))
        df['RFxmin_kN'] = df['RFxmin']/100
        df['RFxmax_kN'] = df['RFxmax']/100
        df['RFymin_kN'] = df['RFymin']/100
        df['RFymax_kN'] = df['RFymax']/100
        df['RFzmin_kN'] = df['RFzmin']/100
        df['RFzmax_kN'] = df['RFzmax']/100

        # If colum 'Nom point' contains '-', then replace colum 'Nom point' by the values of column 'Point
        df['Nom point'] = df.apply(lambda x: x['Point'] if '-' in x['Nom point'] else x['Nom point'], axis=1)
        df.reset_index(drop=True, inplace=True)

        self.df_ddc_combinee = df
    
    #########################################################################
    # Méthode de tracé des graphes de reperage des points

    def plot_graphes_reperage_points(self, numero_cas:int, axe_min_max:tuple, size_font:int=6):
        # Graph 2D      
        # Create a 2d plot of the points X and Y
        fig, ax = plt.subplots()
        ax.scatter(self.df_coordonnees['X'], self.df_coordonnees['Y'])
        for i, txt in self.df_coordonnees.iterrows():
            ax.text(txt['X'], txt['Y'], txt['Nom point'], ha='left', va='bottom')
        # Hide the axes
        ax.set_axis_off()
        fig.savefig(f'assets/img/reperage_points_appuis_gr_{config[numero_cas]["groupe"]}.png', dpi=300, transparent=True)
        # plt.show()
        plt.close()

        # Graph 3D
        # Plot 3D plot of the df_ddc_individuelle 
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.df_coordonnees['X'], self.df_coordonnees['Y'], self.df_coordonnees['Z'], c='r', marker='o')
        #
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_zticklabels([])
        ax.set_xlim(axe_min_max[0],axe_min_max[1])
        ax.set_ylim(axe_min_max[0],axe_min_max[1])
        ax.set_zlim(axe_min_max[0],axe_min_max[1])
        ax.set_axis_off()
        for i, txt in self.df_coordonnees.iterrows():
            ax.text(txt['X'], txt['Y'],txt['Z'], txt['Nom point'], ha='left', va='bottom', size=size_font)
        #
        ax.view_init(elev=config[numero_cas]['elevation'], azim=config[numero_cas]['azimuth'])#) 
        # ax.dist = config[numero_cas]['distance']#
        ax.set_box_aspect(None, zoom=config[numero_cas]['zoom'])
        
        fig.savefig(f'assets/img/reperage_points_appuis_3D_gr_{config[numero_cas]["groupe"]}.png', dpi=300, transparent=True)
        # plt.show()
        plt.close()
    


    #########################################################################
    # Méthode de fusion des points et des charges

    def merge_points_charges(self):
        # individuelle
        self.df_ddc_individuelle_points = pd.merge(self.df_coordonnees, self.df_ddc_individuelle, on='Nom point', how='left')
        try:
            self.df_ddc_individuelle_points['axe_chiffre'] = self.df_ddc_individuelle_points['axe_chiffre'].astype(int)
        except:
            self.df_ddc_individuelle_points['axe_chiffre'] = np.nan
        self.df_ddc_individuelle_points = self.df_ddc_individuelle_points.sort_values(by=['axe_lettre', 'axe_chiffre'])
        self.df_ddc_individuelle_points.reset_index(drop=True, inplace=True)
        # combinee
        self.df_ddc_combinee_points = pd.merge(self.df_coordonnees, self.df_ddc_combinee, on='Nom point', how='left')
        try:
            self.df_ddc_combinee_points['axe_chiffre'] = self.df_ddc_combinee_points['axe_chiffre'].astype(int)
        except:
            self.df_ddc_combinee_points['axe_chiffre'] = np.nan
        self.df_ddc_combinee_points = self.df_ddc_combinee_points.sort_values(by=['axe_lettre', 'axe_chiffre', 'Nom point'])
        self.df_ddc_combinee_points.reset_index(drop=True, inplace=True)
        

    #########################################################################
    # Méthode dqui va sélectionner le cas choisit et le trier

    def sort_df(self, numero_cas:int)-> pd.DataFrame:
        print('Le Cas choisi est :', config[numero_cas])
        if config[numero_cas]['type_charge'] == 'individuelle':
            # Get the dataframe of the points of the cas numero_cas
            df = self.df_ddc_individuelle_points[self.df_ddc_individuelle_points['Cas'].isin(config[numero_cas]['composantes'])]
            df = df[['Nom point', 'RFx_kN', 'RFy_kN', 'RFz_kN']]
            # For each point "Nom point", get the sum of the values of the column 'RFx_kN' and 'RFy_kN' and 'RFz_kN'
            df_cas = df.pivot_table(index='Nom point', values=['RFx_kN', 'RFy_kN', 'RFz_kN'], aggfunc=config[numero_cas]['type_combinaison'])
        elif config[numero_cas]['type_charge'] == 'combinée':
            # Get the dataframe of the points of the cas numero_cas
            df = self.df_ddc_combinee_points[self.df_ddc_combinee_points['Designation'].isin(config[numero_cas]['composantes'])]
            df = df[['Nom point', 'RFxmin_kN', 'RFxmax_kN', 'RFymin_kN', 'RFymax_kN', 'RFzmin_kN', 'RFzmax_kN']]
            # For each point "Nom point", get the sum of the values of the column 'RFx_kN' and 'RFy_kN' and 'RFz_kN'
            df_cas = df.pivot_table(index='Nom point', values=['RFxmin_kN', 'RFxmax_kN', 'RFymin_kN', 'RFymax_kN', 'RFzmin_kN', 'RFzmax_kN'], 
                                    aggfunc=config[numero_cas]['type_combinaison'])
        df_cas.reset_index(inplace=True)
        # Merge df_cas with df_coordonnees
        df_cas = pd.merge(df_cas,self.df_coordonnees, on='Nom point', how='left')
        try:
            df_cas['axe_chiffre'] = df_cas['axe_chiffre'].astype(int)
            df_cas = df_cas.sort_values(by=['axe_lettre', 'axe_chiffre'])
        except:
            pass
        df_cas.reset_index(drop=True, inplace=True)
        
        
        return df_cas
    

    
    #########################################################################
    # Méthode de calcul du facteur d'échelle pour les graphes
    
    def calc_scale_factor(self, coef:float, cas:int)-> tuple:
        # Les longueurs sont identiques
        Lmax = coef*max((self.df_coordonnees['X'].max()-self.df_coordonnees['X'].min(), 
                            self.df_coordonnees['Y'].max(), self.df_coordonnees['Y'].min(),
                            self.df_coordonnees['Z'].max(), self.df_coordonnees['Z'].min()))
        print('Lmax', Lmax)

        if config[cas]['type_charge'] == 'individuelle':
            min_scale_factor = Lmax / self.df_ddc_individuelle_points[['RFx_kN', 'RFy_kN', 'RFz_kN']].max(axis=1).max()
            print('min_scale_factor', min_scale_factor)
            self.df_ddc_individuelle_points['RFx_kN_scaled'] = self.df_ddc_individuelle_points['RFx_kN']*min_scale_factor
            self.df_ddc_individuelle_points['RFy_kN_scaled'] = self.df_ddc_individuelle_points['RFy_kN']*min_scale_factor
            self.df_ddc_individuelle_points['RFz_kN_scaled'] = self.df_ddc_individuelle_points['RFz_kN']*min_scale_factor
            Axe_min = self.df_ddc_individuelle_points[['X', 'Y', 'Z', 'RFx_kN_scaled', 'RFy_kN_scaled', 'RFz_kN_scaled']].min(axis=1).min()
            Axe_max = self.df_ddc_individuelle_points[['X', 'Y', 'Z', 'RFx_kN_scaled', 'RFy_kN_scaled', 'RFz_kN_scaled']].max(axis=1).max()
            #
            try: # Au cas ou les valeurs sont nulles
                scale_factor_X = Lmax / self.df_ddc_individuelle_points['RFx_kN'].abs().max()
                scale_factor_Y = Lmax / self.df_ddc_individuelle_points['RFy_kN'].abs().max()
                scale_factor_Z = Lmax / self.df_ddc_individuelle_points['RFz_kN'].abs().max()
            except:
                scale_factor_X = min_scale_factor
                scale_factor_Y = min_scale_factor
                scale_factor_Z = min_scale_factor

        elif config[cas]['type_charge'] == 'combinée':
            min_scale_factor = Lmax / self.df_ddc_combinee_points[['RFxmin_kN', 'RFxmax_kN', 'RFymin_kN', 'RFymax_kN', 'RFzmin_kN', 'RFzmax_kN']].max(axis=1).max()
            print('min_scale_factor', min_scale_factor)
            self.df_ddc_combinee_points['RFxmin_kN_scaled'] = self.df_ddc_combinee_points['RFxmin_kN']*min_scale_factor
            self.df_ddc_combinee_points['RFxmax_kN_scaled'] = self.df_ddc_combinee_points['RFxmax_kN']*min_scale_factor
            self.df_ddc_combinee_points['RFymin_kN_scaled'] = self.df_ddc_combinee_points['RFymin_kN']*min_scale_factor
            self.df_ddc_combinee_points['RFymax_kN_scaled'] = self.df_ddc_combinee_points['RFymax_kN']*min_scale_factor
            self.df_ddc_combinee_points['RFzmin_kN_scaled'] = self.df_ddc_combinee_points['RFzmin_kN']*min_scale_factor
            self.df_ddc_combinee_points['RFzmax_kN_scaled'] = self.df_ddc_combinee_points['RFzmax_kN']*min_scale_factor
            Axe_min = self.df_ddc_combinee_points[['X', 'Y', 'Z', 'RFxmin_kN_scaled', 'RFxmax_kN_scaled', 'RFymin_kN_scaled', 'RFymax_kN_scaled', 'RFzmin_kN_scaled', 'RFzmax_kN_scaled']].min(axis=1).min()
            Axe_max = self.df_ddc_combinee_points[['X', 'Y', 'Z', 'RFxmin_kN_scaled', 'RFxmax_kN_scaled', 'RFymin_kN_scaled', 'RFymax_kN_scaled', 'RFzmin_kN_scaled', 'RFzmax_kN_scaled']].max(axis=1).max()
            #
            scale_factor_X = Lmax / max(self.df_ddc_combinee_points['RFxmin_kN'].abs().max(), self.df_ddc_combinee_points['RFxmax_kN'].abs().max())
            scale_factor_Y = Lmax / max(self.df_ddc_combinee_points['RFymin_kN'].abs().max(), self.df_ddc_combinee_points['RFymax_kN'].abs().max())
            scale_factor_Z = Lmax / max(self.df_ddc_combinee_points['RFzmin_kN'].abs().max(), self.df_ddc_combinee_points['RFzmax_kN'].abs().max())
        print('Axe_min', Axe_min)
        print('Axe_max', Axe_max)
        print(f'{int(scale_factor_X)=}, {int(scale_factor_Y)=}, {int(scale_factor_Z)=}')
             
        return (scale_factor_X, scale_factor_Y, scale_factor_Z), (Axe_min, Axe_max)