#!/usr/bin/env python

import math
import rospy
from nav_msgs.srv import GetPlan, GetMap
from nav_msgs.msg import GridCells, OccupancyGrid, Path
from geometry_msgs.msg import Point, Pose, PoseStamped



class PathPlanner:


    
    def __init__(self):
        """
        Class constructor
        """
        ### REQUIRED CREDIT
        ## Initialize the node and call it "path_planner"
        rospy.init_node("path_planner")
        ## Create a new service called "plan_path" that accepts messages of
        ## type GetPlan and calls self.plan_path() when a message is received
        self.planning_service = rospy.Service("plan_path", GetPlan, self.plan_path)
        ## Create a publisher for the C-space (the enlarged occupancy grid)
        ## The topic is "/path_planner/cspace", the message type is GridCells
        self.cspace_publisher = rospy.Publisher("path_planner/cspace", GridCells, queue_size=10)
        ## Create publishers for A* (expanded cells, frontier, ...)
        ## Choose a the topic names, the message type is GridCells
        self.expanded_publisher = rospy.Publisher("path_planner/expanded_cells", GridCells, queue_size=10)
        self.frontier_publisher = rospy.Publisher("path_planner/frontier_cells", GridCells, queue_size=10)
        ## Initialize the request counter
        # TODO

        ## Sleep to allow roscore to do some housekeeping
        rospy.sleep(1.0)
        rospy.loginfo("Path planner node ready")

        map = PathPlanner.request_map()

        print("4 (2,2)")
        PathPlanner.neighbors_of_4(map, 2, 2)
        print("4 (0,0)")
        PathPlanner.neighbors_of_4(map, 0, 0)
        print("8 (2,2)")
        PathPlanner.neighbors_of_8(map, 2, 2)
        print("8 (0,0)")
        PathPlanner.neighbors_of_8(map, 0, 0)
        print("8 (36,36)")
        PathPlanner.neighbors_of_8(map, 36, 36)



    @staticmethod
    def grid_to_index(mapdata, x, y):
        """
        Returns the index corresponding to the given (x,y) coordinates in the occupancy grid.
        :param x [int] The cell X coordinate.
        :param y [int] The cell Y coordinate.
        :return  [int] The index.
        """
        ### REQUIRED CREDIT
        pass



    @staticmethod
    def euclidean_distance(x1, y1, x2, y2):
        """
        Calculates the Euclidean distance between two points.
        :param x1 [int or float] X coordinate of first point.
        :param y1 [int or float] Y coordinate of first point.
        :param x2 [int or float] X coordinate of second point.
        :param y2 [int or float] Y coordinate of second point.
        :return   [float]        The distance.
        """
        ### REQUIRED CREDIT
        pass
        


    @staticmethod
    def grid_to_world(mapdata, x, y):
        """
        Transforms a cell coordinate in the occupancy grid into a world coordinate.
        :param mapdata [OccupancyGrid] The map information.
        :param x       [int]           The cell X coordinate.
        :param y       [int]           The cell Y coordinate.
        :return        [Point]         The position in the world.
        """
        ### REQUIRED CREDIT
        pass


        
    @staticmethod
    def world_to_grid(mapdata, wp):
        """
        Transforms a world coordinate into a cell coordinate in the occupancy grid.
        :param mapdata [OccupancyGrid] The map information.
        :param wp      [Point]         The world coordinate.
        :return        [(int,int)]     The cell position as a tuple.
        """
        ### REQUIRED CREDIT
        pass


        
    @staticmethod
    def path_to_poses(mapdata, path):
        """
        Converts the given path into a list of PoseStamped.
        :param mapdata [OccupancyGrid] The map information.
        :param  path   [[(int,int)]]   The path as a list of tuples (cell coordinates).
        :return        [[PoseStamped]] The path as a list of PoseStamped (world coordinates).
        """
        ### REQUIRED CREDIT
        pass

    

    @staticmethod
    def is_cell_walkable(mapdata, x, y):
        """
        A cell is walkable if all of these conditions are true:
        1. It is within the boundaries of the grid;
        2. It is free (not unknown, not occupied by an obstacle)
        :param mapdata [OccupancyGrid] The map information.
        :param x       [int]           The X coordinate in the grid.
        :param y       [int]           The Y coordinate in the grid.
        :return        [boolean]       True if the cell is walkable, False otherwise
        """
        ### REQUIRED CREDIT
        if x < 0 or x >= mapdata.info.width:
            rospy.logerror("Examined value at out of bounds width")
            return False
        if y < 0 or y >= mapdata.info.height:
            rospy.logerror("Examined value at out of bounds width")
            return False

        return mapdata.data[y * mapdata.info.width + x] == 0

    @staticmethod
    def getValue(mapdata, x, y):
        if x < 0 or x >= mapdata.info.width:
            rospy.logerror("Examined value at out of bounds width")
            return -1
        if y < 0 or y >= mapdata.info.height:
            rospy.logerror("Examined value at out of bounds width")
            return -1

        return mapdata.data[y*mapdata.info.width + x]

    @staticmethod
    def neighbors_of_4(mapdata, x, y):
        """
        Returns the walkable 4-neighbors cells of (x,y) in the occupancy grid.
        :param mapdata [OccupancyGrid] The map information.
        :param x       [int]           The X coordinate in the grid.
        :param y       [int]           The Y coordinate in the grid.
        :return        [[(int,int)]]   A list of walkable 4-neighbors.
        """
        ### REQUIRED CREDIT
        out = []
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                x_coord = x + x_offset
                y_coord = y + y_offset
                if (0 <= x_coord < mapdata.info.width) and (0 <= y_coord < mapdata.info.height) and (abs(x_offset) != abs(y_offset)):

                    if PathPlanner.is_cell_walkable(mapdata, x_coord, y_coord):
                        out.append((x_coord, y_coord))

        return out
    
    
    @staticmethod
    def neighbors_of_8(mapdata, x, y):
        """
        Returns the walkable 8-neighbors cells of (x,y) in the occupancy grid.
        :param mapdata [OccupancyGrid] The map information.
        :param x       [int]           The X coordinate in the grid.
        :param y       [int]           The Y coordinate in the grid.
        :return        [[(int,int)]]   A list of walkable 8-neighbors.
        """
        ### REQUIRED CREDIT
        out = []
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                x_coord = x + x_offset
                y_coord = y + y_offset
                if (0 <= x_coord < mapdata.info.width) and (
                        0 <= y_coord < mapdata.info.height) and not (x_offset == 0 and y_offset == 0):
                    if PathPlanner.is_cell_walkable(mapdata, x_coord, y_coord):
                        out.append((x_coord, y_coord))
        return out

    
    
    @staticmethod
    def request_map():
        """
        Requests the map from the map server.
        :return [OccupancyGrid] The grid if the service call was successful,
                                None in case of error.
        """
        ### REQUIRED CREDIT
        rospy.loginfo("Requesting the map")

        rospy.wait_for_service('static_map')
        try:
            get_map_proxy = rospy.ServiceProxy('static_map', GetMap)
            get_map = get_map_proxy()
            return get_map.map
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
            return None




    def calc_cspace(self, mapdata, padding):
        """
        Calculates the C-Space, i.e., makes the obstacles in the map thicker.
        Publishes the list of cells that were added to the original map.
        :param mapdata [OccupancyGrid] The map data.
        :param padding [int]           The number of cells around the obstacles.
        :return        [OccupancyGrid] The C-Space.
        """
        ### REQUIRED CREDIT
        rospy.loginfo("Calculating C-Space")
        ## Go through each cell in the occupancy grid
        ## Inflate the obstacles where necessary
        # TODO
        ## Create a GridCells message and publish it
        # TODO
        ## Return the C-space
        pass


    
    def a_star(self, mapdata, start, goal):
        """
        Using A* algorithm to calculate an path.
        :param mapdata  [OccupancyGrid] The map data.
        :param start    [(int, int)]    The initial point (a grid coordinate).
        :param goal     [(int, int)]    The goal point (a grid coordinate).
        :return         [[(int, int)]]  The path as a list of tuples (grid coordinates)
        """
        ### REQUIRED CREDIT
        rospy.loginfo("Executing A* from (%d,%d) to (%d,%d)" % (start[0], start[1], goal[0], goal[1]))


    
    @staticmethod
    def optimize_path(path):
        """
        Optimizes the path, removing unnecessary intermediate nodes.
        :param path [[(x,y)]] The path as a list of tuples (grid coordinates)
        :return     [[(x,y)]] The optimized path as a list of tuples (grid coordinates)
        """
        ### EXTRA CREDIT
        rospy.loginfo("Optimizing path")

        

    def path_to_message(self, mapdata, path):
        """
        Takes a path on the grid and returns a Path message.
        :param path [[(int,int)]] The path on the grid (a list of tuples)
        :return     [Path]        A Path message (the coordinates are expressed in the world)
        """
        ### REQUIRED CREDIT
        rospy.loginfo("Returning a Path message")


        
    def plan_path(self, msg):
        """
        Plans a path between the start and goal locations in the requested.
        Internally uses A* to plan the optimal path.
        :param req 
        """
        ## Request the map
        ## In case of error, return an empty path
        mapdata = PathPlanner.request_map()
        if mapdata is None:
            return Path()
        ## Calculate the C-space and publish it
        cspacedata = self.calc_cspace(mapdata, 1)
        ## Execute A*
        start = PathPlanner.world_to_grid(mapdata, msg.start.pose.position)
        goal  = PathPlanner.world_to_grid(mapdata, msg.goal.pose.position)
        path  = self.a_star(cspacedata, start, goal)
        ## Optimize waypoints
        waypoints = PathPlanner.optimize_path(path)
        ## Return a Path message
        return self.path_to_message(mapdata, waypoints)


    
    def run(self):
        """
        Runs the node until Ctrl-C is pressed.
        """
        rospy.spin()


        
if __name__ == '__main__':
    PathPlanner().run()
