# A_star-search-algorithm

The objective is to find the “best” path (shortest distance or fewest nodes) from a selected starting node to the goal node “O”. Each node has a name, an x and y position on a 2-dimensional space, and a colored (red or blue) directional arrow (N, S, E, W, NE, NW, SE, SW). From any node the program travels in the direction of the arrow associated with that node and only stops at a node that is associated with an arrow that has a different color.

The user input at runtime consists of the following:
*	The start node 
*	“step-by-step” option or not.
*	The heuristic to use 
  ⋅⋅⋅- Fewest nodes, or 
  ⋅⋅⋅- Straight-line distance
