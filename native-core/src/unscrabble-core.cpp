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

	// Triple Word Score Filter
	Mat hsv, grayscale;
	cvtColor(sourceImage, hsv, COLOR_BGR2HSV_FULL);

	// 0 <= h <= 360, 0 <= s <= 1, 0 <= v <= 1
	// for 8U HSV, H / 2, S * 255, V * 255
	Scalar lower(19, 199, 174), upper(36, 255, 230);
	inRange(hsv, lower, upper, grayscale);
	///////////////////////////

	// Display gray image
	namedWindow("Grayscale", WINDOW_NORMAL);
	imshow("Grayscale", grayscale);

	//Wait until any key is pressed
	waitKey(0);

	cout << "Closing ..." << endl;

	return 0;
}
