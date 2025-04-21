import subprocess
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox
from sv_ttk import set_theme  # Importujemy styl Sun Valley

class FirewallManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Firewall Manager")
        self.root.geometry("600x500")
        
        # Ustawienie nowoczesnego stylu
        set_theme("dark")  # Można zmienić na "light" dla jasnego motywu
        
        # Stylizacja notebooka
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=[10, 5])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_port_management_tab()
        self.create_port_forwarding_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
    
    def create_styled_frame(self, parent, text):
        """Helper function to create consistent styled frames"""
        frame = ttk.LabelFrame(parent, text=text, padding=(15, 10))
        frame.pack(fill="x", padx=10, pady=5)
        return frame
    
    def create_port_management_tab(self):
        """Tab for basic port blocking/allowing"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Port Management")
        
        # Action Frame
        action_frame = self.create_styled_frame(tab, "Action")
        
        self.action_var = tk.StringVar(value="block")
        ttk.Radiobutton(action_frame, text="Block Port", variable=self.action_var, value="block").pack(side="left", padx=5)
        ttk.Radiobutton(action_frame, text="Allow Port", variable=self.action_var, value="allow").pack(side="left", padx=5)
        
        # Direction Frame
        direction_frame = self.create_styled_frame(tab, "Direction")
        
        self.direction_var = tk.StringVar(value="in")
        ttk.Radiobutton(direction_frame, text="Inbound", variable=self.direction_var, value="in").pack(side="left", padx=5)
        ttk.Radiobutton(direction_frame, text="Outbound", variable=self.direction_var, value="out").pack(side="left", padx=5)
        
        # Protocol Frame
        protocol_frame = self.create_styled_frame(tab, "Protocol")
        
        self.protocol_var = tk.StringVar(value="TCP")
        ttk.Radiobutton(protocol_frame, text="TCP", variable=self.protocol_var, value="TCP").pack(side="left", padx=5)
        ttk.Radiobutton(protocol_frame, text="UDP", variable=self.protocol_var, value="UDP").pack(side="left", padx=5)
        
        # Port Frame
        port_frame = self.create_styled_frame(tab, "Port Settings")
        
        ttk.Label(port_frame, text="Port Number:").pack(side="left", padx=(0, 5))
        self.port_entry = ttk.Entry(port_frame, width=8)
        self.port_entry.pack(side="left", padx=5)
        self.port_entry.insert(0, "80")
        
        self.scope_var = tk.StringVar(value="local")
        ttk.Radiobutton(port_frame, text="Local", variable=self.scope_var, value="local").pack(side="left", padx=(15, 5))
        ttk.Radiobutton(port_frame, text="Remote", variable=self.scope_var, value="remote").pack(side="left", padx=5)
        
        # Rule Name Frame
        rule_frame = self.create_styled_frame(tab, "Rule Name")
        
        self.rule_entry = ttk.Entry(rule_frame)
        self.rule_entry.pack(fill="x", padx=5, pady=2)
        self.rule_entry.insert(0, "CustomPortRule")
        
        # Button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Apply Rule", command=self.apply_rule, style="Accent.TButton").pack(padx=10, ipadx=10, ipady=5)
    
    def create_port_forwarding_tab(self):
        """Tab for port forwarding"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Port Forwarding")
        
        # Source Port Frame
        src_frame = self.create_styled_frame(tab, "Source Port")
        
        ttk.Label(src_frame, text="Port:").pack(side="left", padx=(0, 5))
        self.src_port_entry = ttk.Entry(src_frame, width=8)
        self.src_port_entry.pack(side="left", padx=5)
        self.src_port_entry.insert(0, "8080")
        
        # Destination Frame
        dest_frame = self.create_styled_frame(tab, "Destination")
        
        ttk.Label(dest_frame, text="IP Address:").pack(side="left", padx=(0, 5))
        self.dest_ip_entry = ttk.Entry(dest_frame, width=15)
        self.dest_ip_entry.pack(side="left", padx=5)
        self.dest_ip_entry.insert(0, "192.168.1.100")
        
        ttk.Label(dest_frame, text="Port:").pack(side="left", padx=(10, 5))
        self.dest_port_entry = ttk.Entry(dest_frame, width=8)
        self.dest_port_entry.pack(side="left")
        self.dest_port_entry.insert(0, "80")
        
        # Protocol Frame
        proto_frame = self.create_styled_frame(tab, "Protocol")
        
        self.fwd_protocol_var = tk.StringVar(value="TCP")
        ttk.Radiobutton(proto_frame, text="TCP", variable=self.fwd_protocol_var, value="TCP").pack(side="left", padx=5)
        ttk.Radiobutton(proto_frame, text="UDP", variable=self.fwd_protocol_var, value="UDP").pack(side="left", padx=5)
        
        # Interface Frame (optional)
        if_frame = self.create_styled_frame(tab, "Interface (optional)")
        
        ttk.Label(if_frame, text="Interface Name:").pack(side="left", padx=(0, 5))
        self.if_name_entry = ttk.Entry(if_frame)
        self.if_name_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.if_name_entry.insert(0, "Ethernet")
        
        # Button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Setup Port Forwarding", command=self.setup_port_forwarding, style="Accent.TButton").pack(padx=10, ipadx=10, ipady=5)
    
    def apply_rule(self):
        self.status_var.set("Processing...")
        self.root.update()
        
        if not ctypes.windll.shell32.IsUserAnAdmin():
            messagebox.showerror("Error", "Administrator privileges required! Please run as Administrator.")
            self.status_var.set("Error: Need admin rights")
            return
        
        try:
            port = int(self.port_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Port must be a valid number!")
            self.status_var.set("Error: Invalid port")
            return
        
        action = self.action_var.get()
        direction = self.direction_var.get()
        protocol = self.protocol_var.get()
        scope = self.scope_var.get()
        rule_name = self.rule_entry.get()
        
        try:
            # Delete existing rule
            subprocess.run(f'netsh advfirewall firewall delete rule name="{rule_name}"', 
                          shell=True, stderr=subprocess.DEVNULL)
            
            # Create new rule
            port_param = "localport" if scope == "local" else "remoteport"
            command = (
                f'netsh advfirewall firewall add rule '
                f'name="{rule_name}" '
                f'dir={direction} '
                f'action={action} '
                f'protocol={protocol} '
                f'{port_param}={port} '
                f'enable=yes'
            )
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                status = "blocked" if action == "block" else "allowed"
                messagebox.showinfo("Success", 
                    f"Port {port} ({protocol}, {direction}, {scope}) has been {status}.")
                self.status_var.set(f"Rule applied: {rule_name}")
            else:
                messagebox.showerror("Error", result.stderr)
                self.status_var.set("Error applying rule")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
            self.status_var.set("Error: Unexpected error")
    
    def setup_port_forwarding(self):
        self.status_var.set("Configuring port forwarding...")
        self.root.update()
        
        if not ctypes.windll.shell32.IsUserAnAdmin():
            messagebox.showerror("Error", "Administrator privileges required! Please run as Administrator.")
            self.status_var.set("Error: Need admin rights")
            return
        
        try:
            src_port = int(self.src_port_entry.get())
            dest_port = int(self.dest_port_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Ports must be valid numbers!")
            self.status_var.set("Error: Invalid ports")
            return
        
        dest_ip = self.dest_ip_entry.get()
        protocol = self.fwd_protocol_var.get()
        if_name = self.if_name_entry.get()
        
        try:
            # Enable port forwarding globally
            subprocess.run('netsh interface portproxy reset', shell=True, check=True)
            
            # Add forwarding rule
            cmd = (
                f'netsh interface portproxy add v4tov4 '
                f'listenport={src_port} '
                f'listenaddress=0.0.0.0 '
                f'connectport={dest_port} '
                f'connectaddress={dest_ip}'
            )
            
            if if_name:
                cmd += f' interface="{if_name}"'
                
            subprocess.run(cmd, shell=True, check=True)
            
            # Show current configuration
            result = subprocess.run('netsh interface portproxy show all', shell=True, capture_output=True, text=True)
            
            # Create a custom dialog to show the configuration
            config_window = tk.Toplevel(self.root)
            config_window.title("Port Forwarding Configuration")
            config_window.geometry("500x300")
            
            text = tk.Text(config_window, wrap="word", padx=10, pady=10)
            text.pack(fill="both", expand=True)
            
            text.insert("1.0", f"Port forwarding configured:\n{src_port} → {dest_ip}:{dest_port}\n\nCurrent configuration:\n{result.stdout}")
            text.config(state="disabled")
            
            ttk.Button(config_window, text="Close", command=config_window.destroy).pack(pady=10)
            
            self.status_var.set(f"Forwarding: {src_port} → {dest_ip}:{dest_port}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to configure port forwarding:\n{e.stderr}")
            self.status_var.set("Error configuring forwarding")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
            self.status_var.set("Error: Unexpected error")

if __name__ == "__main__":
    try:
        from sv_ttk import set_theme
    except ImportError:
        messagebox.showerror("Error", "Required package 'sv_ttk' not found. Please install it with:\npip install sv_ttk")
        exit(1)
        
    root = tk.Tk()
    app = FirewallManagerApp(root)
    root.mainloop()