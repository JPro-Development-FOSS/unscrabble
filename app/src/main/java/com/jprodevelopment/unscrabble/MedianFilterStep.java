package com.jprodevelopment.unscrabble;

import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;

/**
 * Median filter takes the median of the current pixel and its neighbors.
 */
public class MedianFilterStep extends PipelineStep {

    public MedianFilterStep() {
        super("median_filter");
    }

    /**
     * Apply the filter.
     * @param grayscale 8U_1C format -- filtered image
     * @return grayscale 8U_1C format -- median blur image
     */
    @Override
    public Mat process(Mat grayscale) {

        Imgproc.medianBlur(grayscale, grayscale, 3);

        return grayscale;
    }
}
