#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main()
{
	Mat board = imread("res/test_board_2.jpg");

	// Check if image was successfully read
	if(board.empty())
	{
		cerr << "Could not read image" << endl;
		return 1;
	}

	namedWindow("Grayscale", WINDOW_NORMAL);
	imshow("Grayscale", board);
	waitKey(0);

	// TripleWordScoreFilterStep
	Mat boardHsv, grayscale;
	cvtColor(board, boardHsv, COLOR_BGR2HSV_FULL);

	// 0 <= h <= 360, 0 <= s <= 1, 0 <= v <= 1
	// for 8U HSV, H / 2, S // 255, V // 255
	Scalar lower(19, 199, 174), upper(36, 255, 230);
	inRange(boardHsv, lower, upper, grayscale);
	imshow("Grayscale", grayscale);
	waitKey(0);

 	// MedianFilterStep
	medianBlur(grayscale, grayscale, 3);
	imshow("Grayscale", grayscale);
	waitKey(0);

	// GaussianBlurStep
	GaussianBlur(grayscale, grayscale, Size(9, 9), 2.0, 2.0);
	imshow("Grayscale", grayscale);
	waitKey(0);

 	// GrabBoardCornersStep
	vector<vector<Point>> contours;
	findContours(grayscale, contours, RETR_TREE, CHAIN_APPROX_SIMPLE);
	vector<Point> flattened;
	for(const auto& contour : contours) {
		flattened.insert(flattened.end(), contour.begin(), contour.end());
	}
	vector<Point> hull;
	convexHull(flattened, hull);
	vector<Point> boardRect;
	// Approximate proprtionally to the length of the convex hull.
	approxPolyDP(hull, boardRect, arcLength(hull, true) * 0.05, true);
	Mat overlay(grayscale.size(), CV_8UC3);
	Scalar contourColor(0, 255, 0), hullColor(255, 0, 0);
	for(uint i = 0; i < contours.size(); i++) {
		drawContours(overlay, contours, i, contourColor, 10);
	}
	vector<vector<Point>> boardRect2;
	boardRect2.push_back(boardRect);
	drawContours(overlay, boardRect2, 0, hullColor, 10);
	imshow("Grayscale", overlay);
	waitKey(0);

 	// RectifyBoardStep
	Point center;
	for (int i = 0; i < 4; i++) {
		center.x += boardRect[i].x / 4.0;
		center.y += boardRect[i].y / 4.0;
	}
	// Sort the corners.
	vector<Point2f> sortedCorners(4);
	for (const auto& corner : boardRect) {
		if (corner.x <= center.x && corner.y <= center.y) {
			sortedCorners[0] = corner;
		}
		if (corner.x > center.x && corner.y <= center.y) {
		       sortedCorners[1] = corner;
		}
 		if (corner.x > center.x && corner.y > center.y) {
			sortedCorners[2] = corner;
		}
		if (corner.x <= center.x && corner.y > center.y) {
			sortedCorners[3] = corner;
		}		
	}
	vector<Point2f> rectifiedCorners{Point2f(0, 0), Point2f(1200, 0), Point2f(1200, 1200), Point2f(0, 1200)};
	Mat transform = getPerspectiveTransform(sortedCorners, rectifiedCorners);
	warpPerspective(boardHsv, boardHsv, transform, boardHsv.size());
	imshow("Grayscale", boardHsv);
	waitKey(0);

 	// TileFitlerStep
	inRange(boardHsv, Scalar(14, 92, 150), Scalar(44, 173, 208), boardHsv);
	imshow("Grayscale", boardHsv);
	waitKey(0);
	Mat& grayTiles = boardHsv;

	// Separate Tiles
	int squareSize = 1200 / 15;
	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			Mat tile = grayTiles(Rect2i(squareSize * i, squareSize * j, squareSize, squareSize));
			imshow("Grayscale", tile);
			waitKey(0);
		}
	}
	
	return 0;
}
