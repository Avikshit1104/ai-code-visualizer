async function visualize(){

const code = document.getElementById("codeInput").value

const response = await fetch("http://127.0.0.1:5000/parse",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({code:code})

})

const data = await response.json()

drawTree(data)

}

async function visualizeCFG(){

const code = document.getElementById("codeInput").value

const response = await fetch("http://127.0.0.1:5000/cfg",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({code:code})

})

const data = await response.json()

drawCFG(data)

}

async function explainCode(){

const code = document.getElementById("codeInput").value

const response = await fetch("http://127.0.0.1:5000/explain",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({code:code})

})

const data = await response.json()

document.getElementById("output").innerText = data.explanation

}

function drawTree(treeData){

document.getElementById("tree").innerHTML = ""

const width = 900
const height = 650

const svg = d3.select("#tree")
.append("svg")
.attr("width", width)
.attr("height", height)
.append("g")
.attr("transform", "translate(50,50)")

const root = d3.hierarchy(treeData)

const treeLayout = d3.tree().size([width - 100, height - 100])

treeLayout(root)

svg.selectAll("line")
.data(root.links())
.enter()
.append("line")
.attr("x1",d=>d.source.x)
.attr("y1",d=>d.source.y)
.attr("x2",d=>d.target.x)
.attr("y2",d=>d.target.y)
.attr("stroke","white")

svg.selectAll("circle")
.data(root.descendants())
.enter()
.append("circle")
.attr("cx",d=>d.x)
.attr("cy",d=>d.y)
.attr("r",10)
.attr("fill","#60a5fa")
.attr("stroke","white")
.attr("stroke-width",2)

svg.selectAll("text")
.data(root.descendants())
.enter()
.append("text")
.attr("x",d=>d.x+12)
.attr("y",d=>d.y+4)
.text(d=>d.data.name)
.attr("fill","white")
.attr("font-size","12px")
.attr("font-weight","bold")

}

function drawCFG(data){

document.getElementById("tree").innerHTML=""

const width = 800
const height = 500

const svg = d3.select("#tree")
.append("svg")
.attr("width",width)
.attr("height",height)

const simulation = d3.forceSimulation(data.nodes)
.force("link", d3.forceLink(data.edges).id(d=>d.id).distance(120))
.force("charge", d3.forceManyBody())
.force("center", d3.forceCenter(width/2,height/2))

const link = svg.selectAll("line")
.data(data.edges)
.enter()
.append("line")
.attr("stroke","white")

const node = svg.selectAll("circle")
.data(data.nodes)
.enter()
.append("circle")
.attr("r",10)
.attr("fill","#f59e0b")
.attr("stroke","white")
.attr("stroke-width",2)

const label = svg.selectAll("text")
.data(data.nodes)
.enter()
.append("text")
.text(d => d.label)
.attr("fill", "white")
.attr("font-size", "12px")
.attr("font-weight", "bold")

simulation.on("tick",()=>{

link
.attr("x1",d=>d.source.x)
.attr("y1",d=>d.source.y)
.attr("x2",d=>d.target.x)
.attr("y2",d=>d.target.y)

node
.attr("cx",d=>d.x)
.attr("cy",d=>d.y)

label
.attr("x",d=>d.x+12)
.attr("y",d=>d.y)

})
}