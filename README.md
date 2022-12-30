# Polygon splitter

Polygon splitter is a small FastApi-based service, which :

1) get polygon's points (in 2D) and a plane (represented by normal and point in 3D), define projection line 
2) validate request by pydantic
3) validate is polygon convex, is plane orthogonal to polygon (in fact to XY plane), is plane normal non-zero
4) try to split polygon by plane on two polygons (except non-intersection case, intersection at one point, lying on the polygon's edge)

## Run service
Please, check you have make utility installed.

Firstly, prepare local virtual environment. For it use from the project root directory
```commandline
make dev-env
```

After that:
```commandline
make start
```

## Play with service
The easiest way to play with that service, which is run locally, is Swagger http://127.0.0.1:8000/docs

You can use this example to test:
```json
{
   "polygon": [[0, 0.5], [0.4, 1], [1, 0.3], [0.2, 0]],
   "plane": {
      "point": [0.4, 0.5, 5.1],
      "normal": [0, 1, 0]
   }
}
```

## Run tests
To run test, use:
```commandline
make test
```

## Cleaning
To clean virtualenv use:
```commandline
make clean-env
```
