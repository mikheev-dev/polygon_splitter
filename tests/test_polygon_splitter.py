from fastapi.testclient import TestClient

import pytest

from service import app

client = TestClient(app)


@pytest.mark.parametrize(
    'polygon',
    [
        [[0, 0], [0, 1], [1, 0], [1, 1]],
        [[0, 0], [0, 1], [1, 1], [0.5, 0.5], [1, 0]],
    ]
)
def test_convex_polygon_validator(polygon):
    response = client.post(
        "/split-polygon-by-plane",
        json={
          "polygon": polygon,
          "plane": {
            "point": [0, 0, 0],
            "normal": [-0.5, -0.5, 0]
          }
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Polygon is not convex."


def test_plane_normal_is_not_zero_validator():
    response = client.post(
        "/split-polygon-by-plane",
        json={
          "polygon": [[0, 0], [0, 1], [1, 1], [1, 0]],
          "plane": {
            "point": [10, 10, -3],
            "normal": [0, 0, 0]
          }
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Plane normal could not be a zero vector."


@pytest.mark.parametrize(
    'point, normal',
    [
        ([0, 0, 0], [0, 0, 1]),
        ([0, 0, 0], [0, 0, -1]),
        ([10, 10, -3], [-0.5, 0, 0.5]),
        ([10, 10, -3], [-0.5, 0.3, 0.5])
    ]
)
def test_plane_is_not_orthogonal_to_polygon(point, normal):
    response = client.post(
        "/split-polygon-by-plane",
        json={
          "polygon": [[0, 0], [0, 1], [1, 1], [1, 0]],
          "plane": {
            "point": point,
            "normal": normal
          }
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Plane should be orthogonal to the polygon."


@pytest.mark.parametrize(
    'point, normal',
    [
        ([0, 1, 10], [0, 5, 0]),
        ([0, 1, -10], [-0.5, 0.5, 0]),
        ([10, 10, -3], [0.5, 0.5, 0]),
    ]
)
def test_polygon_splitter_by_plane_no_intersection(point, normal):
    polygon = [[0, 0], [0, 1], [1, 1], [1, 0]]
    response = client.post(
        "/split-polygon-by-plane",
        json={
            "polygon": polygon,
            "plane": {
                "point": point,
                "normal": normal
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["polygon1"] == polygon
    assert response.json()["polygon2"] == []


@pytest.mark.parametrize(
    ('point', 'normal', 'expected_splitter_points'),
    [
        (
            [0.3, 0.7, 10],
            [0, 5, 0],
            [(0., 0.7), (1., 0.7)]
        ),
        (
            [0.5, 0.5, 4],
            [-3, 3, 0],
            []
        ),
        (
            [1, 0.4, 4],
            [3, 3, 0],
            [(0.4, 1.), (1, 0.4)]
        ),
        (
            [0, 0, 0],
            [0.66, -1, 0],
            [(1, 0.66)]
        ),
    ]
)
def test_polygon_splitter_by_plane(point, normal, expected_splitter_points):
    polygon = [[0., 0.], [0., 1.], [1., 1.], [1., 0.]]
    response = client.post(
        "/split-polygon-by-plane",
        json={
            "polygon": polygon,
            "plane": {
                "point": point,
                "normal": normal
            }
        }
    )
    assert response.status_code == 200

    connected_response_polygons = response.json()["polygon1"] + response.json()["polygon2"]
    ps_in_original = list({tuple(p) for p in connected_response_polygons if p in polygon})
    ps_not_in_original = list({tuple(p) for p in connected_response_polygons if p not in polygon})

    assert sorted(ps_in_original) == list(map(tuple, sorted(polygon)))
    assert sorted(ps_not_in_original) == expected_splitter_points
