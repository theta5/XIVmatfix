# --- THETA IS BAD AT COMMENTING CODE ---
# --- THIS ADDON DOES STUFF ---

bl_info = {
    "name": "Theta's FFXIV Material Fixer",
    "author": "Theta Five",
    "version": (0, 0, 1),
    "blender": (2, 92, 0),
    "location": "3D Viewport N-Panel",
    "description": "Thing to convert textools and Godbert materials to Blender",
    "warning": "",
    "support": 'COMMUNITY',
    "category": "Materials",
    }

import bpy
import os
from math import radians

# --- Panel ---
# ------------------------------------------------------------------------------------

class ThetaPanel(bpy.types.Panel):
    
    bl_label = "Thetas' Matfixes"
    bl_idname = "PT_Thetamatpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'XIVMatFixer'

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        
        selected_objects = bpy.context.selected_objects
        
        layout.label(text="Material Fixes")

        layout.label(text="Apply Material fixes to")
        layout.label(text="current material and object")
        row = layout.row()
        row.scale_y = 2.0
        row.operator("myops.matfix", text = "Apply Custom Material Nodes")

        layout.label(text="The Scary Button(tm)", icon="ERROR")
        layout.label(text="Press to apply to all materials")

        row = layout.row()
        row.scale_y = 2.0
        row.operator("myops.fixall", text = "Apply to ALL nodes")

#class ThetaGranularControls(bpy.types.Panel):
#    bl_label = "Granular Controls"
#    bl_idname = "PT_Thetamatpanel2"
#    bl_space_type = 'VIEW_3D'
#    bl_region_type = 'UI'
#    bl_category = 'MatFixer'
#    bl_options = 'DEFAULT_CLOSED'
    
#    def draw(self, context):
#        layout = self.layout

#        scene = context.scene

#        layout.label(text="Individual Functions")

#        row = layout.row()
#        row.scale_y = 1.0
#        row.operatorw("myops.testbutton", text = "Template Button")
    
# --- Ops ---
# ------------------------------------------------------------------------------------



class AppendNodes(bpy.types.Operator): # Appends custom nodes to file
    bl_idname = "myops.nodeappend"
    bl_label = "Append Material Nodegroups"
    bl_description = "Appends Material Nodes to the file (DO THIS ONLY ONCE!)"

    def execute(self,context):
        check_for_nodes()
        return {"FINISHED"}
        
class MaterialFix(bpy.types.Operator): # Adds Custom Shader to active material
    bl_idname = "myops.matfix"
    bl_label = "Apply Custom Material Nodes"
    bl_description = "Applies Custom Material Node to objects for fixing shading issues present in FFXIV Furniture and Landscape objects"

    def execute(self, context):
        check_for_nodes()
        selected_material = bpy.context.active_object.active_material
        selected_objects = bpy.context.active_object
        change_material(selected_material)
        clear_split_normals(selected_objects)
        return {"FINISHED"}

class FixAllNodes(bpy.types.Operator):
    bl_idname = "myops.fixall"
    bl_label = "Fix All Materials"
    bl_description = "Applies Custom Material Node to all objects in the scene whether they want it or not. Warning: this can take an EXTREMELY long time on scenes with a large number of objects"

    def execute(self, context):
        check_for_nodes()
        for item in bpy.data.materials:
            change_material(item)
        for objects in bpy.data.objects:
            clear_split_normals(objects)
        return {"FINISHED"}
    
# --- Functions ---
# ------------------------------------------------------------------------------------

def append_nodegroups():
    path = os.path.dirname(__file__) + '/blends/nodegroups.blend\\NodeTree\\'
    import_node = 'Diff-Spec-Converter'
    bpy.ops.wm.append( filename = import_node, directory = path)

def change_material(mat):

    to_remove = []
    fix_alphablend(mat)
    for node in mat.node_tree.nodes:
        if node.bl_idname == 'ShaderNodeNormalMap':
            replace_normalmap_to_custom(node, mat.node_tree)
            to_remove.append(node)
        if node.bl_idname == 'ShaderNodeBsdfPrincipled':
            if len(node.inputs[0].links) > 0:
                checknode = node.inputs[0].links[0].from_node
                if checknode.bl_idname != 'ShaderNodeTexImage':
                    return
                else:
                    connect_alpha(node, mat)
                    add_slap(node, mat.node_tree)
                    fix_metallic(node)
                    remove_emission(node, mat)
    for node in to_remove:
        mat.node_tree.nodes.remove(node)

