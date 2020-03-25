# For each cylinder in the scan, find its ray and depth.
# 03_c_find_cylinders
# Claus Brenner, 09 NOV 2012
from pylab import *
from lego_robot import *

# Find the derivative in scan data, ignoring invalid measurements.
def compute_derivative(scan, min_dist):
    jumps = [ 0 ]
    for i in range(1, len(scan) - 1):
        if scan[i-1] > min_dist and scan[i+1] > min_dist:
            der = (scan[i+1]-scan[i-1])/2
            jumps.append(der)
        else:
            jumps.append(0)
        # --->>> Insert your code here.
        # Compute derivative using formula "(f(i+1) - f(i-1)) / 2".
        # Do not use erroneous scan values, which are below min_dist.
         # Replace this line, append derivative instead.

    jumps.append(0)
    return jumps
# For each area between a left falling edge and a right rising edge,
# determine the average ray number and the average depth.
def find_cylinders(scan, scan_derivative, jump, min_dist):
    print(scan_derivative)
    cylinder_list = []
    on_cylinder = False
    sum_ray, sum_depth, rays = 0.0, 0.0, 0
    print(scan_derivative)
    count = 0
    for i in xrange(len(scan_derivative)-1):
        # --->>> Insert your cylinder code here.
        # Whenever you find a cylinder, add a tuple
        # (average_ray, average_depth) to the cylinder_list.
        if on_cylinder == False and scan_derivative[i] <= -100:
            on_cylinder = True
            print "negative edge detected at i = ", i
            print "scan_derevative[i] =", scan_derivative[i]
        elif on_cylinder == True:
            # print "rays = ", rays
            # print "sum_rays = ", sum_ray
            if scan_derivative[i] <= -100:
                print "second negative edge detected at i = ",i
                print "scan_derevative[i] =", scan_derivative[i]
                rays = 0
                sum_ray = 0
                sum_depth = 0 
            rays = rays + 1
            sum_ray = sum_ray + i
            sum_depth = sum_depth + scan[i]
            if scan_derivative[i] >= 100:
                print "positive edge detected at i = ", i
                print "scan_derevative[i] =", scan_derivative[i]
                average_ray = (sum_ray)/rays
                on_cylinder = False
                print "cylinder is at i = ", average_ray
                cylinder_list.append((average_ray, scan[average_ray]))
                count = count + 1
                print "No. of cylinders detected = ",count
                rays = 0
                sum_ray = 0
                sum_depth = 0 
        # Just for fun, I'll output some cylinders.
        # Replace this by your code.
        # if i % 100 == 0:
        #     cylinder_list.append( (i, scan[i]) )

    return cylinder_list


if __name__ == '__main__':

    minimum_valid_distance = 20.0
    depth_jump = 100.0

    # Read the logfile which contains all scans.
    logfile = LegoLogfile()
    logfile.read("robot4_scan.txt")

    # Pick one scan.
    scan = logfile.scan_data[8]

    # Find cylinders.
    der = compute_derivative(scan, minimum_valid_distance)
    cylinders = find_cylinders(scan, der, depth_jump,
                               minimum_valid_distance)

    # Plot results.
    plot(scan)
    plot(der)
    plot(depth_jump)
    scatter([c[0] for c in cylinders], [c[1] for c in cylinders],
        c='r', s=200)
    show()
