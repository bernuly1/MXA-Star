import heapq
import sys
from g_node import g_node
from heapq import heapify, heappush, heappop


class MinHeap:

    def __init__(self):
        self.heap = []
        heapify(self.heap)

    # Function to return the position of
    # parent for the node currently
    # at pos
    def parent(self, pos):
        return pos // 2

    # Function to return the position of
    # the left child for the node currently
    # at pos
    def leftChild(self, pos):
        return 2 * pos

    # Function to return the position of
    # the right child for the node currently
    # at pos
    def rightChild(self, pos):
        return (2 * pos) + 1

    # Function that returns true if the passed
    # node is a leaf node
    def isLeaf(self, pos):
        if pos >= (self.size // 2) and pos <= self.size:
            return True
        return False

    # Function to swap two nodes of the heap
    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]

    # Function to heapify the node at pos
    def minHeapify(self, pos):

        # If the node is a non-leaf node and greater
        # than any of its child
        if not self.isLeaf(pos):
            if self.lessThen(self.Heap[self.leftChild(pos)], self.Heap[pos]) or \
                    self.lessThen(self.Heap[self.rightChild(pos)], self.Heap[pos]):
                # Swap with the left child and heapify
                # the left child
                if self.lessThen(self.Heap[self.leftChild(pos)], self.Heap[self.rightChild(pos)]):
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))

                # Swap with the right child and heapify
                # the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))

    def lessThen(self, element1, element2):
        return element1.f < element2.f or (element1.f == element2.f and element1.h < element2.h)
    # Function to insert a node into the heap
    def insert(self, element):
        heappush(self.heap, element)

    def get(self, pos):
        for i in range(len(self.heap)):
            if self.heap[i].position == pos:
                # element = self.heap.pop(i)
                # heapify(self.heap)
                element = self.heap[i]
                self.heap[i] = self.heap[-1]
                self.heap.pop()
                if i < len(self.heap):
                    heapq._siftup(self.heap, i)
                    heapq._siftdown(self.heap, 0, i)
                break
        return element

    # Function to print the contents of the heap
    def Print(self):
        for i in range(1, (self.size // 2) + 1):
            print(" PARENT : " + str(self.Heap[i]) + " LEFT CHILD : " +
                  str(self.Heap[2 * i]) + " RIGHT CHILD : " +
                  str(self.Heap[2 * i + 1]))

    # Function to build the min heap using
    # the minHeapify function
    def minHeap(self):

        for pos in range(self.size // 2, 0, -1):
            self.minHeapify(pos)

    # Function to remove and return the minimum
    # element from the heap
    def remove(self):
        return heappop(self.heap)
