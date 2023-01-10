import vtk

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