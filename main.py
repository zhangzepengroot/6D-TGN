import numpy as np
import matplotlib.pyplot as plt

# 强制 Matplotlib 使用系统自带的中文字体并解决负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Heiti TC'] 
plt.rcParams['axes.unicode_minus'] = False 

class UltimateMilitaryHMPRSimulator:
    def __init__(self):
        # 战术超参数 (终极防脱靶版本)
        self.epochs = 500       # 迭代深度：给足时间让系统沉入真正的谷底
        self.initial_lr = 0.05  # [修复] 初始步长大幅降低，禁止“弹射起步”越过真实目标
        self.lr_decay = 0.995   # [修复] 步长衰减放缓，保持持久的微调下探能力
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.epsilon = 1e-8

    def get_physical_fields(self, x, y, z):
        """
        [终极形态] 六维量子张量场：融合微观高频精度与宏观全局唯一性
        """
        # 1-3 维：微观高频场 (提供亚毫米级“针眼”精度，但存在空间混叠)
        f_muon = np.sin(x * 0.5) * np.cos(y * 0.5) + np.sin(z)
        f_grav = np.exp(-(x**2 + y**2) * 0.05) * np.cos(z * 0.8)
        f_mag  = (x**2 - y**2) * 0.1 + np.sin(z * 2.0)
        
        # 4-6 维：宏观绝对背景场 (模拟地幔梯度、地壳厚度、绝对位势，提供全局唯一约束)
        f_mantle = 0.5 * x + 0.1 * y
        f_crust  = 0.1 * x + 0.5 * y
        f_geopot = 0.8 * z
        
        # 返回 6 维观测张量
        return np.array([f_muon, f_grav, f_mag, f_mantle, f_crust, f_geopot])

    def analytical_gradients(self, x, y, z, obs_tensor):
        """匹配六维张量的解析梯度极速计算内核"""
        fields = self.get_physical_fields(x, y, z)
        
        # 计算 6 维张量残差
        err = fields - obs_tensor
        err_muon, err_grav, err_mag = err[0], err[1], err[2]
        err_mantle, err_crust, err_geopot = err[3], err[4], err[5]

        # 1. 计算微观高频场的局部偏导数
        dx_muon = 0.5 * np.cos(x * 0.5) * np.cos(y * 0.5)
        dy_muon = -0.5 * np.sin(x * 0.5) * np.sin(y * 0.5)
        dz_muon = np.cos(z)
        
        dx_grav = np.exp(-(x**2 + y**2) * 0.05) * (-0.1 * x) * np.cos(z * 0.8)
        dy_grav = np.exp(-(x**2 + y**2) * 0.05) * (-0.1 * y) * np.cos(z * 0.8)
        dz_grav = np.exp(-(x**2 + y**2) * 0.05) * (-0.8 * np.sin(z * 0.8))
        
        dx_mag = 0.2 * x
        dy_mag = -0.2 * y
        dz_mag = 2.0 * np.cos(z * 2.0)

        # 2. 合成 6 维全局梯度 (融入宏观场的常数导数: dx_mantle=0.5, dy_crust=0.5, etc.)
        # 这股强大的宏观梯度，会像一只巨手，把陷入假坑的坐标强行拽回真实的势井！
        grad_x = 2.0 * (err_muon*dx_muon + err_grav*dx_grav + err_mag*dx_mag + err_mantle*0.5 + err_crust*0.1)
        grad_y = 2.0 * (err_muon*dy_muon + err_grav*dy_grav + err_mag*dy_mag + err_mantle*0.1 + err_crust*0.5)
        grad_z = 2.0 * (err_muon*dz_muon + err_grav*dz_grav + err_mag*dz_mag + err_geopot*0.8)
        
        return np.array([grad_x, grad_y, grad_z])

    def simulate_ins_midcourse_drift(self, true_pos):
        """模拟飞行 1000 公里后，捷联惯导 (SINS) 产生的系统漂移"""
        np.random.seed(42) # 锁定随机种子，复现经典的脱靶方位
        ins_noise = np.random.normal(loc=0.0, scale=0.8, size=3) 
        ins_pos = np.array(true_pos) + ins_noise
        initial_error = np.linalg.norm(ins_pos - np.array(true_pos))
        return ins_pos, initial_error

    def tactical_grid_scan(self, center_pos, obs_tensor, search_radius=2.0, grid_points=11):
        """
        [新增架构] 战术 3D 网格粗筛系统 (TERCOM)
        在惯导给出的不靠谱坐标周围，快速撒网，跨越物理场的“伪装山脊”
        """
        print(f"[战术雷达] 启动 3D 网格拓扑扫描，搜索半径 {search_radius} km，正在跨越局部极值陷阱...")
        best_pos = center_pos
        min_loss = float('inf')
        
        # 在 XYZ 三个方向构建均匀分布的探测网
        offsets = np.linspace(-search_radius, search_radius, grid_points)
        for dx in offsets:
            for dy in offsets:
                for dz in offsets:
                    test_pos = center_pos + np.array([dx, dy, dz])
                    fields = self.get_physical_fields(*test_pos)
                    loss = np.sum((fields - obs_tensor)**2)
                    
                    if loss < min_loss:
                        min_loss = loss
                        best_pos = test_pos
                        
        print(f"[战术雷达] 网格扫描完成！锁定全局最佳势井入口: X={best_pos[0]:.4f}, Y={best_pos[1]:.4f}, Z={best_pos[2]:.4f}")
        return best_pos

    def run_tactical_simulation(self, true_pos):
        print("="*65)
        print("[交战指令] 复合制导系统启动 - 末端突防阶段 (三段式猎杀架构)")
        print(f"[交战指令] 目标真实物理坐标锁定: X={true_pos[0]}, Y={true_pos[1]}, Z={true_pos[2]}")
        
        # 阶段一：模拟惯导中段粗对准
        ins_pos, initial_error = self.simulate_ins_midcourse_drift(true_pos)
        print("-" * 65)
        print(f"[传感器] 捷联惯导(SINS)当前指示坐标: X={ins_pos[0]:.4f}, Y={ins_pos[1]:.4f}, Z={ins_pos[2]:.4f}")
        print(f"[警告] 飞行1000公里后，惯导系统累积绝对误差: {initial_error:.4f} 千米")
        
        # 获取目标真实的多维物理场指纹
        obs_tensor = self.get_physical_fields(*true_pos)
        
        # 阶段二：战术网格雷达扫除“鬼影陷阱”
        print("-" * 65)
        safe_entry_pos = self.tactical_grid_scan(ins_pos, obs_tensor, search_radius=2.0)
        
        # 阶段三：HSAS 量子流形算法接管，开启精确坍缩
        print("-" * 65)
        print("[系统接管] HMPR 量子流形算法强行介入，从安全入口平滑探底...")
        pos = safe_entry_pos.copy() 
        m = np.zeros(3)
        v = np.zeros(3)
        
        # 记录网格扫描后的误差起点
        grid_scan_error = np.linalg.norm(pos - np.array(true_pos))
        history_pos = [pos.copy()]
        history_error = [initial_error, grid_scan_error] # 加入粗筛后的跳变点

        for epoch in range(1, self.epochs + 1):
            grads = self.analytical_gradients(pos[0], pos[1], pos[2], obs_tensor)
            
            # Adam 状态机滑移
            m = self.beta1 * m + (1 - self.beta1) * grads
            v = self.beta2 * v + (1 - self.beta2) * (grads**2)
            m_hat = m / (1 - self.beta1**epoch)
            v_hat = v / (1 - self.beta2**epoch)
            
            # 动态学习率衰减
            current_lr = self.initial_lr * (self.lr_decay ** epoch)
            
            # 坐标更新
            pos -= current_lr * m_hat / (np.sqrt(v_hat) + self.epsilon)
            
            # 记录当前误差
            current_error = np.linalg.norm(pos - np.array(true_pos))
            history_pos.append(pos.copy())
            history_error.append(current_error)
            
            # 关键节点输出
            if epoch == 10 or epoch == 100 or epoch == 300 or epoch == 500:
                print(f"  -> 迭代 {epoch:03d} 次 (步长 {current_lr:.4f}): 当前脱靶量 {current_error:.6e} 千米")

        # --- 最终战术核查 ---
        print("-" * 65)
        final_error_km = history_error[-1]
        final_error_meters = final_error_km * 1000  
        final_error_mm = final_error_meters * 1000     
        
        print(f"[战术核查] 最终锁定坐标: X={pos[0]:.8f}, Y={pos[1]:.8f}, Z={pos[2]:.8f}")
        
        if final_error_mm < 1.0:
            print(f"[结论] 致命打击锁定！全息共振达成，成功压缩至亚毫米级：{final_error_mm:.4f} mm")
        elif final_error_meters < 10.0:
            print(f"[结论] 常规打击锁定！误差在战术容忍范围内：{final_error_meters:.2f} m")
        else:
            print(f"[警告] 致命故障！算法依然陷入局部极值，脱靶量 {final_error_meters:.2f} 米！")
        print("="*65)

        self.plot_error_collapse(history_error)

    def plot_error_collapse(self, h_err):
        """生成极速误差坍缩图，展示网格跳变与平滑衰减的双重威力"""
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(111)
        
        ax.plot(h_err, color='magenta', linewidth=2.5, label='绝对交战误差 (HMPR 轨迹)')
        ax.set_yscale('log')
        
        ax.set_title("三段式猎杀链：网格跳变与量子坍缩绝对误差曲线", fontsize=16)
        ax.set_xlabel('战术迭代周期 (Epochs)', fontsize=12)
        ax.set_ylabel('绝对误差 (千米 - 对数缩放)', fontsize=12)
        
        # 标注网格粗筛的瞬间跳变
        ax.annotate('网格雷达瞬间跨越伪装陷阱', xy=(1, h_err[1]), xytext=(20, h_err[0]*2),
                    arrowprops=dict(facecolor='yellow', shrink=0.05, width=1.5, headwidth=8),
                    fontsize=10, color='yellow')

        # 添加战术标定线
        ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.6, label='1公里 (SINS 中段漂移误差)')
        ax.axhline(y=1e-3, color='yellow', linestyle='--', alpha=0.6, label='1米 (常规精确制导极限)')
        ax.axhline(y=1e-6, color='cyan', linestyle='--', alpha=0.8, label='1毫米 (HSAS 物理坍缩极限)')
        
        ax.legend(loc='upper right')
        ax.grid(True, which="both", ls="--", alpha=0.3)
        plt.tight_layout()
        plt.show()

# 执行终极系统仿真
if __name__ == "__main__":
    simulator = UltimateMilitaryHMPRSimulator()
    # 设定任意的真实坐标，测试系统的鲁棒性
    true_target_position = [4.5, -2.3, 6.8]
    simulator.run_tactical_simulation(true_pos=true_target_position)