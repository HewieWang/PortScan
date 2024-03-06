import socket
import concurrent.futures
import tkinter as tk
from tkinter import ttk, messagebox

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return port if result == 0 else None

def start_scan():
    scan_button.config(state=tk.DISABLED)  # 禁用扫描按钮
    host = host_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())

    result_text.delete(1.0, tk.END)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}

        open_ports = []
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            try:
                result = future.result()
                if result is not None:
                    open_ports.append(result)
            except Exception as e:
                print(f"Error scanning port {port}: {e}")

            root.update()  # 刷新GUI

    if open_ports:
        result_text.insert(tk.END, f"Open ports on {host}:\n")
        for port in open_ports:
            result_text.insert(tk.END, f"{port}\n")
    else:
        result_text.insert(tk.END, f"No open ports found on {host}.")

    scan_button.config(state=tk.NORMAL)  # 启用扫描按钮
    messagebox.showinfo("Scan Complete", "Port scan completed.")

# 创建主窗口
root = tk.Tk()
root.title("Port Scanner")

# 添加组件
host_label = ttk.Label(root, text="Target Host:")
host_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

host_entry = ttk.Entry(root, width=20)
host_entry.grid(row=0, column=1, padx=10, pady=10)

start_port_label = ttk.Label(root, text="Start Port:")
start_port_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

start_port_entry = ttk.Entry(root, width=10)
start_port_entry.grid(row=1, column=1, padx=10, pady=10)

end_port_label = ttk.Label(root, text="End Port:")
end_port_label.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)

end_port_entry = ttk.Entry(root, width=10)
end_port_entry.grid(row=1, column=3, padx=10, pady=10)

scan_button = ttk.Button(root, text="Scan Ports", command=start_scan)
scan_button.grid(row=2, column=0, columnspan=4, pady=10)

result_text = tk.Text(root, height=10, width=40)
result_text.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

# 启动主循环
root.mainloop()
