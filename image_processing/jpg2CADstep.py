import numpy as np
import cv2
from build123d import *
from ocp_vscode import show

# ================= 参数配置 =================
IMAGE_PATH = "test.jpg"
OUTPUT_STEP = "test2.step"
SCALE = 0.5                  # 坐标缩放比例
BLUR_KERNEL = (5,5)          # 去噪卷积核大小
ADAPTIVE_THRESH = True       # 使用自适应阈值
SMOOTH_KERNEL_SIZE = 11       # 平滑窗口大小（建议选择较小的奇数）
EPSILON = 1.0                # RDP算法允许的最大偏差（单位与CAD坐标一致）
COLLINEAR_THRESHOLD = 0.5    # 合并共线点的阈值，调节小突起的消除

# ---------------- 平滑函数 ----------------
def smooth_contour_points(points, kernel_size=5):
    """
    对轮廓点进行移动平均平滑处理，保持闭合曲线特性
    """
    pts = np.array(points)
    if kernel_size % 2 == 0:
        kernel_size += 1
    kernel = np.ones(kernel_size) / kernel_size
    pts_padded = np.pad(pts, ((kernel_size//2, kernel_size//2), (0,0)), mode='wrap')
    smoothed_pts = []
    for i in range(pts.shape[0]):
        window = pts_padded[i:i+kernel_size]
        smoothed_point = np.sum(window * kernel[:, None], axis=0)
        smoothed_pts.append(tuple(smoothed_point))
    return smoothed_pts

# ---------------- Ramer-Douglas-Peucker (RDP) 算法 ----------------
def rdp(points, epsilon):
    """
    递归实现 RDP 算法，简化点集
    :param points: list of (x, y)
    :param epsilon: 最大允许偏差
    :return: 简化后的点列表
    """
    if len(points) < 3:
        return points
    start = np.array(points[0])
    end = np.array(points[-1])
    line_vec = end - start
    line_length = np.linalg.norm(line_vec)
    if line_length == 0:
        dists = np.linalg.norm(np.array(points) - start, axis=1)
    else:
        line_unitvec = line_vec / line_length
        dists = []
        for p in points:
            p_vec = np.array(p) - start
            proj_length = np.dot(p_vec, line_unitvec)
            proj_point = start + proj_length * line_unitvec
            dist = np.linalg.norm(np.array(p) - proj_point)
            dists.append(dist)
        dists = np.array(dists)
    idx = np.argmax(dists)
    max_dist = dists[idx]
    if max_dist > epsilon:
        left = rdp(points[:idx+1], epsilon)
        right = rdp(points[idx:], epsilon)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]

# ---------------- 合并共线点函数 ----------------
def merge_collinear_points(points, threshold=COLLINEAR_THRESHOLD):
    """
    合并连续共线的点：对于连续三个点，如果中间点到直线的距离小于阈值，则去除中间点。
    """
    if len(points) < 3:
        return points
    new_points = [points[0]]
    for i in range(1, len(points)-1):
        A = np.array(new_points[-1])
        B = np.array(points[i])
        C = np.array(points[i+1])
        AC = C - A
        if np.linalg.norm(AC) == 0:
            continue
        # 计算B到直线AC的垂直距离
        distance = np.abs(np.cross(AC, B-A)) / np.linalg.norm(AC)
        if distance > threshold:
            new_points.append(points[i])
    new_points.append(points[-1])
    return new_points

# ================= 图像预处理 =================
img = cv2.imread(IMAGE_PATH)
assert img is not None, "无法读取图像文件，请检查路径"
cv2.imshow("1. 原始图像", img)
cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, BLUR_KERNEL, 0)

if ADAPTIVE_THRESH:
    thresh = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
else:
    _, thresh = cv2.threshold(gray, 0, 255, 
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 添加形态学闭运算，填补小空洞并消除噪点
kernel_morph = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_morph)

cv2.imshow("2. 二值化结果", thresh)
cv2.waitKey(0)

# ---------------- 轮廓检测 ----------------
# 使用 CHAIN_APPROX_NONE 保留所有细节点
contours, _ = cv2.findContours(
    thresh, 
    cv2.RETR_LIST,          
    cv2.CHAIN_APPROX_NONE
)

img_h, img_w = gray.shape
border_margin = 5  # 边框容差
valid_contours = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if not (x < border_margin or y < border_margin or (x+w) > img_w-border_margin or (y+h) > img_h-border_margin):
        valid_contours.append(cnt)

print(f"有效轮廓数量：{len(valid_contours)}")
assert len(valid_contours) > 0, "未检测到有效轮廓！"

valid_contours = sorted(valid_contours, key=cv2.contourArea, reverse=True)
target_contour = valid_contours[0]

contour_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
cv2.drawContours(contour_img, [target_contour], -1, (0,255,0), 2)
cv2.imshow("3. 目标轮廓", contour_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ---------------- CAD 坐标转换 ----------------
raw_points = []
for point in target_contour:
    x = (point[0][0] - img_w/2) * SCALE
    y = (img_h/2 - point[0][1]) * SCALE
    raw_points.append((x, y))

# 第一步平滑：减少锯齿状
smoothed_points = smooth_contour_points(raw_points, kernel_size=SMOOTH_KERNEL_SIZE)
# 第二步 RDP 算法简化：修正直线段并去除局部噪声
refined_points = rdp(smoothed_points, EPSILON)
# 第三步 合并共线点：消除小突起或迂回的小段
refined_points = merge_collinear_points(refined_points, threshold=COLLINEAR_THRESHOLD)

if not np.allclose(refined_points[0], refined_points[-1], atol=1e-3):
    print("⚠️ 轮廓未闭合，自动添加闭合点")
    refined_points.append(refined_points[0])

print(f"最终点数：{len(refined_points)}")
print(f"前几个点：{refined_points[:3]}")
xs = [p[0] for p in refined_points]
ys = [p[1] for p in refined_points]
print(f"点坐标范围：X({min(xs)} to {max(xs)}), Y({min(ys)} to {max(ys)})")

# ---------------- 创建 CAD 轮廓线 ----------------
with BuildLine() as outline:
    try:
        if len(refined_points) < 3:
            print("警告：点数不足，使用备用形状")
            Rectangle(10, 10, mode=Mode.PRIVATE)
        else:
            poly_line = Polyline(*refined_points, close=True)
            if outline.edges():
                total_length = sum(edge.length for edge in outline.edges())
                print(f"✅ 创建的轮廓线总长：{total_length}")
            else:
                print("❌ 轮廓线创建失败，使用备用形状")
                Rectangle(10, 10, mode=Mode.PRIVATE)
    except Exception as e:
        print(f"轮廓线创建异常：{str(e)}")
        Rectangle(10, 10, mode=Mode.PRIVATE)

show(outline)

# export_step(outline.line, OUTPUT_STEP)
