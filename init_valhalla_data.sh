#!/bin/bash
set -e

# Dossier pour les données
VALHALLA_DATA_DIR="$(pwd)/valhalla_data"
OSM_PBF_URL="https://download.geofabrik.de/europe/andorra-latest.osm.pbf"
OSM_PBF_FILE="$VALHALLA_DATA_DIR/andorra-latest.osm.pbf"

mkdir -p "$VALHALLA_DATA_DIR"

# 1. Télécharger l'extrait OSM si absent
if [ ! -f "$OSM_PBF_FILE" ]; then
  echo "Téléchargement de l'extrait OSM Andorra (ultra-léger pour test)..."
  wget -O "$OSM_PBF_FILE" "$OSM_PBF_URL"
else
  echo "Extrait OSM déjà présent."
fi

# 2. Générer les tiles Valhalla
# Utilise le container pour builder les tiles

docker run --rm \
  -v "$VALHALLA_DATA_DIR:/data/valhalla" \
  ghcr.io/valhalla/valhalla:latest \
  valhalla_build_tiles -c /data/valhalla/valhalla.json /data/valhalla/andorra-latest.osm.pbf

# Création de l'archive tiles.tar attendue par Valhalla (depuis le conteneur Docker pour éviter les problèmes de droits)
docker run --rm \
  -v "$VALHALLA_DATA_DIR:/data/valhalla" \
  ghcr.io/valhalla/valhalla:latest \
  bash -c "cd /data/valhalla/tiles && tar -cvf tiles.tar *"

echo "Les données Valhalla sont prêtes dans ./valhalla_data.\nLancez Valhalla avec : make valhalla-up"
