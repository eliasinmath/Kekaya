import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon

# === Create figure ===
fig = plt.figure(figsize=(13, 9))
axes = [plt.subplot(2,2,i+1) for i in range(4)]
titles = [
    "Phase 1: Needle in Triangle",
    "Phase 2: Split Triangle",
    "Phase 3: Overlap Triangles",
    "Phase 4: Small-Area Fractal-like Set"
]

for ax, t in zip(axes, titles):å
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.set_title(t, fontsize=11)
    ax.grid(alpha=0.3)

ax1, ax2, ax3, ax4 = axes

# === Basic triangle ===
tri_base = np.array([[0,0],[2,0],[1,2]])
ax1.add_patch(Polygon(tri_base, color='lightblue', alpha=0.3))

needle1, = ax1.plot([], [], 'r-', lw=3)

# === Split triangles ===
tri2_patches = [Polygon([[0,0],[0,0],[0,0]], color='red', alpha=0.4) for _ in range(4)]
for p in tri2_patches: ax2.add_patch(p)

# === Overlap ===
tri3_patches = [Polygon([[0,0],[0,0],[0,0]], color='purple', alpha=0.3) for _ in range(5)]
for p in tri3_patches: ax3.add_patch(p)

# === Fractal-like point cloud ===
scatter4 = ax4.scatter([], [], s=3, color='blue', alpha=0.4)

def simple_fractal(level=3):
    pts = [(1,1)]
    for l in range(level):
        new = []
        for x,y in pts:
            for a in np.linspace(0,2*np.pi,5):
                new.append((x+0.4**l*np.cos(a), y+0.4**l*np.sin(a)))
        pts = new
    return np.array(pts)

# === Animation function ===
def update(f):
    phase = f // 60  # decide phase (0–3)
    t = (f % 60) / 60

    # === phase 1 ===
    if phase == 0:
        # rotating needle
        angle = t * 2 * np.pi
        x2, y2 = 1 + 0.8*np.cos(angle), 1 + 0.8*np.sin(angle)
        needle1.set_data([1,x2],[1,y2])

    # === phase 2 ===
    elif phase == 1:
        # split triangle into 4 and move outwards a bit
        A,B,C = tri_base
        midAB = (A+B)/2
        midAC = (A+C)/2
        midBC = (B+C)/2
        tris = [
            [A, midAB, midAC],
            [midAB, B, midBC],
            [midAC, midBC, C],
            [midAB, midBC, midAC]
        ]
        offsets = [(0.15,0),(0.15,0.1),(0,0.15),(-0.1,0.1)]
        for patch, tri, off in zip(tri2_patches, tris, offsets):
            tri = np.array(tri) + t*np.array(off)
            patch.set_xy(tri)

    # === phase 3 ===
    elif phase == 2:
        center = np.array([1,1])
        for i, patch in enumerate(tri3_patches):
            angle = i * np.pi/4
            s = 0.8 - 0.3*t
            tri = []
            for k in range(3):
                a = angle + k*2*np.pi/3
                tri.append(center + s*np.array([np.cos(a), np.sin(a)]))
            patch.set_xy(tri)

    # === phase 4 ===
    elif phase == 3:
        pts = simple_fractal(level=2 + int(t*2))
        scatter4.set_offsets(pts)

    return []

ani = FuncAnimation(fig, update, frames=240, interval=80, blit=False)
plt.tight_layout()
plt.show()
