import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter


class PokerCardRankDetector:
    def __init__(self, templates_dir):
        """
        初始化扑克牌点数识别器

        参数:
        templates_dir (str): 包含所有点数模板图像的文件夹路径
        """
        # 设置中文字体
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False

        self.templates = {}
        self.load_templates(templates_dir)

        # 点数名称映射
        self.rank_names = {
            "big_joker": "big_joker",
            "small_joker": "small_joker",
            "A": "A",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "10": "10",
            "J": "J",
            "Q": "Q",
            "K": "K",
        }

    def load_templates(self, templates_dir):
        """
        加载所有点数模板图像

        参数:
        templates_dir (str): 包含所有点数模板图像的文件夹路径
        """
        print(f"正在加载模板图像从 {templates_dir}...")

        if not os.path.exists(templates_dir):
            print(f"错误: 模板目录 {templates_dir} 不存在!")
            return

        # 遍历模板目录中的所有文件
        for filename in os.listdir(templates_dir):
            if filename.endswith((".jpg", ".png", ".jpeg")):
                # 提取点数名称 (假设文件名格式为 "rank_name.jpg")
                rank_name = os.path.splitext(filename)[0]

                # 读取模板图像
                template_path = os.path.join(templates_dir, filename)
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

                if template is None:
                    print(f"无法加载模板: {template_path}")
                    continue

                # 存储模板
                self.templates[rank_name] = template
                print(f"已加载模板: {rank_name}")

        print(f"共加载了 {len(self.templates)} 个点数模板")

    def detect_cards(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )

        # 添加形态学操作（先注释掉）
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))  # 使用较小核
        # dilated = cv2.dilate(thresh, kernel, iterations=1)
        # thresh = dilated

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        cards = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # 基础条件
            if w > 15 and h > 30:  # 适当放大最小尺寸
                aspect_ratio = w / h
                if 0.3 < aspect_ratio < 2.0:  # 保守宽高比
                    # 添加安全区域裁剪
                    try:
                        card_img = image[
                            max(0, y - 2) : min(image.shape[0], y + h + 2),
                            max(0, x - 2) : min(image.shape[1], x + w + 2),
                        ]
                        cards.append((card_img, (x, y, w, h)))
                    except:
                        continue

        print(f"优化后检测到 {len(cards)} 个候选区域")
        return cards

    def extract_rank_region(self, card_img):
        """改进的点数区域提取"""
        h, w = card_img.shape[:2]

        # 扩大检测区域（适应"10"的情况）
        return cv2.cvtColor(
            card_img[0 : int(h / 3), 0 : int(w / 2)],  # 扩大宽度到1/2
            cv2.COLOR_BGR2GRAY,
        )

    def extract_rank_region(self, card_img):
        """
        从扑克牌图像中提取左上角的点数区域

        参数:
        card_img (numpy.ndarray): 单张扑克牌图像

        返回:
        numpy.ndarray: 点数区域图像
        """
        # 获取图像尺寸
        h, w = card_img.shape[:2]

        # 提取左上角区域 (假设点数在左上角)
        # 根据实际情况调整比例
        corner_img = card_img[0 : int(h / 3), 0 : int(w / 2)]
        # corner_img = card_img[0 : int(h / 5), 0 : int(w / 4)]
        cv2.imwrite("debug_roi.jpg", corner_img)
        # 转换为灰度图
        if len(corner_img.shape) > 2:
            corner_img = cv2.cvtColor(corner_img, cv2.COLOR_BGR2GRAY)

        # 二值化处理
        _, thresh = cv2.threshold(corner_img, 120, 255, cv2.THRESH_BINARY)

        return thresh

    def identify_rank(self, corner_img):
        """改进的识别逻辑"""
        # 预处理增强对比度
        _, processed = cv2.threshold(
            cv2.GaussianBlur(corner_img, (3, 3), 0),
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )

        best_match = None
        highest_score = -1

        for rank_name, template in self.templates.items():
            try:
                # 动态调整模板大小
                scaled_template = cv2.resize(
                    template,
                    (processed.shape[1], processed.shape[0]),
                    interpolation=cv2.INTER_AREA,
                )

                result = cv2.matchTemplate(
                    processed, scaled_template, cv2.TM_CCOEFF_NORMED
                )
                _, max_val, _, _ = cv2.minMaxLoc(result)

                if max_val > highest_score:
                    highest_score = max_val
                    best_match = rank_name
            except:
                continue

        # 降低匹配阈值适应复杂情况
        return (best_match, highest_score) if highest_score > 0.4 else (None, 0)

    def process_image(self, image_path, output_dir=None):
        """
        处理图像并统计每个点数的数量

        参数:
        image_path (str): 输入图像路径
        output_dir (str, optional): 输出目录，用于保存标记后的图像

        返回:
        dict: 每个点数的数量统计
        """
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法读取图像: {image_path}")
            return {}

        # 调试步骤1：显示阈值处理结果
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            cv2.GaussianBlur(gray, (5, 5), 0),
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2,
        )
        cv2.imwrite("debug_thresh.jpg", thresh)

        # 调试步骤2：显示轮廓检测结果
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contour_img = image.copy()
        cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
        cv2.imwrite("debug_contours.jpg", contour_img)

        # 测试不同核大小（逐步调整）
        # kernel_sizes = [(3, 3), (5, 3), (7, 3), (15, 3)]
        # for w, h in kernel_sizes:
        #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (w, h))
        #     dilated = cv2.dilate(thresh, kernel, iterations=1)
        #     cv2.imwrite(f"debug_dilated_{w}x{h}.jpg", dilated)

        # 测试不同宽高比阈值
        # aspect_ratios = [(0.1, 5), (0.3, 3), (0.5, 2)]
        # for min_r, max_r in aspect_ratios:
        #     filtered = [
        #         c
        #         for c in contours
        #         if min_r < (cv2.boundingRect(c)[2] / cv2.boundingRect(c)[3]) < max_r
        #     ]
        #     print(f"宽高比 {min_r}-{max_r} 检测到 {len(filtered)} 个轮廓")

        # 复制一份用于绘制结果
        result_image = image.copy()

        # 检测卡片
        cards = self.detect_cards(image)
        print(f"检测到 {len(cards)} 张扑克牌")

        # 存储每张牌的识别结果
        detections = []

        # 处理每张牌
        for i, (card_img, (x, y, w, h)) in enumerate(cards):
            # 提取点数区域
            corner_img = self.extract_rank_region(card_img)

            # 识别点数
            rank, confidence = self.identify_rank(corner_img)

            # 处理识别结果
            if rank:
                rank_display = self.rank_names.get(rank, rank)
                detections.append(rank)

                # 在原图上绘制矩形和标签
                cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                label = f"{rank_display} ({confidence:.2f})"
                cv2.putText(
                    result_image,
                    label,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
            else:
                # 无法识别的牌
                cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(
                    result_image,
                    "未知",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2,
                )

        # 统计每个点数的数量
        rank_counts = Counter(detections)

        # 显示并保存结果图像
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.title("扑克牌点数识别结果")

        # 如果指定了输出目录则保存结果图像
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, "result.jpg")
            cv2.imwrite(output_path, result_image)
            print(f"已保存结果图像到: {output_path}")

        # plt.show()

        return rank_counts


# 使用示例
if __name__ == "__main__":
    # 创建模板目录 (存放各点数的小图片)
    templates_dir = "rank_templates"

    # 确保模板目录存在
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"创建了模板目录: {templates_dir}")
        print("请将每个点数的小图片放入此目录，命名格式为 'A.jpg'、'2.jpg' 等")

    # 初始化检测器
    detector = PokerCardRankDetector(templates_dir)

    # 替换为你的游戏截图路径
    image_path = "test.png"

    # 处理图像
    output_dir = "output"
    rank_counts = detector.process_image(image_path, output_dir)

    # 打印统计结果
    print("\n扑克牌点数统计结果:")
    for rank, count in rank_counts.items():
        rank_display = detector.rank_names.get(rank, rank)
        print(f"{rank_display}: {count} 张")
