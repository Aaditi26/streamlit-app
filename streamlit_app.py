import streamlit as st
import math
from fpdf import FPDF
import tempfile
import os

st.set_page_config(
    page_title="Cost Estimating App",
    page_icon="📊",
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
        **Developed by IIT Kharagpur students**
        """)
    st.info("👉 Go to the **Machining** tab to get started.")



def Machining():
    st.header("Machining")

    # Initialize session state
    if "job_material" not in st.session_state:
        st.session_state.job_material = None
    if "machining_entries" not in st.session_state:
        st.session_state.machining_entries = []
    if "extra_entries" not in st.session_state:
        st.session_state.extra_entries = []

    st.title("🛠️ Lathe Machining Processes")

    # --- Step 0: Material & Labor Costs ---
    st.header("📦 Cost/Job Inputs")

    material_option = ["Select", "Aluminium", "Brass", "Copper", "Steel"]
    job_material = st.selectbox("Job Material",material_option)
    st.session_state.job_material = job_material

    material_cost = st.number_input("Material Cost (Rs.)", value=1000.00, step=100.00)
    labor_cost_per_hour = st.number_input("Labor Cost per Hour (Rs.)", value=500.00, step=50.0)


    # Step 1: Process selection + Add button
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ Machining Processes")
        machining_options = [ "Boring", "Drilling - Center", "Drilling - Pilot", "Drilling - Main", "Facing", "Grooving", "Knurling", "Reaming", "Threading", "Turning - Concave", "Turning - Convex", "Turning - Straight", "Turning - Taper"]
        selected_machining = st.selectbox("Select a Process", machining_options, key="machining_select")
        if st.button("Add Machining Process"):
            st.session_state.machining_entries.append({"type": selected_machining})

    with col2:
        st.subheader("➕ Other Processes")
        extra_options = [ "Custom", "Blanking", "Chamfering", "Parting", "Resharpening", "Tool Change"]
        selected_extra = st.selectbox("Select Other Process", extra_options, key="extra_select")
        if st.button("Add Other Process"):
            st.session_state.extra_entries.append({"type": selected_extra})


    # Step 2: Render input fields for each Machining process
    st.divider()
    st.header("🔩 Machining Inputs")
    for i, entry in enumerate(st.session_state.machining_entries):
        ptype = entry["type"]
        st.markdown(f"### 🔧 {ptype} #{i+1}")  

        if entry ["type"] == "Boring":
            col1, col2 = st.columns(2)
            with col1:
                di = st.number_input(f"Initial Diameter (mm)", key=f"bore_di_{i}", value=25.00)
                df = st.number_input(f"Final Diameter (mm)", key=f"bore_df_{i}", value=28.00)
                d = st.number_input(f"Boring Length (mm)", key=f"bore_d_{i}", value=12.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"bore_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"bore_n_{i}", value=170)
                an = st.number_input(f"Drill Angle (degree)", key=f"bore_ann_{i}", value=118.00)
            with col2:
                doc = st.number_input(f"Depth of cut (mm/pass)", key=f"bore_doc_{i}", value=0.10)
                js = st.number_input(f"Job Setting Time (min)", key=f"bore_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"bore_ts_{i}", value=5.00)
                a = st.number_input(f"Approach (mm)", key=f"bore_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"bore_o_{i}", value=0.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"bore_t_{i}", value=10.00)
            entry.update({"initial diameter": di, "final diameter": df, "depth": d, "feed": f, "angle": an, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts, "approach": a, "overrun": o, "tool cost": t})
        
        elif entry ["type"] == "Drilling - Center":
            col1, col2 = st.columns(2)
            with col1:
                l = st.number_input(f"Drilling Depth (mm)", key=f"drill_l_{i}", value=5.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"drill_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"drill_n_{i}", value=170)
                tu = st.number_input(f"Num of times drilled", key=f"drill_tu_{i}", value=4)
                d = st.number_input(f"Drill Diameter", key=f"drill_d_{i}", value=6.00)
            with col2: 
                js = st.number_input(f"Job Setting Time (min)", key=f"drill_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"drill_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"drill_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"drill_o_{i}", value=0.00) 
                t = st.number_input(f"Tool Cost (Rs)", key=f"drill_t_{i}", value=10.00)
            entry.update({"depth": l, "feed": f, "diameter":d, "rpm": n, "turn": tu, "job set time": js, "tool set time": ts,  "approach": a, "overrun": o, "tool cost": t})    
        
        elif entry ["type"] == "Drilling - Pilot":
            col1, col2 = st.columns(2)
            with col1:
                l = st.number_input(f"Drilling Depth (mm)", key=f"drill_l_{i}", value=12.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"drill_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"drill_n_{i}", value=170)
                tu = st.number_input(f"Num of times drilled", key=f"drill_tu_{i}", value=5)
                d = st.number_input(f"Drill Diameter", key=f"drill_d_{i}", value=15.00)
            with col2: 
                js = st.number_input(f"Job Setting Time (min)", key=f"drill_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"drill_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"drill_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"drill_o_{i}", value=0.00) 
                t = st.number_input(f"Tool Cost (Rs)", key=f"drill_t_{i}", value=10.00)
            entry.update({"depth": l, "feed": f, "diameter":d, "rpm": n, "turn": tu, "job set time": js, "tool set time": ts,  "approach": a, "overrun": o, "tool cost": t})    
        
        elif entry ["type"] == "Drilling - Main":
            col1, col2 = st.columns(2)
            with col1:
                l = st.number_input(f"Drilling Depth (mm)", key=f"drill_l_{i}", value=12.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"drill_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"drill_n_{i}", value=170)
                tu = st.number_input(f"Num of times drilled", key=f"drill_tu_{i}", value=7)
                d = st.number_input(f"Drill Diameter", key=f"drill_d_{i}", value=25.00)
            with col2: 
                js = st.number_input(f"Job Setting Time (min)", key=f"drill_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"drill_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"drill_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"drill_o_{i}", value=0.00) 
                t = st.number_input(f"Tool Cost (Rs)", key=f"drill_t_{i}", value=10.00)
            entry.update({"depth": l, "feed": f, "diameter":d, "rpm": n, "turn": tu, "job set time": js, "tool set time": ts,  "approach": a, "overrun": o, "tool cost": t})    
        
        elif entry ["type"] == "Facing":
            col1, col2 = st.columns(2)
            with col1:
                d = st.number_input(f"Facing Diameter (mm)", key=f"face_d_{i}", value=50.00)
                l = st.number_input(f"Facing Lenght (mm)", key=f"face_l_{i}", value=7.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"face_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"face_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm/pass)", key=f"face_doc_{i}", value=2.00)
            with col2:    
                js = st.number_input(f"Job Setting Time (min)", key=f"face_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"face_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"face_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"face_o_{i}", value=10.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"face_t_{i}", value=10.00)
            entry.update({"diameter": d, "length": l, "feed": f, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts,  "approach": a, "overrun": o, "tool cost": t})

        elif entry ["type"] == "Grooving":
            col1, col2 = st.columns(2)
            with col1:
                di = st.number_input(f"Initial Diameter(mm)", key=f"groove_di_{i}", value=28.00)
                df = st.number_input(f"Final Diameter(mm)", key=f"groove_df_{i}", value=30.00)
                l = st.number_input(f"Groove Length", key=f"groove_l_{i}", value=10.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"groove_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"groove_pn_{i}", value=170)
                w = st.number_input(f"Tool Width (mm)", key=f"groove_w_{i}", value=1.00)
            with col2:          
                doc = st.number_input(f"Depth of Cut (mm/pass)", key=f"groove_pdoc_{i}", value=1.00)  
                js = st.number_input(f"Job Setting Time (min)", key=f"groove_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"groove_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"groove_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"groove_o_{i}", value=0.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"groove_t_{i}", value=10.00)
            entry.update({"initial diameter": di, "final diameter": df, "length": l, "feed": f, "tool width": w, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts,  "approach": a, "overrun": o, "tool cost": t})
        
        elif entry ["type"] == "Knurling":
            col1, col2 = st.columns(2)
            with col1:
                l = st.number_input(f"Knurling Lenght (mm)", key=f"knurl_l_{i}", value=20.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"knurl_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"knurl_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm/pass)", key=f"knurl_doc_{i}", value=0.10)
                js = st.number_input(f"Job Setting Time (min)", key=f"knurl_js_{i}", value=0.00)
            with col2:
                ts = st.number_input(f"Tool Setting Time (min)", key=f"knurl_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"knurl_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"knurl_o_{i}", value=0.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"knurl_t_{i}", value=10.00)
            entry.update({"length": l, "feed": f, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts,  "approach": a, "overrun": o, "tool cost": t})
        
        elif entry ["type"] == "Reaming":
            col1, col2 = st.columns(2)
            with col1:
                l = st.number_input(f"Reaming Lenght (mm)", key=f"ream_l_{i}", value=20.00)
                di = st.number_input(f"Initial Diameter (mm)", key=f"ream_di_{i}", value=28.00)
                df = st.number_input(f"Final Diameter (mm)", key=f"ream_df_{i}", value=30.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"ream_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"ream_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm/pass)", key=f"ream_doc_{i}", value=0.10)
            with col2:
                js = st.number_input(f"Job Setting Time (min)", key=f"ream_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"ream_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"ream_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"ream_o_{i}", value=0.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"ream_t_{i}", value=10.00)
            entry.update({"length": l, "initial diameter": di, "final diameter": df, "feed": f, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts, "approach": a, "overrun": o, "tool cost": t})
        
        elif entry ["type"] == "Threading":
            col1, col2 = st.columns(2)
            with col1:
                p = st.number_input(f"Thread Pitch (TPI)", key=f"thread_p_{i}", value=2.00)
                l = st.number_input(f"Thread Lenght (mm)", key=f"thread_l_{i}", value=12.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"thread_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"thread_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm/pass)", key=f"thread_doc_{i}", value=0.10)
            with col2:
                js = st.number_input(f"Job Setting Time (min)", key=f"thread_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"thread_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"thread_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"thread_o_{i}", value=0.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"thread_t_{i}", value=10.00)
            entry.update({"pitch": p, "length": l, "feed": f, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts, "approach": a, "overrun": o, "tool cost": t})
        
        elif entry ["type"] == "Turning - Concave":
            col1, col2 = st.columns(2)
            with col1:
                d = st.number_input(f"Diameter (mm)", key=f"turn_cave_d_{i}", value=50.00)
                an = st.number_input(f"Conacve Angle (Degree)", key=f"turn_cave_an_{i}", value=20.00)
                l = st.number_input(f"Turning Lenght (mm)", key=f"turn_cave_l_{i}", value=25.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"turn_cave_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"tur_caven_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm/pass)", key=f"turn_cave_doc_{i}", value=1.00)
            with col2:
                js = st.number_input(f"Job Setting Time (min)", key=f"turn_cave_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"turn_cave_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"turn_cave_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"turn_cave_o_{i}", value=10.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"turn_cave_t_{i}", value=10.00)
            entry.update({"diameter": d, "angle": an, "length": l, "feed": f, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts, "approach": a, "overrun": o, "tool cost": t})

        elif entry ["type"] == "Turning - Convex":
            col1, col2 = st.columns(2)
            with col1:
                d = st.number_input(f"Diameter (mm)", key=f"turn_vex_d_{i}", value=50.00)
                an = st.number_input(f"Convex Angle (Degree)", key=f"turn_vex_an_{i}", value=20.00)
                l = st.number_input(f"Turning Lenght (mm)", key=f"turn_vex_l_{i}", value=25.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"turn_vex_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"turn_vex_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm/pass)", key=f"turn_vex_doc_{i}", value=1.00)
            with col2:
                js = st.number_input(f"Job Setting Time (min)", key=f"turn_vex_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"turn_vex_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"turn_vex_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"turn_vex_o_{i}", value=10.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"turn_vex_t_{i}", value=10.00)
            entry.update({"diameter": d, "angle": an, "length": l, "feed": f, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts, "approach": a, "overrun": o, "tool cost": t})
        
        elif entry ["type"] == "Turning - Straight":
            col1, col2 = st.columns(2)
            with col1:
                di = st.number_input(f"Initial Diameter (mm)", key=f"turn_di_{i}", value=50.00)
                df = st.number_input(f"Final Diameter (mm)", key=f"turn_df_{i}", value=38.00)
                l = st.number_input(f"Turning Lenght (mm)", key=f"turn_l_{i}", value=25.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"turn_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"turn_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm/pass)", key=f"turn_doc_{i}", value=1.00)
            with col2:
                js = st.number_input(f"Job Setting Time (min)", key=f"turn_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"turn_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"turn_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"turn_o_{i}", value=0.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"turn_t_{i}", value=10.00)
            entry.update({"initial diameter": di, "final diameter": df, "length": l, "feed": f, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts, "approach": a, "overrun": o, "tool cost": t})

        elif entry ["type"] == "Turning - Taper":
            col1, col2 = st.columns(2)
            with col1:
                dl = st.number_input(f"Larger Diameter (mm)", key=f"turn_taper_dl_{i}", value=50.00)
                ds = st.number_input(f"Smaller Diameter (mm)", key=f"turn_taper_ds_{i}", value=38.00)
                l = st.number_input(f"Turning Lenght (mm)", key=f"turn_taper_l_{i}", value=25.00)
                f = st.number_input(f"Feed (mm/rev)", key=f"turn_taper_f_{i}", value=0.16)
                n = st.number_input(f"RPM", key=f"turn_taper_n_{i}", value=170)
                doc = st.number_input(f"Depth of cut (mm/pass)", key=f"turn_taper_doc_{i}", value=1.00)
            with col2:
                js = st.number_input(f"Job Setting Time (min)", key=f"turn_taper_js_{i}", value=0.00)
                ts = st.number_input(f"Tool Setting Time (min)", key=f"turn_taper_ts_{i}", value=5.00) 
                a = st.number_input(f"Approach (mm)", key=f"turn_taper_a_{i}", value=10.00)
                o = st.number_input(f"Overrun (mm)", key=f"turn_taper_o_{i}", value=0.00)
                t = st.number_input(f"Tool Cost (Rs)", key=f"turn_taper_t_{i}", value=10.00)
            entry.update({"larger diameter": dl, "smaller diameter": ds, "length": l, "feed": f, "rpm": n, "depth of cut": doc, "job set time": js, "tool set time": ts, "approach": a, "overrun": o, "tool cost": t})  

        
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
                time = st.number_input(f"Time Taken (min)", key=f"custom_time_{i}", value=10.00)
                cost_hr = st.number_input(f"Extra Tool Cost (Rs.)", key=f"custom_cost_{i}", value=100.00)
                entry.update({"custom_name": custom_name, "time_min": time, "extra_tool_cost": cost_hr})
        
        elif  ptype == "Blanking":
            col1, col2 = st.columns(2)
            with col1:
                time = st.number_input(f"Time Taken (min)", key=f"blank_time_{i}", value=15.00)
            with col2:    
                cost_hr = st.number_input(f"Extra Tool Cost (Rs.)", key=f"blank_cost_{i}", value=50.00)
            entry.update({"time_min": time, "extra_tool_cost": cost_hr})
        
        elif  ptype == "Chamfering":
            col1, col2 = st.columns(2)
            with col1:
                time = st.number_input(f"Time Taken (min)", key=f"chamfer_time_{i}", value=5.00)
            with col2:    
                cost_hr = st.number_input(f"Extra Tool Cost (Rs.)", key=f"chamfer_cost_{i}", value=10.00)
            entry.update({"time_min": time, "extra_tool_cost": cost_hr})
        
        elif  ptype == "Parting":
            col1, col2 = st.columns(2)
            with col1:
                time = st.number_input(f"Time Taken (min)", key=f"part_time_{i}", value=20.00)
            with col2:    
                cost_hr = st.number_input(f"Extra Tool Cost (Rs.)", key=f"part_cost_{i}", value=50.00)
            entry.update({"time_min": time, "extra_tool_cost": cost_hr})
        
        elif  ptype == "Resharpening":
            col1, col2 = st.columns(2)
            with col1:
                time = st.number_input(f"Time Taken (min)", key=f"resharp_time_{i}", value=35.00)
            with col2:    
                cost_hr = st.number_input(f"Extra Tool Cost (Rs.)", key=f"resharp_cost_{i}", value=50.00)
            entry.update({"time_min": time, "extra_tool_cost": cost_hr})

        elif  ptype == "Tool Change":
            col1, col2 = st.columns(2)
            with col1:
                time = st.number_input(f"Time Taken (min)", key=f"tool_change_time_{i}", value=35.00)
            with col2:    
                cost_hr = st.number_input(f"Extra Tool Cost (Rs.)", key=f"tool_change_cost_{i}", value=50.00)
            entry.update({"time_min": time, "extra_tool_cost": cost_hr})

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

            if process_type == "Boring":
                try:
                    a = math.radians((180 - entry["angle"]) / 2)
                    extra_length = (entry["initial diameter"] / 2) * (math.tan(a))
                    turn = (entry["final diameter"] - entry["initial diameter"]) / ((entry["depth of cut"]) * 2)
                    time = (((entry["approach"] + entry["overrun"] + (entry["depth"])) / (entry["rpm"] * entry["feed"]) * (turn * 2)) + (((10 + extra_length) / (entry["feed"] * entry["rpm"])) * (turn * 2))) + (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0
            
            elif process_type == "Drilling - Center":
                try:
                    drill_length = ((entry["diameter"] / 2) * (math.tan(math.radians((180 - 118) / 2)))) + entry["depth"]
                    time = ((entry["approach"] + entry["overrun"] + drill_length) / (entry["rpm"] * entry["feed"]) * (entry["turn"])) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0

            elif process_type == "Drilling - Pilot":
                try:
                    drill_length = ((entry["diameter"] / 2) * (math.tan(math.radians((180 - 118) / 2)))) + entry["depth"]
                    time = ((entry["approach"] + entry["overrun"] + drill_length) / (entry["rpm"] * entry["feed"]) * (entry["turn"])) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0

            elif process_type == "Drilling - Main":
                try:
                    drill_length = ((entry["diameter"] / 2) * (math.tan(math.radians((180 - 118) / 2)))) + entry["depth"]
                    time = ((entry["approach"] + entry["overrun"] + drill_length) / (entry["rpm"] * entry["feed"]) * (entry["turn"])) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0
            
            elif process_type == "Facing":
                try:
                    turn = (entry["length"]/entry["depth of cut"]) 
                    time = ((((entry["approach"] + entry["overrun"] + (entry["diameter"] / 2)) / (entry["feed"] * entry["rpm"])) * turn)) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0
        
            elif process_type == "Grooving":
                try:
                    turn = (entry["length"]) / (entry["tool width"])
                    time = ((((entry["approach"] + entry["overrun"] + (entry["final diameter"] - entry["initial diameter"])) / (entry["feed"] * entry["rpm"])) * turn)) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0
            
            elif process_type == "Knurling":
                try:
                    time = ((((entry["approach"] + entry["overrun"] + (entry["length"])) / (entry["feed"] * entry["rpm"])) * 4)) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0
            
            elif process_type == "Reaming":
                try:
                    turn = (entry["final diameter"] - entry["initial diameter"]) / (2 * entry["depth of cut"])
                    time = ((((entry["approach"] + entry["overrun"] + (entry["length"])) / (entry["feed"] * entry["rpm"])) * turn)) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0
            
            elif process_type == "Threading":
                try:
                    turn = (0.6134 * entry["pitch"]) / (entry["depth of cut"])
                    time = (((entry["approach"] + entry["overrun"] + (entry["length"])) / (entry["rpm"] * entry["feed"]) * (turn))) +  (entry["job set time"] + entry["tool set time"]) 
                except ZeroDivisionError:
                    time = 0
            
            elif process_type == "Turning - Concave":
                try:
                    concave_length = entry["length"] * (math.radians(entry["angle"]))
                    turn = (entry["diameter"]) / (entry["depth of cut"] * 4) 
                    time = ((((entry["approach"] + entry["overrun"] + concave_length) / (entry["feed"] * entry["rpm"])) * turn)) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0

            elif process_type == "Turning - Convex":
                try:
                    convex_length = entry["length"] * (math.radians(entry["angle"]))
                    turn = (entry["diameter"]) / (entry["depth of cut"] * 4) 
                    time = ((((entry["approach"] + entry["overrun"] + convex_length) / (entry["feed"] * entry["rpm"])) * turn)) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0
            
            elif process_type == "Turning - Straight":
                try:
                    turn = ((entry["initial diameter"]) - (entry["final diameter"])) / ((entry["depth of cut"]) * 2) 
                    time = ((((entry["approach"] + entry["overrun"] + (entry["length"])) / (entry["feed"] * entry["rpm"])) * turn)) +  (entry["job set time"] + entry["tool set time"])
                except ZeroDivisionError:
                    time = 0

            elif process_type == "Turning - Taper":
                try:
                    h_length = math.sqrt(((entry["length"]) ** 2) + (((entry["larger diameter"] - entry["smaller diameter"]) / 2) ** 2))
                    turn = (((entry["larger diameter"]) - (entry["smaller diameter"])) / ((entry["depth of cut"]) * 2)) 
                    time = ((((entry["approach"] + entry["overrun"] + h_length) / (entry["feed"] * entry["rpm"])) * turn)) +  (entry["job set time"] + entry["tool set time"])
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
            cost_hr = entry.get("extra_tool_cost", 0.0)

            minutes_with_overhead = minutes + 5
            total_time_min += minutes_with_overhead
            total_extra_cost += cost_hr

            # Handle label
            if ptype == "Custom":
                label = entry.get("custom_name", f"Custom #{i+1}")
            else:
                label = ptype

            extra_times.append({
                "ptype": label,
                "index": i + 1,
                "time": minutes_with_overhead,
                "cost": cost_hr
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


from fpdf import FPDF
import streamlit as st
import tempfile
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, 'Machining Time & Cost Estimate', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def table(self, title, data_list):
        if not data_list:
            return

        self.add_page()
        self.set_font("Helvetica", 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Helvetica", '', 10)
        self.ln(2)

        keys = list(data_list[0].keys())
        epw = self.w - 2 * self.l_margin
        col_width = max(30, epw / min(len(keys), 6))  # reasonable width per column
        columns_per_page = int(epw // col_width)
        total_pages = math.ceil(len(keys) / columns_per_page)

        for page in range(total_pages):
            start_col = page * columns_per_page
            end_col = start_col + columns_per_page
            current_keys = keys[start_col:end_col]

            if page > 0:
                self.add_page()
                self.set_font("Helvetica", 'B', 12)
                self.cell(0, 10, f"{title} (continued)", ln=True)
                self.set_font("Helvetica", '', 10)
                self.ln(2)

            # Table header
            self.set_font("Helvetica", 'B', 9)
            for k in current_keys:
                self.cell(col_width, 8, k[:15], border=1)
            self.ln()

            # Table rows
            self.set_font("Helvetica", '', 9)
            for row in data_list:
                for k in current_keys:
                    val = str(row.get(k, ""))
                    self.cell(col_width, 8, val[:20], border=1)
                self.ln()
                # Page break if needed
                if self.get_y() > 270:
                    self.add_page()
                    # Reprint header on new page
                    self.set_font("Helvetica", 'B', 9)
                    for k in current_keys:
                        self.cell(col_width, 8, k[:15], border=1)
                    self.ln()
                    self.set_font("Helvetica", '', 9)

def generate_pdf():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)

    # --- Summary Table ---
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, 'Summary', ln=True)
    pdf.set_font("Helvetica", '', 10)

    summary_data = [
        ["Total Time (hr:min)", f"{int(st.session_state.total_time_min//60)}:{int(st.session_state.total_time_min%60)}"],
        ["Labor Cost (Rs.)", f"{st.session_state.labor_cost:.2f}"],
        ["Job Material", f"{st.session_state.job_material}"],
        ["Material Cost (Rs.)", f"{st.session_state.material_cost:.2f}"],
        ["Tool Cost (Rs.)", f"{st.session_state.tool_cost:.2f}"],
        ["Extra Process Cost (Rs.)", f"{st.session_state.total_extra_cost:.2f}"],
        ["Total Estimated Cost (Rs.)", f"{st.session_state.total_cost:.2f}"]
    ]
    for row in summary_data:
        pdf.cell(60, 8, row[0], border=1)
        pdf.cell(80, 8, row[1], border=1)
        pdf.ln()

    pdf.ln(5)

    # --- Process Time Tables ---
    if st.session_state.machining_times:
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 10, 'Machining Process Times', ln=True)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(50, 8, "Process", border=1)
        pdf.cell(40, 8, "Time (min)", border=1)
        pdf.cell(40, 8, "Cost (Rs.)", border=1)
        pdf.ln()
        pdf.set_font("Helvetica", '', 10)
        for t in st.session_state.machining_times:
            pdf.cell(50, 8, f"{t['process']} #{t['index']}", border=1)
            pdf.cell(40, 8, f"{t['time']:.2f}", border=1)
            pdf.cell(40, 8, f"{t['cost']:.2f}", border=1)
            pdf.ln()
        pdf.ln(5)

    if st.session_state.extra_times:
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 10, 'Extra Processes', ln=True)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(50, 8, "Process", border=1)
        pdf.cell(40, 8, "Time (min)", border=1)
        pdf.cell(40, 8, "Cost (Rs.)", border=1)
        pdf.ln()
        pdf.set_font("Helvetica", '', 10)
        for t in st.session_state.extra_times:
            pdf.cell(50, 8, f"{t['ptype']} #{t['index']}", border=1)
            pdf.cell(40, 8, f"{t['time']:.2f}", border=1)
            pdf.cell(40, 8, f"{t['cost']:.2f}", border=1)
            pdf.ln()
        pdf.ln(5)

    # --- Full DataFrames ---
    #pdf.table("Machining Entries", st.session_state.machining_entries)
    #pdf.table("Extra Process Entries", st.session_state.extra_entries)

    # Save and offer download
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        with open(tmpfile.name, "rb") as f:
            st.download_button("⬇️ Download Full PDF", f, file_name="machining_full_result.pdf")
    os.unlink(tmpfile.name)



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
    st.success(f"📦 Job Material : {st.session_state.job_material}")
    st.success(f"📦 Material Cost: Rs. {st.session_state.material_cost:.2f}")
    st.success(f"🧰 Tool Cost: Rs. {st.session_state.tool_cost:.2f}")
    st.success(f"➕ Extra Process Tool Cost: Rs. {st.session_state.total_extra_cost:.2f}")
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

    st.markdown("---")
    if st.button("Export as PDF"):
        generate_pdf()


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
