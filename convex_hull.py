import math
import sys
from typing import List
from typing import Tuple
import math
import random
import time
# from my_tests import *

EPSILON = sys.float_info.epsilon
Point = Tuple[int, int]


def y_intercept(p1: Point, p2: Point, x: int) -> float:
    """
    Given two points, p1 and p2, an x coordinate from a vertical line,
    compute and return the the y-intercept of the line segment p1->p2
    with the vertical line passing through x.
    """
    x1, y1 = p1
    x2, y2 = p2
    slope = (y2 - y1) / (x2 - x1)
    return y1 + (x - x1) * slope

#----------------------------------------------------------------------------------

def triangle_area(a: Point, b: Point, c: Point) -> float:
    """
    Given three points a,b,c,
    computes and returns the area defined by the triangle a,b,c.
    Note that this area will be negative if a,b,c represents a clockwise sequence,
    positive if it is counter-clockwise,
    and zero if the points are collinear.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    return ((cx - bx) * (by - ay) - (bx - ax) * (cy - by)) / 2

#----------------------------------------------------------------------------------

def is_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) < -EPSILON

#----------------------------------------------------------------------------------

def is_counter_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a counter-clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) > EPSILON

#----------------------------------------------------------------------------------

def collinear(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c are collinear
    (subject to floating-point precision)
    """
    return abs(triangle_area(a, b, c)) <= EPSILON

#----------------------------------------------------------------------------------

def clockwise_sort(points: List[Point]):
    """
    Given a list of points, sorts those points in clockwise order about their centroid.
    Note: this function modifies its argument.
    """
    # get mean x coord, mean y coord
    x_mean = sum(p[0] for p in points) / len(points)
    y_mean = sum(p[1] for p in points) / len(points)

    def angle(point: Point):
        return (math.atan2(point[1] - y_mean, point[0] - x_mean) + 2 * math.pi) % (2 * math.pi)

    points.sort(key=angle)
    return

#----------------------------------------------------------------------------------

#   Evan DeBassio & Jacob Dion
#   Due: Tuesday, February 23
#   Assignment: A2: Convex Hull

#----------------------------------------------------------------------------------

#       *** HELPER FUNCTIONS ***

#----------------------------------------------------------------------------------

def check_for_vertical_line(points):

    key = points[0][1]

    for i in range(len(points)):
        if points[i][0] != key:
            return False
    
    return True

def find_closest_points_idx(left_list, right_list):

    left_list_furthest_right = 0
    right_list_furthest_left = 0

    #Left List
    for i in range(1, len(left_list)):
        if left_list[i][0] > left_list[left_list_furthest_right][0]:
            left_list_furthest_right = i
    
    #Right List
    for i in range(1, len(right_list)):
        if right_list[i][0] < right_list[right_list_furthest_left][0]:
            right_list_furthest_left = i

    return left_list_furthest_right, right_list_furthest_left

def find_upper_tanget(left_list, right_list):

    #Finding the starting points
    i,j = find_closest_points_idx(left_list, right_list)

    #Making the y-intercept line
    L = (left_list[i][0] + right_list[j][0]) / 2

    clockwise_sort(right_list)
    clockwise_sort(left_list)

    while True:
        #Finding the y-intercepts of i,j, and all of its nearest neighbors
        current_yint = y_intercept(left_list[i % len(left_list)], right_list[j % len(right_list)], L)
        #           Mod by len to wrap around back to the start of the list
        i_up_one = y_intercept(left_list[(i + 1) % len(left_list)], right_list[j % len(right_list)], L) 
        i_down_one = y_intercept(left_list[(i - 1) % len(left_list)], right_list[j % len(right_list)], L)
        j_up_one = y_intercept(left_list[i % len(left_list)], right_list[(j + 1) % len(right_list)], L)
        j_down_one = y_intercept(left_list[i % len(left_list)], right_list[(j - 1) % len(right_list)], L)
        #Check if any of the neareast neighbor has a higher y-intercept
        if i_up_one > current_yint and i_up_one >= i_down_one and i_up_one >= j_down_one and i_up_one >= j_up_one:
            i += 1
        elif i_down_one > current_yint and i_down_one >= i_up_one and i_down_one >= j_up_one and i_down_one >= j_down_one:
            i -= 1
        elif j_down_one > current_yint and j_down_one >= i_down_one and j_down_one >= i_up_one and j_down_one >= j_up_one:
            j -= 1
        elif j_up_one > current_yint and j_up_one >= i_down_one and j_up_one >= i_up_one and j_up_one >= j_down_one:
            j += 1
        else:
            break

    return left_list[i % len(left_list)], right_list[j % len(right_list)]


