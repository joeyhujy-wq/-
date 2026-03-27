# -胡家瑜-25306025-第二次人工智能编程作业
注：仓库中文件“mission 4”是最终完整的代码，可以实现4个功能。余下三个文件是是代码逐渐丰满的过程，分别可以实现1、2、3个功能。文件“test”是测试文件，与本次作业无关。
1. 任务拆解与 AI 协作策略
我使用kimi辅助，尝试分步与AI协同完成任务，主要依次按任务1、任务2、任务3、任务4的顺序完成，同时要求AI遵守技术与工程规范。AI生成代码后，我再进行最后的测试、调整、优化。
2. 核心 Prompt 迭代记录
在测试第四个功能时，我发现AI给出的代码有一个逻辑问题：在还未生座位表时，程序就可以生成准考证。这就可能造成准考证与座位表对不上的问题。因此我指出了这一漏洞并命令AI修复，最后得到了一个完美符合工程规范的程序。
最开始我的请求是：“请帮我实现第四个功能：4.生成准考证目录与文件：在根目录下创建一个名为"准考证"的文件夹。根据考场安排信息，在该文件夹内生成『01.txt』、『02.txt』等独立文件，每个文件内写入对应学生的考场座位号、姓名、学号信息。”
AI 生成的代码在‘generate_admission_tickets()’方法中直接调用了‘random.shuffle()’重新打乱学生顺序，而不是基于已生成的考场安排表。
于是我追问：“有一点不足：还没有生成考试安排之前，怎么能生成准考证呢？请修复这一漏洞。”
AI新生成的代码先检查了准考证状态，未生成时提示：”请先执行功能【3.生成考场安排表】，再生成准考证“，保证了准考证上的信息与安排表一致。
3.Debug 与异常处理记录
在使用AI的过程中，我暂时没有遇到程序报错的情况。不过值得一提的是，AI生成的代码在读取文件的时候都会写”/mnt/kimi/upload/人工智能编程语言学生名单.txt“。所以在测试之前，我都会先修改路径，使其读取到正确的文件。
4.人工代码审查 (Code Review)
def generate_admission_tickets(self, folder_name="准考证"):
    """
    生成准考证：基于已生成的考场安排表，为每个学生生成独立的准考证文件
    """
    #验证前置条件：必须已生成考场安排表才能生成准考证
    if not self.arrangement_generated or not self.exam_arrangement:
        print("\n❌ 错误：无法生成准考证！")
        print("   ⚠️  原因：尚未生成考场安排表")
        print("   💡 请先执行功能【3.生成考场安排表】，再生成准考证")
        print("   📝 这样可以确保准考证座位号与考场安排一致\n")
        return None, []  #返回空值表示生成失败
    
    try:
        #使用os.path.join拼接路径
        #os.getcwd()获取当前工作目录
        folder_path = os.path.join(os.getcwd(), folder_name)
        
        #如果目录已存在不会报错，这样多次运行功能4不会出错
         os.makedirs(folder_path, exist_ok=True)
        
        generated_files = []  # 用于记录生成的文件名列表
        
        #基于已保存的考场安排顺序遍历
        #生成从1开始的座位号
        for seat_no, student in enumerate(self.exam_arrangement, 1):
            
            #将数字补零至两位
            filename = f"{str(seat_no).zfill(2)}.txt"
            
            #拼接文件夹和文件名
            file_path = os.path.join(folder_path, filename)
            
            #确保文件正确关闭
            with open(file_path, 'w', encoding='utf-8') as f:
                # 写入格式化的准考证内容，生成重复的分隔线
                f.write("=" * 30 + "\n")           #顶部边框
                f.write("      考 试 准 考 证\n")   #标题居中
                f.write("=" * 30 + "\n\n")         #空行分隔
                
                # 写入核心信息
                f.write(f"座位号：{seat_no}\n")     #获取的座位号
                f.write(f"姓  名：{student.name}\n") #获取姓名
                f.write(f"学  号：{student.student_id}\n")  #获取学号
                f.write(f"学  院：{student.college}学院\n") #学院名+后缀
                f.write(f"班  级：{student.class_no}班\n")  #班级号+后缀
                
                #底部装饰
                f.write("\n" + "=" * 30 + "\n")
                f.write("祝考试顺利！\n")
                f.write("=" * 30 + "\n")
            
            #记录已生成的文件名
            generated_files.append(filename)
        
        #向用户展示生成结果摘要
        print(f"\n✅ 准考证生成成功！")
        print(f"📁 文件夹路径：{folder_path}")
        print(f"📄 生成文件数：{len(generated_files)} 个")
        print(f"\n📋 文件列表（前5个）：")
        for fname in generated_files[:5]:  #只显示前5个避免刷屏
            print(f"   - {fname}")
        if len(generated_files) > 5:       #提示还有更多
            print(f"   ... 还有 {len(generated_files) - 5} 个文件")
        print()
        
        return folder_path, generated_files  #返回路径和文件列表        
    #异常处理
    except PermissionError:
        #权限错误
        print(f"\n❌ 错误：没有权限创建目录或写入文件 '{folder_name}'")
        print("   请检查目录权限。")
        raise
    except OSError as e:
        #OS错误
        print(f"\n❌ 错误：创建目录或文件时发生OS错误 - {e}")
        raise
    except Exception as e:
        #兜底异常
        print(f"\n❌ 错误：生成准考证时发生未知错误 - {e}")
        raise
