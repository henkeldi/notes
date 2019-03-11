
# Search and Sample Return

Goal: Learn about perception, decision making and action

### Perception step

* 320x160 pixel camera images

#### Apply color Threshold

For identifying navigable terrain

```python
rgb_thresh = (180, 180, 180)

def color_thresh(img, rgb_thresh):
    return np.all(img > rgb_thresh, axis=2)
```

#### Perspective Transform

Transform camera view to top down view

```python
def perspective_transform(img, grid_size, margin_bottom):
    h, w = img.shape[:2]
    pts_src = np.float32([(15, 140), (118, 96), (200, 96), (301, 140)])
    pts_dest = np.float32([(w/2-grid_size/2, h-margin_bottom),
                           (w/2-grid_size/2, h-margin_bottom-grid_size),
                           (w/2+grid_size/2, h-margin_bottom-grid_size),
                           (w/2+grid_size/2, h-margin_bottom)])

    m = cv2.getPerspectiveTransform(pts_src, pts_dest)
    return cv2.warpPerspective(img, m, (w, h))
```

#### Transform to rover coordinates

```python
def rover_coordinates(thresh_img):
    h, w = thresh_img.shape[:2]
    y_pos, x_pos = thresh_img.nonzero()
    x_out = -y_pos + h
    y_out = -x_pos + w/2
    return x_out, y_out
```

#### Transform to world coordinates

```python
def rotate_pix(x_pix, y_pix, yaw):
    yaw_rad = np.deg2rad(yaw)

    x_pix_rotated = x_pix * np.cos(yaw_rad) - y_pix * np.sin(yaw_rad)
    y_pix_rotated = x_pix * np.sin(yaw_rad) + y_pix * np.cos(yaw_rad)

    return x_pix_rotated, y_pix_rotated


def translate_pix(x_pix_rot, y_pix_rot, x_pos, y_pos, scale):
    x_pix_translated = np.int_(x_pix_rot/scale + x_pos)
    y_pix_translated = np.int_(y_pix_rot/scale + y_pos)

    return x_pix_translated, y_pix_translated


def pix_to_world(x_pix, y_pix, x_pos, y_pos, yaw, world_size, scale):
    # Apply rotation
    x_pix_rot, y_pix_rot = rotate_pix(x_pix, y_pix, yaw)

    # Apply translation
    x_pix_tran, y_pix_tran = translate_pix(x_pix_rot,
                                           y_pix_rot,
                                           x_pos,
                                           y_pos,
                                           scale)

    # Clip to world_size
    x_pix_world = np.clip(np.int_(x_pix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(y_pix_tran), 0, world_size - 1)

    return x_pix_world, y_pix_world
```


#### Where to go
```python
def to_polar_coords(xpix, ypix):
    # Calculate distance to each pixel
    dist = np.sqrt(xpix**2 + ypix**2)
    # Calculate angle using arctangent function
    angles = np.arctan2(ypix, xpix)
    return dist, angles

distances, angles = to_polar_coords(xpix, ypix) # Convert to polar coords
avg_angle = np.mean(angles) # Compute the average angle
avg_angle_degrees = avg_angle * 180/np.pi
steering = np.clip(avg_angle_degrees, -15, 15)
```

