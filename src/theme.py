from tkinter import ttk

# 主题和样式定义
class Theme:
    FONT_FAMILY = "Courier New"
    
    # 颜色定义
    COLORS = {
        "bg_wood":      "#A0522D",
        "bg_panel":     "#DEB887",
        "paper":        "#FFF8DC",
        "text_dark":    "#2F1B08",  
        "border":       "#5C3317",
        "accent":       "#FF8C00",
        "button":       "#D2691E",
        "button_active":"#CD853F",
        "info":         "#006400",
        "warn":         "#8B0000"
    }

    # 插值路径颜色
    PATH_COLORS = {
        "Newton F": "#E74C3C", # 鲜红
        "Newton B": "#3498DB", # 亮蓝
        "Gauss F":  "#2ECC71", # 翠绿
        "Gauss B":  "#9B59B6", # 紫色
        "Stirling": "#F1C40F", # 金黄
        "Bessel":   "#FF1493"  # 深粉
    }

    # 应用样式方法
    @staticmethod
    def apply_styles():
        style = ttk.Style()
        style.theme_use('clam') 

        c = Theme.COLORS
        f = Theme.FONT_FAMILY
        
        base_font = (f, 11, "bold")       
        title_font = (f, 13, "bold") 
        entry_font = (f, 12) 
        
        style.configure("TFrame", background=c["bg_panel"])
        style.configure("TLabelframe", background=c["bg_panel"], borderwidth=3, relief="solid") 
        style.configure("TLabelframe.Label", font=title_font, background=c["bg_panel"], foreground=c["border"])
        style.configure("TLabel", font=base_font, background=c["bg_panel"], foreground=c["border"])
        style.configure("TButton", font=(f, 14, "bold"), background=c["button"], foreground="white", borderwidth=4, relief="raised", focuscolor=c["accent"])
        style.map("TButton", background=[('active', c["button_active"]), ('pressed', c["border"])], relief=[('pressed', 'sunken')])
        style.configure("TEntry", fieldbackground=c["paper"], foreground=c["text_dark"], font=entry_font, borderwidth=2, relief="solid")
        
        style.configure("Treeview", background=c["paper"], fieldbackground=c["paper"], foreground=c["text_dark"], font=(f, 10), rowheight=28, borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", background=c["button"], foreground="white", font=base_font, relief="raised")
        style.map("Treeview.Heading", background=[('active', c["button"])])
        style.map("Treeview", background=[('selected', c["accent"])])
