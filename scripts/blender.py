import bpy

# Affiche une ligne de séparation
print("-----------------------------------")

# Définit le chemin du fichier
filePath = "D:\kDrive Perso\\2-PERSO\MAISON 3D\RENDUS\encours\\"

# Active l'utilisation des noeuds dans la scène
bpy.context.scene.use_nodes = True
# Récupère l'arbre des noeuds de la scène
tree = bpy.context.scene.node_tree

# Initialise une liste vide

# Initialise une liste de motifs à rechercher




# Liste des render layers
render_layers = ["RL_ETAGE1_salon", "RL_ETAGE1_emissive", "RL_ETAGE1_chambre", "RL_ETAGE1_chambre.001", "RL_ETAGE1_chambre.002"]

denoise_list_all = []



# Parcourt les render layers
for render_layer in render_layers:
    list_clear = []
    list = []
    list_pattern = ["Combined"]

    # Parcourt les sorties du noeud du render layer
    for i in tree.nodes[render_layer].outputs :
        # Si la sortie est activée
        if i.enabled :
            # Ajoute le nom de la sortie à la liste
            list.append(i.name)

    list_clear = [elem for elem in list if any(suite in elem for suite in list_pattern)]

    # Définit le décalage en y
    decal_y = 300
    # Initialise une liste pour les noeuds de débruitage
    denoise_list = []

    # Initialise la position en y
    loc_y = 500    






    # Parcourt la liste des éléments clairs
    for i in list_clear :
        print (i)
        # Crée un nouveau noeud de débruitage
        denoise_node = tree.nodes.new("CompositorNodeDenoise")
        # Nomme le noeud de débruitage
        denoise_node.name = "denoise_" + i
        # Définit la position du noeud de débruitage
        #denoise_node.location[0] = -2000
        denoise_node.location[1] = loc_y - decal_y
        # Connecte la sortie du noeud du render layer au noeud de débruitage
        tree.links.new(tree.nodes[render_layer].outputs[i], denoise_node.inputs[0])

        # Ajoute le nom du noeud de débruitage à la liste
        denoise_list.append(denoise_node.name)
        denoise_list_all.append([render_layer, denoise_node.name, denoise_node])



        # Décale la position en y
        #loc_y -= decal_y

    # Crée un CompositorNodeOutputFile avec autant de file_slots qu'il y a de denoise_node

loc_y = 500
decal_y = 500
for render_layer in render_layers:
    file_output_node = tree.nodes.new('CompositorNodeOutputFile')
    file_output_node.base_path = filePath + render_layer
    file_output_node.location[0] = 1000
    file_output_node.location[1] = loc_y - decal_y
    loc_y -= decal_y
    for i in denoise_list_all:
        if i[0] == render_layer:
            denoise_node_name = i[1]
            denoise_node = i[2]
            print(denoise_node_name)
            print(denoise_node)
            # Ajoute un nouveau file_slot pour chaque denoise_node
            try:
                file_output_node.file_slots.new(denoise_node_name)
                tree.links.new(denoise_node.outputs[0], file_output_node.inputs[denoise_node_name])
            except Exception as e:
                print(f"Erreur lors de la création du file_slot pour {denoise_node_name}: {str(e)}")