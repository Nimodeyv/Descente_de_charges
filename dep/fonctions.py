
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


from dep.config import * # workbook, config, data



# FONCTIONS:
# - split_premier
# - split_deuxieme
# - create_3D_plot
# - create_main_info_latex
# - insert_nb_de_cas_dans_latex
# - create_latex_table
# - create_latex_cas
# - fill_cas_in_excel
# - crop_image


###########################################################################################
# Fonction qui permet de splitter une chaine de caractères en deux en fonction d'un séparateur
def split_premier(x, sep)-> str:
    try:
        premier = x.split(sep)[0]
    except:
        premier = np.nan
    return premier

def split_deuxieme(x, sep)-> str:
    try:
        deuxieme = x.split(sep)[1]
    except:
        deuxieme = np.nan
    return deuxieme


###########################################################################################
# Fonction qui permet de créer un dataframe à partir de la liste

def create_latex_table(df_latex:pd.DataFrame, numero_cas:int)-> None:
        df= df_latex.copy()
        df['Nom point'] = df['Nom point'].apply(lambda x: x.replace('_', '\\_'))
        # Replace all columns names containing '_' by '\\_' in df
        df_latex = df.copy()
        df_latex.columns = df_latex.columns.str.replace('_', '\\_')
        if config[numero_cas]['type_charge'] == 'individuelle':
            df_latex[['Nom point','X', 'Y', 'Z', 'RFx\\_kN', 'RFy\\_kN', 'RFz\\_kN']].to_latex(f'latex_files/table_{numero_cas}.tex', 
                                                                                    index=False, header=True, bold_rows=True,
                                                                                    float_format="%.1f")
        elif config[numero_cas]['type_charge'] == 'combinée':
            df_latex[['Nom point', 'RFxmin\\_kN', 'RFxmax\\_kN', 'RFymin\\_kN', 'RFymax\\_kN', 'RFzmin\\_kN', 'RFzmax\\_kN']].to_latex(f'latex_files/table_{numero_cas}.tex', 
                                                                                    index=False, header=True, bold_rows=True,
                                                                                    float_format="%.1f")



#########################################################################
# Fonction qui permet de créer les informations principales du document latex

def create_main_info_latex()-> None:
    # Avec MISE A JOUR DU LATEX
    # Create the main_infos.tex file
    with open('latex_files/main_infos.tex', 'w') as file:
        file.write(f"""
    \\maitriseouvrage{{{data['main_infos']['maitrise_ouvrage']}}}
    \\architectes{{{data['main_infos']['architectes']}}}
    \\bureauetudescontrole{{{data['main_infos']['bureau_etudes_controle']}}}
    \\titreprojet{{{data['main_infos']['titre_projet']}}}
    \\soustitreprojet{{{data['main_infos']['soustitre_projet']}}}
    \\redacteur{{{data['main_infos']['redacteur']}}}
    \\emailredacteur{{{data['main_infos']['email_redacteur']}}}
    \\verificateur{{{data['main_infos']['verificateur']}}}
    \\emailverificateur{{{data['main_infos']['email_verificateur']}}}
    \\numeroaffaire{{{data['main_infos']['numero_affaire']}}}
    \\notehypotheses{{{data['main_infos']['note_hypotheses']}}}
    \\adresseprojet{{{data['main_infos']['adresse_projet']}}}
    \\numeroreference{{{data['main_infos']['numero_reference']}}}
    \\numerodoc{{{data['main_infos']['numero_doc']}}}
    """)



#########################################################################
# Fonction qui permet de créer les graphiques 3D des charges

