#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main()
{
	Mat sourceImage = imread("res/test_board_2.jpg");

	// Check if image was successfully read
	if(sourceImage.empty())
	{
		cerr << "Could not read image" << endl;
		return 1;
	}

	namedWindow("Grayscale", WINDOW_NORMAL);

	// TripleWordScoreFilterStep
	Mat hsv, grayscale;
	cvtColor(sourceImage, hsv, COLOR_BGR2HSV_FULL);

	// 0 <= h <= 360, 0 <= s <= 1, 0 <= v <= 1
	// for 8U HSV, H / 2, S // 255, V // 255
	Scalar lower(19, 199, 174), upper(36, 255, 230);
	inRange(hsv, lower, upper, grayscale);
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
 // RectifyBoardStep
 // TileFitlerStep
	// Display gray image

	return 0;
}
