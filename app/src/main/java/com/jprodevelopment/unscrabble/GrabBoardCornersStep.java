package com.jprodevelopment.unscrabble;

import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfInt;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
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

    public GrabBoardCornersStep(PipelineContext context) {
        super("grab_corners", context);
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

        // Find the convex hull of all of the points (rough board outline)
        MatOfInt hull = new MatOfInt();
        List<Point> allPoints = new ArrayList<Point>();
        for(int i=0; i < contours.size(); i++){
            allPoints.addAll(contours.get(i).toList());
        }

        MatOfPoint allPointsMat = new MatOfPoint();
        allPointsMat.fromList(allPoints);
        Imgproc.convexHull(allPointsMat, hull);

        Point[] points = new Point[hull.rows()];
        for(int j=0; j < hull.rows(); j++){
            int index = (int)hull.get(j, 0)[0];
            points[j] = new Point(allPointsMat.get(index, 0)[0], allPointsMat.get(index, 0)[1]);
        }
        MatOfPoint2f mop = new MatOfPoint2f();
        mop.fromArray(points);
        MatOfPoint2f approx = new MatOfPoint2f();

        // approximate proportionally to the length of the convex hull
        Imgproc.approxPolyDP(mop, approx, Imgproc.arcLength(mop, true) * 0.05, true);
        getContext().setCorners(approx);
        MatOfPoint approxMop = new MatOfPoint();
        approxMop.fromList(approx.toList());

        // TODO(j): only take points that look like they're on a corner that is close to a right
        // angle we want to walk away with only 4 corners

        List<MatOfPoint> toDraw = new ArrayList<>();
        toDraw.add(approxMop);

        // Draw contours + hull results
        Mat overlay = new Mat(grayscale.size(), CvType.CV_8UC3);
        Scalar contourColor = new Scalar(0, 255, 0);   // Green
        Scalar hullColor = new Scalar(255, 0, 0);   // Red
        for(int i=0; i < contours.size(); i++){
            Imgproc.drawContours(overlay, contours, i, contourColor, 10);
        }
        Imgproc.drawContours(overlay, toDraw, 0, hullColor, 10);

        return overlay;
    }

    @Override
    public boolean postSanityCheck(Mat input) {
        return getContext().getCorners().rows() == 4;
    }
}
