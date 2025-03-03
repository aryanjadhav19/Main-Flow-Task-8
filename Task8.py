# Importing necessary libraries
import sys
from collections import defaultdict

# --- 55. Serialize and Deserialize Binary Tree ---
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class BinaryTree:
    def serialize(self, root):
        def pre_order(node):
            if node is None:
                return 'None'
            return str(node.val) + ',' + pre_order(node.left) + pre_order(node.right)
        return pre_order(root)
    def deserialize(self, data):
        values = iter(data.split(','))
        def build_tree():
            val = next(values)
            if val == 'None':
                return None
            node = TreeNode(int(val))
            node.left = build_tree()
            node.right = build_tree()
            return node
        return build_tree()

# --- 56. Maximum Flow in a Graph (Ford-Fulkerson) ---
def bfs(capacity, source, sink, parent):
    visited = [False] * len(capacity)
    queue = [source]
    visited[source] = True
    while queue:
        u = queue.pop(0)
        for v in range(len(capacity)):
            if not visited[v] and capacity[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    return False

def ford_fulkerson(capacity, source, sink):
    parent = [-1] * len(capacity)
    max_flow = 0
    while bfs(capacity, source, sink, parent):
        path_flow = float('Inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s])
            s = parent[s]
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = parent[v]
    return max_flow

# --- 57. Edit Distance (Levenshtein Distance) ---
def edit_distance(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

# --- 58. K-th Smallest Element in a BST ---
def kth_smallest_in_bst(root, k):
    def inorder_traversal(node):
        if node is None:
            return []
        return inorder_traversal(node.left) + [node.val] + inorder_traversal(node.right)
    return inorder_traversal(root)[k - 1]

# --- 59. Maximum Subarray Product ---
def max_subarray_product(arr):
    if not arr:
        return 0
    max_prod = min_prod = result = arr[0]
    for num in arr[1:]:
        if num < 0:
            max_prod, min_prod = min_prod, max_prod
        max_prod = max(num, max_prod * num)
        min_prod = min(num, min_prod * num)
        result = max(result, max_prod)
    return result

# --- 60. Find All Paths in a Graph ---
def find_all_paths(graph, start, end):
    def dfs(u, path):
        if u == end:
            paths.append(path[:])
            return
        for v in graph[u]:
            if v not in path:
                path.append(v)
                dfs(v, path)
                path.pop()
    paths = []
    dfs(start, [start])
    return paths

# --- Menu Driven Program ---
def menu():
    print("\nMenu:")
    print("1. Serialize and Deserialize Binary Tree")
    print("2. Maximum Flow in a Graph (Ford-Fulkerson)")
    print("3. Edit Distance (Levenshtein Distance)")
    print("4. K-th Smallest Element in a BST")
    print("5. Maximum Subarray Product")
    print("6. Find All Paths in a Graph")
    print("7. Exit")

def main():
    while True:
        menu()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            tree = BinaryTree()
            root = TreeNode(1, TreeNode(2), TreeNode(3))
            serialized = tree.serialize(root)
            print(f"Serialized Tree: {serialized}")
            deserialized = tree.deserialize(serialized)
            print(f"Deserialized Tree Root: {deserialized.val}")

        elif choice == 2:
            graph = [[0, 16, 13, 0, 0, 0],
                     [0, 0, 10, 12, 0, 0],
                     [0, 4, 0, 0, 14, 0],
                     [0, 0, 9, 0, 0, 20],
                     [0, 0, 0, 7, 0, 4],
                     [0, 0, 0, 0, 0, 0]]
            source = 0
            sink = 5
            max_flow = ford_fulkerson(graph, source, sink)
            print(f"Maximum Flow: {max_flow}")

        elif choice == 3:
            str1 = input("Enter first string: ")
            str2 = input("Enter second string: ")
            print(f"Edit Distance: {edit_distance(str1, str2)}")

        elif choice == 4:
            # Example BST
            root = TreeNode(5)
            root.left = TreeNode(3)
            root.right = TreeNode(8)
            root.left.left = TreeNode(2)
            root.left.right = TreeNode(4)
            root.right.left = TreeNode(7)
            root.right.right = TreeNode(9)
            k = int(input("Enter k: "))
            print(f"{k}-th Smallest Element: {kth_smallest_in_bst(root, k)}")

        elif choice == 5:
            arr = list(map(int, input("Enter array elements: ").split()))
            print(f"Maximum Subarray Product: {max_subarray_product(arr)}")

        elif choice == 6:
            graph = defaultdict(list)
            graph[0] = [1, 2]
            graph[1] = [3]
            graph[2] = [3]
            graph[3] = [4]
            start = 0
            end = 4
            paths = find_all_paths(graph, start, end)
            print(f"All paths from {start} to {end}: {paths}")

        elif choice == 7:
            print("Exiting program...")
            sys.exit()

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()