import os
import random
from datetime import datetime


# ==================== 数据类 ====================

class Student:
    """学生数据类：封装学生基本信息"""

    def __init__(self, seq_no, name, gender, class_no, student_id, college):
        self.seq_no = seq_no
        self.name = name
        self.gender = gender
        self.class_no = class_no
        self.student_id = student_id
        self.college = college

    def __str__(self):
        return (f"┌────────────── 学生信息 ──────────────┐\n"
                f"│ 序号: {self.seq_no:<4}  姓名: {self.name:<6}      │\n"
                f"│ 性别: {self.gender:<2}    班级: {self.class_no}班          │\n"
                f"│ 学号: {self.student_id}                │\n"
                f"│ 学院: {self.college:<10}            │\n"
                f"└─────────────────────────────────────┘")

    def __repr__(self):
        return f"Student({self.student_id}, {self.name}, {self.college})"


# ==================== 控制类（完整版） ====================

class ExamSystem:
    """考场管理系统：负责学生信息的加载、查找、随机点名、生成考场安排表等功能"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.students = {}
        self._load_data()

    def _load_data(self):
        """私有方法：从文件加载学生数据"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                header = f.readline()
                for line_num, line in enumerate(f, start=2):
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split('\t')
                    if len(parts) != 6:
                        print(f"⚠️ 警告：第{line_num}行数据格式异常，已跳过")
                        continue
                    try:
                        seq_no = int(parts[0])
                        name = parts[1]
                        gender = parts[2]
                        class_no = int(parts[3])
                        student_id = parts[4]
                        college = parts[5]
                        if not self.validate_student_id(student_id):
                            print(f"⚠️ 警告：第{line_num}行学号格式异常 '{student_id}'")
                        student = Student(seq_no, name, gender, class_no, student_id, college)
                        self.students[student_id] = student
                    except ValueError as e:
                        print(f"⚠️ 警告：第{line_num}行数值转换失败 - {e}")
                        continue
            print(f"✅ 数据加载成功！共加载 {len(self.students)} 名学生信息\n")
        except FileNotFoundError:
            print(f"❌ 错误：找不到文件 '{self.file_path}'")
            raise
        except PermissionError:
            print(f"❌ 错误：没有权限读取文件 '{self.file_path}'")
            raise
        except Exception as e:
            print(f"❌ 错误：读取文件时发生未知错误 - {e}")
            raise

    @staticmethod
    def validate_student_id(student_id):
        """静态方法：校验学号格式（7位数字）"""
        if not isinstance(student_id, str):
            return False
        if len(student_id) != 7:
            return False
        return student_id.isdigit()

    @classmethod
    def create_default_path(cls, filename):
        """类方法：生成默认文件路径"""
        return os.path.join(os.getcwd(), filename)

    def find_student(self, student_id):
        """查找学生信息"""
        if not self.validate_student_id(student_id):
            print(f"⚠️ 提示：学号 '{student_id}' 格式不符合规范（应为7位数字）")
        return self.students.get(student_id)

    def list_all_students(self):
        """列出所有学生"""
        print("\n📋 当前系统内所有学生列表：")
        print("-" * 50)
        for sid in sorted(self.students.keys()):
            s = self.students[sid]
            print(f"{sid} | {s.name} | {s.gender} | {s.college}学院")
        print("-" * 50)

    def random_pick(self, count):
        """随机点名：从所有学生中随机选取指定数量的不重复学生"""
        total = len(self.students)

        if count <= 0:
            raise ValueError(f"抽取数量必须大于0，当前输入：{count}")

        if count > total:
            raise ValueError(f"抽取数量不能超过总人数！当前输入：{count}，总人数：{total}")

        all_students = list(self.students.values())
        selected = random.sample(all_students, count)

        return selected

    def display_random_pick(self, count):
        """显示随机点名结果（带格式美化）"""
        try:
            selected = self.random_pick(count)

            print(f"\n🎲 随机点名结果（共 {count} 人）：")
            print("=" * 50)

            for i, student in enumerate(selected, 1):
                print(f"\n【第 {i} 位】")
                print(student)

            print("=" * 50)
            print(f"✅ 成功抽取 {count} 名学生\n")

        except ValueError as e:
            print(f"\n❌ 抽取失败：{e}")
            return None

    # ==================== 新增：生成考场安排表功能 ====================

    def generate_exam_arrangement(self, output_filename="考场安排表.txt"):
        """
        生成考场安排表：将所有学生顺序随机打乱，生成包含座位号、姓名、学号的文件

        Args:
            output_filename: 输出文件名，默认为"考场安排表.txt"

        Returns:
            str: 生成的文件完整路径

        Raises:
            IOError: 当文件写入失败时
        """
        try:
            # 1. 获取所有学生并随机打乱顺序
            all_students = list(self.students.values())
            random.shuffle(all_students)  # 原地打乱顺序

            # 2. 获取当前时间并格式化
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 3. 构建输出文件路径（程序根目录）
            output_path = os.path.join(os.getcwd(), output_filename)

            # 4. 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                # 第一行：生成时间（满足特殊要求）
                f.write(f"生成时间：{current_time}\n")
                f.write("=" * 40 + "\n")
                f.write(f"{'座位号':<8}{'姓名':<10}{'学号':<12}\n")
                f.write("-" * 40 + "\n")

                # 写入学生信息（打乱后的顺序）
                for seat_no, student in enumerate(all_students, 1):
                    f.write(f"{seat_no:<8}{student.name:<10}{student.student_id:<12}\n")

                f.write("=" * 40 + "\n")
                f.write(f"总人数：{len(all_students)} 人\n")

            print(f"\n✅ 考场安排表生成成功！")
            print(f"📄 文件路径：{output_path}")
            print(f"🕐 生成时间：{current_time}")
            print(f"👥 安排人数：{len(all_students)} 人\n")

            return output_path

        except PermissionError:
            print(f"\n❌ 错误：没有权限写入文件 '{output_filename}'")
            print("   请检查目录权限或更换保存路径。")
            raise
        except IOError as e:
            print(f"\n❌ 错误：写入文件时发生IO错误 - {e}")
            raise
        except Exception as e:
            print(f"\n❌ 错误：生成考场安排表时发生未知错误 - {e}")
            raise


