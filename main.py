import display
import slicer

# Conversion parameters
MM_TO_PIXELS = 10
LAYER_THICKNESS_MM = 10

hdmi_outputs = display.list_hdmi_outputs()
selected_output = int(input("Select the HDMI output by entering the corresponding number: "))
selected_monitor = hdmi_outputs[selected_output]
monitor_resolution = (selected_monitor.width, selected_monitor.height)
stl_path = '3DBenchy.stl'
stl_model = slicer.load_stl(stl_path)
sliced_layers = slicer.slice_stl(stl_model, monitor_resolution, MM_TO_PIXELS, LAYER_THICKNESS_MM)
print("Slicing complete. Resulting 3D array shape:", sliced_layers.shape)
display.display_layers_on_hdmi(selected_monitor, sliced_layers, delay=5)