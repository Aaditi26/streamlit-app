import streamlit as st
import math

st.set_page_config(
    page_title="Cost Estimating App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

def Home():
    st.markdown("## 🏠 Welcome to Machining Time & Cost Estimator")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("machine.jpg")
    with col2:
        st.markdown("""
        This web app helps estimate **machining time and cost** for processes like Turning, Milling, and Drilling.

        **Features:**
        - Add and customize machining operations  
        - Input process-specific parameters  
        - View route sheet  
        - Export data as PDF

        ---
        **Developed by an IIT Kharagpur student**
        """)
    st.info("👉 Go to the **Machining** tab to get started.")



def Machining():
    st.header("Machining")

    # Initialize session state
    if "machining_entries" not in st.session_state:
        st.session_state.machining_entries = []
    if "extra_entries" not in st.session_state:
        st.session_state.extra_entries = []

    st.title("🛠️ Lathe Machining Processes")

    # --- Step 0: Material & Labor Costs ---
    st.header("📦 Cost Inputs")
    material_cost = st.number_input("Enter Material Cost (Rs.)", value=1000.0, step=100.0)
    labor_cost_per_hour = st.number_input("Enter Labor Cost per Hour (Rs.)", value=500.0, step=50.0)

    # Step 1: Process selection + Add button
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ Machining Processes")
        machining_options = ["Facing", "Turning", "Drilling", "Boring", "Threading", "Knurling"]
        selected_machining = st.selectbox("Select a Process", machining_options, key="machining_select")
        if st.button("Add Machining Process"):
            st.session_state.machining_entries.append({"type": selected_machining})

    with col2:
        st.subheader("➕ Other Processes")
        extra_options = ["Parting", "Blanking", "Resharpening", "Custom"]
        selected_extra = st.selectbox("Select Other Process", extra_options, key="extra_select")
        if st.button("Add Other Process"):
            st.session_state.extra_entries.append({"type": selected_extra})


    # Step 2: Render input fields for each Machining process
    st.divider()
    st.header("🔩 Machining Inputs")
    for i, entry in enumerate(st.session_state.machining_entries):
        ptype = entry["type"]
        st.markdown(f"### 🔧 {ptype} #{i+1}")  

        if entry ["type"] == "Facing":
            col1, col2 = st.columns(2)
            with col1:
                d = st.number_input(f"Facing Diameter (mm)", key=f"face_d_{i}", value=50)
                l = st.number_input(f"Facing Lenght (mm)", key=f"face_l_{i}", value=7)
                f = st.number_input(f"Feed (mm/min)", key=f"face_f_{i}", value=0.16)
            with col2:    
                n = st.number_input(f"RPM", key=f"face_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm)", key=f"face_doc_{i}", value=2)
                t = st.number_input(f"Tool Cost (Rs)", key=f"face_t_{i}", value=10)
            entry.update({"diameter": d, "length": l, "feed": f, "rpm": n, "depth of cut": doc, "tool cost": t})

        elif entry ["type"] == "Turning":
            col1, col2 = st.columns(2)
            with col1:
                di = st.number_input(f"Initial Diameter (mm)", key=f"turn_di_{i}", value=50)
                df = st.number_input(f"Final Diameter (mm)", key=f"turn_df_{i}", value=38)
                l = st.number_input(f"Turning Lenght (mm)", key=f"turn_l_{i}", value=25)
                f = st.number_input(f"Feed (mm/min)", key=f"turn_f_{i}", value=0.16)
            with col2:
                n = st.number_input(f"RPM", key=f"turn_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm)", key=f"turn_doc_{i}", value=1)
                t = st.number_input(f"Tool Cost (Rs)", key=f"turn_t_{i}", value=10)
            entry.update({"initial diameter": di, "final diameter": df, "length": l, "feed": f, "rpm": n, "depth of cut": doc, "tool cost": t})

        elif entry ["type"] == "Drilling":
            col1, col2 = st.columns(2)
            with col1:
                d = st.number_input(f"Drilling Depth (mm)", key=f"drill_d_{i}", value=12)
                f = st.number_input(f"Feed (mm/min)", key=f"drill_f_{i}", value=0.16)
                tu = st.number_input(f"Num of times drilled", key=f"drill_tu_{i}", value=5)
            with col2:    
                n = st.number_input(f"RPM", key=f"drill_n_{i}", value=170)
                t = st.number_input(f"Tool Cost (Rs)", key=f"drill_t_{i}", value=10)
            entry.update({"depth": d, "feed": f, "rpm": n, "turn": tu, "tool cost": t})      

        elif entry ["type"] == "Boring":
            col1, col2 = st.columns(2)
            with col1:
                di = st.number_input(f"Initial Diameter (mm)", key=f"bore_di_{i}", value=25)
                df = st.number_input(f"Final Diameter (mm)", key=f"bore_df_{i}", value=28)
                d = st.number_input(f"Boring Depth (mm)", key=f"bore_d_{i}", value=12)
                f = st.number_input(f"Feed (mm/min)", key=f"bore_f_{i}", value=0.16)
            with col2:
                a = st.number_input(f"Drill Angle (degree)", key=f"bore_a_{i}", value=118)
                n = st.number_input(f"RPM", key=f"bore_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm)", key=f"bore_doc_{i}", value=0.1)
                t = st.number_input(f"Tool Cost (Rs)", key=f"bore_t_{i}", value=10)
            entry.update({"initial diameter": di, "final diameter": df, "depth": d, "feed": f, "angle": a, "rpm": n, "depth of cut": doc, "tool cost": t})

        elif entry ["type"] == "Threading":
            col1, col2 = st.columns(2)
            with col1:
                p = st.number_input(f"Thread Pitch (TPI)", key=f"thread_p_{i}", value=2)
                l = st.number_input(f"Thread Lenght (mm)", key=f"thread_l_{i}", value=12)
                f = st.number_input(f"Feed (mm/min)", key=f"thread_f_{i}", value=0.16)
            with col2:
                n = st.number_input(f"RPM", key=f"thread_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm)", key=f"thread_doc_{i}", value=0.1)
                t = st.number_input(f"Tool Cost (Rs)", key=f"thread_t_{i}", value=10)
            entry.update({"pitch": p, "length": l, "feed": f, "rpm": n, "depth of cut": doc, "tool cost": t})

        elif entry ["type"] == "Knurling":
            col1, col2 = st.columns(2)
            with col1:
                l = st.number_input(f"Knurling Lenght (mm)", key=f"knurl_l_{i}", value=20)
                f = st.number_input(f"Feed (mm/min)", key=f"knurl_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"knurl_n_{i}", value=170)
            with col2:
                doc = st.number_input(f"Depth of cut (mm)", key=f"knurl_doc_{i}", value=0.1)
                t = st.number_input(f"Tool Cost (Rs)", key=f"knurl_t_{i}", value=10)
            entry.update({"length": l, "feed": f, "rpm": n, "depth of cut": doc, "tool cost": t})

        if st.button(f"❌ Remove", key=f"remove_{i}"):
            st.session_state.machining_entries.pop(i)
            st.rerun()  # Refresh the UI immediately

    # Step 3: Render input fields for each Other process
    st.divider()
    st.header("📦 Extra Process Inputs")
    for i, entry in enumerate(st.session_state.extra_entries):
        ptype = entry["type"]
        st.markdown(f"### {ptype} #{i+1}")
    
        if ptype == "Custom":
            col1, col2 = st.columns(2)
            with col1:
                custom_name = st.text_input(f"Enter Custom Process Name", key=f"custom_name_{i}", value=f"Custom #{i+1}")
            with col2:
                time = st.number_input(f"Time Taken (min)", key=f"custom_time_{i}", value=10.0)
                cost_hr = st.number_input(f"Cost per Hour (Rs.)", key=f"custom_cost_{i}", value=100.0)
                entry.update({"custom_name": custom_name, "time_min": time, "cost_per_hr": cost_hr})
        elif  ptype == "Parting":
            col1, col2 = st.columns(2)
            with col1:
                time = st.number_input(f"Time Taken (min)", key=f"part_time_{i}", value=20.0)
            with col2:    
                cost_hr = st.number_input(f"Cost per Hour (Rs.)", key=f"part_cost_{i}", value=50.0)
            entry.update({"time_min": time, "cost_per_hr": cost_hr})
        elif  ptype == "Blanking":
            col1, col2 = st.columns(2)
            with col1:
                time = st.number_input(f"Time Taken (min)", key=f"blank_time_{i}", value=15.0)
            with col2:    
                cost_hr = st.number_input(f"Cost per Hour (Rs.)", key=f"blank_cost_{i}", value=50.0)
            entry.update({"time_min": time, "cost_per_hr": cost_hr})
        elif  ptype == "Resharpening":
            col1, col2 = st.columns(2)
            with col1:
                time = st.number_input(f"Time Taken (min)", key=f"resharp_time_{i}", value=35.0)
            with col2:    
                cost_hr = st.number_input(f"Cost per Hour (Rs.)", key=f"resharp_cost_{i}", value=50.0)
            entry.update({"time_min": time, "cost_per_hr": cost_hr})
        if st.button(f"❌ Remove!", key=f"remove!_{i}"):
            st.session_state.extra_entries.pop(i)
            st.rerun()

    # Step 4: Submit all
    st.divider()
    if st.button("✅ Submit All"):
        
        total_time_min = 0.0
        total_extra_cost = 0.0
        total_tool_cost = 0.0

        machining_times =[]
        for i, entry in enumerate(st.session_state.machining_entries):
            process_type = entry["type"]
            time = 0.0

            if process_type == "Facing":
                try:
                    turn = (entry["length"]/entry["depth of cut"]) 
                    time = ((((20 + (entry["diameter"] / 2)) / (entry["feed"] * entry["rpm"])) * turn) + ((20 + (entry["diameter"] / 2)) / (entry["feed"] * 285))) + 5
                except ZeroDivisionError:
                    time = 0
        
            elif process_type == "Turning":
                try:
                    turn = ((entry["initial diameter"]) - (entry["final diameter"])) / ((entry["depth of cut"]) * 2) 
                    time = ((((20 + (entry["length"])) / (entry["feed"] * entry["rpm"])) * turn) + ((20 + (entry["length"])) / (entry["feed"] * 285))) + 5
                except ZeroDivisionError:
                    time = 0
        
            elif process_type == "Drilling":
                try:
                    time = (((10 + (entry["depth"])) / (entry["rpm"] * entry["feed"]) * (entry["turn"])) + ((10 + (entry["depth"])) / (285 * entry["feed"]))) + 5
                except ZeroDivisionError:
                    time = 0
            
            elif process_type == "Boring":
                try:
                    a = math.radians((180 - entry["angle"]) / 2)
                    extra_length = (entry["initial diameter"] / 2) * (math.tan(a))
                    turn = (entry["final diameter"] - entry["initial diameter"]) / ((entry["depth of cut"]) * 2)
                    time = (((10 + (entry["depth"])) / (entry["rpm"] * entry["feed"]) * (turn * 2)) + ((10 + (entry["depth"])) / (285 * entry["feed"])) + (((10 + extra_length) / (entry["feed"] * entry["rpm"])) * (turn * 2))) + 5
                except ZeroDivisionError:
                    time = 0

            elif process_type == "Threading":
                try:
                    turn = (entry["pitch"]) / (entry["depth of cut"])
                    time = (((10 + (entry["length"])) / (entry["rpm"] * entry["feed"]) * (turn)) + ((10 + (entry["length"])) / (285 * entry["feed"]))) + 5 
                except ZeroDivisionError:
                    time = 0
            
            elif process_type == "Knurling":
                try:
                    time = ((((20 + (entry["length"])) / (entry["feed"] * entry["rpm"])) * 4) + ((20 + (entry["length"])) / (entry["feed"] * 285))) + 5
                except ZeroDivisionError:
                    time = 0
        
            total_time_min += time
            total_tool_cost += entry.get("tool cost", 0)
            mid_cost = (time * (labor_cost_per_hour / 60))
            machining_times.append({
                "process": process_type, 
                "index": i+1, 
                "time": time,
                "cost": mid_cost
            })

        extra_times = []
        for i, entry in enumerate(st.session_state.extra_entries):
            ptype = entry["type"]
            minutes = entry.get("time_min", 0.0)
            cost_hr = entry.get("cost_per_hr", 0.0)
            cost = (minutes / 60) * cost_hr

            minutes_with_overhead = minutes + 5
            total_time_min += minutes_with_overhead
            total_extra_cost += cost

            # Handle label
            if ptype == "Custom":
                label = entry.get("custom_name", f"Custom #{i+1}")
            else:
                label = ptype

            extra_times.append({
                "ptype": label,
                "index": i + 1,
                "time": minutes_with_overhead,
                "cost": cost
            })


        st.session_state.total_time_min = total_time_min
        st.session_state.total_extra_cost = total_extra_cost
        st.session_state.material_cost = material_cost
        st.session_state.tool_cost = total_tool_cost
        st.session_state.labor_cost = (total_time_min / 60) * labor_cost_per_hour
        st.session_state.total_cost = material_cost + st.session_state.labor_cost + total_extra_cost + total_tool_cost
        st.session_state.result_ready = True
        st.session_state.machining_times = machining_times
        st.session_state.extra_times = extra_times
        st.session_state.page = "Result"
        st.rerun()
        
        

def Result():
    st.header("📄 Route Sheet / Results")

    if not st.session_state.get("result_ready", False):
        st.info("No results yet. Go to the **Machining** tab and calculate first.")
        return
    
    if "extra_times" not in st.session_state:
        st.session_state.extra_times = []

    st.subheader("✅ Summary")
    st.success(f"⏱️ Total Time: {st.session_state.total_time_min//60:.2f} hr {st.session_state.total_time_min%60:.2f} min")
    st.success(f"Handling Time assumed fo each process: 5 min")
    st.success(f"👷 Labor Cost: Rs. {st.session_state.labor_cost:.2f}")
    st.success(f"📦 Material Cost: Rs. {st.session_state.material_cost:.2f}")
    st.success(f"🧰 Tool Cost: Rs. {st.session_state.tool_cost:.2f}")
    st.success(f"➕ Extra Process Cost: Rs. {st.session_state.total_extra_cost:.2f}")
    st.header(f"💰 Total Estimated Cost: Rs. {st.session_state.total_cost:.2f}")

    st.markdown("---")
    st.subheader("⚙️ Machining Process Times")
    for t in st.session_state.machining_times:
        if 'cost' not in t:
            st.write("Missing 'cost' in:", t)
        st.write(f"{t['process']} #{t['index']} → {t['time']:.2f} min → Rs. {t['cost']:.2f}")

    st.subheader("📋 All Machining Entries")
    st.dataframe(st.session_state.machining_entries)

    st.divider()
    st.subheader("➕ Other Processes")
    for t in st.session_state.extra_times:
        st.write(f"{t['ptype']} #{t['index']} → {t['time']:.2f} min → Rs. {t['cost']:.2f}")
    
    st.subheader("📋 All Other Entries")
    st.dataframe(st.session_state.extra_entries)

# --- Sidebar Navigation with Buttons ---
st.sidebar.title("📁 Navigation")

if "page" not in st.session_state:
    st.session_state.page = "Home"

if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"
if st.sidebar.button("🛠️ Machining"):
    st.session_state.page = "Machining"
if st.sidebar.button("📄 Result"):
    st.session_state.page = "Result"

# 🔄 Add Reset Button
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset All Data"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- Define Pages ---
pages = {
    "Home": Home,
    "Machining": Machining,
    "Result": Result
}

# --- Load Selected Page ---
pages[st.session_state.page]()
