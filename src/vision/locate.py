import math

def sim_locate(depth_data, camera_intrinsics, x_centre: int, y_centre: int, curr_pos: dict):
    relative_location, is_max = _relative_locate(depth_data=depth_data, camera_intrinsics=camera_intrinsics, x_centre=x_centre, y_centre=y_centre)
    if relative_location is None:
        return None
    
    location = _transform_location(relative_location=relative_location, curr_pos=curr_pos)
    return location, is_max

def _transform_location(relative_location: dict, curr_pos: dict):
    X = curr_pos["x"] + relative_location["x"] * math.sin(curr_pos["yaw"]) + relative_location["z"] * math.cos(curr_pos["yaw"])
    Y = curr_pos["y"] + relative_location["x"] * math.cos(curr_pos["yaw"]) - relative_location["z"] * math.sin(curr_pos["yaw"])
    Z = curr_pos["z"] - relative_location["y"] # z is negative

    location = {
        "x": round(X, 2),
        "y": round(Y, 2),
        "z": round(Z, 2)
    }

    return location

def _relative_locate(depth_data, camera_intrinsics, x_centre: int, y_centre: int, max_distance: int=50):
    fx, fy, cx, cy = camera_intrinsics

    Z = min(depth_data[y_centre, x_centre], max_distance)
    if Z == 0:
        return None, False

    X = (x_centre - cx) * Z / fx
    Y = (y_centre - cy) * Z / fy

    location = {
        "x": float(X),
        "y": float(Y),
        "z": float(Z)
    }
    is_max = Z == max_distance

    return location, is_max

def irl_locate(depth_data, x_centre: int, y_centre: int, curr_pos: dict):
    pass