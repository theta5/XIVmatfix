# XIVmatfix

9/21/2021 | Hey everyone! If you're finding this through a Meku related source, please note that this addon is currently broken if you're using mektools, as we ended up sharing some code, and requiring a refactor on this addon I just haven't found time for. Please uninstall this addon for the time being if you are experiencing issues with either this addon or mektools.

XIV Material Fix Addon (for Godbert and Textools furniture and map assets) Written by Theta Five and Skulblaka Drotningu

If you like this or have a feature request, please show your support for my work at https://ko-fi.com/thetafive

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

Granular Control features:
automatically quadruple the size of texture maps on the selected node (to handle FFXIV's terrain mapping)
