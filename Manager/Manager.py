import queue
import tkinter as tk
from tkinter import ttk

from View_value import start_get_thread
from Oid_config import OID_OPTIONS
from Trap_receiver import start_trap_thread

AGENT_PORT = 161
MANAGER_PORT = 162
manager_ip = '0.0.0.0'

agents = {}
request_id = 1

def add_agent():
    agent_ip = agent_var.get().strip()
    if agent_ip:
        if agent_ip not in agents:
            agents[agent_ip] = {}
            create_agent_tab(agent_ip)
            agent_var.set("")
        else:
            print(f"Agent with IP {agent_ip} already exists.")
    else:
        print("Agent IP cannot be empty.")


def create_agent_tab(agent_ip):
    tab = ttk.Frame(agent_tabs)
    agent_tabs.add(tab, text=agent_ip)

    ttk.Label(tab, text=f"Agent: {agent_ip}", font=("Arial", 12, "bold")).pack(pady=10)

    ttk.Label(tab, text="Enter OID:").pack(pady=5)
    oid_var = tk.StringVar()
    oid_entry = ttk.Entry(tab, textvariable=oid_var, width=40)
    oid_entry.pack(pady=5)

    ttk.Label(tab, text="Value:").pack(pady=5)
    value_var = tk.StringVar()
    value_entry = ttk.Entry(tab, textvariable=value_var, width=40)
    value_entry.pack(pady=5)

    view_button = ttk.Button(tab, text="View Value", command=lambda: view_oid_value(agent_ip, oid_var.get(),value_var))
    view_button.pack(pady=5)

    update_button = ttk.Button(tab, text="Update Value", command=lambda: update_oid_value(agent_ip, oid_var.get(), value_var.get()))
    update_button.pack(pady=5)

    unit_frame = ttk.Frame(root, padding=10)
    unit_frame.pack(side="top", fill="x")

    cpu_unit_var = tk.StringVar(value="Celsius")
    gpt_unit_var = tk.StringVar(value="Celsius")

    ttk.Label(unit_frame, text="Change CPU Temp Unit:").pack(side="left", padx=5)
    cpu_unit_dropdown = ttk.OptionMenu(unit_frame, cpu_unit_var, "Celsius", "Celsius", "Fahrenheit", "Kelvin")
    cpu_unit_dropdown.pack(side="left", padx=5)

    ttk.Label(unit_frame, text="Change GPT Temp Unit:").pack(side="left", padx=5)
    gpt_unit_dropdown = ttk.OptionMenu(unit_frame, gpt_unit_var, "Celsius", "Celsius", "Fahrenheit", "Kelvin")
    gpt_unit_dropdown.pack(side="left", padx=5)


def view_oid_value(agent_ip, oid,value_var):
    global request_id
    oid = [int(x) for x in oid.split(',')]
    start_get_thread(value_var,manager_ip,agent_ip, oid, request_id)
    request_id += 1

def update_oid_value(agent_ip, oid, value):
    print(f"Updating OID {oid} on agent {agent_ip} to value '{value}'.")

#inceput definite gui
root = tk.Tk()
root.title("OID Management Tool")
root.geometry("800x900")


oid_frame = ttk.Frame(root, padding=10)
oid_frame.pack(side="top", fill="both", expand=False)

ttk.Label(oid_frame, text="Available OIDs:", font=("Arial", 12, "bold")).pack(pady=5)

oid_listbox = tk.Text(oid_frame, height=10, wrap="none")
oid_listbox.pack(fill="both", expand=True, padx=10, pady=5)

for oid, name in OID_OPTIONS.items():
    oid_listbox.insert("end", f"{oid} - {name}\n")
oid_listbox.config(state="disabled")



trap_frame = ttk.Frame(root, padding=10)
trap_frame.pack(side="top", fill="both", expand=False)
ttk.Label(trap_frame, text="Received traps", font=("Arial", 12, "bold")).pack(pady=5)
trap_listbox = tk.Text(trap_frame, height=10, wrap="none")
trap_listbox.pack(fill="both", expand=True, padx=10, pady=5)
trap_listbox.config(state="disabled")

start_trap_thread(trap_listbox)


for oid, name in OID_OPTIONS.items():
    trap_listbox.insert("end", f"{oid} - {name}\n")
trap_listbox.config(state="disabled")



agent_tabs = ttk.Notebook(root)
agent_tabs.pack(fill="both", expand=True, padx=10, pady=10)

add_agent_frame = ttk.Frame(root, padding=10)
add_agent_frame.pack(side="bottom", fill="x")

ttk.Label(add_agent_frame, text="Add Agent by IP:").pack(side="left", padx=5)

agent_var = tk.StringVar()
agent_entry = ttk.Entry(add_agent_frame, textvariable=agent_var, width=30)
agent_entry.pack(side="left", padx=5)

add_agent_button = ttk.Button(add_agent_frame, text="Add Agent", command=add_agent)
add_agent_button.pack(side="left", padx=5)


root.mainloop()


