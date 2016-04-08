#-*- coding: utf-8 -*-
#
# patwork blender tools addon
# v0.1 - 2016-04-07
#

# ----------------------------------------------------------------------------
bl_info = {
	'name': 'patwork tools',
	'description': 'My tools for Blender',
	'author': 'patwork@gmail.com',
	'version': (0, 1),
	'blender': (2, 77, 0),
	'location': 'Tool Shelf',
	'warning': '',
	'wiki_url': 'https://github.com/patwork/blender-tools',
	'category': 'Scene'
}

ui = {
	'panel_category': 'patwork',
	'label_tools': 'Tools',

	'label_world': 'World',
	'id_syncskywithsun': 'patwork.syncskywithsun',
	'txt_syncskywithsun': 'Sync sky',

	'label_archicad': 'ArchiCad',
	'id_archicadgroups': 'patwork.archicadgroups',
	'txt_archicadgroups': 'Make groups'
}

# ----------------------------------------------------------------------------
import bpy
from math import *
from mathutils import *

# ----------------------------------------------------------------------------
class SyncSkyWithSun(bpy.types.Operator):
	'''Synchronize Sky Texture with Sun lamp'''

	bl_idname = ui['id_syncskywithsun']
	bl_label = ui['txt_syncskywithsun']

	# ----------------------------------------------------------------------------
	def my_sync_sky_with_sun(self):

		if 'Sky Texture' in bpy.context.scene.world.node_tree.nodes:
			sky = bpy.context.scene.world.node_tree.nodes['Sky Texture']
		else:
			self.report({'ERROR'}, '%s: cannot find sky texture!' % ui['txt_syncskywithsun'])
			return False

		if 'Sun' in bpy.context.scene.objects:
			sun = bpy.context.scene.objects['Sun']
		else:
			self.report({'ERROR'}, '%s: cannot find sun lamp!' % ui['txt_syncskywithsun'])
			return False

		m = sun.matrix_world
		sky.sun_direction = Vector((m[0][2], m[1][2], m[2][2]))

		print('synchronized %s to %s (%f, %f, %f)' % (sky.name, sun.name, m[0][2], m[1][2], m[2][2]))

		return True

	# ----------------------------------------------------------------------------
	def execute(self, context):

		if self.my_sync_sky_with_sun():
			self.report({'INFO'}, '%s: done.' % ui['txt_syncskywithsun'])

		return {'FINISHED'}

# ----------------------------------------------------------------------------
class ArchicadGroups(bpy.types.Operator):
	'''Clean mess from ArchiCad'''

	bl_idname = ui['id_archicadgroups']
	bl_label = ui['txt_archicadgroups']

	my_empty = '_ARCHICAD'

	# ----------------------------------------------------------------------------
	def my_create_empty(self, object_name, object_parent):

		if object_name in bpy.data.objects:
			return bpy.data.objects[object_name]

		print('creating empty %s' % object_name)

		bpy.ops.object.add(type = 'EMPTY')
		object_new = bpy.context.active_object

		if object_new is None:
			self.report({'ERROR'}, '%s: cannot create empty %s!' % ui['txt_archicadgroups'], object_name)
			return None

		object_new.name = object_name
		object_new.rotation_euler = Euler((0.0, 0.0, 0.0))
		object_new.location = Vector((0.0, 0.0, 0.0))
		object_new.scale = Vector((1.0, 1.0, 1.0))

		if object_parent:
			object_new.parent = object_parent

		return object_new

	# ----------------------------------------------------------------------------
	def my_archicad_groups(self):

		if self.my_empty in bpy.data.objects:
			self.report({'WARNING'}, '%s: there can be only one!' % ui['txt_archicadgroups'])
			return False

		top = self.my_create_empty(self.my_empty, None)
		if not top:
			return False

		groups = {}

		for loop in [ 0, 1 ]:
			for obj in bpy.data.objects:
				if obj.type == 'MESH' and obj.parent is None:
					arr = obj.name.strip().split()
					if len(arr) > 1:
						pre = arr[0].upper()

						if loop == 0:
							if pre in groups:
								groups[pre] = groups[pre] + 1
							else:
								groups[pre] = 1

						else:
							if pre in groups and groups[pre] > 1:
								obj.parent = self.my_create_empty('_' + pre, top)
								if not obj.parent:
									return False
							else:
								obj.parent = top

		return True

	# ----------------------------------------------------------------------------
	def execute(self, context):

		if self.my_archicad_groups():
			self.report({'INFO'}, '%s: done.' % ui['txt_archicadgroups'])

		return {'FINISHED'}

# ----------------------------------------------------------------------------
class ToolsPanel(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = 'objectmode'
	bl_category = ui['panel_category']
	bl_label = ui['label_tools']

	# ----------------------------------------------------------------------------
	def draw(self, context):
		col = self.layout.column(align = True)

		col.label(ui['label_world'])
		col.operator(ui['id_syncskywithsun'], text = ui['txt_syncskywithsun'], icon = 'MAT_SPHERE_SKY')

		col.label(ui['label_archicad'])
		col.operator(ui['id_archicadgroups'], text = ui['txt_archicadgroups'], icon = 'SCRIPTWIN')

# ----------------------------------------------------------------------------
def register():
	print('register: %s (%d.%d)' % (bl_info['name'], bl_info['version'][0], bl_info['version'][1]))
	bpy.utils.register_class(SyncSkyWithSun)
	bpy.utils.register_class(ArchicadGroups)
	bpy.utils.register_class(ToolsPanel)

# ----------------------------------------------------------------------------
def unregister():
	print('unregister: %s (%d.%d)' % (bl_info['name'], bl_info['version'][0], bl_info['version'][1]))
	bpy.utils.unregister_class(SyncSkyWithSun)
	bpy.utils.unregister_class(ArchicadGroups)
	bpy.utils.unregister_class(ToolsPanel)

# ----------------------------------------------------------------------------
if __name__ == '__main__':
	register()

# EoF
# vim: noexpandtab tabstop=4 softtabstop=4 shiftwidth=4
