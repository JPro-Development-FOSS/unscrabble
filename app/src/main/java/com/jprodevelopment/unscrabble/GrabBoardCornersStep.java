package com.jprodevelopment.unscrabble;

import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfInt;
import org.opencv.core.MatOfPoint;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;

import java.util.ArrayList;
import java.util.List;

/**
 * This step gets a convex hull of the board and stores the corner coordinates.
 */
public class GrabBoardCornersStep extends PipelineStep {

    public GrabBoardCornersStep() {
        super("grab_corners");
    }

    /**
     * Apply the filter.
     * @param grayscale 8U_1C format -- grayscale image
     * @return grayscale 8U_1C format -- gaussian blur image
     */
    @Override
    public Mat process(Mat grayscale) {

        Mat img_canny = grayscale;
        Mat hierarchy = new Mat(img_canny.rows(),img_canny.cols(),CvType.CV_8UC1,new Scalar(0));
        List<MatOfPoint> contours =new ArrayList<MatOfPoint>();

        Imgproc.findContours(grayscale, contours, hierarchy,Imgproc.RETR_TREE, Imgproc.CHAIN_APPROX_SIMPLE, new Point(0, 0));


        // Find the convex hull
        List<MatOfInt> hull = new ArrayList<MatOfInt>();
        for(int i=0; i < contours.size(); i++){
            hull.add(new MatOfInt());
        }
        for(int i=0; i < contours.size(); i++){
            Imgproc.convexHull(contours.get(i), hull.get(i));
        }

        // Convert MatOfInt to MatOfPoint for drawing convex hull

        // Loop over all contours
        List<Point[]> hullpoints = new ArrayList<Point[]>();
        for(int i=0; i < hull.size(); i++){
            Point[] points = new Point[hull.get(i).rows()];

            // Loop over all points that need to be hulled in current contour
            for(int j=0; j < hull.get(i).rows(); j++){
                int index = (int)hull.get(i).get(j, 0)[0];
                points[j] = new Point(contours.get(i).get(index, 0)[0], contours.get(i).get(index, 0)[1]);
            }

            hullpoints.add(points);
        }

        // Convert Point arrays into MatOfPoint
        List<MatOfPoint> hullmop = new ArrayList<MatOfPoint>();
        for(int i=0; i < hullpoints.size(); i++){
            MatOfPoint mop = new MatOfPoint();
            mop.fromArray(hullpoints.get(i));
            hullmop.add(mop);
        }


        // Draw contours + hull results
        Mat overlay = new Mat(grayscale.size(), CvType.CV_8UC3);
        Scalar contourColor = new Scalar(0, 255, 0);   // Green
        Scalar hullColor = new Scalar(255, 0, 0);   // Red
        for(int i=0; i < contours.size(); i++){
            Imgproc.drawContours(overlay, contours, i, contourColor, 10);
            Imgproc.drawContours(overlay, hullmop, i, hullColor, 10);
        }

        return overlay;
    }
}
