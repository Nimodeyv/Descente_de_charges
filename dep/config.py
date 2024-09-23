import xlwings as xw
import yaml


def build_segment(L: list) -> list:
    segment = []
    for seg in L.split(','):
        if '-' not in seg:
            segment.append(seg)
        else:
            lettre = seg.split('-')[0].split('_')[0]
            init = int(seg.split('-')[0].split('_')[1])
            end = int(seg.split('-')[1].split('_')[1])
            liste_pts = [lettre+'_'+str(i) for i in range(init, end+1)]
            segment += liste_pts
    return segment




#######################################################################################
# Fonction qui importe la configuration des cas de test depuis un fichier Excel
#######################################################################################

def import_config_excel(workbook: xw.Book) -> dict:
    config_sheet = workbook.sheets['config']
    last_row = config_sheet.range('B1').end('down').row
    last_col = config_sheet.range('A1').end('right').column
    nb_cas = last_col-2
    print(f'last_row={last_row}, last_col={last_col}, nb_cas={nb_cas}')
    config = {}

    for col in range(3, last_col+1):
        config[int(config_sheet.range((1,col)).value)] = {}
        for row in range(2, last_row+1):
            config[int(config_sheet.range((1,col)).value)][config_sheet.range((row,2)).value] = config_sheet.range((row,col)).value
        # On convertit les variables dans le bon format s'il y a lieu
        # Liste des composantes
        if config[int(config_sheet.range((1,col)).value)]['composantes']!=None:
            config[int(config_sheet.range((1,col)).value)]['composantes'] = config[int(config_sheet.range((1,col)).value)]['composantes'].split(';')
        # Liste des segments
        if config[int(config_sheet.range((1,col)).value)]['segments_pour_groupe_lineaire']!=None:
            liste_segments = list()
            L = config[int(config_sheet.range((1,col)).value)]['segments_pour_groupe_lineaire'].split(';')
            for segment in L:
                liste_segments.append(build_segment(segment))
            config[int(config_sheet.range((1,col)).value)]['liste_points_pour_groupe_lineaire'] = liste_segments
        # Groupe integer
        if config[int(config_sheet.range((1,col)).value)]['groupe']!=None:
            config[int(config_sheet.range((1,col)).value)]['groupe'] = int(config[int(config_sheet.range((1,col)).value)]['groupe'])
        # Colonne de référence integer
        if config[int(config_sheet.range((1,col)).value)]['col_ref']!=None:
            config[int(config_sheet.range((1,col)).value)]['col_ref'] = int(config[int(config_sheet.range((1,col)).value)]['col_ref'])
        # Ligne de référence integer
        if config[int(config_sheet.range((1,col)).value)]['row_ref']!=None:
            config[int(config_sheet.range((1,col)).value)]['row_ref'] = int(config[int(config_sheet.range((1,col)).value)]['row_ref'])   
    print(f'{config}')

    return config

#######################################################################################
# Fonction qui importe la configuration des cas de test depuis un fichier YAML
#######################################################################################

def import_data_yaml(yaml_path:str)->dict:
    with open(yaml_path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    print(f'{data}')
    return data


#######################################################################################
# Open the existing workbook
print('Chargement du fichier Excel TEMPLATE_DDC.xlsx') 
workbook = xw.Book('TEMPLATE_DDC.xlsx')
print('-----------------------------------------------')


# Import the configuration from the Excel file
print('Chargement de la configuration des cas de test à partir du fichier Excel')
config = import_config_excel(workbook=workbook)
print('-----------------------------------------------')

# Import the configuration from the YAML file
print('Chargement de la configuration des cas de test à partir du fichier YAML')
data = import_data_yaml(yaml_path='input_data/infos_générales.yaml')
print('-----------------------------------------------')