package com.jprodevelopment.unscrabble.step;

import com.jprodevelopment.unscrabble.PipelineContext;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Range;
import org.opencv.core.Scalar;
import org.opencv.imgproc.Imgproc;

/**
 * Filters the image by converting RGB to HSV and filtering for the yellow triple word scores. The
 * returned image is in 8U_1C grayscale mode.
 */
public class TripleWordScoreFilterStep extends PipelineStep {

    // private final Mat mIntermediateMat;

    public TripleWordScoreFilterStep(PipelineContext context) {
        super("triple_word_score_filter", context);
        //mIntermediateMat = new Mat();
    }

    /**
     * Apply the filter.
     * @param rgba 8U_4C format
     * @return grayscale 8U_1C format -- filtered image
     */
    @Override
    public Mat process(Mat rgba) {
        getContext().setOriginalBoard(rgba);
        Mat hsvThenGrayscale = new Mat(rgba, Range.all());
        // convert to hsv since we can better detect alike chrominance vs in rgb space
        Imgproc.cvtColor(rgba, hsvThenGrayscale, Imgproc.COLOR_RGB2HSV_FULL);
        // 0 <= h <= 360, 0 <= s <= 1, 0 <= v <= 1

        // for 8U HSV, H / 2, S * 255, V * 255
        Scalar lower = new Scalar(19, 199, 174);
        Scalar upper = new Scalar(36, 255, 230);
        // inrange outputs 8U1C set to white where it passes and black where it fails.
        Core.inRange(hsvThenGrayscale, lower, upper, hsvThenGrayscale);

        return hsvThenGrayscale;
    }
}