def find_lower_tanget(left_list, right_list):

    #Finding the starting points
    i,j = find_closest_points_idx(left_list, right_list)

    #Making the y-intercept line
    L = (left_list[i][0] + right_list[j][0]) / 2

    clockwise_sort(right_list)
    clockwise_sort(left_list)

    while True:
        #Finding the y-intercepts of i,j, and all of its nearest neighbors
        current_yint = y_intercept(left_list[i % len(left_list)], right_list[j % len(right_list)], L)
        #           Mod by len to wrap around back to the start of the list
        i_up_one = y_intercept(left_list[(i + 1) % len(left_list)], right_list[j % len(right_list)], L) 
        i_down_one = y_intercept(left_list[(i - 1) % len(left_list)], right_list[j % len(right_list)], L)
        j_up_one = y_intercept(left_list[i % len(left_list)], right_list[(j + 1) % len(right_list)], L)
        j_down_one = y_intercept(left_list[i % len(left_list)], right_list[(j - 1) % len(right_list)], L)
        #Check if any of the neareast neighbor has a higher y-intercept
        if i_up_one < current_yint and i_up_one <= i_down_one and i_up_one <= j_down_one and i_up_one <= j_up_one:
            i += 1
        elif i_down_one < current_yint and i_down_one <= i_up_one and i_down_one <= j_up_one and i_down_one <= j_down_one:
            i -= 1
        elif j_down_one < current_yint and j_down_one <= i_down_one and j_down_one <= i_up_one and j_down_one <= j_up_one:
            j -= 1
        elif j_up_one < current_yint and j_up_one <= i_down_one and j_up_one <= i_up_one and j_up_one <= j_down_one:
            j += 1
        else:
            break

    return left_list[i % len(left_list)], right_list[j % len(right_list)]

#Merges the two convex hulls
def merge_points(new_list1, new_list2):

    convex_hull = []

    #Finding the points closest to the denter
    x1,y1 = new_list1[-1]
    x2,y2 = new_list2[0]

    #Finding L, which is the median of the two hulls 
    #   (Used for finding upper and lower tangents)
    L = (x1 + x2) / 2
    L = int(L)

    #Sorting
    clockwise_sort(new_list1)
    clockwise_sort(new_list2)

    #Getting the upper and lower tangents
    upper_tan_left, upper_tan_right = find_upper_tanget(new_list1, new_list2)
    lower_tan_left, lower_tan_right = find_lower_tanget(new_list1, new_list2)

    #Find index location of the upper right
    i = new_list2.index(lower_tan_right)
    #Adding all points from upper right tan to lower right tan in clockwise order
    while 1:
        convex_hull.append(new_list2[i % len(new_list2)])
        if new_list2[i% len(new_list2)] == upper_tan_right:
            break
        i+=1

    #Find index of lower ledt
    j = new_list1.index(upper_tan_left)
    #Adding all the points from the lower left tan to the upper left tan in clockwise order
    while 1:
        convex_hull.append(new_list1[j % len(new_list1)])
        if new_list1[j % len(new_list1)] == lower_tan_left:
            break
        j+=1

    return convex_hull
  
    # #Initializing clockwise / counterclockwise movement
    # end_new_list1 = new_list1[-1]
    # start_new_list2 = new_list2[0]

    # second_to_last = new_list1[-2]
    # second_coord = new_list2[1]

    # #Initial y-intercepts to be compared
    # yint1 = y_intercept(end_new_list1, start_new_list2, L)
    # yint2 = y_intercept(second_to_last, second_coord, L)

    # start_counter = 1
    # end_counter = -2

    # #Finding the bottom of the convex hull (left list) - counterclockwise
    # while yint2 < yint1:
    #     yint1 = yint2
    #     end_counter = end_counter - 1
    #     yint2 = y_intercept(new_list1[end_counter], new_list2[start_counter], L)
     
    # bottom_left_point = new_list1[end_counter]

    # #Reset
    # yint2 = y_intercept(second_to_last, second_coord, L)

    # #Finding the bottom of the convex hull (right list) - clockwise
    # while yint2 < yint1:
    #     yint1 = yint2
    #     start_counter = start_counter + 1
    #     yint2 = y_intercept(new_list1[end_counter], new_list2[start_counter], L)

    # bottom_right_point = new_list2[start_counter]

    # #------------------------------------------------------------------------------

    # #RESET for top of convex hull
    # yint1 = y_intercept(end_new_list1, start_new_list2, L)
    # yint2 = y_intercept(second_to_last, second_coord, L)

    # start_counter = 1
    # end_counter = -2

    # #Finding the top of the convex hull (left list) - clockwise
    # while yint2 > yint1:
    #     yint1 = yint2
    #     end_counter = end_counter + 1
    #     yint2 = y_intercept(new_list1[end_counter], new_list2[start_counter], L)
  
    # top_left_point = new_list1[end_counter]

    # #Reset yint2
    # yint2 = y_intercept(second_to_last, second_coord, L)

    # #Finding the top of the convex hull (right list) - counterclockwise
    # while yint2 > yint1:
    #     yint1 = yint2
    #     start_counter = start_counter - 1
    #     yint2 = y_intercept(new_list1[end_counter], new_list2[start_counter], L)
     
    # top_right_point = new_list1[end_counter]

    # #------------------------------------------------------------------------------

    # # print("The bottom left point is: ", bottom_left_point, '\n')
    # # print("The bottom right point is: ", bottom_right_point, '\n')
    # # print("The top left point is: ", top_left_point, '\n')
    # # print("The top right point is: ", top_right_point, '\n')

