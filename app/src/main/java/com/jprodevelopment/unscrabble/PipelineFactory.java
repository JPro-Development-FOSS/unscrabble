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

        PipelineStep tripWordStep = new TripleWordScoreFilterStep();
        addStep(captureDebugOutputImages, outputStorageDir, tripWordStep);

        PipelineStep medianStep = new MedianFilterStep();
        addStep(captureDebugOutputImages, outputStorageDir, medianStep);

        PipelineStep gaussianStep = new GaussianBlurStep();
        addStep(captureDebugOutputImages, outputStorageDir, gaussianStep);

        PipelineStep grabBoardCornersStep = new GrabBoardCornersStep();
        addStep(captureDebugOutputImages, outputStorageDir, grabBoardCornersStep);
    }

    private void addStep(boolean captureDebugOutputImages, String outputStorageDir, PipelineStep tripWordStp) {
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
