from fastapi import FastAPI, HTTPException
from typing import Union, Tuple

from src.data_model import SplittingRequestData, SplittingResponseData, PolygonModel, EmptyPolygonModel
from src.polygon_splitter import SympyPolygonSplitter


app = FastAPI()


@app.post("/split-polygon-by-plane")
def split_polygon_by_plane(splitting_request_data: SplittingRequestData) -> SplittingResponseData:
    try:
        splitted_polygons: Union[PolygonModel, Tuple[PolygonModel, PolygonModel]] = SympyPolygonSplitter(
            polygon_model=splitting_request_data.polygon,
        ).split_by_plane(
            plane_normal=splitting_request_data.plane.normal,
            plane_point=splitting_request_data.plane.point
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    if isinstance(splitted_polygons, tuple):
        return SplittingResponseData(
            polygon1=splitted_polygons[0],
            polygon2=splitted_polygons[1]
        )
    return SplittingResponseData(
        polygon1=splitting_request_data.polygon,
        polygon2=EmptyPolygonModel(__root__=[])
    )
