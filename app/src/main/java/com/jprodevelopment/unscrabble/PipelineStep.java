package com.jprodevelopment.unscrabble;

import org.opencv.core.Mat;

public abstract class PipelineStep {

    private String name;

    public PipelineStep(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    };

    public abstract Mat apply(Mat input);
}
