
# Tensorflow Graphics

### Installation

```bash
pip install tensorflow-graphics
```

## Scene Parameters

* Transformations
* Cameras
* Lights and Materials
* Geometry

### Transformation

```python
import tensorflow_graphics.geometry.transformation as tfg_transformation

cube = load_cube() # cube vertices.
axis = (0., 1., 0.) # y axis.
angle = (np.pi / 4)
cube_rotated = tfg_transformation.axis_angle.rotate(cube, axis, angle)
```

### Camera

```python
import tensorflow_graphics.rendering.camera as tfg_camera

cube = load_cube() # cube vertices.
focal = (100., 100.) # focal length of the camera
principal_point = (256., 256.) # principal point of the camera
projected_cube = tfg_camera.perspective.project(points, focal, principal_point)
```

### Light and Material

```python
import tensorflow_graphics.rendering.reflectance as tfg_reflectance

surface_normal = (0., 1., 0.) # surface normal
incoming_ray = (100., 100.) # incoming ray from the light
outgoing_ray = (256., 256.) # outgoing ray toward the camera
color = (1., 1., 1.) # color of the surface
shininess = (0.5,) # shininess of the surface

output_color = tfg_reflectance.blinn_phong.brdf(incoming_ray, outgoing_ray, surface_normal,
                                                shininess, color)
```

### Graph convolution

```python
import tensorflow as tf
import tensorflow_graphics.nn.layer.graph_convolution as tf_graph_conf

vertices, connectivity = load_mesh() # mesh vertices and connectivity
output = tf_graph_conv.freature_steered_convolution_layer(vertices, connectivity)
output = tf.nn.relu(output)
```