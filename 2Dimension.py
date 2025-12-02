import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from matplotlib.patches import Polygon, FancyArrow
import math

# Set font and style
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Create figure and subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle('Kakeya Conjecture: Two Methods of Needle Rotation', fontsize=16, fontweight='bold')

# ========== Left Plot: Rotating 360 degrees around a point ==========
ax1 = axes[0]
ax1.set_xlim(-1.2, 1.2)
ax1.set_ylim(-1.2, 1.2)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)
ax1.set_title('Method 1: Rotate 360° around an endpoint', fontsize=14)

# Initial needle position (horizontal, length=1)
needle_length = 1.0
initial_needle = plt.Line2D([0, needle_length], [0, 0], color='red', linewidth=3, label='Needle')
ax1.add_line(initial_needle)

# Circular swept area
circle = patches.Circle((0, 0), needle_length, alpha=0.2, color='blue', label='Swept Area')
ax1.add_patch(circle)

# Rotation center point
center_point = plt.Circle((0, 0), 0.03, color='black', zorder=5)
ax1.add_patch(center_point)

# Calculate area
circle_area = math.pi * needle_length ** 2
ax1.text(0, -1.1, f'Swept Area = π×1² ≈ {circle_area:.3f}', 
         ha='center', fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))

# Animation variables
current_angle1 = 0
needle_line1 = plt.Line2D([0, 0], [0, 0], color='red', linewidth=3)
ax1.add_line(needle_line1)

# Direction arrow (left plot)
dir_arrow1 = ax1.arrow(0, 0, 0, 0, head_width=0.05, head_length=0.08, 
                      fc='darkred', ec='darkred', alpha=0)

ax1.legend(loc='upper right')

# ========== Right Plot: Sliding inside an equilateral triangle ==========
ax2 = axes[1]
ax2.set_xlim(-0.1, 1.1)
ax2.set_ylim(-0.1, 1.0)
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)
ax2.set_title('Method 2: Sliding inside an equilateral triangle', fontsize=14)

# Equilateral triangle (height=1)
triangle_height = 1.0
triangle_side = 2 * triangle_height / math.sqrt(3)
triangle_base = triangle_side

# Triangle vertices
triangle_vertices = [
    [0, 0],  # Bottom left
    [triangle_base, 0],  # Bottom right
    [triangle_base / 2, triangle_height]  # Top
]

# Draw triangle
triangle_patch = Polygon(triangle_vertices, alpha=0.2, color='green', label='Triangle Swept Area')
ax2.add_patch(triangle_patch)

# Calculate triangle area
triangle_area = triangle_base * triangle_height / 2
ax2.text(triangle_base/2, -0.08, f'Swept Area ≈ {triangle_area:.3f}', 
         ha='center', fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))

# Initial needle position (base)
initial_triangle_needle = plt.Line2D([0, triangle_base], [0, 0], color='red', linewidth=3, label='Needle')
ax2.add_line(initial_triangle_needle)

# Animation variables
needle_line2 = plt.Line2D([0, 0], [0, 0], color='red', linewidth=3)
ax2.add_line(needle_line2)

# Direction arrow (right plot)
dir_arrow2 = ax2.arrow(0, 0, 0, 0, head_width=0.03, head_length=0.05, 
                      fc='darkred', ec='darkred', alpha=0)

# Mark sliding positions
ax2.scatter([0, triangle_base/2, triangle_base], [0, triangle_height, 0], 
           color='blue', s=50, zorder=5, alpha=0.7)
ax2.text(0, 0.05, 'A', fontsize=12, ha='right', va='bottom')
ax2.text(triangle_base, 0.05, 'B', fontsize=12, ha='left', va='bottom')
ax2.text(triangle_base/2, triangle_height+0.05, 'C', fontsize=12, ha='center', va='bottom')

ax2.legend(loc='upper right')

