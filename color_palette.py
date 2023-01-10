import vtk

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