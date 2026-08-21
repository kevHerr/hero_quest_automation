import matplotlib.pyplot as plt
import numpy as np
import heapq


dungeon_matrix = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,1,1,1,1,2,2,2,2,3,3,3,0,0,4,4,4,5,5,5,5,6,6,6,6,0],
[0,1,1,1,1,2,2,2,2,3,3,3,0,0,4,4,4,5,5,5,5,6,6,6,6,0],
[0,1,1,1,1,2,2,2,2,3,3,3,0,0,4,4,4,5,5,5,5,6,6,6,6,0],
[0,7,7,7,7,8,8,8,8,3,3,3,0,0,4,4,4,5,5,5,5,6,6,6,6,0],
[0,7,7,7,7,8,8,8,8,3,3,3,0,0,4,4,4,10,10,10,10,11,11,11,11,0],
[0,7,7,7,7,8,8,8,8,0,0,0,0,0,0,0,0,10,10,10,10,11,11,11,11,0],
[0,7,7,7,7,8,8,8,8,0,9,9,9,9,9,9,0,10,10,10,10,11,11,11,11,0],
[0,7,7,7,7,8,8,8,8,0,9,9,9,9,9,9,0,10,10,10,10,11,11,11,11,0],
[0,0,0,0,0,0,0,0,0,0,9,9,9,9,9,9,0,0,0,0,0,0,0,0,0,0],
[0,12,12,12,12,13,13,14,14,0,9,9,9,9,9,9,0,15,15,15,15,16,16,16,16,0],
[0,12,12,12,12,13,13,14,14,0,9,9,9,9,9,9,0,15,15,15,15,16,16,16,16,0],
[0,12,12,12,12,13,13,14,14,0,0,0,0,0,0,0,0,15,15,15,15,16,16,16,16,0],
[0,12,12,12,12,18,18,18,18,19,19,19,0,0,20,20,20,20,15,15,15,16,16,16,16,0],
[0,17,17,17,17,18,18,18,18,19,19,19,0,0,20,20,20,20,21,21,21,22,22,22,22,0],
[0,17,17,17,17,18,18,18,18,19,19,19,0,0,20,20,20,20,21,21,21,22,22,22,22,0],
[0,17,17,17,17,18,18,18,18,19,19,19,0,0,20,20,20,20,21,21,21,22,22,22,22,0],
[0,17,17,17,17,18,18,18,18,19,19,19,0,0,20,20,20,20,21,21,21,22,22,22,22,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

]


def find_nearest_block(matrix, reference, valid_range):
    rows, cols = len(matrix), len(matrix[0])
    rx, ry = reference
    nearest = None
    min_dist = float('inf')

    for i in range(rows):
        for j in range(cols):
            if valid_range[0] <= matrix[i][j] <= valid_range[1]:
                dist = abs(rx - i) + abs(ry - j)  # distance from END point
                if dist < min_dist:
                    min_dist = dist
                    nearest = (i, j)
    return nearest


def astar_with_condition(matrix, start, end):
    start_val = matrix[start[0]][start[1]]
    end_val   = matrix[end[0]][end[1]]

    # Condition: end between 200–299
    if 200 <= end_val <= 299 and start_val != end_val:
        # Find nearest 300–399 block relative to END
        nearest_door = find_nearest_block(matrix, end, (100, 199))
        if nearest_door is None:
            print("No valid 300–399 block found!")
            return None

        # Path: start → nearest door → end
        path1 = movement_astar(matrix, start, nearest_door)
        path2 = movement_astar(matrix, nearest_door, end)

        if path1 and path2:
            return path1 + path2[1:]  # merge paths
        else:
            return None
    else:
        # Normal A*
        return movement_astar(matrix, start, end)



def movement_astar(matrix, start, end):
    rows, cols = len(matrix), len(matrix[0])
    print(rows, cols, type(matrix))
    def heuristic(a, b): #manhatan distance
        return(abs(a[0]- b[0]+ abs(a[1]-b[1])))
    
    def neighbors(node):
        x, y = node
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x +dx, y +dy
            #check that is a walkable path, 
            if 0 <= nx <  rows and 0 <= ny < cols:
                cell_value = matrix[nx][ny]
                if cell_value == 0 or cell_value >100 and cell_value< 300:
                    yield(nx, ny) 
    
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start,end), 0, start,[start]))
    visited = set()        
    
    while open_set:
        f,g, current, path = heapq.heappop(open_set)
        if current is visited:
            continue
        visited.add(current)
        if current == end:
            return path
        
        for neighbor in neighbors(current):
            if neighbor not in visited:
                new_g = g+1 
                new_f = new_g + heuristic(neighbor, end)
                heapq.heappush(open_set,(new_f, new_g, neighbor, path + [neighbor]))
                
    
    
    return None


def open_room(matrix,pos1,pos2,value):
    dungeon = matrix
    door = value + dungeon[pos1][pos2]
    dungeon[pos1][pos2] = door
    arr = np.array(dungeon)
    arr[arr == dungeon[pos1][pos2]- 100]= door + 100
    new_dungeon = arr.tolist()    
    return new_dungeon




def print_Map(matrix, path=None):
    plt.figure(figsize=(10,6))
    plt.imshow(np.array(dungeon_matrix), cmap='tab20', origin='upper')
    plt.colorbar(label='Room Number')
    plt.title('Dungeon Layout Visualization')
    
    if path:
        path_x =[p[1] for p in path]
        path_y =[p[0] for p in path]
        plt.plot(path_x, path_y, color='red', linewidth=2, marker='o', markersize=4, label="A*path" )
        plt.legend()
    doors = [(i,j) for i, row in enumerate(matrix) for j, val in enumerate(row) if val > 100]
    if doors:
        door_x = [d[1] for d in doors]
        door_y = [d[0] for d in doors]
        plt.scatter(door_x, door_y, color='yellow', marker='s', s=80, label='Doors')
    plt.show()


start= 0,0
end = 9,13
end2 = 16,21

path_opened = open_room(dungeon_matrix, pos1=9,pos2=10, value=100)
path_opened2 = open_room(dungeon_matrix, pos1=17,pos2=23, value=100)
print(path_opened2)
path =astar_with_condition(path_opened2, start,end2)
print(path)
print_Map(dungeon_matrix,path)


