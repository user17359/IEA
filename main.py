import vtk

colors = vtk.vtkNamedColors()
fileName = 'rawData\Ear-CT.nrrd' # raw data location

reader = vtk.vtkNrrdReader() # reading nrrd file
reader.SetFileName(fileName)

outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(colors.GetColor3d("White")) 

ren1 = vtk.vtkRenderer()
ren1.SetBackground(0.1, 0.2, 0.4)
ren1.AddActor(outline)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(300, 300)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()
