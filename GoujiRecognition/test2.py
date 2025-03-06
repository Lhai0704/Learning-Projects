import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

class PokerCardRankDetector:
    def __init__(self, templates_dir):
        """
        初始化扑克牌点数识别器
        
        参数:
        templates_dir (str): 包含所有点数模板图像的文件夹路径
        """
        self.templates = {}
        self.load_templates(templates_dir)
        
        # 点数名称映射
        self.rank_names = {
            'big_joker': '大王',
            'small_joker': '小王',
            'joker': 'JOKER',  # 新增JOKER识别
            'A': 'A',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9',
            '10': '10',
            'J': 'J',
            'Q': 'Q',
            'K': 'K'
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
            if filename.endswith(('.jpg', '.png', '.jpeg')):
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
    
    def detect_cards_using_vertical_projection(self, image, min_width=10, max_width=100, min_gap=5):
        """
        使用垂直投影方法检测横向排列的扑克牌
        
        参数:
        image (numpy.ndarray): 输入图像
        min_width (int): 最小牌宽度
        max_width (int): 最大牌宽度
        min_gap (int): 牌之间的最小间隔
        
        返回:
        list: 扑克牌区域列表, 每个元素为 (card_img, (x, y, w, h))
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 二值化
        _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
        
        # 垂直投影
        v_projection = np.sum(binary, axis=0)
        
        # 找出牌的边界
        cards = []
        start_x = None
        width = 0
        
        for i in range(len(v_projection)):
            if v_projection[i] > 0 and start_x is None:
                # 找到牌的左边界
                start_x = i
                width = 1
            elif v_projection[i] > 0 and start_x is not None:
                # 继续计算宽度
                width += 1
            elif v_projection[i] == 0 and start_x is not None:
                # 找到牌的右边界
                if min_width <= width <= max_width:
                    # 提取牌的图像区域
                    x = start_x
                    y = 0
                    w = width
                    h = image.shape[0]
                    card_img = image[y:y+h, x:x+w]
                    cards.append((card_img, (x, y, w, h)))
                
                # 重置
                start_x = None
                width = 0
        
        # 处理最后一张牌
        if start_x is not None and min_width <= width <= max_width:
            x = start_x
            y = 0
            w = width
            h = image.shape[0]
            card_img = image[y:y+h, x:x+w]
            cards.append((card_img, (x, y, w, h)))
        
        # 合并相邻的小区域 (处理像"10"这样被分开的问题)
        merged_cards = []
        i = 0
        while i < len(cards):
            curr_card, (curr_x, curr_y, curr_w, curr_h) = cards[i]
            
            # 检查是否需要合并
            if i + 1 < len(cards):
                next_card, (next_x, next_y, next_w, next_h) = cards[i + 1]
                gap = next_x - (curr_x + curr_w)
                
                # 如果间隔很小，合并它们
                if gap <= min_gap:
                    merged_w = next_x + next_w - curr_x
                    merged_card = image[curr_y:curr_y+curr_h, curr_x:curr_x+merged_w]
                    merged_cards.append((merged_card, (curr_x, curr_y, merged_w, curr_h)))
                    i += 2  # 跳过下一个已合并的牌
                    continue
            
            # 不需要合并，保留当前牌
            merged_cards.append((curr_card, (curr_x, curr_y, curr_w, curr_h)))
            i += 1
        
        return merged_cards
    
    # 特殊处理JOKER牌
    def detect_joker(self, image):
        """
        特别检测JOKER牌
        
        参数:
        image (numpy.ndarray): 输入图像
        
        返回:
        list: JOKER牌区域列表
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 二值化
        _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
        
        # 查找轮廓
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        joker_cards = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # JOKER牌通常是竖直排列的几个字母，宽高比较小
            if h > w * 3 and h > 50:  # 高是宽的3倍以上，且高度足够
                card_img = image[y:y+h, x:x+w]
                joker_cards.append((card_img, (x, y, w, h)))
        
        return joker_cards
    
    def extract_rank_region(self, card_img):
        """
        从扑克牌图像中提取点数区域
        
        参数:
        card_img (numpy.ndarray): 单张扑克牌图像
        
        返回:
        numpy.ndarray: 点数区域图像
        """
        # 对于横向排列的牌，整个图像就是点数区域
        if len(card_img.shape) > 2:
            gray = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = card_img
        
        # 二值化处理
        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        
        return thresh
    
    def identify_rank(self, corner_img):
        """
        使用模板匹配识别点数
        
        参数:
        corner_img (numpy.ndarray): 点数区域图像
        
        返回:
        str: 识别出的点数名称
        float: 匹配置信度
        """
        best_match = None
        highest_score = -1
        
        # 对每个模板进行匹配
        for rank_name, template in self.templates.items():
            # 确保模板和目标图像大小合适
            if template.shape[0] > corner_img.shape[0] or template.shape[1] > corner_img.shape[1]:
                # 如果模板比目标图像大，可以调整模板大小或跳过
                continue
            
            # 使用模板匹配
            result = cv2.matchTemplate(corner_img, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # 更新最佳匹配
            if max_val > highest_score:
                highest_score = max_val
                best_match = rank_name
        
        # 设置一个阈值, 低于该值的匹配结果被视为不可靠
        if highest_score < 0.4:  # 降低阈值以提高识别率
            return None, highest_score
        
        return best_match, highest_score
    
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
        
        # 复制一份用于绘制结果
        result_image = image.copy()
        
        # 检测普通牌
        cards = self.detect_cards_using_vertical_projection(image)
        print(f"检测到 {len(cards)} 张普通扑克牌")
        
        # 检测JOKER牌
        joker_cards = self.detect_joker(image)
        print(f"检测到 {len(joker_cards)} 张JOKER牌")
        
        # 合并所有牌
        all_cards = cards + joker_cards
        
        # 存储每张牌的识别结果
        detections = []
        
        # 处理每张牌
        for i, (card_img, (x, y, w, h)) in enumerate(all_cards):
            # 保存检测到的牌图像用于调试
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if output_dir:
                card_path = os.path.join(output_dir, f"card_{i}.jpg")
                cv2.imwrite(card_path, card_img)
            
            # 提取点数区域
            corner_img = self.extract_rank_region(card_img)
            
            # 识别点数
            rank, confidence = self.identify_rank(corner_img)
            
            # 处理识别结果
            if rank:
                rank_display = self.rank_names.get(rank, rank)
                detections.append(rank)
                
                # 在原图上绘制矩形和标签
                cv2.rectangle(result_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                label = f"{rank_display} ({confidence:.2f})"
                cv2.putText(result_image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                # 无法识别的牌
                cv2.rectangle(result_image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(result_image, "未知", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # 统计每个点数的数量
        rank_counts = Counter(detections)
        
        # 显示并保存结果图像
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title('扑克牌点数识别结果')
        
        # 保存结果图像
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, 'result.jpg')
            cv2.imwrite(output_path, result_image)
            print(f"已保存结果图像到: {output_path}")
        
        plt.show()
        
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