def fix_metallic(node):
    if node.bl_idname == 'ShaderNodeBsdfPrincipled':
        node.inputs[4].default_value = 0    

def fix_alphablend(mat):
    mat.blend_method = 'HASHED'

def add_slap(node, node_tree): # Relink existing materials to custom nodegroup

    #Create groupnode
    groupnode = node_tree.nodes.new('ShaderNodeGroup')
    groupnode.node_tree = bpy.data.node_groups['Diff-Spec-Converter']
    SpecExists = False #Yes I know this logic is janky it's really late at night ok? TODO: fix this later

    if len(node.inputs[0].links) > 0: #This should really never fail
        diffimage = node.inputs[0].links[0].from_node
        #Connect diff node to slap node
        node_tree.links.new(groupnode.inputs[0], diffimage.outputs[0])

    if len(node.inputs[5].links) > 0: #Sometimes there's no alpha
        SpecExists = True
        specimage = node.inputs[5].links[0].from_node
        #Connect spec node to slap node
        node_tree.links.new(groupnode.inputs[1], specimage.outputs[0])
    
    #Connect slap node outputs to main node inputs.
    node_tree.links.new(groupnode.outputs[0], node.inputs[0])
    node_tree.links.new(groupnode.outputs[1], node.inputs[5])
    node_tree.links.new(groupnode.outputs[2], node.inputs[7])

    move_node(groupnode, -200, 250)
    move_node(diffimage, -200, -100)
    if SpecExists == True:
        move_node(specimage, -200, -100)

def replace_normalmap_to_custom(node, node_tree):
    # Create groupnode
    groupnode = node_tree.nodes.new('ShaderNodeGroup')
    groupnode.node_tree = bpy.data.node_groups['Normal-Converter']
    
    # Place node same position
    groupnode.location = (node.location.x, node.location.y)
    move_node(groupnode, 100, 100)
        
    # Connect
    node_tree.links.new(groupnode.inputs[0], node.inputs[1].links[0].from_node.outputs[0])
    node_tree.links.new(groupnode.outputs[0], node.outputs[0].links[0].to_node.inputs[20])

    normaltexnode = groupnode.inputs[0].links[0].from_node
    move_node(normaltexnode, 100, 650)

def remove_emission(node, mat):
        if node.bl_idname == 'ShaderNodeBsdfPrincipled':
            if len(node.inputs[17].links) > 0:
                emissionnode = node.inputs[17].links[0].from_node
                if emissionnode.bl_idname == 'ShaderNodeTexImage':
                    mat.node_tree.nodes.remove(emissionnode)

def connect_alpha(node, mat):
    if len(node.inputs[0].links) > 0:
        if len(node.inputs[19].links) > 0:
            alphanode = node.inputs[19].links[0].from_node
            if alphanode.bl_idname == 'ShaderNodeTexImage':
                mat.node_tree.nodes.remove(alphanode)
        mat.node_tree.links.new(node.inputs[0].links[0].from_node.outputs[1], node.inputs[19])

def clear_split_normals(meshobject):
    if meshobject.type == 'MESH':
        try:
            bpy.context.view_layer.objects.active = meshobject
            bpy.ops.mesh.customdata_custom_splitnormals_clear() #clear custom split normals
            bpy.context.object.data.use_auto_smooth = True  # Set autosmooth to enabled
            bpy.context.object.data.auto_smooth_angle = radians(180) # Set autosmooth to 180 degrees
        except:
            pass

def move_node(node, x_amount, y_amount):
    node.location.x += x_amount
    node.location.y += y_amount

def place_node(node, x_pos, y_pos):
    node.location.x = x_pos
    node.location.y = y_pos

def check_for_nodes():
    nodesappended = False
    for n in bpy.data.node_groups:
        if n.name == 'Diff-Spec-Converter':
            nodesappended = True
    if nodesappended == False:
        append_nodegroups()

# --- Main Addon Stuff ---
# ------------------------------------------------------------------------------------

classes = [ThetaPanel, MaterialFix, FixAllNodes]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
# --- Main Code ---

if __name__ == "__main__":
    register()