# ==================== 主程序（完整版） ====================

def main():
    """主函数：程序交互入口"""
    file_path = "人工智能编程语言学生名单.txt"
    if not os.path.exists(file_path):
        file_path = "人工智能编程语言学生名单.txt"

    print("=" * 50)
    print("🎓 学生信息与考场管理系统 v3.0")
    print("   功能：1.信息查询  2.随机点名  3.生成考场安排表")
    print("=" * 50)

    try:
        system = ExamSystem(file_path)
        total_students = len(system.students)

        while True:
            print("\n" + "=" * 50)
            print("请选择功能：")
            print("   [1] 学生信息查询（输入学号）")
            print("   [2] 随机点名（输入人数）")
            print("   [3] 生成考场安排表")
            print("   [q] 退出系统")
            print("=" * 50)

            choice = input("请输入选项: ").strip()

            # 退出
            if choice.lower() in ('q', 'quit', 'exit', '退出'):
                print("\n👋 感谢使用，再见！")
                break

            # 功能1：信息查询
            if choice == '1':
                student_id = input("请输入学号: ").strip()
                if not student_id:
                    print("⚠️ 输入不能为空")
                    continue

                student = system.find_student(student_id)
                if student:
                    print("\n✅ 找到学生信息：")
                    print(student)
                else:
                    print(f"\n❌ 未找到学号为 '{student_id}' 的学生")
                    print(f"   💡 提示：系统中现有学号示例：{', '.join(list(system.students.keys())[:3])}...")

            # 功能2：随机点名
            elif choice == '2':
                print(f"\n📢 当前系统共有 {total_students} 名学生")
                user_input = input(f"请输入需要点名的学生数量 (1-{total_students}): ").strip()

                try:
                    count = int(user_input)
                except ValueError:
                    print(f"\n❌ 输入错误：'{user_input}' 不是有效的数字！")
                    print("   💡 提示：请输入纯数字，例如：3")
                    continue

                system.display_random_pick(count)

            # 功能3：生成考场安排表
            elif choice == '3':
                print("\n📝 正在生成考场安排表...")
                system.generate_exam_arrangement()

            # 无效选项
            else:
                print(f"\n⚠️ 无效选项：'{choice}'")
                print("   💡 提示：请输入 1、2、3 或 q")

    except FileNotFoundError:
        print("\n💥 系统初始化失败：无法找到数据文件")
    except Exception as e:
        print(f"\n💥 系统发生错误：{e}")


# 运行程序
if __name__ == "__main__":
    main()