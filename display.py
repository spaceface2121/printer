from screeninfo import get_monitors
import pyglet
from screeninfo import Monitor
from PIL import Image
import time

def display_layers_on_hdmi(monitor: Monitor, layers, delay=1):
    # Create a pyglet window on the selected monitor
    window = pyglet.window.Window(fullscreen=True, width=monitor.width, height=monitor.height)
    window.set_location(monitor.x, monitor.y)
    
    current_layer = [0]  # Using a list to allow modification in inner function scope
    pyglet_image = [None]  # Store the current image to display

    def update_layer(dt):
        if current_layer[0] < len(layers):
            # Convert the current 2D array layer to an image
            image_array = layers[current_layer[0]]
            image = Image.fromarray(image_array * 255)
            image_data = image.tobytes()
            width, height = image.size
            pyglet_image[0] = pyglet.image.ImageData(width, height, 'L', image_data)

            print(f"Displaying layer {current_layer[0]+1}/{len(layers)}")

            current_layer[0] += 1
        else:
            pyglet.app.exit()  # Exit the event loop when all layers are displayed
        
    @window.event
    def on_draw():
        window.clear()
        if pyglet_image[0]:
            pyglet_image[0].blit(0, 0)

    # Schedule the update function to run periodically
    pyglet.clock.schedule_interval(update_layer, delay)

    pyglet.app.run()

def list_hdmi_outputs():
    monitors = get_monitors()
    hdmi_outputs = []
    for i, monitor in enumerate(monitors):
        print(f"Monitor {i}: {monitor.name} ({monitor.width}x{monitor.height})")
        hdmi_outputs.append(monitor)
    return hdmi_outputs