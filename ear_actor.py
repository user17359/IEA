import vtk

def create_smooth_ear_actor(reader, tissue):
    select_tissue = vtk.vtkImageThreshold()
    select_tissue.ThresholdBetween(tissue, tissue)
    select_tissue.SetInValue(255)
    select_tissue.SetOutValue(0)
    select_tissue.SetInputConnection(reader.GetOutputPort())

    gaussian_radius = 1
    gaussian_standard_deviation = 2.0
    gaussian = vtk.vtkImageGaussianSmooth()
    gaussian.SetStandardDeviations(gaussian_standard_deviation, gaussian_standard_deviation,
                                   gaussian_standard_deviation)
    gaussian.SetRadiusFactors(gaussian_radius, gaussian_radius, gaussian_radius)
    gaussian.SetInputConnection(select_tissue.GetOutputPort())

    iso_value = 127.5
    iso_surface = vtk.vtkFlyingEdges3D()
            
    iso_surface.SetInputConnection(gaussian.GetOutputPort())
    iso_surface.ComputeScalarsOff()
    iso_surface.ComputeGradientsOff()
    iso_surface.ComputeNormalsOff()
    iso_surface.SetValue(0, iso_value)

    
    smoothing_iterations = 20
    pass_band = 0.001
    feature_angle = 60.0
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputConnection(iso_surface.GetOutputPort())
    smoother.SetNumberOfIterations(smoothing_iterations)
    smoother.BoundarySmoothingOff()
    smoother.FeatureEdgeSmoothingOff()
    smoother.SetFeatureAngle(feature_angle)
    smoother.SetPassBand(pass_band)
    smoother.NonManifoldSmoothingOn()
    smoother.NormalizeCoordinatesOff()
    smoother.Update()

    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(smoother.GetOutputPort())
    normals.SetFeatureAngle(feature_angle)

    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(normals.GetOutputPort())

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(stripper.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor