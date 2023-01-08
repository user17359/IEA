import vtk

colors = vtk.vtkNamedColors()
fileName = 'rawData\Ear-CT.nrrd' # raw data location

# colors
colors.SetColor('SkinColor', [240, 184, 160, 255])
colors.SetColor('BackfaceColor', [255, 229, 200, 255])
colors.SetColor('BkgColor', [51, 77, 102, 255])


reader = vtk.vtkNrrdReader() # reading nrrd file
reader.SetFileName(fileName)

# skin mapper
skin_extractor = vtk.vtkMarchingCubes()
skin_extractor.SetInputConnection(reader.GetOutputPort())
skin_extractor.SetValue(0, 500)

skin_mapper = vtk.vtkPolyDataMapper()
skin_mapper.SetInputConnection(skin_extractor.GetOutputPort())
skin_mapper.ScalarVisibilityOff()

skin = vtk.vtkActor()
skin.SetMapper(skin_mapper)
skin.GetProperty().SetDiffuseColor(colors.GetColor3d('SkinColor'))

back_prop = vtk.vtkProperty()
back_prop.SetDiffuseColor(colors.GetColor3d('BackfaceColor'))
skin.SetBackfaceProperty(back_prop)

# outlines
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(colors.GetColor3d("White")) 


# renderer
ren1 = vtk.vtkRenderer()
ren1.SetBackground(0.1, 0.2, 0.4)
ren1.AddActor(outline)
ren1.AddActor(skin)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(300, 300)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()
