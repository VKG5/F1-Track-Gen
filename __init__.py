# To register this as an add-on!
bl_info = {
    'name': 'F1 Track Generator',
    'author': 'Varun Kumar Gupta, Nazzal Naseer',
    'version': (1, 0, 0),
    'blender': (3, 0, 0),
    'location': "3D Viewport",
    'description': 'A simple add-on to generate F1 tracks based off of API Data',
    'warning': '',
    'wiki_url': 'https://github.com/VKG5/F1-Track-Gen',
    'category': 'Object',
}

import bpy

from . import generateTrack as genTrack
from . import generateFillers as genFillers

'''Main Code starts HERE'''
# GLOBAL VARIABLES
# Properties/Inputs for our add-on
# Format : ("Name", The bpy.property relevant to the field - Int, String, Float, etc.)
PROPS = [
    ('sectors', bpy.props.IntProperty(name='Sectors', default=1, min=1, max=3)),
    ('apiName', bpy.props.EnumProperty(
                                name='API Type',
                                description = 'Selection a track preset',
                                items = [
                                    ('api001', 'Melbourne', ''),
                                    ('api002', 'Texas', ''),
                                    ('api003', 'Sakhir (Baharain)', '')
                                ] ) ),
    ('trackNumber', bpy.props.EnumProperty(
                                name='Track Type',
                                description = 'Selection a track preset',
                                items = [
                                    ('Track001', 'Melbourne', ''),
                                    ('Track002', 'Texas', '')
                                ] ) ),
    ('poleOffset', bpy.props.FloatProperty(name='Pole Distance')),
    ('flagOffset', bpy.props.FloatProperty(name='Flag Distance')),
    ('poleOffsetTrack', bpy.props.FloatProperty(name='Pole Offset')),
    ('flagOffsetTrack', bpy.props.FloatProperty(name='Flag Offset')),
    ('deletePrev', bpy.props.BoolProperty(name='Delete Prev Fillers'))
]


'''
Functions calls/Dependent Functions
The functions that will be used by the operator class
'''
def selectOptions(params, context):
    ## Debugging
    #print("Types of the parameters : %s, %s" % (type(params[0]), type(params[1])))
    
    # Calling the generate track function from the generateTrack script
    genTrack.generateTrack(params, context.scene.trackNumber, context.scene.apiName)
    
    ## Debugging
    #print(type(bpy.context.scene.trackNumber))
    
def placeDecors(context):
    ## Debugging
    #print("Inside Decors")    
    
    # Calling the fillers functions
    genFillers.addFillers(context.scene.flagOffset, context.scene.poleOffset, context.scene.deletePrev, context.scene.flagOffsetTrack, context.scene.poleOffsetTrack)
    
    
'''
Class that actually calls all the necessary code
'''
# Operator Class
class f1TrackProps(bpy.types.Operator):
    bl_idname = "opr.generate_f1_track"
    bl_label = "Generate F1 Track"
    
    def execute(self, context):
        # Accessing the values from the UI
        scene = context.scene
        params = (
            scene.sectors
        )
        
        ## Debugging
        #print("Hey!")
        
        # Sending the input to the actual code
        selectOptions(params, context)
        
        return {'FINISHED'}

# Operator Class
# To generate Fillers for the above class
class f1TrackPropsFillers(bpy.types.Operator):
    bl_idname = "opr.generate_f1_track_fillers"
    bl_description = "Generate Fillers (Poles, Flags) on top of the already generated Track"
    bl_label = "Generate F1 Track Fillers"
    
    def execute(self, context):
        # Sending the input to the actual code
        placeDecors(context)
        
        return {'FINISHED'}


'''
Class that generates the UI 
'''            
# UI CLASS
class f1TrackDemoUI(bpy.types.Panel):
    # Creates a side panel in the 3D Viewport under "Misc"    
    bl_idname = "VIEW3D_PT_F1_Track_Generator"
    bl_label = "F1 Track Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    # To draw/create the actual panel
    def draw(self, context):
        
        # Generating the fields that would be visible in the UI Panel
        col = self.layout.column()
        for(prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
        
        # Button to run the generateTrack() script
        col.operator('opr.generate_f1_track', text='Generate')
        
        # Button to run the generateFillers() script
        col.operator('opr.generate_f1_track_fillers', text='Generate Fillers')
        

'''
Driver Code
This part includes all the calls and registrations (Without which the add-on won't work!
'''
# To automate the instlalation and uninstallation of multiple scripts/classes!
# Just add the class name in this list
CLASSES = [
    f1TrackProps,
    f1TrackPropsFillers,
    f1TrackDemoUI
]

# To install the add-on for the first time
def register():
    # Registering the Properties before the classes
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    ## Debugging
    #print("Registered")
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    
# To delete the add-on upon uninstallation
def unregister():
    # De-Registering the properties
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
        
    ## Debugging
    #print("Unregistered")
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

# To make this work
if __name__ == "__main__":
    register() 