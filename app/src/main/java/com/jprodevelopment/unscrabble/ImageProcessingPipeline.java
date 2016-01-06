package com.jprodevelopment.unscrabble;

import org.opencv.core.Mat;

import java.util.List;

public class ImageProcessingPipeline {
    private List<PipelineStep> steps;
    public Mat runPipeline(Mat intermediate) {
        for(PipelineStep step : steps) {
            intermediate = step.apply(intermediate);
        }
        return intermediate;
    }
}
