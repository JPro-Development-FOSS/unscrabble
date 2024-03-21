package com.jprodevelopment.unscrabble;

import com.jprodevelopment.unscrabble.step.PipelineStep;

import org.opencv.core.Mat;

public class ImageProcessingPipeline {

    private PipelineStep firstStep;
    private PipelineStep lastStep;

    public Mat runPipeline(Mat input) {
        if(input == null || firstStep == null)
            return new Mat();
        return firstStep.apply(input);
    }
    public void addStep(PipelineStep step) {
        if(firstStep == null) {
            firstStep = lastStep = step;
            return;
        }
        lastStep.addNextStep(step);
        lastStep = step;
    }
}
