import vtk
from ear_actor import *
from color_palette import *
from sliders import *

if __name__ == '__main__':
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
    
    # setting window properties
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
    axial.SetDisplayExtent(0, 510, 0, 510, 200, 200)
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