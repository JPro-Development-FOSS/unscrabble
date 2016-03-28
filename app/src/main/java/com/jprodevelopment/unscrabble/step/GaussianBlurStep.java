package com.jprodevelopment.unscrabble.step;

import com.jprodevelopment.unscrabble.PipelineContext;

import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;

/**
 * Gaussian blur filter applies a normalized kernel to the image, taking neighbors pixel values into
 * account in a normal-weighted way (I think).
 */
public class GaussianBlurStep extends PipelineStep {

    public GaussianBlurStep(PipelineContext context) {
        super("gaussian_blur", context);
    }

    /**
     * Apply the filter.
     * @param grayscale 8U_1C format -- grayscale image
     * @return grayscale 8U_1C format -- gaussian blur image
     */
    @Override
    public Mat process(Mat grayscale) {
        Imgproc.GaussianBlur(grayscale, grayscale, new Size(9, 9), 2.0, 2.0);

        return grayscale;
    }
}
