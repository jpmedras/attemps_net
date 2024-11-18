graph [
  name "G"
  graph [
    rankdir "BT"
  ]
  node [
    id 0
    label "1"
    size 2
    neighborhood "A"
    neighborhood "B"
    shape "circle"
    style "filled"
    fillcolor "lightblue"
    community 0
  ]
  node [
    id 1
    label "2"
    size 3
    neighborhood "A"
    neighborhood "B"
    neighborhood "C"
    shape "circle"
    style "filled"
    fillcolor "lightblue"
    community 0
  ]
  node [
    id 2
    label "3"
    size 2
    neighborhood "C"
    neighborhood "D"
    shape "circle"
    style "filled"
    fillcolor "lightblue"
    community 1
  ]
  edge [
    source 0
    target 1
    weight 2
    label "2"
  ]
]
