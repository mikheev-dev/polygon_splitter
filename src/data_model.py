from pydantic import BaseModel, Field
from typing import List, Union

import pydantic

from .validators import validate_polygon, validate_is_plane_orthogonal_to_polygon, validate_plane_normal_is_not_zero


class Point3DModel(BaseModel):
    __root__: List[float] = Field(..., min_items=3, max_items=3)


class PlaneModel(BaseModel):
    point: Point3DModel = Field()
    normal: Point3DModel = Field()

    @pydantic.validator('normal', always=True)
    @classmethod
    def validate_plane_normal_is_not_zero(cls, value):
        validate_plane_normal_is_not_zero(value.__root__)
        return value


class Point2DModel(BaseModel):
    __root__: List[float] = Field(..., min_items=2, max_items=2)

    def to_3D(self) -> Point3DModel:
        return Point3DModel(__root__=[*self.__root__, 0])


class EmptyPolygonModel(BaseModel):
    __root__: List[Point2DModel] = Field(..., min_items=0, max_items=0)


class PolygonModel(BaseModel):
    __root__: List[Point2DModel] = Field(..., min_items=3)

    @classmethod
    def get_polygon_normal(cls) -> Point3DModel:
        return Point3DModel(__root__=[0, 0, 1])

    @classmethod
    def get_polygon_plane(cls) -> PlaneModel:
        return PlaneModel(
            point=Point3DModel(__root__=[0, 0, 0]),
            normal=cls.get_polygon_normal()
        )

    @pydantic.validator('__root__', always=True)
    @classmethod
    def validate_is_polygon_convex(cls, value):
        points = [v.__root__ for v in value]
        validate_polygon(points)
        return value


class SplittingRequestData(BaseModel):
    polygon: PolygonModel = Field()
    plane: PlaneModel = Field()

    @pydantic.root_validator(skip_on_failure=True)
    @classmethod
    def validate_is_plane_orthogonal_to_polygon(cls, values):
        plane_normal = values['plane'].normal
        polygon_normal = PolygonModel.get_polygon_normal()
        validate_is_plane_orthogonal_to_polygon(
            plane_normal.__root__,
            polygon_normal.__root__,
        )
        return values


class SplittingResponseData(BaseModel):
    polygon1: PolygonModel = Field()
    polygon2: Union[PolygonModel, EmptyPolygonModel] = Field()

