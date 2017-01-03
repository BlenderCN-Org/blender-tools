# Blender tools addon

```python
bl_info = {
	'name': 'patwork tools',
	'description': 'My tools for Blender',
	'author': 'patwork@gmail.com',
	'version': (0, 3),
	'blender': (2, 78, 0),
	'location': 'Tool Shelf',
	'warning': '',
	'wiki_url': 'https://github.com/patwork/blender-tools',
	'category': 'Scene'
}
```

## Synchronize Sky Texture with Sun lamp

```python
sky = bpy.context.scene.world.node_tree.nodes['Sky Texture']
sun = bpy.context.scene.objects['Sun']
m = sun.matrix_world
sky.sun_direction = Vector((m[0][2], m[1][2], m[2][2]))
```

### Rename meshes to match parent objects

```python
for obj in bpy.data.objects:
	# [...]
	obj.data.name = obj.name
```

### Copy render settings to clipboard

```python
scene = bpy.context.scene
txt_render = self.my_get_attrs(scene.render, 'S.render')
txt_cycles = self.my_get_attrs(scene.cycles, 'S.cycles')
bpy.context.window_manager.clipboard = txt_render + txt_cycles
```

## ArchiCad groups

```python
op.axis_forward = 'Y'
op.axis_up = 'Z'
op.use_edges = True
op.use_smooth_groups = True
op.use_split_objects = True
op.use_split_groups = True
op.use_groups_as_vgroups = False
op.use_image_search = False
op.split_mode = 'ON'
op.global_clamp_size = 0.0
```

## License

MIT