def create_3D_plot(df, numero_cas:int, scale_factor:tuple, axe_min_max:tuple, size_font:int=6)-> None: 
    if config[numero_cas]['type_charge'] == 'individuelle':
        # df['RFx_kN'] = df.apply(lambda x: '' if abs(x['RFx_kN'])<config[numero_cas]['valeur_mini_affichage_RFx_kN'] else -round(x['RFx_kN']), axis=1)
        # df['RFy_kN'] = df.apply(lambda x: '' if abs(x['RFy_kN'])<config[numero_cas]['valeur_mini_affichage_RFy_kN'] else -round(x['RFy_kN']), axis=1)
        # df['RFz_kN'] = df.apply(lambda x: '' if abs(x['RFz_kN'])<config[numero_cas]['valeur_mini_affichage_RFz_kN'] else -round(x['RFz_kN']), axis=1)
        df['RFx_kN'] = df.apply(lambda x: -round(x['RFx_kN']), axis=1)
        df['RFy_kN'] = df.apply(lambda x: -round(x['RFy_kN']), axis=1)
        df['RFz_kN'] = df.apply(lambda x: -round(x['RFz_kN']), axis=1)
        for reaction in ['RFx_kN', 'RFy_kN', 'RFz_kN']:
                max = df[reaction].abs().max()
                ###############################################
                # Create figure and 3D axis
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                # Plot the 3D data
                ax.scatter(xs=df.X, ys=df.Y, zs=df.Z, 
                        marker='o', edgecolor='black',  facecolor='none', s=10, alpha=1)      
                ax.set_xlim(axe_min_max[0],axe_min_max[1])
                ax.set_ylim(axe_min_max[0],axe_min_max[1])
                ax.set_zlim(axe_min_max[0],axe_min_max[1])
                ax.set_axis_off()
                # Change the angle of vision (elevation, azimuth)
                ax.view_init(elev=config[numero_cas]['elevation'], azim=config[numero_cas]['azimuth'])#) 
                ax.set_box_aspect(None, zoom=config[numero_cas]['zoom'])
                #
                if reaction == 'RFz_kN':
                        for i, txt in df.iterrows():
                                if txt['RFz_kN'] != '':        
                                        ax.plot(xs= [txt['X'], txt['X']], 
                                                ys=[txt['Y'], txt['Y']], 
                                                zs=[txt['Z'], txt['Z']+txt['RFz_kN']*scale_factor[2]], 
                                                marker=None, color='red', linestyle='-', linewidth=1) 
                                        if abs(txt['RFz_kN']) > config[numero_cas]['pourcentage_pour_affichage']*max:
                                            ax.text(txt['X'], txt['Y'], txt['Z']+txt['RFz_kN']*scale_factor[2], 
                                                    txt['RFz_kN'], ha='center', va='top', size=size_font, color='red')
                        fig.savefig(f"assets/img/graph3D_charges_cas_{numero_cas}_RFz_kN.png", dpi=300, transparent=True)
                        # plt.show()
                        plt.close()
                elif reaction == 'RFy_kN':
                        for i, txt in df.iterrows():
                                if txt['RFy_kN'] != '':        
                                        ax.plot(xs= [txt['X'], txt['X']], 
                                                ys=[txt['Y'], txt['Y']+txt['RFy_kN']*scale_factor[1]], 
                                                zs=[txt['Z'], txt['Z']], 
                                                marker=None, color='blue', linestyle='-', linewidth=1)  
                                        if abs(txt['RFy_kN']) > config[numero_cas]['pourcentage_pour_affichage']*max:
                                            ax.text(txt['X'], txt['Y']+txt['RFy_kN']*scale_factor[1], txt['Z'], 
                                                    txt['RFy_kN'], ha='center', va='bottom', size=size_font, color='blue')
                        fig.savefig(f"assets/img/graph3D_charges_cas_{numero_cas}_RFy_kN.png", dpi=300, transparent=True)
                        # plt.show()
                        plt.close()
                elif reaction == 'RFx_kN':
                        for i, txt in df.iterrows():
                                if txt['RFx_kN'] != '':        
                                        ax.plot(xs= [txt['X'], txt['X']+txt['RFx_kN']*scale_factor[0]], 
                                                ys=[txt['Y'], txt['Y']], 
                                                zs=[txt['Z'], txt['Z']], 
                                                marker=None, color='grey', linestyle='-', linewidth=1) 
                                        if abs(txt['RFx_kN']) > config[numero_cas]['pourcentage_pour_affichage']*max:
                                            ax.text(txt['X']+txt['RFx_kN']*scale_factor[0], txt['Y'], txt['Z'], 
                                                    txt['RFx_kN'], ha='left', va='center', size=size_font, color='grey')
                        fig.savefig(f"assets/img/graph3D_charges_cas_{numero_cas}_RFx_kN.png", dpi=300, transparent=True)
                        # plt.show()
                        plt.close()
    elif config[numero_cas]['type_charge'] == 'combinée':
        # Arrondi les charges à l'entier le plus proche et change de signe pour la réaction
        df['RFxmin_kN'] = df.apply(lambda x: -round(x['RFxmin_kN']), axis=1)
        df['RFxmax_kN'] = df.apply(lambda x: -round(x['RFxmax_kN']), axis=1)
        df['RFymin_kN'] = df.apply(lambda x: -round(x['RFymin_kN']), axis=1)
        df['RFymax_kN'] = df.apply(lambda x: -round(x['RFymax_kN']), axis=1)
        df['RFzmin_kN'] = df.apply(lambda x: -round(x['RFzmin_kN']), axis=1)
        df['RFzmax_kN'] = df.apply(lambda x: -round(x['RFzmax_kN']), axis=1)
        # Replace in column name 'min' by 'max' and vice versa
        df.columns = df.columns.str.replace('min', 'INTER')
        df.columns = df.columns.str.replace('max', 'min')
        df.columns = df.columns.str.replace('INTER', 'max')
        for reaction in ['RFxmin_kN', 'RFxmax_kN', 'RFymin_kN', 'RFymax_kN', 'RFzmin_kN', 'RFzmax_kN']:
                max = df[reaction].abs().max()
                ###############################################
                # Create figure and 3D axis
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                # Plot the 3D data
                ax.scatter(xs=df.X, ys=df.Y, zs=df.Z, 
                        marker='o', edgecolor='black',  facecolor='none', s=10, alpha=1)      
                ax.set_xlim(axe_min_max[0],axe_min_max[1])
                ax.set_ylim(axe_min_max[0],axe_min_max[1])
                ax.set_zlim(axe_min_max[0],axe_min_max[1])
                ax.set_axis_off()
                # Change the angle of vision (elevation, azimuth)
                ax.view_init(elev=config[numero_cas]['elevation'], azim=config[numero_cas]['azimuth'])
                ax.set_box_aspect(None, zoom=config[numero_cas]['zoom'])
                #
                if reaction in ['RFzmin_kN', 'RFzmax_kN']:
                    for i, txt in df.iterrows():
                            if txt['RFzmin_kN'] != '':        
                                    ax.plot(xs= [txt['X'], txt['X']], 
                                            ys=[txt['Y'], txt['Y']], 
                                            zs=[txt['Z'], txt['Z']+txt['RFzmin_kN']*scale_factor[2]], 
                                            marker=None, color='red', linestyle='-', linewidth=1) 
                                    if abs(txt['RFzmin_kN']) > config[numero_cas]['pourcentage_pour_affichage']*max: 
                                        ax.text(txt['X'], txt['Y'], txt['Z']+txt['RFzmin_kN']*scale_factor[2], 
                                                txt['RFzmin_kN'], ha='center', va='top', size=size_font, color='red')
                            if txt['RFzmax_kN'] != '':        
                                    ax.plot(xs= [txt['X'], txt['X']], 
                                            ys=[txt['Y'], txt['Y']], 
                                            zs=[txt['Z'], txt['Z']+txt['RFzmax_kN']*scale_factor[2]], 
                                            marker=None, color='red', linestyle='-', linewidth=1)  
                                    if abs(txt['RFzmax_kN']) > config[numero_cas]['pourcentage_pour_affichage']*max:
                                        ax.text(txt['X'], txt['Y'], txt['Z']+txt['RFzmax_kN']*scale_factor[2], 
                                                txt['RFzmax_kN'], ha='center', va='top', size=size_font, color='red')
                    fig.savefig(f"assets/img/graph3D_charges_cas_{numero_cas}_RFz_kN.png", dpi=300, transparent=True)
                    # plt.show()
                    plt.close()
                elif reaction in ['RFymin_kN', 'RFymax_kN']:
                    for i, txt in df.iterrows():
                        if txt['RFymin_kN'] != '':        
                                ax.plot(xs= [txt['X'], txt['X']], 
                                          ys=[txt['Y'], txt['Y']+txt['RFymin_kN']*scale_factor[1]], 
                                          zs=[txt['Z'], txt['Z']], 
                                          marker=None, color='blue', linestyle='-', linewidth=1) 
                                if abs(txt['RFymin_kN']) > config[numero_cas]['pourcentage_pour_affichage']*max: 
                                    ax.text(txt['X'], txt['Y']+txt['RFymin_kN']*scale_factor[1], txt['Z'], 
                                            txt['RFymin_kN'], ha='center', va='bottom', size=size_font, color='blue')
                        if txt['RFymax_kN'] != '':
                                ax.plot(xs= [txt['X'], txt['X']], 
                                            ys=[txt['Y'], txt['Y']+txt['RFymax_kN']*scale_factor[1]], 
                                            zs=[txt['Z'], txt['Z']], 
                                            marker=None, color='blue', linestyle='-', linewidth=1)  
                                if abs(txt['RFymax_kN']) > config[numero_cas]['pourcentage_pour_affichage']*max:
                                    ax.text(txt['X'], txt['Y']+txt['RFymax_kN']*scale_factor[1], txt['Z'], 
                                                txt['RFymax_kN'], ha='center', va='bottom', size=size_font, color='blue')
                    fig.savefig(f"assets/img/graph3D_charges_cas_{numero_cas}_RFy_kN.png", dpi=300, transparent=True)
                    # plt.show()
                    plt.close()
                elif reaction in ['RFxmin_kN', 'RFxmax_kN']:
                    for i, txt in df.iterrows():
                        if txt['RFxmin_kN'] != '':        
                                ax.plot(xs= [txt['X'], txt['X']+txt['RFxmin_kN']*scale_factor[0]], 
                                          ys=[txt['Y'], txt['Y']], 
                                          zs=[txt['Z'], txt['Z']], 
                                          marker=None, color='grey', linestyle='-', linewidth=1)  
                                if abs(txt['RFxmin_kN']) > config[numero_cas]['pourcentage_pour_affichage']*max:
                                    ax.text(txt['X']+txt['RFxmin_kN']*scale_factor[0], txt['Y'], txt['Z'], 
                                            txt['RFxmin_kN'], ha='left', va='center', size=size_font, color='grey')
                        if txt['RFxmax_kN'] != '':
                                ax.plot(xs= [txt['X'], txt['X']+txt['RFxmax_kN']*scale_factor[0]], 
                                          ys=[txt['Y'], txt['Y']], 
                                          zs=[txt['Z'], txt['Z']], 
                                          marker=None, color='grey', linestyle='-', linewidth=1)
                                if abs(txt['RFxmax_kN']) > config[numero_cas]['pourcentage_pour_affichage']*max:  
                                    ax.text(txt['X']+txt['RFxmax_kN']*scale_factor[0], txt['Y'], txt['Z'], 
                                            txt['RFxmax_kN'], ha='left', va='center', size=size_font, color='grey')
                    fig.savefig(f"assets/img/graph3D_charges_cas_{numero_cas}_RFx_kN.png", dpi=300, transparent=True)
                    # plt.show()
                    plt.close()
                            
                                
