"""GeoJSON helper utilities for simple coordinate conversions and simplification."""

from __future__ import annotations

import json
from dataclasses import dataclass
from math import atan, exp, pi
from pathlib import Path
from typing import Iterable, Literal


Radians = float
Degrees = float


def mercator_to_lon_lat(x: float, y: float) -> tuple[Degrees, Degrees]:
    """Convert Web Mercator (EPSG:3857) coordinates to longitude/latitude degrees."""
    radius = 6378137.0
    lon = (x / radius) * 180.0 / pi
    lat = (2.0 * atan(exp(y / radius)) - pi / 2.0) * 180.0 / pi
    return lon, lat


def _downsample_ring(
    ring: list[list[float]], keep_ratio: float, *, min_points: int
) -> list[list[float]]:
    """Downsample a polygon ring by keeping approximately keep_ratio of points."""
    if not 0 < keep_ratio <= 1:
        raise ValueError("keep_ratio must be within (0, 1].")

    n_points = len(ring)
    if n_points <= min_points:
        return ring

    target_count = max(min_points, int(n_points * keep_ratio))
    target_count = min(n_points, target_count)

    if target_count >= n_points:
        return ring

    step = (n_points - 1) / (target_count - 1)
    result: list[list[float]] = []
    idx = 0.0
    for _ in range(target_count - 1):
        result.append(ring[int(idx)])
        idx += step
    result.append(ring[-1])

    if result[0] != result[-1]:
        result.append(result[0])
    return result


def _convert_ring_to_lonlat(ring: list[list[float]]) -> list[list[float]]:
    return [list(mercator_to_lon_lat(*point[:2])) for point in ring]


def _simplify_ring(ring: list[list[float]], keep_ratio: float, *, min_points: int) -> list[list[float]]:
    return _downsample_ring(ring, keep_ratio, min_points=min_points)


def convert_and_simplify_geometry(
    geometry: dict, keep_ratio: float, *, convert_mercator: bool
) -> dict:
    """Optionally convert geometry to lon/lat and drop vertices based on keep_ratio."""
    geom_type = geometry.get("type")
    coords = geometry.get("coordinates", [])

    if geom_type == "Polygon":
        processed: list[list[list[float]]] = []
        for idx, ring in enumerate(coords):
            coords_ring = (
                _convert_ring_to_lonlat(ring) if convert_mercator else ring
            )
            ring_keep = keep_ratio if idx > 0 else max(keep_ratio, 0.3)
            min_points = 30 if idx > 0 else 60
            processed.append(_simplify_ring(coords_ring, ring_keep, min_points=min_points))
        geometry["coordinates"] = processed
    elif geom_type == "MultiPolygon":
        processed_polygons: list[list[list[list[float]]]] = []
        for polygon in coords:
            processed_polygon: list[list[list[float]]] = []
            for idx, ring in enumerate(polygon):
                coords_ring = (
                    _convert_ring_to_lonlat(ring) if convert_mercator else ring
                )
                ring_keep = keep_ratio if idx > 0 else max(keep_ratio, 0.3)
                min_points = 30 if idx > 0 else 60
                processed_polygon.append(_simplify_ring(coords_ring, ring_keep, min_points=min_points))
            processed_polygons.append(processed_polygon)
        geometry["coordinates"] = processed_polygons
    else:
        raise ValueError(f"Unsupported geometry type: {geom_type}")

    return geometry


@dataclass(frozen=True)
class SimplifyConfig:
    source: Path
    target: Path
    keep_ratio: float = 0.2  # keep ~20% of the points


