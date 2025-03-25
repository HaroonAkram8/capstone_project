import math

def sim_locate(depth_data, camera_intrinsics, x_centre: int, y_centre: int, curr_pos: dict):
    relative_location = _relative_locate(depth_data=depth_data, camera_intrinsics=camera_intrinsics, x_centre=x_centre, y_centre=y_centre)
    location = _transform_location(relative_location=relative_location, curr_pos=curr_pos)
    return location

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

def _relative_locate(depth_data, camera_intrinsics, x_centre: int, y_centre: int):
    fx, fy, cx, cy = camera_intrinsics

    Z = depth_data[y_centre, x_centre]
    if Z == 0:
        return None

    X = (x_centre - cx) * Z / fx
    Y = (y_centre - cy) * Z / fy

    return {
        "x": float(X),
        "y": float(Y),
        "z": float(Z)
    }

def irl_locate(depth_data, x_centre: int, y_centre: int, curr_pos: dict):
    pass