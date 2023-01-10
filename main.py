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

def create_ear_lut(colors):
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfColors(16)
    lut.SetTableRange(0, 15)
    lut.Build()

    lut.SetTableValue(0, colors.GetColor4d('Black'))
    lut.SetTableValue(1, colors.GetColor4d('black'))  # Temporal_Bone
    lut.SetTableValue(2, colors.GetColor4d('salmon'))  # Tympanic_Membrane
    lut.SetTableValue(3, colors.GetColor4d('van_dyke_brown'))  # Facial_Nerve
    lut.SetTableValue(4, colors.GetColor4d('olive_drab'))  # Cochlear_Nerve
    lut.SetTableValue(5, colors.GetColor4d('indigo'))  # Labyrinth
    lut.SetTableValue(6, colors.GetColor4d('cobalt'))  # Fenestra_Rotunda
    lut.SetTableValue(7, colors.GetColor4d('raspberry'))  # Incus_Bone
    lut.SetTableValue(8, colors.GetColor4d('banana'))  # Stapes_Bone
    lut.SetTableValue(9, colors.GetColor4d('greenish_umber'))  # Tensor_Tympani_Muscle
    lut.SetTableValue(10, colors.GetColor4d('peacock'))  # Internal_Jugular_Vein
    lut.SetTableValue(11, colors.GetColor4d('aquamarine_medium'))  # Osseous_Spiral_Lamina
    lut.SetTableValue(12, colors.GetColor4d('carrot'))  # Internal_Carotd_Artery
    lut.SetTableValue(13, colors.GetColor4d('cobalt_green'))  # Vestibular_Nerve
    lut.SetTableValue(14, colors.GetColor4d('violet'))  # Stapedius_Muscle
    lut.SetTableValue(15, colors.GetColor4d('warm_grey'))  # Malleus_Bone

    return lut

def make_slider_widget(properties, colors, lut, idx):
    slider = vtk.vtkSliderRepresentation2D()

    slider.SetMinimumValue(properties.value_minimum)
    slider.SetMaximumValue(properties.value_maximum)
    slider.SetValue(properties.value_initial)
    slider.SetTitleText(properties.title)

    slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    slider.GetPoint1Coordinate().SetValue(properties.p1[0], properties.p1[1])
    slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    slider.GetPoint2Coordinate().SetValue(properties.p2[0], properties.p2[1])

    slider.SetTubeWidth(properties.tube_width)
    slider.SetSliderLength(properties.slider_length)
    slider.SetSliderWidth(properties.slider_width)
    slider.SetTitleHeight(properties.title_height)
    slider.SetLabelHeight(properties.label_height)

    # Set the color properties
    # Change the color of the bar.
    slider.GetSliderProperty().SetColor(colors.GetColor3d(properties.slider_color))
    # Change the color of the ends of the bar.
    slider.GetCapProperty().SetColor(colors.GetColor3d(properties.bar_ends_color))
    # Change the color of the knob that slides.
    slider.GetTitleProperty().SetColor(colors.GetColor3d(properties.title_color))
    # Change the color of the knob when the mouse is held on it.
    slider.GetSelectedProperty().SetColor(colors.GetColor3d(properties.selected_color))
    # Change the color of the text displaying the value.
    slider.GetLabelProperty().SetColor(colors.GetColor3d(properties.value_color))
    # Change the color of the text indicating what the slider controls
    if idx in range(0, 16):
        slider.GetTubeProperty().SetColor(lut.GetTableValue(idx)[:3])
    else:
        slider.GetTubeProperty().SetColor(colors.GetColor3d(properties.title_color))

    slider_widget = vtk.vtkSliderWidget()
    slider_widget.SetRepresentation(slider)

    return slider_widget

# how the slider will be displayed
class SliderProperties:
    tube_width = 0.008
    slider_length = 0.05
    slider_width = 0.015
    title_height = 0.02
    label_height = 0.01

    value_minimum = 0.0
    value_maximum = 1.0
    value_initial = 1.0

    p1 = [0.1, 0.1]
    p2 = [0.3, 0.1]

    title = None

    title_color = 'Gray'
    value_color = 'Gray'
    slider_color = 'Black'
    selected_color = 'Gray'
    bar_color = 'Black'
    bar_ends_color = 'Black'

# callback determining what slider will do on value change
class SliderCB:
    def __init__(self, actor_property):
        self.actorProperty = actor_property

    def __call__(self, caller, ev):
        slider_widget = caller
        value = slider_widget.GetRepresentation().GetValue()
        self.actorProperty.SetOpacity(value)

colors = vtk.vtkNamedColors()
rawData = 'rawData\Ear-CT.nrrd' # raw data location
segmentation = 'segmantation\Ear-seg.nrrd' # segmentation data location