def simplify_region_geojson(config: SimplifyConfig) -> None:
    with config.source.open(encoding="utf-8") as f:
        data = json.load(f)

    crs_name = data.get("crs", {}).get("properties", {}).get("name", "")
    needs_projection_fix = "3857" in crs_name or "webmercator" in crs_name.lower()

    for feature in data.get("features", []):
        props = feature.setdefault("properties", {})
        feature["geometry"] = convert_and_simplify_geometry(
            feature.get("geometry", {}),
            keep_ratio=config.keep_ratio,
            convert_mercator=needs_projection_fix,
        )

        code = (
            props.get("region_code")
            or props.get("regionskode")
            or props.get("REGIONCODE")
            or props.get("regionscode")
        )
        name = props.get("region_name") or props.get("REGIONNAVN")

        props["region_code"] = str(code) if code is not None else ""
        props["region_name"] = str(name) if name is not None else ""

    data.pop("crs", None)
    with config.target.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def _add_points_to_ring(ring: list[list[float]], extra_points: int) -> list[list[float]]:
    if extra_points <= 0 or len(ring) < 2:
        return ring

    closed = ring[0] == ring[-1]
    working = ring[:] if closed else ring + [ring[0]]
    segments = len(working) - 1

    base = extra_points // segments
    remainder = extra_points % segments

    new_ring: list[list[float]] = []
    for idx in range(segments):
        start = working[idx]
        end = working[idx + 1]
        new_ring.append(start)

        extra = base + (1 if idx < remainder else 0)
        for j in range(1, extra + 1):
            t = j / (extra + 1)
            new_ring.append(
                [
                    start[0] + (end[0] - start[0]) * t,
                    start[1] + (end[1] - start[1]) * t,
                ]
            )

    new_ring.append(working[-1])
    return new_ring


def densify_simple_regions_geojson(
    source: Path, target: Path, extra_points: int = 100
) -> None:
    with source.open(encoding="utf-8") as f:
        data = json.load(f)

    features = []
    for feature in data.get("features", []):
        geometry = feature.get("geometry", {})
        geom_type = geometry.get("type")
        coords = geometry.get("coordinates", [])

        if geom_type == "Polygon":
            new_coords = [
                _add_points_to_ring(ring, extra_points) for ring in coords
            ]
        elif geom_type == "MultiPolygon":
            new_coords = [
                [_add_points_to_ring(ring, extra_points) for ring in polygon]
                for polygon in coords
            ]
        else:
            raise ValueError(f"Unsupported geometry type: {geom_type}")

        features.append(
            {
                "type": "Feature",
                "properties": feature.get("properties", {}),
                "geometry": {"type": geom_type, "coordinates": new_coords},
            }
        )

    output = {
        "type": data.get("type", "FeatureCollection"),
        "name": "denmark_regions",
        "features": features,
    }
    with target.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)


def export_regioner_to_denmark_geojson(source: Path, target: Path) -> None:
    with source.open(encoding="utf-8") as f:
        data = json.load(f)

    crs_name = data.get("crs", {}).get("properties", {}).get("name", "")
    convert_mercator = "3857" in crs_name or "webmercator" in crs_name.lower()

    features: list[dict] = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        code = str(
            props.get("region_code")
            or props.get("regionskode")
            or props.get("REGIONCODE")
            or props.get("regionscode")
            or ""
        ).strip()
        name = props.get("region_name") or props.get("REGIONNAVN") or code

        geometry = convert_and_simplify_geometry(
            feature.get("geometry", {}),
            keep_ratio=1.0,
            convert_mercator=convert_mercator,
        )

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "region_code": code,
                    "region_name": name,
                },
                "geometry": geometry,
            }
        )

    collection = {
        "type": "FeatureCollection",
        "name": "denmark_regions",
        "features": features,
    }
    with target.open("w", encoding="utf-8") as f:
        json.dump(collection, f, ensure_ascii=False)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    source = project_root / "data" / "regioner.geojson"
    simplified = project_root / "data" / "geo" / "regioner_simplified.geojson"
    simplify_region_geojson(SimplifyConfig(source=source, target=simplified))

    denmark_regions_target = project_root / "data" / "geo" / "denmark_regions.geojson"
    export_regioner_to_denmark_geojson(source, denmark_regions_target)


if __name__ == "__main__":
    main()
