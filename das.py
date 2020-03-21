# for this task, i try to build a mesh using OOP
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
from node import Node
from element import Element
import time
from value import Value
import time

node_array = []
element_array = []
value_array = []
hotspot_array = []
st_time_1 = time.time()
with open("mesh_x_sin_cos_10000.txt", "r") as f :
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

element_array.sort(key=lambda x : x.value, reverse=True)
end_time_1 = time.time()
print("Computational time: {}s".format(end_time_1 - st_time_1))

st_time_3 =time.time()
def is_neighbor(e1, e2) :
    if e1.node1 == e2.node1 or e1.node1 == e2.node2 or e1.node1 == e2.node3 : return True
    if e1.node2 == e2.node1 or e1.node2 == e2.node2 or e1.node2 == e2.node3 : return True
    if e1.node3 == e2.node1 or e1.node3 == e2.node2 or e1.node3 == e2.node3 : return True
    return False
end_time_3 = time.time()
print("Computational time: {}s".format(end_time_3 - st_time_3))


[i.neighbors.add(j.id) for i in element_array for j in element_array if (is_neighbor(i, j) and i.id != j.id)]


def mark_as_visited(lst) :
    for ls in lst :
        for el in element_array :
            if el.id == ls : el.visited = True


def get_element(id) :
    for el in element_array :
        if el.id == id : return el


st_time = time.time()


def find_hotspot(N) :
    while N >= 1 :
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
                N -= 1


find_hotspot(3)

end_time = time.time()
print("Computational time: {}s".format(end_time - st_time))
