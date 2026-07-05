import json

with open("../website/public/brazil-states.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

output = []
output.append("import React from 'react';\n")
output.append("export function BrazilSVG({ activeStates }) {\n")
# SVG viewBox: X min (longitude), Y min (inverted latitude), Width, Height
output.append("  return (")
output.append("    <svg viewBox=\"-72 -6 42 40\" style={{ width: '100%', height: 'auto', maxHeight: '400px' }} stroke=\"var(--color-bg-secondary)\" strokeWidth=\"0.08\" strokeLinejoin=\"round\" strokeLinecap=\"round\" shapeRendering=\"geometricPrecision\">")

for feature in data.get('features', []):
    sigla = feature['properties']['sigla']
    geom_type = feature['geometry']['type']
    coords = feature['geometry']['coordinates']
    
    paths = []
    if geom_type == 'Polygon':
        polygons = [coords]
    elif geom_type == 'MultiPolygon':
        polygons = coords
    else:
        continue
        
    for polygon in polygons:
        for ring in polygon:
            # We negate Y because SVG Y goes top-to-bottom, but latitude goes bottom-to-top
            # We also slightly scale X by a constant to account for equirectangular projection roughly at Brazil's latitude (-15 deg). cos(15 deg) = 0.965
            path_str = "M " + " L ".join([f"{x * 0.965},{-y}" for x, y in ring]) + " Z"
            paths.append(path_str)
    
    d = " ".join(paths)
    output.append(f"      <path id=\"{sigla}\" d=\"{d}\" fill={{activeStates.has('{sigla}') ? 'var(--color-accent)' : '#2a3b32'}} />")

output.append("    </svg>")
output.append("  );\n}")

with open("../website/src/components/BrazilSVG.jsx", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
