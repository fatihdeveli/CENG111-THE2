def minority_shape_intersect(shape1, shape2):
    """
    Author: Fatih Develi
    Calculates and returns the edge coordinates of the shape which created by the intersection of two given shapes.
    :param shape1: List of edge coordinates
    :param shape2: List of edge coordinates
    :return: List of intersection shape coordinates

    """
    max_int = 9223372036854775807
    min_int = -9223372036854775807

    def segment(shape):
        """
        Takes the vertex coordinates of a shape and returns the line segments.
        :param shape: A list of coordinates of the given shape's vertices.
        :return: The list of coordinate couples of line segments that forms the shape.
        """
        segments = []
        for i, coordinate in enumerate(shape):
            try:
                segments.append((shape[i], shape[i+1]))
            except IndexError:
                segments.append((shape[i], shape[0]))
        return segments

    def intersection(seg1, seg2):
        """
        Calculates the intersection coordinates of given two line segments. Returns [] if they do not intersect.
        :param seg1: Line segment coordinates
        :param seg2: Line segment coordinates
        :return: Intersection point coordinates
        """
        # seg1 = (x1, y1), (x2, y2)
        # seg2 = (x3, y3), (x4, y4)
        x1 = seg1[0][0]  # Ax
        x2 = seg1[1][0]  # Bx
        x3 = seg2[0][0]  # Cx
        x4 = seg2[1][0]  # Dx
        y1 = seg1[0][1]  # Ay
        y2 = seg1[1][1]  # By
        y3 = seg2[0][1]  # Cy
        y4 = seg2[1][1]  # Dy

        if float(((y4-y3)*(x2-x1)-(y2-y1)*(x4-x3)) == 0):
            return []
        else:
            t = ((y4-y3)*(x3-x1) - (y3-y1)*(x4-x3)) / float(((y4-y3)*(x2-x1) - (y2-y1)*(x4-x3)))

        intersection_x = x1 + (x2-x1)*t
        intersection_y = y1 + (y2-y1)*t

        # Following commented out piece of code is implemented using approx_less_eq() function instead of <= operator
        # to avoid float comparison errors.
        '''
        if not (min(x1, x2) <= intersection_x <= max(x1, x2) and min(x3, x4) <= intersection_x <= max(x3, x4) and
                min(y1, y2) <= intersection_y <= max(y1, y2) and min(y3, y4) <= intersection_y <= max(y3, y4)):
            return [] 
        '''
        # Return empty list if found coordinates do not belong to line segments.
        if not (approx_less_eq(min(x1, x2), intersection_x) and approx_less_eq(intersection_x, max(x1, x2))
                and approx_less_eq(min(x3, x4), intersection_x) and approx_less_eq(intersection_x, max(x3, x4))
                and approx_less_eq(min(y1, y2), intersection_y) and approx_less_eq(intersection_y, max(y1, y2))
                and approx_less_eq(min(y3, y4), intersection_y) and approx_less_eq(intersection_y, max(y3, y4))):
            return []

        return [intersection_x, intersection_y]

    def is_inside(pnt, shape):
        """
        Determine if the point is inside the shape using Jordan Curve Theorem.
        If a ray going out of a point intersect the shape odd number of times, then the point is inside that shape.
        Two rays going towards opposite sides are used to avoid the case where a ray from an outside point intersects
        the shape at one point. If both rays intersect the shape an odd number of times, then the point is inside.
        :param pnt: Coordinates of the point
        :param shape: Vertex coordinates of the shape
        :return: True if inside, False if not.
        """
        ray1 = (pnt, (pnt[0], max_int))  # The ray from the point to +y
        ray2 = (pnt, (pnt[0], min_int))  # The ray from the point to -y
        # If the ray intersects a vertex, intersection is counted for both line segments of that intersection.
        # To prevent this, checked points are saved to a list to not check them again.
        checked_points = []
        counter1 = 0
        counter2 = 0

        # Check how many times the first ray intersects the shape
        for seg in segment(shape):
            intersection_point = intersection(ray1, seg)
            # Check if intersection returns a valid value and not checked before
            if intersection_point and intersection_point not in checked_points:
                checked_points.append(intersection_point)
                counter1 = counter1 + 1

        # Check how many times the second ray intersects the shape
        for seg in segment(shape):
            intersection_point = intersection(ray2, seg)
            # Check if intersection returns a valid value and not checked before
            if intersection_point and intersection_point not in checked_points:
                checked_points.append(intersection_point)
                counter2 = counter2 + 1

        if counter1 % 2 == 1 and counter2 % 2 == 1:
            return True
        else:
            return False

    def approx_less_eq(number1, number2):
        """
        Checks if number1 is approximately less than or equal to number2. Used to deal with float comparison errors.
        :return: True if number1 <= number2 (within the error range)
        """
        if number1 < number2 or abs(number1-number2) < 0.0001:
            return True
        else:
            return False

    def not_in(numbers, lst):
        """
        Checks if the given number set is not approximately equal to any number set in the list lst. Used do deal with
        float comparison errors.
        :return: True if the number set is not approximately equal to any number set in lst.
        """
        def approx_equal(number1, number2):
            return abs(number1-number2) < 0.0001
        for num in lst:
            if approx_equal(numbers[0], num[0]) and approx_equal(numbers[1], num[1]):
                return False
        return True

    # Set of the answer points
    answer = []

    # Find the line segments of given shapes
    segments1 = segment(shape1)
    segments2 = segment(shape2)

    # Check if a point is inside the other shape
    for point in shape1:
        if point not in answer and is_inside(point, shape2):
            answer.append(tuple(point))

    for point in shape2:
        if point not in answer and is_inside(point, shape1):
            answer.append(tuple(point))

    # Check intersecting points for every possible line segment couple
    for segment1 in segments1:
        for segment2 in segments2:
            intersection_p = intersection(segment1, segment2)
            # Check if the point is not already in the answer set and the intersection point is not null.
            if intersection_p and not_in(tuple(intersection_p), answer):
                answer.append(tuple(intersection_p))

    return answer


def main():
    print(minority_shape_intersect([(4., 8.), (20.6, 10.), (9.4, 18.1)],
                                   [(12.5, 7.), (18.7, 16.2), (2., 12.), (12.5, 11.3)]))
    # from draw_shapes import draw_shapes
    # print(draw_shapes([s1, s2]))


if __name__ == "__main__":
    main()
