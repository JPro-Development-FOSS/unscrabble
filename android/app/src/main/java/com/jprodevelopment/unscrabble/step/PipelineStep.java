package com.jprodevelopment.unscrabble.step;

import android.util.Log;

import com.jprodevelopment.unscrabble.PipelineContext;

import org.opencv.core.Mat;

public abstract class PipelineStep {

    private final String TAG = PipelineStep.class.getName();
    private final String name;
    private final PipelineContext context;
    protected PipelineStep prev;
    protected PipelineStep next;

    public PipelineStep(String name, PipelineContext context) {
        this.name = name;
        this.context = context;
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

    protected PipelineContext getContext() { return context; }

    public final Mat apply(Mat input) {
        if(preSanityCheck(input)) {
            Mat output = process(input);
            if(postSanityCheck(output)) {
                if(next == null) {
                    return output;
                } else {
                    return next.apply(output);
                }
            } else {
                Log.i(TAG, "Failed post sanity check for " + getName());
            }
        } else {
            Log.i(TAG, "Failed pre sanity check for " + getName());
        }
        return null;
    };

    protected abstract Mat process(Mat input);

    public boolean preSanityCheck(Mat input) { return true; }
    public boolean postSanityCheck(Mat output) { return true; }
}