#########################################################################
# Fonction qui permet de créer un fichier latex .tex pour chaque cas                   
        
def create_latex_cas(numero_cas:int)-> None:
    # latex-workshop.latex.autoBuild.run set to never in order to not compile always the latex file
    nom = config[numero_cas]['nom']
    table  = f'table_{numero_cas}.tex'
    with open(f'latex_files/cas_{numero_cas}.tex', 'w') as file:
        file.write(f"""
    \\section{{{nom}}}
    \\import{{latex_files/}}{{{table}}}

    \\begin{{figure}}[H] % Pour insérer une figure
        \\centering % Pour centrer l'image
        \\includegraphics[width=\\textwidth]{{assets/img/graph3D_charges_cas_{numero_cas}_RFx_kN_cropped.png}} % Pour insérer l'image
        \\caption{{{nom}\_RFx\_kN}} % Légende de l'image
    \\end{{figure}}

    \\begin{{figure}}[H] % Pour insérer une figure
        \\centering % Pour centrer l'image
        \\includegraphics[width=\\textwidth]{{assets/img/graph3D_charges_cas_{numero_cas}_RFy_kN_cropped.png}} % Pour insérer l'image
        \\caption{{{nom}\_RFy\_kN}} % Légende de l'image
    \\end{{figure}}

    \\begin{{figure}}[H] % Pour insérer une figure
        \\centering % Pour centrer l'image
        \\includegraphics[width=\\textwidth]{{assets/img/graph3D_charges_cas_{numero_cas}_RFz_kN_cropped.png}} % Pour insérer l'image
        \\caption{{{nom}\_RFz\_kN}} % Légende de l'image
    \\end{{figure}}

    """)
    

