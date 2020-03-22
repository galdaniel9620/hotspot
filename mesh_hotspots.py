
from node import Node
from element import Element
import time


node_array = []
element_array = []
value_array = []
hotspots_array = []

with open("mesh_x_sin_cos_20000.txt", "r") as f :
    lines = [line.strip() for line in f.readlines()]
    try :
        nodes_idx = lines.index("NODES")
        elements_idx = lines.index("ELEMENTS")
        values_idx = lines.index("VALUES")
        if not nodes_idx < elements_idx < values_idx :
            raise ValueError()
        nodes = [eval(line) for line in
                 lines[nodes_idx + 1 : elements_idx]]
        elements = [eval(line) for line in lines[elements_idx + 1 : values_idx]]
        values = [eval(line) for line in lines[values_idx + 1 : :]]
        [node_array.append(Node(i[0], i[1], [2])) for i in nodes]
        [element_array.append(Element(j[0], j[1], j[2], j[3])) for j in elements]
        for k in range(len(element_array)) :
            element_array[k].value = values[k][1]
    except ValueError :
        print("Invalid mesh file format")


def is_neighbor(e1, e2) :
    if e1.node1 == e2.node1 or e1.node1 == e2.node2 or e1.node1 == e2.node3 : return True
    if e1.node2 == e2.node1 or e1.node2 == e2.node2 or e1.node2 == e2.node3 : return True
    if e1.node3 == e2.node1 or e1.node3 == e2.node2 or e1.node3 == e2.node3 : return True
    return False


[element_array[i].neighbors.add(element_array[j].id) for i in range(0, len(element_array)) for j in
 range(i + 1, len(element_array)) if
 is_neighbor(element_array[i], element_array[j]) and element_array[i].id != element_array[j].id if
 element_array[j].id not in element_array[i].neighbors]


def mark_as_visited(lst) :
    for ls in lst :
        for el in element_array :
            if el.id == ls : el.visited = True


def get_element(id) :
    for el in element_array :
        if el.id == id : return el


def find_hotspots(h) :
    while h >= 1 :
        for x in element_array :
            is_hotspot = True
            for y in x.neighbors :
                if x.value < get_element(y).value :
                    is_hotspot = False
                    break
                x.is_hotspot = is_hotspot
            if is_hotspot :
                x.visited = True
                mark_as_visited(x.neighbors)
                hotspots_array.append([x.id, x.value])
                h -= 1


def display(N) :
    find_hotspots(2)
    hotspots_array.sort(key=lambda x : x[1], reverse=True)
    for i in range(0, N) :
        print(hotspots_array[i])


display(int(input("N =")))
