package com.jprodevelopment.unscrabble;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.Scalar;
import org.opencv.imgproc.Imgproc;

/**
 * Filters the image by converting RGB to HSV and filtering for the yellow triple word scores. The
 * returned image is in 8U_1C grayscale mode.
 */
public class TripleWordScoreFilterStep extends PipelineStep {

    // private final Mat mIntermediateMat;

    public TripleWordScoreFilterStep() {
        super("triple_word_score_filter");
        //mIntermediateMat = new Mat();
    }

    /**
     * Apply the filter.
     * @param rgba 8U_4C format
     * @return grayscale 8U_1C format -- filtered image
     */
    @Override
    public Mat process(Mat rgba) {

        Mat grayscale = rgba;
        // convert to hsv since we can better detect alike chrominance vs in rgb space
        Imgproc.cvtColor(rgba, grayscale, Imgproc.COLOR_RGB2HSV_FULL);
        // 0 <= h <= 360, 0 <= s <= 1, 0 <= v <= 1
        // 26*,95%,74% to 26*,80%,85%
        // for 8U HSV, H / 2, S * 255, V * 255
        Scalar lower = new Scalar(12, 199, 174);
        Scalar upper = new Scalar(20, 255, 230);
        // inrange outputs 8U1C set to white where it passes and black where it fails.
        Core.inRange(grayscale, lower, upper, grayscale);

        return grayscale;

        // uncomment these if we need to get back to rgba in the future
        //Imgproc.cvtColor(mIntermediateMat, mIntermediateMat, Imgproc.COLOR_GRAY2RGBA);
        //mIntermediateMat.copyTo(rgba);
        //return rgba;
    }
}
