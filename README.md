# XIVmatfix
XIV Material Fix Addon (for Godbert and Textools furniture and map assets)

This Blender addon performs several functions to fix exported terrain, building, and furniture models exported from Godbert tools and Textools from FFXIV. 

v0.1--
Material fixes applied currently:

Sets alpha blend to hashed.
Removes custom split normals and enables autosmooth.
Removes an incorrect "Metallic" property set by default by Textools.
Relinks transparency to correct map.
Adds custom nodegroup to more closely match ingame shading and material settings.
Adds custom normal map interperetater nodegroup to fix compatibility issues with FFXIV's "bump" style normal maps.
Removes unneeded material nodes (emission and duplicate diffuse for alpha).
Reorganizes material node tree.
