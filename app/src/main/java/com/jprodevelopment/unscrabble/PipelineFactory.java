package com.jprodevelopment.unscrabble;

import com.jprodevelopment.unscrabble.step.GaussianBlurStep;
import com.jprodevelopment.unscrabble.step.GrabBoardCornersStep;
import com.jprodevelopment.unscrabble.step.MedianFilterStep;
import com.jprodevelopment.unscrabble.step.PipelineStep;
import com.jprodevelopment.unscrabble.step.PrintDebugImageStep;
import com.jprodevelopment.unscrabble.step.RectifyBoardStep;
import com.jprodevelopment.unscrabble.step.TileFilterStep;
import com.jprodevelopment.unscrabble.step.TripleWordScoreFilterStep;

/**
 * Describes the scrabble board image processing pipeline.
 */
public class PipelineFactory {
    private final ImageProcessingPipeline pipeline;
    private final PipelineContext context;
    public PipelineFactory() {
        this(false, "");
    }
    public PipelineFactory(boolean captureDebugOutputImages, String outputStorageDir) {
        pipeline = new ImageProcessingPipeline();
        context = new PipelineContext();

        PipelineStep tripWordStep = new TripleWordScoreFilterStep(context);
        addStep(captureDebugOutputImages, outputStorageDir, tripWordStep);

        PipelineStep medianStep = new MedianFilterStep(context);
        addStep(captureDebugOutputImages, outputStorageDir, medianStep);

        PipelineStep gaussianStep = new GaussianBlurStep(context);
        addStep(captureDebugOutputImages, outputStorageDir, gaussianStep);

        PipelineStep grabBoardCornersStep = new GrabBoardCornersStep(context);
        addStep(captureDebugOutputImages, outputStorageDir, grabBoardCornersStep);

        PipelineStep rectifyBoardStep = new RectifyBoardStep(context);
        addStep(captureDebugOutputImages, outputStorageDir, rectifyBoardStep);

        PipelineStep tileFilterStep = new TileFilterStep(context);
        addStep(captureDebugOutputImages, outputStorageDir, tileFilterStep);
    }

    private void addStep(boolean captureDebugOutputImages, String outputStorageDir, PipelineStep tripWordStp) {
        pipeline.addStep(tripWordStp);
        if(captureDebugOutputImages) {
            pipeline.addStep(new PrintDebugImageStep(
                    tripWordStp.getName(),
                    outputStorageDir,
                    Long.toString(System.currentTimeMillis()),
                    context));
        }
    }

    public ImageProcessingPipeline getPipeline() { return pipeline; }
}
