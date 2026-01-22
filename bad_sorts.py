"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.
"""
import random


# Create a random list length "length" containing whole numbers between 0 and max_value inclusive
def create_random_list(length, max_value):
    return [random.randint(0, max_value) for _ in range(length)]


# Creates a near sorted list by creating a random list, sorting it, then doing a random number of swaps
def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L


# I have created this function to make the sorting algorithm code read easier
def swap(L, i, j):
    L[i], L[j] = L[j], L[i]


# ******************* Insertion sort code *******************

# This is the traditional implementation of Insertion Sort.
def insertion_sort(L):
    for i in range(1, len(L)):
        insert(L, i)


def insert(L, i):
    while i > 0:
        if L[i] < L[i-1]:
            swap(L, i-1, i)
            i -= 1
        else:
            return


# This is the optimization/improvement we saw in lecture
def insertion_sort2(L):
    for i in range(1, len(L)):
        insert2(L, i)


def insert2(L, i):
    value = L[i]
    while i > 0:
        if L[i - 1] > value:
            L[i] = L[i - 1]
            i -= 1
        else:
            L[i] = value
            return
    L[0] = value


# ******************* Bubble sort code *******************

# Traditional Bubble sort
def bubble_sort(L):
    for i in range(len(L)):
        for j in range(len(L) - 1):
            if L[j] > L[j+1]:
                swap(L, j, j+1)


# ******************* Selection sort code *******************

# Traditional Selection sort
def selection_sort(L):
    for i in range(len(L)):
        min_index = find_min_index(L, i)
        swap(L, i, min_index)


def find_min_index(L, n):
    min_index = n
    for i in range(n+1, len(L)):
        if L[i] < L[min_index]:
            min_index = i
    return min_index

# ******************* Experiment 2: Variations *******************

# Bubble variation: use "insert + shift" idea (similar to insertion_sort2)
def bubblesort2(L):
    n = len(L)
    for i in range(n):
        for j in range(0, n - 1):
            if L[j] > L[j + 1]:
                value = L[j + 1]
                k = j + 1
                while k > 0 and L[k - 1] > value:
                    L[k] = L[k - 1]
                    k -= 1
                L[k] = value


# Selection variation: find BOTH min and max each pass, shrink boundaries
def selection_sort2(L):
    left = 0
    right = len(L) - 1

    while left < right:
        min_i = left
        max_i = left

        for i in range(left, right + 1):
            if L[i] < L[min_i]:
                min_i = i
            if L[i] > L[max_i]:
                max_i = i

        # put min at left
        swap(L, left, min_i)

        # if max was at left, it moved to min_i after the swap
        if max_i == left:
            max_i = min_i

        # put max at right
        swap(L, right, max_i)

        left += 1
        right -= 1
