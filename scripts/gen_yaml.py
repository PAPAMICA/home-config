import itertools
filelocation = "/local/images/salon/"

lumieres = [
    ("L1", "light.hue_play_gradient_lightstrip_1"),
    ("L2", "light.salon_led_canape_2"),
    ("L3", "light.hue_ambiance_lamp_1"),
    ("L4", "light.salon_led_escaliers"),
    ("L5", "light.salon_lumiere_lustre"),
    ("L6", "light.salle_lumiere_lustre"),
    ("L7", "light.cuisine_lumiere_lustre"),
    # ("L8", "cover.cuisine_volets"),
    # ("L9", "cover.salle_volets"),
    # ("L10", "cover.salon_volets")
]

scenarios = []

# Générer tous les scénarios possibles
for i in range(1, len(lumieres) + 1):
    for comb in itertools.combinations(lumieres, i):
        scenario = {
            "conditions": [],
            "elements": []
        }
        for lumiere in lumieres:
            nom, entity = lumiere
            if lumiere in comb:
                if entity.startswith("light."):
                    scenario["conditions"].append({
                        "entity": entity,
                        "state": "on"
                    })
                elif entity.startswith("cover."):
                    scenario["conditions"].append({
                        "entity": entity,
                        "state": "open"
                    })
            else:
                if entity.startswith("light."):
                    scenario["conditions"].append({
                        "entity": entity,
                        "state": "off"
                    })
                elif entity.startswith("cover."):
                    scenario["conditions"].append({
                        "entity": entity,
                        "state": "close"
                    })
        scenario["elements"].append({
            "type": "image",
            "image": f"{filelocation}{'-'.join([nom for nom, _ in comb])}.png"
        })
        scenarios.append(scenario)


# Générer le contenu du fichier dash.yaml
content = "type: picture-elements"
content += f"image: {filelocation}L0.png"
content += "elements:"
for i, scenario in enumerate(scenarios):
    content += f"  - type: conditional\n"
    content += "    condition: and\n"
    content += "    conditions:\n"
    for condition in scenario["conditions"]:
        content += f"      - entity: {condition['entity']}\n"
        content += f"        state: {condition['state']}\n"
    content += "    elements:\n"
    for element in scenario["elements"]:
        content += f"      - type: {element['type']}\n"
        content += f"        image: {element['image']}\n"
        content += f"        style:\n"
        content += f"          top: 50%\n"
        content += f"          left: 50%\n"
        content += f"          width: 100%\n"

    if i < len(scenarios) - 1:
        content += "\n"

# Écrire le contenu dans le fichier dash.yaml
with open("dash.yaml", "w") as file:
    file.write(content)

print("Le fichier dash.yaml a été généré avec succès.")