#########################################################################
# Fonction qui permet d'insérer un groupe de cas dans un fichier latex .tex


def insert_nb_de_cas_dans_latex(groupe:list)-> None:
    with open(f'latex_files/insert_nb_cas.tex', 'w') as file:
        for g in groupe:
            file.write(f"""
    %%%%%%%%%%%%%%%%%%%%%%                      
    \\begin{{figure}}[H] % Pour insérer une figure
        \\centering % Pour centrer l'image
        \\includegraphics[width=0.7\\textwidth]{{reperage_points_appuis_gr_{g}.png}} % Pour insérer l'image
        \\caption{{Repèrage des points d'appui 2D - Groupe {g}}} % Légende de l'image
    \\end{{figure}}

    \\begin{{figure}}[H] % Pour insérer une figure
        \\centering % Pour centrer l'image
        \\includegraphics[width=\\textwidth]{{assets/img/reperage_points_appuis_3D_gr_{g}_cropped.png}} % Pour insérer l'image
        \\caption{{Repèrage des points d'appui 3D - Groupe {g}}} % Légende de l'image
   \\end{{figure}}
    """)
            
        file.write(f"""
    \\newpage
    \\chapter{{DESCENTE DE CHARGES}}
    """)
        for i in config.keys():
            file.write(f"""
    %%%%%%%%%%%%%%%%%%%%%%

    \\import{{latex_files/}}{{cas_{i}.tex}}

    \\newpage
    """)

