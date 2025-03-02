import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io  # Import io module to handle in-memory file

# Streamlit Sidebar Inputs
st.sidebar.header("Plot Settings")
plot_width = st.sidebar.number_input("Plot Width (m)", min_value=1, value=40, step=1)
plot_height = st.sidebar.number_input("Plot Height (m)", min_value=1, value=30, step=1)
tilt_angle = st.sidebar.number_input("Tilt Angle from North (°)", min_value=-180, max_value=180, value=0, step=1)

def rotate_point(x, y, angle, cx, cy):
    rad = np.radians(angle)
    x_rot = cx + (x - cx) * np.cos(rad) - (y - cy) * np.sin(rad)
    y_rot = cy + (x - cx) * np.sin(rad) + (y - cy) * np.cos(rad)
    return x_rot, y_rot

# Define Plot Center
Cx, Cy = plot_width / 2, plot_height / 2

# Create Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, plot_width)
ax.set_ylim(0, plot_height)

# Define plot boundary points
# boundary_points = [(0, 0), (plot_width, 0), (plot_width, plot_height), (0, plot_height), (0, 0)]
# rotated_boundary = [rotate_point(x, y, tilt_angle, Cx, Cy) for x, y in boundary_points]
# rot_x, rot_y = zip(*rotated_boundary)
# ax.plot(rot_x, rot_y, 'k-', linewidth=2)  # Keeping the outer boundary

# Draw Axes (rotated)
north_x, north_y = rotate_point(Cx, plot_height, tilt_angle, Cx, Cy)
ax.plot([Cx, north_x], [Cy, north_y], 'b--', linewidth=1.5, label="North Axis")
east_x, east_y = rotate_point(plot_width, Cy, tilt_angle, Cx, Cy)
ax.plot([Cx, east_x], [Cy, east_y], 'r--', linewidth=1.5, label="East Axis")

# Draw Vaastu Zones (rotated)
start_angle = 11.25  # Vaastu base angle
angles = np.linspace(start_angle, start_angle + 360, 17)  # 16 zones
for angle in angles:
    adjusted_angle = angle + tilt_angle  # Apply rotation
    rad = np.radians(adjusted_angle)
    x_end = Cx + max(plot_width, plot_height) * np.cos(rad)
    y_end = Cy + max(plot_width, plot_height) * np.sin(rad)
    ax.plot([Cx, x_end], [Cy, y_end], 'g-', linewidth=1.2, alpha=0.7)

# Labels
ax.set_title("Vaastu Zone Chart", fontsize=14)
ax.set_aspect(aspect=1)

# Display in Streamlit
st.pyplot(fig)

# Save figure as binary data in memory
img_buffer = io.BytesIO()
fig.savefig(img_buffer, format="png")  # Save figure to memory buffer
img_buffer.seek(0)  # Move cursor to the start of the buffer

# Download Option
st.sidebar.download_button(
    label="Download Chart as PNG",
    # data=fig.savefig("vaastu_chart.png"),
     data=img_buffer,  # Pass the in-memory file
    file_name="vaastu_chart.png",
    mime="image/png"
)
