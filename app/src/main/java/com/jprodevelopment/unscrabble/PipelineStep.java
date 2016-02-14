package com.jprodevelopment.unscrabble;

import org.opencv.core.Mat;

public abstract class PipelineStep {

    private final String name;
    protected PipelineStep prev;
    protected PipelineStep next;

    public PipelineStep(String name) {
        this.name = name;
    }

    public void addNextStep(PipelineStep next) {
        if(next != null) {
            this.next = next;
            next.prev = this;
        }
    }

    public String getName() {
        return name;
    };

    public final Mat apply(Mat input) {
        if(preSanityCheck(input)) {
            Mat output = process(input);
            if(postSanityCheck(output)) {
                if(next == null) {
                    return output;
                } else {
                    return next.apply(output);
                }
            }
        }
        return null;
    };

    protected abstract Mat process(Mat input);

    public boolean preSanityCheck(Mat input) { return true; }
    public boolean postSanityCheck(Mat output) { return true; }
}
