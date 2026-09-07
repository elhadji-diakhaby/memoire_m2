import argparse
import arcpy


def main():
    p = argparse.ArgumentParser(description="Rasterise un nuage LAS/LAZ par moyenne avec ArcGIS Pro.")
    p.add_argument("source_laz")
    p.add_argument("output_tif")
    p.add_argument("snap_raster")
    p.add_argument("--cell-size", type=float, default=1.0)
    p.add_argument("--epsg", type=int, default=2154)
    p.add_argument("--lasd", default="temp.lasd")
    args = p.parse_args()
    arcpy.env.overwriteOutput = True
    sr = arcpy.SpatialReference(args.epsg)
    arcpy.management.CreateLasDataset([args.source_laz], args.lasd, spatial_reference=sr, compute_stats="NO_COMPUTE_STATS")
    arcpy.env.outputCoordinateSystem = sr
    arcpy.env.snapRaster = args.snap_raster
    arcpy.env.extent = args.snap_raster
    arcpy.env.cellSize = args.cell_size
    arcpy.env.compression = "NONE"
    arcpy.conversion.LasDatasetToRaster(args.lasd, args.output_tif, "ELEVATION", "BINNING AVERAGE NONE", "FLOAT", "CELLSIZE", args.cell_size, 1.0)


if __name__ == "__main__":
    main()
