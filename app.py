# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xBW4r1yKO0XbKDX1JZpg9haMCN1EpOE1
"""

from flask import Flask, jsonify, request

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def insert(self, data, priority):
        if self.size() == 0:
            self.queue.append((data, priority))
        else:
            for index, (d, p) in enumerate(self.queue):
                if priority < p:
                    self.queue.insert(index, (data, priority))
                    return
            self.queue.append((data, priority))

    def delete(self, data):
        index = next((i for i, (d, p) in enumerate(self.queue) if d == data), None)
        if index is not None:
            self.queue.pop(index)

    def extractMin(self):
        if self.size() == 0:
            return None
        else:
            return self.queue.pop(0)

    def decreaseKey(self, data, priority):
        self.delete(data)
        self.insert(data, priority)

    def size(self):
        return len(self.queue)

    def __contains__(self, data):
        return any(data == d for d, _ in self.queue)

def myDijkstra(adj_matrix, origin):
    n = len(adj_matrix)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[origin] = 0
    Q = PriorityQueue()
    for i in range(n):
        Q.insert(i, dist[i])

    while Q.size() > 0:
        u, _ = Q.extractMin()
        for v, w in enumerate(adj_matrix[u]):
            if w != 0:
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    Q.decreaseKey(v, alt)

    return dist, prev

# Sample adjacency matrix for testing purposes
adj_matrix = [
    [0, 1, 4, 0, 0, 0],
    [1, 0, 4, 2, 7, 0],
    [4, 4, 0, 3, 5, 0],
    [0, 2, 3, 0, 4, 6],
    [0, 7, 5, 4, 0, 7],
    [0, 0, 0, 6, 7, 0]
]

app = Flask(__name__)

@app.route('/')
def home():
    return "Dijkstra's algorithm web server"

@app.route('/shortest_path/<int:origin>/<int:destination>')
def get_shortest_path(origin, destination):
    dist, prev = myDijkstra(adj_matrix, origin)
    path = [destination]
    while destination != origin:
        destination = prev[destination]
        if destination is None:
            return jsonify({"error": "No path found"}), 400
        path.append(destination)
    path.reverse()
    return jsonify(path)

if __name__ == '__main__':
    app.run(debug=True)