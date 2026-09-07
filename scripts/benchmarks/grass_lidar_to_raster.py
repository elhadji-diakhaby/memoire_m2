import argparse
import time
import grass.script as gs


def main():
    p = argparse.ArgumentParser(description="Rasterise un nuage LAS/LAZ par moyenne avec GRASS GIS.")
    p.add_argument("source_laz")
    p.add_argument("output_tif")
    p.add_argument("--west", type=float, required=True)
    p.add_argument("--south", type=float, required=True)
    p.add_argument("--east", type=float, required=True)
    p.add_argument("--north", type=float, required=True)
    p.add_argument("--resolution", type=float, default=1.0)
    args = p.parse_args()
    gs.run_command("g.region", w=args.west, s=args.south, e=args.east, n=args.north, res=args.resolution)
    t0 = time.perf_counter()
    gs.run_command("r.in.lidar", input=args.source_laz, output="lidar_mean", method="mean", type="FCELL", percent=100, overwrite=True)
    gs.run_command("r.out.gdal", input="lidar_mean", output=args.output_tif, format="GTiff", type="Float32", nodata=-9999, createopt="COMPRESS=NONE", overwrite=True)
    print(f"CORE_SECONDS={time.perf_counter() - t0}")


if __name__ == "__main__":
    main()