# elements that will be used with indexes form EarAtlasColors.ctbl
elements = {"Tympanic membrane" : 4, "Facial nerve" : 5, "Cochlear nerve" : 9, "Labirynth" : 10, "Fenestra rotunda" : 12,
            "Incus bone" : 14, "Stapes bone" : 17, "Tensor tympani muscle" : 19, "Internal jugular vein" : 21, "Osseous spiral lamina" : 23,
            "Internal carotid artery" : 24, "Vestibular nerve" : 25, "Stapedius muscle" : 28, "Malleus bone" : 140}

# colors
colors.SetColor('BkgColor', [51, 77, 102, 255])

# reading raw data nrrd file
reader = vtk.vtkNrrdReader() 
reader.SetFileName(rawData)

# reading segmentation nrrd file
segment_reader = vtk.vtkNrrdReader() 
segment_reader.SetFileName(segmentation)
segment_reader.Update()

# for sliders that will be rendered in menu
sliders = dict()
step_size = 1.0 / 15
pos_y = 0.075

# creating actors for particular segments
lut = create_ear_lut(colors)

# List of segment indexes form EarAtlasColors.ctbl
actor_list = []
i = 2

# Create renderers
ren1 = vtk.vtkRenderer()
ren1.SetBackground(0.1, 0.2, 0.4)

# slider renderer
ren2 = vtk.vtkRenderer()
ren2.SetBackground(colors.GetColor3d('Lavender'))

ren1.SetViewport(0.0, 0.0, 0.7, 1.0)
ren2.SetViewport(0.7, 0.0, 1, 1)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)
renWin.SetSize(1200, 900)
renWin.SetWindowName('IEA')

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(renWin)

for element, element_index in elements.items():
    a = create_smooth_ear_actor(segment_reader, element_index)
    a.GetProperty().SetDiffuseColor(lut.GetTableValue(i)[:3]) # :3
    actor_list.append(a)
    
    # creating slider
    slider_properties = SliderProperties()
    slider_properties.value_initial = 1
    slider_properties.title = element
    # Screen coordinates
    slider_properties.p1 = [0.05, pos_y]
    slider_properties.p2 = [0.25, pos_y]
    pos_y += step_size
    cb = SliderCB(a.GetProperty())

    slider_widget = make_slider_widget(slider_properties, colors, lut, i)
    slider_widget.SetCurrentRenderer(ren2)
    slider_widget.SetInteractor(render_window_interactor)
    slider_widget.SetAnimationModeToJump()
    slider_widget.EnabledOn()
    slider_widget.AddObserver(vtk.vtkCommand.InteractionEvent, cb)
    sliders[element] = slider_widget
    
    i = i + 1

# outlines
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(segment_reader.GetOutputPort())

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(colors.GetColor3d("White")) 

# lookup table for planes
# Start by creating a black/white lookup table.
bw_lut = vtk.vtkLookupTable()
bw_lut.SetTableRange(-980, 5144)
bw_lut.SetSaturationRange(0, 0)
bw_lut.SetHueRange(0, 0)
bw_lut.SetValueRange(0.2, 0.7)
bw_lut.Build()  # effective built

# sagittal
sagittal_colors = vtk.vtkImageMapToColors()
sagittal_colors.SetInputConnection(reader.GetOutputPort())
sagittal_colors.SetLookupTable(bw_lut)
sagittal_colors.Update()

sagittal = vtk.vtkImageActor()
sagittal.GetMapper().SetInputConnection(sagittal_colors.GetOutputPort())
sagittal.SetDisplayExtent(255, 255, 0, 510, 0, 510)
sagittal.ForceOpaqueOn()

# axial
axial_colors = vtk.vtkImageMapToColors()
axial_colors.SetInputConnection(reader.GetOutputPort())
axial_colors.SetLookupTable(bw_lut)
axial_colors.Update()

axial = vtk.vtkImageActor()
axial.GetMapper().SetInputConnection(axial_colors.GetOutputPort())
axial.SetDisplayExtent(0, 510, 0, 510, 255, 255)
axial.ForceOpaqueOn()

# coronal
coronal_colors = vtk.vtkImageMapToColors()
coronal_colors.SetInputConnection(reader.GetOutputPort())
coronal_colors.SetLookupTable(bw_lut)
coronal_colors.Update()

coronal = vtk.vtkImageActor()
coronal.GetMapper().SetInputConnection(coronal_colors.GetOutputPort())
coronal.SetDisplayExtent(0, 510, 255, 255, 0, 510)
coronal.ForceOpaqueOn()

# renderer actors
ren1.AddActor(outline)

# adding segmentation results
for actor in actor_list:
    ren1.AddActor(actor)
    
ren1.AddActor(sagittal)
ren1.AddActor(axial)
ren1.AddActor(coronal)


style = vtk.vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)


render_window_interactor.Start()