#----------------------------------------------------------------------------------

#Base Case
def base_case_hull(points: List[Point]) -> List[Point]:

    final_list = []
    
    #No work to be done
    if len(points) <= 3:
        clockwise_sort(points)
        return points
    
    else:
        
        num_positive = 0
        num_negative = 0
        num_collinear = 0

        #
        for point1 in points:
            point1_on_hull = False
            for point2 in points:
                point2_on_hull = True
                if point1 == point2:
                    continue
                for i in range(len(points)):
                    if points[i] == point1 or points[i] == point2:
                        continue
                    temp_area = triangle_area(point1, point2, points[i])
                    if temp_area > 0:
                        num_positive+= 1
                    if temp_area < 0:
                        num_negative+= 1
                    if temp_area == 0:
                        num_collinear+= 1
                        continue
                    if num_positive > 0 and num_negative > 0:
                        point2_on_hull = False
                        break
                num_positive = num_negative = 0
                
                if point2_on_hull == True:
                    point1_on_hull = True
                    if point2 not in final_list:
                        final_list.append(point2)
            if point1_on_hull == True and (point1 not in final_list):
                final_list.append(point1)
    
    clockwise_sort(final_list)           
    return final_list


                # if num_positive + num_collinear == len(points):
                #     final_list.append(point1)
                #     final_list.append(point2)
                #     if num_collinear != 0:
                #         for point in points:
                #             if collinear(point1, point2, point):
                #                 final_list.append(point)
                # if num_negative + num_collinear == len(points):
                #     final_list.append(point1)
                #     final_list.append(point2)
                #     if num_collinear != 0:
                #         for point in points:
                #             if collinear(point1, point2, point):
                #                 final_list.append(point)

#----------------------------------------------------------------------------------

#                           *** INVARIANT DOCUMENTATION ***

#       Initialiaation:

#       Maintanence:

#       Completion:

#----------------------------------------------------------------------------------

#
def compute_hull(points: List[Point]) -> List[Point]:

    convex_hull = []

    #Sort input list by x postion
    points = sorted(points)

    if check_for_vertical_line(points) == True:
        temp = points.sort(key=lambda x: x[1])
        return temp

    #Check the length of points
    if len(points) <= 6:
        #Preform naive(base case) method on the six points
        base_points = base_case_hull(points)

        return base_points

    else:

        list1 = []
        list2 = []

        #Split list in the middle
        halfway_point = len(points) / 2
        halfway_point = int(halfway_point)
        for i in range (halfway_point):
            list1.append(points[i])        
        
        # print(list1,'\n')
        
        for i in range(halfway_point, len(points)):
            list2.append(points[i])   

        #Check for unproportional splits
        if not list1:
            clockwise_sort(list2)
            return list2
        if not list2:
            clockwise_sort(list1)
            return list1     
        
        # print(list2,'\n')

        #If two or more middle points have the same x value, do NOT seperate them from each other

        x1,y1 = list1[-1]
        x2,y2 = list2[0]

        while x1 == x2:
            list1.append(list2[0])
            list2.remove(list2[0])
            #Check for unproportional splits
            if not list1:
                clockwise_sort(list2)
                return list2
            if not list2:
                clockwise_sort(list1)
                return list1  
            x1,y1 = list1[-1]
            x2,y2 = list2[0]

        #print(list1)

        #Recursivley call the function on both of the lists (until you get down to six points)
        #Going to have two recursive calls, one for each half
        new_list1 = compute_hull(list1)
        new_list2 = compute_hull(list2)

        #Make sure that neither list is empty
        if not new_list1:
            clockwise_sort(new_list2)
            return new_list2
        if not new_list2:
            clockwise_sort(new_list1)
            return new_list1

        #Sort lists again before merging
        new_list1 = sorted(new_list1)
        new_list2 = sorted(new_list2)

        convex_hull = merge_points(new_list1, new_list2)

        clockwise_sort(convex_hull)
        return convex_hull

#----------------------------------------------------------------------------------

#                           *** INVARIANT DOCUMENTATION ***

#       Initialiaation:

#       Maintanence:

#       Completion:


#----------------------------------------------------------------------------------

def main():

    # p1 = (4,1)
    # p2 = (5,20)
    # p3 = (1,10)
    # p4 = (4,25)
    # p5 = (6,10)
    # p6 = (6, 12)
    # p7 = (10,10)

    # points = [p1,p2,p3,p4,p5,p6,p7]
    # points = [(226, 47), (645, 166), (603, 438), (211, 505), (189, 217), (443, 298), (501, 151), (300, 279), (448, 388)]
    points = []

    for i in range(10000):
        points.append((random.randint(1, 1000), random.randint(1, 1000)))
    now = time.time()
    hullPoints = compute_hull(points)
    rightnow = time.time()

    print(rightnow - now)

    # print(is_convex_hull(hullPoints, points))
if __name__ == '__main__':
    main()