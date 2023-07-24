// Récupérer le document actif
var doc = app.activeDocument;

// Récupérer tous les calques visibles
var visibleLayers = [];
for (var i = 0; i < doc.layers.length; i++) {
  var layer = doc.layers[i];
  visibleLayers.push(layer);
}

// Générer toutes les combinaisons possibles de calques
var combinations = [];
var numCombinations = Math.pow(2, visibleLayers.length) - 1;
for (var i = 1; i <= numCombinations; i++) {
  var combination = [];
  for (var j = 0; j < visibleLayers.length; j++) {
    if ((i >> j) & 1) {
      combination.push(visibleLayers[j]);
    }
  }

  // Créer un groupe pour stocker les calques de la combinaison
  var group = doc.layerSets.add();
  group.name = "Combinaison " + i;

  // Copier les calques de la combinaison dans le groupe et les rendre visibles
  for (var k = 0; k < combination.length; k++) {
    var layer = combination[k];
    layer.visible = true;
    layer.duplicate(group, ElementPlacement.INSIDE);
    layer.visible = false;
  }

  // Générer le nom du fichier
  var fileName = "";
  for (var k = combination.length - 1; k >= 0; k--) {
    fileName += combination[k].name.replace(/\s+/g, "_");
    if (k > 0) {
      fileName += "-";
    }
  }
  fileName += ".png";


  // Exporter l'image de la combinaison
  var exportOptions = new ExportOptionsSaveForWeb();
  exportOptions.format = SaveDocumentType.PNG;
  exportOptions.PNG8 = false;
  exportOptions.transparency = true;
  var exportFile = new File(doc.path + "/" + fileName);
  doc.exportDocument(exportFile, ExportType.SAVEFORWEB, exportOptions);

  // Supprimer le groupe
  group.remove();
}
