package com.jprodevelopment.unscrabble;

import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;

import java.util.ArrayList;
import java.util.List;

/**
 * Given the input of where the board's 4 corners are, rectify the board image into a square one.
 */
public class RectifyBoardStep extends PipelineStep {

    public RectifyBoardStep(PipelineContext context) {
        super("rectify_board", context);
    }

    /**
     * Apply the filter.
     * @param unrectifiedBoard 8U_3C format -- image with board in it somewhere
     * @return color 8U_3C format -- rectified board
     */
    @Override
    public Mat process(Mat unrectifiedBoard) {

        MatOfPoint2f corners = getContext().getCorners();
        // Get mass center
        Point center = new Point(0, 0);
        for (int i = 0; i < 4; i++) {
            center.x += corners.get(i, 0)[0];
            center.y += corners.get(i, 0)[1];
        }

        center.x /= 4.0;
        center.y /= 4.0;
        MatOfPoint2f sortedCorners = sortCorners(corners, center);

        // Define the destination image
        Mat rectified = new Mat(1200, 1200, CvType.CV_8UC3);

        // Corners of the destination image
        List<Point> quadPoints = new ArrayList<>();
        quadPoints.add(new Point(0, 0));
        quadPoints.add(new Point(rectified.cols(), 0));
        quadPoints.add(new Point(rectified.cols(), rectified.rows()));
        quadPoints.add(new Point(0, rectified.rows()));
        MatOfPoint2f quadPointMat = new MatOfPoint2f();
        quadPointMat.fromList(quadPoints);

        // Get transformation matrix 4*1*CV_32SC2
        Mat transform = Imgproc.getPerspectiveTransform(sortedCorners, quadPointMat);
        Imgproc.warpPerspective(unrectifiedBoard, rectified, transform, rectified.size());

        return rectified;
    }


    MatOfPoint2f sortCorners(MatOfPoint2f corners, Point center)
    {
        List<Point> top = new ArrayList<>(), bot = new ArrayList<>();

        for (int i = 0; i < 4; i++)
        {
            if (corners.get(i, 0)[1] < center.y)
                top.add(new Point(corners.get(i, 0)[0],corners.get(i, 0)[1]));
            else
                bot.add(new Point(corners.get(i, 0)[0],corners.get(i, 0)[1]));
        }

        Point tl = top.get(0).x > top.get(1).x ? top.get(1) : top.get(0);
        Point tr = top.get(0).x > top.get(1).x ? top.get(0) : top.get(1);
        Point bl = bot.get(0).x > bot.get(1).x ? bot.get(1) : bot.get(0);
        Point br = bot.get(0).x > bot.get(1).x ? bot.get(0) : bot.get(1);

        List<Point> ordered = new ArrayList<>();
        ordered.add(tl);
        ordered.add(tr);
        ordered.add(br);
        ordered.add(bl);

        MatOfPoint2f orderedPoints = new MatOfPoint2f();
        orderedPoints.fromList(ordered);
        return orderedPoints;
    }
}
