import numpy as np
import matplotlib.pyplot as plt

# 创建一个更直观的演示
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Visualizing the Besicovitch Construction Step by Step', fontsize=16, fontweight='bold')

# 步骤1：初始三角形
ax1 = axes[0, 0]
triangle1 = np.array([[1, 0], [3, 0], [2, 2]])
ax1.add_patch(plt.Polygon(triangle1, alpha=0.7, color='blue'))
ax1.set_xlim(0, 4)
ax1.set_ylim(-0.5, 2.5)
ax1.set_aspect('equal')
ax1.set_title('Step 1: Initial Triangle')
ax1.text(2, -0.2, f'Area = 1.732', ha='center', fontsize=10, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))
# 添加方向指示
for angle in [0, 60, 120]:
    rad = np.deg2rad(angle)
    ax1.plot([2, 2+0.8*np.cos(rad)], [1, 1+0.8*np.sin(rad)], 'r-', alpha=0.5)

# 步骤2：第一次分割
ax2 = axes[0, 1]
# 分割三角形
t1 = np.array([[1, 0], [2, 0], [1.5, 1]])
t2 = np.array([[2, 0], [3, 0], [2.5, 1]])
t3 = np.array([[1.5, 1], [2.5, 1], [2, 2]])
ax2.add_patch(plt.Polygon(t1, alpha=0.7, color='red'))
ax2.add_patch(plt.Polygon(t2, alpha=0.7, color='green'))
ax2.add_patch(plt.Polygon(t3, alpha=0.7, color='blue'))
ax2.set_xlim(0, 4)
ax2.set_ylim(-0.5, 2.5)
ax2.set_aspect('equal')
ax2.set_title('Step 2: Split into 3 Triangles')
ax2.text(2, -0.2, f'Total Area = 1.732', ha='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))
# 更多方向
for angle in [0, 30, 60, 90, 120, 150]:
    rad = np.deg2rad(angle)
    ax2.plot([2, 2+0.8*np.cos(rad)], [1, 1+0.8*np.sin(rad)], 'r-', alpha=0.5)

# 步骤3：平移产生重叠
ax3 = axes[0, 2]
# 平移小三角形，使其重叠
t1_trans = t1 + [0.2, 0.1]
t2_trans = t2 + [-0.1, 0.2]
t3_trans = t3 + [0.1, -0.1]
ax3.add_patch(plt.Polygon(t1_trans, alpha=0.5, color='red'))
ax3.add_patch(plt.Polygon(t2_trans, alpha=0.5, color='green'))
ax3.add_patch(plt.Polygon(t3_trans, alpha=0.5, color='blue'))
ax3.set_xlim(0, 4)
ax3.set_ylim(-0.5, 2.5)
ax3.set_aspect('equal')
ax3.set_title('Step 3: Translate to Create Overlap')
ax3.text(2, -0.2, f'Effective Area < 1.732', ha='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))
# 更多方向
for angle in np.arange(0, 180, 15):
    rad = np.deg2rad(angle)
    ax3.plot([2, 2+0.8*np.cos(rad)], [1, 1+0.8*np.sin(rad)], 'r-', alpha=0.3)

# 步骤4：第二次分割
ax4 = axes[1, 0]
# 创建更小的三角形
small_triangles = []
for i in range(3):
    for j in range(4):
        x = 0.5 + i * 1.0 + (j % 2) * 0.3
        y = 0.2 + j * 0.5
        triangle = np.array([[x, y], [x+0.6, y], [x+0.3, y+0.6]])
        small_triangles.append(triangle)
        ax4.add_patch(plt.Polygon(triangle, alpha=0.4, color=plt.cm.tab20(i/3)))
ax4.set_xlim(0, 4)
ax4.set_ylim(-0.5, 2.5)
ax4.set_aspect('equal')
ax4.set_title('Step 4: Further Splitting')
ax4.text(2, -0.2, f'12 small triangles', ha='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

# 步骤5：大量重叠
ax5 = axes[1, 1]
# 创建高度重叠的三角形
for i in range(20):
    angle = i * 18  # 覆盖0-360度
    rad = np.deg2rad(angle)
    length = 0.8 + 0.4 * np.sin(i * 0.5)  # 变化长度
    
    # 创建指向不同方向的细长三角形
    center_x, center_y = 2, 1
    x1 = center_x
    y1 = center_y
    x2 = center_x + length * np.cos(rad)
    y2 = center_y + length * np.sin(rad)
    x3 = center_x + length * np.cos(rad + np.deg2rad(10))
    y3 = center_y + length * np.sin(rad + np.deg2rad(10))
    
    triangle = np.array([[x1, y1], [x2, y2], [x3, y3]])
    ax5.add_patch(plt.Polygon(triangle, alpha=0.1, color='blue'))
    
    # 画出中心方向线
    ax5.plot([center_x, x2], [center_y, y2], 'r-', alpha=0.2, linewidth=0.5)

ax5.set_xlim(0, 4)
ax5.set_ylim(-0.5, 2.5)
ax5.set_aspect('equal')
ax5.set_title('Step 5: Many Overlapping Triangles')
ax5.text(2, -0.2, f'High overlap, low effective area', ha='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

# 步骤6：极限情况 - 面积任意小
ax6 = axes[1, 2]
# 画出最终的理论Kakeya集
# 创建一些随机点来表示分形集合
np.random.seed(42)
n_points = 500
points = []
for _ in range(n_points):
    # 使用分形分布
    x, y = 2, 1
    for _ in range(10):
        if np.random.random() < 0.5:
            x = x/2 + 1
            y = y/2 + 0.5
        else:
            x = x/2 + 2
            y = y/2 + 1
    points.append([x, y])

points = np.array(points)
ax6.scatter(points[:, 0], points[:, 1], s=1, alpha=0.3, color='blue')

# 画出一些方向线
center_x, center_y = 2, 1
for angle in np.arange(0, 180, 10):
    rad = np.deg2rad(angle)
    length = 1.0
    x_end = center_x + length * np.cos(rad)
    y_end = center_y + length * np.sin(rad)
    ax6.plot([center_x, x_end], [center_y, y_end], 'r-', alpha=0.3, linewidth=1)

ax6.set_xlim(0, 4)
ax6.set_ylim(-0.5, 2.5)
ax6.set_aspect('equal')
ax6.set_title('Step 6: Limit Set (Area → 0)')
ax6.text(2, -0.2, f'Area < ε for any ε > 0', ha='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

plt.tight_layout()

# 添加总体说明
fig.text(0.02, 0.02, 
         'Key Insight: By infinitely repeating the process of splitting triangles and overlapping them cleverly,\n'
         'we can cover ALL directions while making the total area arbitrarily small.\n'
         'This is the essence of Besicovitch\'s proof that Kakeya sets can have zero area.',
         fontsize=11, style='italic', bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))

plt.show()

print("\n" + "="*80)
print("SUMMARY OF THE CONSTRUCTION:")
print("="*80)
print("1. Start with a triangle that covers a range of directions")
print("2. Split it into smaller triangles")
print("3. Translate the pieces so they overlap heavily")
print("4. Each piece still contains segments in its original direction range")
print("5. By arranging them cleverly, together they cover ALL directions")
print("6. Repeat this process infinitely many times")
print("7. In the limit, the area can be made smaller than any positive number ε")
print("8. But the set still contains a unit segment in EVERY direction")
print("\nThis proves the existence of Kakeya sets with Lebesgue measure ZERO!")
print("="*80)
