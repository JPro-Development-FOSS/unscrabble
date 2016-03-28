package com.jprodevelopment.unscrabble.step;

import com.jprodevelopment.unscrabble.PipelineContext;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.Range;
import org.opencv.core.Scalar;
import org.opencv.imgproc.Imgproc;

/**
 * Filters the image by converting RGB to HSV and filtering for the yellow triple word scores. The
 * returned image is in 8U_1C grayscale mode.
 */
public class TileFilterStep extends PipelineStep {

    public TileFilterStep(PipelineContext context) {
        super("tile_filter", context);
    }

    /**
     * Apply the filter.
     * @param unused 8U_4C format
     * @return b/w 8U_1C format -- filtered image
     */
    @Override
    public Mat process(Mat unused) {
        Mat input = getContext().getRectifiedBoard();

        // convert to hsv since we can better detect alike chrominance vs in rgb space
        Imgproc.cvtColor(input, input, Imgproc.COLOR_RGB2HSV_FULL);
        // 0 <= h <= 360, 0 <= s <= 1, 0 <= v <= 1
        // for 8U HSV, H / 2, S * 255, V * 255
        Scalar lower = new Scalar(14, 92, 150);
        Scalar upper = new Scalar(44, 173, 208);
        // inrange outputs 8U1C set to white where it passes and black where it fails.
        Core.inRange(input, lower, upper, input);

        return input;
    }
}