# ========== Animation Update Function ==========
def update(frame):
    # Update left plot (circular rotation)
    current_angle1 = frame % 360
    angle_rad = np.deg2rad(current_angle1)
    
    # Calculate needle endpoints
    x_end = needle_length * np.cos(angle_rad)
    y_end = needle_length * np.sin(angle_rad)
    
    # Update needle position
    needle_line1.set_data([0, x_end], [0, y_end])
    
    # Update left plot direction arrow
    arrow_length = 0.3
    arrow_x = arrow_length * np.cos(angle_rad + np.pi/2)
    arrow_y = arrow_length * np.sin(angle_rad + np.pi/2)
    mid_x = x_end / 2
    mid_y = y_end / 2
    
    # Create new arrow (simple method: remove old, add new)
    global dir_arrow1
    try:
        dir_arrow1.remove()
    except:
        pass
    
    dir_arrow1 = ax1.arrow(mid_x, mid_y, arrow_x, arrow_y, 
                          head_width=0.05, head_length=0.08, 
                          fc='darkred', ec='darkred')
    
    # Update right plot (triangle sliding)
    progress = (frame % 240) / 60  # 60 frames per phase
    
    if progress < 1:  # Phase 1: A to C (left side)
        alpha = progress
        x_start = 0 * (1 - alpha) + triangle_base/2 * alpha
        y_start = 0 * (1 - alpha) + triangle_height * alpha
        x_end_r = triangle_base * (1 - alpha) + triangle_base/2 * alpha
        y_end_r = 0 * (1 - alpha) + triangle_height * alpha
    elif progress < 2:  # Phase 2: C to B (right side)
        alpha = progress - 1
        x_start = triangle_base/2 * (1 - alpha) + triangle_base * alpha
        y_start = triangle_height * (1 - alpha) + 0 * alpha
        x_end_r = triangle_base/2 * (1 - alpha) + 0 * alpha
        y_end_r = triangle_height * (1 - alpha) + 0 * alpha
    elif progress < 3:  # Phase 3: B to A (base)
        alpha = progress - 2
        x_start = triangle_base * (1 - alpha) + 0 * alpha
        y_start = 0
        x_end_r = 0 * (1 - alpha) + triangle_base * alpha
        y_end_r = 0
    else:  # Phase 4: Return to start
        alpha = progress - 3
        x_start, y_start = 0, 0
        x_end_r, y_end_r = triangle_base, 0
    
    # Update needle position
    needle_line2.set_data([x_start, x_end_r], [y_start, y_end_r])
    
    # Update right plot direction arrow
    dx = x_end_r - x_start
    dy = y_end_r - y_start
    length = np.sqrt(dx**2 + dy**2)
    
    global dir_arrow2
    try:
        dir_arrow2.remove()
    except:
        pass
    
    if length > 0:
        # Calculate perpendicular direction (to the left of needle)
        perp_dx = -dy * 0.2 / length
        perp_dy = dx * 0.2 / length
        mid_x = (x_start + x_end_r) / 2
        mid_y = (y_start + y_end_r) / 2
        
        dir_arrow2 = ax2.arrow(mid_x, mid_y, perp_dx, perp_dy, 
                              head_width=0.03, head_length=0.05, 
                              fc='darkred', ec='darkred')
    else:
        # Create invisible arrow if length is zero
        dir_arrow2 = ax2.arrow(0, 0, 0, 0, alpha=0)
    
    return needle_line1, needle_line2, dir_arrow1, dir_arrow2

# Create animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), 
                    interval=50, blit=False, repeat=True)

# Add explanatory text
fig.text(0.05, 0.02, 
         'Left: Rotating needle 360° around an endpoint sweeps a full disk with area π ≈ 3.142\n'
         'Right: Sliding needle inside an equilateral triangle (A→C→B→A) sweeps only the triangle with area ≈ 0.433\n'
         'Conclusion: The triangle method achieves needle reversal with much smaller swept area',
         fontsize=11, style='italic', bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))

plt.tight_layout(rect=[0, 0.1, 1, 0.95])
plt.show()

# Optional: Save as gif (requires pillow)
# ani.save('kakeya_animation.gif', writer='pillow', fps=20)

print("Animation started!")
print("Left: Needle rotates 360° around endpoint, sweeps circular area ≈ 3.142")
print("Right: Needle slides inside equilateral triangle, sweeps triangular area ≈ 0.433")
print("Press Ctrl+C or close window to stop animation")
