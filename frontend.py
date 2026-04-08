import streamlit as st
import requests
import networkx as nx
import matplotlib.pyplot as plt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Code Visualizer", layout="wide")

st.title("🔥 Code Visualizer (AST + CFG + Explanation)")
st.info("This tool analyzes Python code using AST (structure) and CFG (execution flow).")

# ---------- SAMPLE CODE ----------
sample_code = """def add(a, b):
    return a + b

for i in range(5):
    if i % 2 == 0:
        print(add(i, i))"""

if st.button("⚡ Load Sample Code"):
    st.session_state.code = sample_code

# ---------- INPUT ----------
code = st.text_area(
    "✍️ Enter Python Code:",
    height=250,
    value=st.session_state.get("code", "")
)

# ---------- SHOW CODE ----------
if code.strip():
    st.subheader("📄 Your Code")
    st.code(code, language="python")

# ---------- AST TREE ----------
def display_tree(node, level=0):
    indent = "   " * level
    st.write(f"{indent}👉 {node['type']} → {node['description']}")
    for child in node.get("children", []):
        display_tree(child, level + 1)

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["🌳 AST", "🔗 CFG", "🧠 Explanation"])

# ================= AST =================
with tab1:
    if code.strip() == "":
        st.warning("Enter code to see AST")
    else:
        with st.spinner("Generating AST..."):
            try:
                res = requests.post("http://127.0.0.1:5000/parse", json={"code": code})
                data = res.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.success("AST Generated Successfully!")
                    display_tree(data)

            except:
                st.error("⚠️ Backend not running!")

# ================= CFG =================
with tab2:
    if code.strip() == "":
        st.warning("Enter code to see CFG")
    else:
        with st.spinner("Generating CFG..."):
            try:
                res = requests.post("http://127.0.0.1:5000/cfg", json={"code": code})
                data = res.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.success("CFG Generated Successfully!")

                    G = nx.DiGraph()

                    for node in data["nodes"]:
                        G.add_node(node["id"], label=node["label"])

                    for edge in data["edges"]:
                        G.add_edge(edge["source"], edge["target"])

                    pos = nx.spring_layout(G, seed=42)
                    labels = nx.get_node_attributes(G, 'label')

                    # 🎨 Color logic
                    color_map = []
                    for node in data["nodes"]:
                        label = node["label"]

                        if "Loop" in label:
                            color_map.append("lightblue")
                        elif "IF" in label:
                            color_map.append("lightcoral")
                        elif "START" in label:
                            color_map.append("lightgreen")
                        elif "END" in label:
                            color_map.append("orange")
                        else:
                            color_map.append("lightgrey")

                    plt.figure(figsize=(7, 5))
                    nx.draw(
                        G,
                        pos,
                        labels=labels,
                        with_labels=True,
                        node_color=color_map,
                        node_size=2200,
                        font_size=9
                    )

                    st.pyplot(plt)

            except:
                st.error("⚠️ Backend not running!")

# ================= EXPLANATION =================
with tab3:
    if code.strip() == "":
        st.warning("Enter code to see explanation")
    else:
        with st.spinner("Analyzing Code..."):
            try:
                res = requests.post("http://127.0.0.1:5000/explain", json={"code": code})
                data = res.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.success("Explanation Generated!")

                    st.text_area(
                        "🧠 Explanation Output",
                        data["explanation"],
                        height=300
                    )

            except:
                st.error("⚠️ Backend not running!")

# ---------- FOOTER ----------
st.markdown("---")
st.write("💡 Built using Flask + Streamlit | Advanced Code Visualizer")