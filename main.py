import vtk

def create_ear_actor(reader, tissue):
    
    select_tissue = vtk.vtkImageThreshold()
    select_tissue.ThresholdBetween(tissue, tissue)
    select_tissue.SetInValue(255)
    select_tissue.SetOutValue(0)
    select_tissue.SetInputConnection(reader.GetOutputPort())

    iso_value = 63.5
    iso_surface = vtk.vtkFlyingEdges3D()

    iso_surface.SetInputConnection(select_tissue.GetOutputPort())
    iso_surface.ComputeScalarsOff()
    iso_surface.ComputeGradientsOff()
    iso_surface.ComputeNormalsOn()
    iso_surface.SetValue(0, iso_value)

    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(iso_surface.GetOutputPort())

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
    lut.SetTableValue(1, colors.GetColor4d('salmon'))  # Temporal_Bone
    lut.SetTableValue(2, colors.GetColor4d('beige'))  # Tympanic_Membrane
    lut.SetTableValue(3, colors.GetColor4d('orange'))  # Facial_Nerve
    lut.SetTableValue(4, colors.GetColor4d('misty_rose'))  # Cochlear_Nerve
    lut.SetTableValue(5, colors.GetColor4d('white'))  # Labyrinth
    lut.SetTableValue(6, colors.GetColor4d('tomato'))  # Fenestra_Rotunda
    lut.SetTableValue(7, colors.GetColor4d('raspberry'))  # Incus_Bone
    lut.SetTableValue(8, colors.GetColor4d('banana'))  # Stapes_Bone
    lut.SetTableValue(9, colors.GetColor4d('peru'))  # Tensor_Tympani_Muscle
    lut.SetTableValue(10, colors.GetColor4d('pink'))  # Internal_Jugular_Vein
    lut.SetTableValue(11, colors.GetColor4d('powder_blue'))  # Osseous_Spiral_Lamina
    lut.SetTableValue(12, colors.GetColor4d('carrot'))  # Internal_Carotd_Artery
    lut.SetTableValue(13, colors.GetColor4d('wheat'))  # Vestibular_Nerve
    lut.SetTableValue(14, colors.GetColor4d('violet'))  # Stapedius_Muscle
    lut.SetTableValue(15, colors.GetColor4d('plum'))  # Malleus_Bone

    return lut

colors = vtk.vtkNamedColors()
rawData = 'rawData\Ear-CT.nrrd' # raw data location
segmentation = 'segmantation\Ear-seg.nrrd' # segmentation data location

# colors
colors.SetColor('AColor', [255, 0, 0, 255])
colors.SetColor('BColor', [0, 255, 0, 255])
colors.SetColor('BkgColor', [51, 77, 102, 255])

# reading raw data nrrd file
reader = vtk.vtkNrrdReader() 
reader.SetFileName(rawData)

# reading segmentation nrrd file
segment_reader = vtk.vtkNrrdReader() 
segment_reader.SetFileName(segmentation)
segment_reader.Update()


# creating actors for particular segments

lut = create_ear_lut(colors)

# List of segment indexes form EarAtlasColors.ctbl
indexes = (4, 5, 9, 10, 12, 14, 17, 19, 21, 23, 24, 25, 28, 140) 
actor_list = []
i = 2

for index in indexes:
    a = create_ear_actor(segment_reader, index)
    a.GetProperty().SetDiffuseColor(lut.GetTableValue(i)[:3]) # :3
    actor_list.append(a)
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

# renderer
ren1 = vtk.vtkRenderer()
ren1.SetBackground(0.1, 0.2, 0.4)
ren1.AddActor(outline)

# adding segmentation results
for actor in actor_list:
    ren1.AddActor(actor)
    
ren1.AddActor(sagittal)
ren1.AddActor(axial)
ren1.AddActor(coronal)


renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(900, 600)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()