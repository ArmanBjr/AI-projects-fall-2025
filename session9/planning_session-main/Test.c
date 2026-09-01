#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);

    int height[100000];  
    for (int i = 0; i < n; i++) {
        scanf("%d", &height[i]);
    }

    int left = 0;
    int right = n - 1;
    int max_area = 0;

    while (left < right) {
        int h = height[left] < height[right] ? height[left] : height[right];
        int width = right - left;
        int area = h * width;

        if (area > max_area)
            max_area = area;

        if (height[left] < height[right])
            left++;
        else
            right--;
    }

    printf("%d\n", max_area);
    return 0;
}
