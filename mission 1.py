import os


# ==================== 数据类 ====================

class Student:
    """学生数据类：封装学生基本信息"""

    def __init__(self, seq_no, name, gender, class_no, student_id, college):
        """初始化学生属性"""
        self.seq_no = seq_no  # 序号
        self.name = name  # 姓名
        self.gender = gender  # 性别
        self.class_no = class_no  # 班级
        self.student_id = student_id  # 学号
        self.college = college  # 学院

    def __str__(self):
        """友好打印学生信息（使用边框美化输出）"""
        return (f" 序号: {self.seq_no:<4}  姓名: {self.name:<6}\n"
                f" 性别: {self.gender:<2}    班级: {self.class_no}班\n"
                f" 学号: {self.student_id}\n"
                f" 学院: {self.college:<10}\n")

    def __repr__(self):
        """开发调试用的表示"""
        return f"Student({self.student_id}, {self.name}, {self.college})"


# ==================== 控制类 ====================

class ExamSystem:
    """考场管理系统：负责学生信息的加载、查找和管理"""

    def __init__(self, file_path):
        """初始化系统，加载学生数据"""
        self.file_path = file_path
        self.students = {}  # 使用字典存储，key为学号，value为Student对象
        self._load_data()

    def _load_data(self):
        """私有方法：从文件加载学生数据（内部使用）"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                # 跳过标题行
                header = f.readline()

                for line_num, line in enumerate(f, start=2):
                    line = line.strip()
                    if not line:  # 跳过空行
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

                        # 学号格式校验
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
            print("   请确保文件路径正确，且文件存在于指定位置。")
            raise  # 重新抛出，让调用者知道初始化失败
        except PermissionError:
            print(f"❌ 错误：没有权限读取文件 '{self.file_path}'")
            raise
        except Exception as e:
            print(f"❌ 错误：读取文件时发生未知错误 - {e}")
            raise

    @staticmethod
    def validate_student_id(student_id):
        """
        静态方法：校验学号格式
        规则：学号应为7位数字（根据样例数据：2001101格式）
        """
        if not isinstance(student_id, str):
            return False
        if len(student_id) != 7:
            return False
        return student_id.isdigit()

    @classmethod
    def create_default_path(cls, filename):
        """
        类方法：生成默认文件路径（在当前工作目录下查找）
        """
        return os.path.join(os.getcwd(), filename)

    def find_student(self, student_id):
        """
        查找学生信息

        Args:
            student_id: 要查找的学号

        Returns:
            Student对象 或 None（未找到）
        """
        # 先校验学号格式
        if not self.validate_student_id(student_id):
            print(f"⚠️ 提示：学号 '{student_id}' 格式不符合规范（应为7位数字）")

        return self.students.get(student_id)

    def list_all_students(self):
        """列出所有学生（调试用）"""
        print("\n📋 当前系统内所有学生列表：")
        print("-" * 50)
        for sid in sorted(self.students.keys()):
            s = self.students[sid]
            print(f"{sid} | {s.name} | {s.gender} | {s.college}学院")
        print("-" * 50)


# ==================== 主程序入口 ====================

def main():
    """主函数：程序交互入口"""
    # 文件路径（使用上传的文件，或当前目录下的文件）
    file_path = "人工智能编程语言学生名单.txt"

    # 如果上述路径不存在，尝试当前目录
    if not os.path.exists(file_path):
        file_path = "人工智能编程语言学生名单.txt"

    print("=" * 50)
    print("🎓 学生信息与考场管理系统 v1.0")
    print("=" * 50)

    try:
        # 初始化系统（自动加载数据）
        system = ExamSystem(file_path)

        # 交互式查找循环
        while True:
            print("\n" + "=" * 50)
            print("🔍 学生信息查询")
            print("   输入学号进行查询，或输入 'q' 退出系统")
            print("=" * 50)

            user_input = input("请输入学号: ").strip()

            # 退出命令
            if user_input.lower() in ('q', 'quit', 'exit', '退出'):
                print("\n👋 感谢使用，再见！")
                break

            # 空输入检查
            if not user_input:
                print("⚠️ 输入不能为空，请重新输入")
                continue

            # 查找学生
            student = system.find_student(user_input)

            if student:
                print("\n✅ 找到学生信息：")
                print(student)
            else:
                print(f"\n❌ 未找到学号为 '{user_input}' 的学生")
                print("   💡 提示：请检查学号是否输入正确")
                print(f"   📚 系统中现有学号示例：{', '.join(list(system.students.keys())[:3])}...")

    except FileNotFoundError:
        print("\n💥 系统初始化失败：无法找到数据文件")
        print("   请确认 '人工智能编程语言学生名单.txt' 文件存在")
    except Exception as e:
        print(f"\n💥 系统发生错误：{e}")


# 运行程序
if __name__ == "__main__":
    main()