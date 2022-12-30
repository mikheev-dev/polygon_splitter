from fastapi import HTTPException
from sympy import Polygon
from typing import List

import numpy as np


def validate_polygon(value: List[List[float]]):
    points = [tuple(v) for v in value]
    polygon = Polygon(*points)
    if not isinstance(polygon, Polygon):
        raise HTTPException(status_code=422, detail="Couldn't build a polygon from points.")
    if not polygon.is_convex():
        raise HTTPException(status_code=422, detail="Polygon is not convex.")


def validate_plane_normal_is_not_zero(value: List[float]):
    if np.dot(value, value) == 0.0:
        raise HTTPException(status_code=422, detail="Plane normal could not be a zero vector.")


def validate_is_plane_orthogonal_to_polygon(plane_normal: List[float], polygon_normal: List[float]):
    dot = np.dot(plane_normal, polygon_normal)
    if dot != 0.0:
        raise HTTPException(status_code=422, detail="Plane should be orthogonal to the polygon.")
