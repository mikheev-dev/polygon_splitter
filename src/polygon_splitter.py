from abc import abstractmethod, ABC
from sympy import Polygon, Plane, Line2D, Point
from typing import Tuple, Union

from .data_model import Point3DModel, PolygonModel


class BasePolygonSplitter(ABC):
    _polygon_model: PolygonModel

    def __init__(self, polygon_model: PolygonModel):
        self._polygon_model = polygon_model

    @abstractmethod
    def split_by_plane(
            self,
            plane_normal: Point3DModel,
            plane_point: Point3DModel,
    ) -> Union[PolygonModel, Tuple[PolygonModel, PolygonModel]]:
        raise NotImplementedError


class SympyPolygonSplitter(BasePolygonSplitter):
    _polygon: Polygon

    @staticmethod
    def sympy_polygon_to_polygon_model(polygon: Polygon) -> PolygonModel:
        return PolygonModel(
            __root__=[
                list(v)
                for v in polygon.vertices
            ]
        )

    @staticmethod
    def polygon_model_to_sympy_polygon(polygon_model: PolygonModel) -> Polygon:
        return Polygon(*[
            tuple(point.__root__)
            for point in polygon_model.__root__
        ])

    def __init__(self, polygon_model: PolygonModel):
        super().__init__(polygon_model)
        self._polygon = self.polygon_model_to_sympy_polygon(polygon_model)

    def split_by_plane(
            self,
            plane_normal: Point3DModel,
            plane_point: Point3DModel,
    ) -> Union[PolygonModel, Tuple[PolygonModel, PolygonModel]]:
        plane = Plane(tuple(plane_point.__root__), normal_vector=tuple(plane_normal.__root__))

        intersection_line_points = self._polygon.intersection(plane)

        if not intersection_line_points or len(intersection_line_points) == 1:
            return self._polygon_model

        if len(intersection_line_points) == 2:
            if intersection_line_points[0] in self._polygon.vertices \
                    or intersection_line_points[1] in self._polygon.vertices:
                return self._polygon_model

        polygon1, polygon2 = self._polygon.cut_section(
            Line2D(
                Point(intersection_line_points[0].x, intersection_line_points[0].y),
                Point(intersection_line_points[1].x, intersection_line_points[1].y)
            )
        )
        return self.sympy_polygon_to_polygon_model(polygon1), self.sympy_polygon_to_polygon_model(polygon2)
