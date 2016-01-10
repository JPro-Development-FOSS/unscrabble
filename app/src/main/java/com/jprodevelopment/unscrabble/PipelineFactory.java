package com.jprodevelopment.unscrabble;

/**
 * Describes the scrabble board image processing pipeline.
 */
public class PipelineFactory {
    private final ImageProcessingPipeline pipeline;
    public PipelineFactory() {
        this(false, "");
    }
    public PipelineFactory(boolean captureDebugOutputImages, String outputStorageDir) {
        pipeline = new ImageProcessingPipeline();
        PipelineStep tripWordStp = new TripleWordScoreFilterStep();
        pipeline.addStep(tripWordStp);
        if(captureDebugOutputImages) {
            pipeline.addStep(new PrintDebugImageStep(
                    tripWordStp.getName(),
                    outputStorageDir,
                    Long.toString(System.currentTimeMillis())));
        }
    }
    public ImageProcessingPipeline getPipeline() { return pipeline; }
}