#########################################################################
# Fonction qui permet de remplir les cas dans le fichier Excel


def fill_cas_in_excel(groupe: int, numero_cas:int, sheet:xw.main.Sheet, df_temp=pd.DataFrame)-> None:
    
    df= df_temp.copy()
    # La référence de chaque cas est la premiere valeur du tableau de valeurs pour le premier Nom point
    offset_tableau = 26
    offset_cas = 57
    offset_col = {'Nom point': 0, 'RFx_kN':12, 'RFxmin_kN':10, 'RFxmax_kN':12, 
                  'RFy_kN':16, 'RFymin_kN':14, 'RFymax_kN':16,
                  'RFz_kN':20, 'RFzmin_kN':18, 'RFzmax_kN':20,
                  'X':4, 'Y':6, 'Z':8, 
                'Graphe_reperage': -1, 'Graphe_RFx_kN': 25, 'Graphe_RFy_kN': -1, 'Graphe_RFz_kN': 25,
                'titre': -2,
                'RFx_kN/ml': 12, 'RFy_kN/ml': 16, 'RFz_kN/ml': 20, 'Segments': 0}
    offset_row = {'Nom point': 0, 'RFx_kN': 0, 'RFxmin_kN':0, 'RFxmax_kN': 0,
                   'RFy_kN': 0, 'RFymin_kN':0, 'RFymax_kN': 0,
                   'RFz_kN': 0, 'RFzmin_kN':0, 'RFzmax_kN': 0,
                   'X': 0, 'Y': 0, 'Z': 0,
                    'Graphe_reperage': 27, 'Graphe_RFx_kN': 50, 'Graphe_RFy_kN': 50, 'Graphe_RFz_kN': 27,
                    'titre': -5}
    
    refr = config[numero_cas]['row_ref']
    refc = config[numero_cas]['col_ref']+(numero_cas-1)*offset_cas

    # Chargement du titre du cas 1
    sheet.range((refr+offset_row['titre']), (refc+offset_col['titre'])).value = f'{numero_cas+1}.DESCENTE DE CHARGES: {config[numero_cas]["nom"]}'

    # Chargement des données dans le tableau
    if config[numero_cas]['type_groupe'] == 'ponctuel':
        if config[numero_cas]['type_charge'] == 'individuelle':
            for col in ['Nom point', 'RFx_kN', 'RFy_kN', 'RFz_kN', 'X', 'Y', 'Z']:
                sheet.range((refr, (refc+offset_col[col]))).options(transpose=True).value = df.loc[0:23, col].values.tolist()
                sheet.range((refr, (refc+offset_tableau+offset_col[col]))).options(transpose=True).value = df.loc[24:, col].values.tolist()
        elif config[numero_cas]['type_charge'] == 'combinée':
            for col in ['Nom point', 'RFxmin_kN', 'RFxmax_kN', 'RFymin_kN', 'RFymax_kN', 'RFzmin_kN', 'RFzmax_kN', 'X', 'Y', 'Z']:
                sheet.range((refr, (refc+offset_col[col]))).options(transpose=True).value = df.loc[0:23, col].values.tolist()
                sheet.range((refr, (refc+offset_tableau+offset_col[col]))).options(transpose=True).value = df.loc[24:, col].values.tolist()
        # In excel 1 point ~ 1/72 of an inch
        width = 15*0.3937*72
        # Chargement des images dans le cas numero_cas
        image_path = r'C:\Users\nmorand\OneDrive - SIMONIN SAS\_Descente_de_charge\assets\img\reperage_points_appuis_3D_gr_'+str(groupe)+'_cropped.png'
        sheet.pictures.add(image_path, left=sheet.range(((refr+offset_row['Graphe_reperage']),(refc+offset_col['Graphe_reperage']))).left, 
                        top=sheet.range(((refr+offset_row['Graphe_reperage']),(refc+offset_col['Graphe_reperage']))).top, width=width)

        for graphe in ['Graphe_RFx_kN', 'Graphe_RFy_kN', 'Graphe_RFz_kN']:
            # Define the path to the image
            image_path = r'C:\Users\nmorand\OneDrive - SIMONIN SAS\_Descente_de_charge\assets\img\graph3D_charges_cas_'+str(numero_cas)+'_'+graphe.replace('Graphe_','')+'_cropped.png'
            # print(type(image_path))
            # print(image_path)
            # Insert the image at a specific cell
            sheet.pictures.add(image_path, left=sheet.range((refr+offset_row[graphe]),(refc+offset_col[graphe])).left, 
                            top=sheet.range((refr+offset_row[graphe]),(refc+offset_col[graphe])).top, width=width)  
    
    elif config[numero_cas]['type_groupe'] == 'lineaire':   
        for col in ['Segments', 'RFx_kN/ml', 'RFy_kN/ml', 'RFz_kN/ml']:
            sheet.range((refr, (refc+offset_col[col]))).options(transpose=True).value = df.loc[:, col].values.tolist()
    
    # # Sauvegarde du fichier Excel sous le nom TEST.xlsx
    # workbook.save(r'C:\Users\nmorand\OneDrive - SIMONIN SAS\_Descente_de_charge\TEST.xlsx')
          


#########################################################################
# Fonction qui permet de cropper les images

def crop_image(img_path:str, top:int, bottom:int, left:int, right:int, show:bool=False)-> None:
    img = Image.open(img_path)
    img_array = np.array(img)
    # Crop the image
    img_cropped = img_array[top:bottom, left:right]
    if show:
        plt.imshow(img_array)
        plt.show()
        plt.imshow(img_cropped)
        plt.show()
    # Save the cropped image
    img_cropped = Image.fromarray(img_cropped)
    img_cropped.save(img_path.replace('.png', '_cropped.png'))  