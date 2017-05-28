#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <dirent.h>
#include <errno.h>
#include <iostream>
#include <string>
#include <map>

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
	Mat rectified(1200, 1200, CV_8UC3);
	warpPerspective(boardHsv, rectified, transform, rectified.size());
	warpPerspective(board, board, transform, rectified.size());
	imshow("Grayscale", rectified);
	imshow("Grayscale", board);
	waitKey(0);

 	// TileFitlerStep
	Mat grayTiles(1200, 1200, CV_8UC1);
	inRange(rectified, Scalar(14, 92, 150), Scalar(44, 173, 208), grayTiles); // output is 8U1C
	imshow("Grayscale", grayTiles);
	waitKey(0);

	// load all letters and make them small and gray.
	map<string, Mat> tiles;
	int squareSize = 1200 / 15;
	DIR *dp;
	struct dirent *dirp;
	if ((dp = opendir("res/tiles/")) == NULL) {
		cout << "Error(" << errno << ") opening res/tiles/" << endl;
		return errno;
	}
	while ((dirp = readdir(dp)) != NULL) {
		string fname = string(dirp->d_name);
		size_t found = fname.find(".png");
		if (found == string::npos) {
			cout << "skipping " << fname << endl;
			continue;
		}
		cout << "importing " << fname << endl;
		Mat rawTile, grayTile, tile;
		rawTile = imread("res/tiles/" + fname);
		cvtColor(rawTile, grayTile, COLOR_BGR2GRAY);
		resize(grayTile, tile, Size(squareSize, squareSize));
		tiles[fname] = tile;
	}
	closedir(dp);

	// try matching each template. record the max match for each tile.
	pair<string, float> matches[15][15];
	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			matches[i][j] = make_pair("dummy", 0);
		}
	}
	Mat matched;
	for (auto it=tiles.begin(); it != tiles.end(); ++it) {
		cout << "matching " << it->first << endl;
		matchTemplate(grayTiles, it->second, matched, TM_CCORR_NORMED);
		// imshow("Grayscale", matched);
		// waitKey(0);

		for (int i = 0; i < 15; i++) {
			for (int j = 0; j < 15; j++) {
				// record max at this tile
				float match = matched.at<float>(i*squareSize, j*squareSize);
				if (match > matches[i][j].second) {
					matches[i][j] = make_pair(it->first, match);
				}
			}
		}
		// imshow("Grayscale", it->second);
		// waitKey(0);
	}
	// overlay letters on to tiles to check out work
	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			cout << matches[i][j].first << ", ";
			putText(board,
				matches[i][j].first.substr(0,1),
				Point(i*squareSize, (1+j)*squareSize),
				FONT_HERSHEY_PLAIN,
				1.0,
				Scalar(255, 0, 0));
		}
		cout << endl;
	}
	imshow("Grayscale", board);
	waitKey(0);
	
	return 0;
}
